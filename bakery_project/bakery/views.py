from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Prefetch
from .models import MenuItem, Order, OrderItem, Payment, UserProfile
import json
import uuid
from django.utils import timezone
from decimal import Decimal


# Utility function to handle cart processing
def process_cart_items(cart_data):
    """Process cart data and return valid order items with total amount"""
    cart = json.loads(cart_data)
    if not cart:
        return None, None, "Cart is empty"
    
    total_amount = Decimal('0.00')
    order_items = []
    
    for item_id, item_data in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=int(item_id))
            quantity = int(item_data.get('quantity', 0))
            if quantity > 0:
                subtotal = menu_item.price * quantity
                total_amount += subtotal
                order_items.append({
                    'menu_item': menu_item,
                    'quantity': quantity,
                    'price': menu_item.price
                })
        except (MenuItem.DoesNotExist, ValueError):
            continue
    
    if not order_items:
        return None, None, "No valid items in cart"
    
    return order_items, total_amount, None


# Simple template views
def index(request):
    return render(request, 'bakery/index.html')


def menu_view(request):
    menu_items = MenuItem.objects.filter(available=True)
    return render(request, 'bakery/menu.html', {'menu_items': menu_items})


def about_view(request):
    return render(request, 'bakery/about.html')


def contact_view(request):
    return render(request, 'bakery/contact.html')


@login_required
def cart_view(request):
    return render(request, 'bakery/cart.html')


@login_required
def orders_view(request):
    """Display user-specific orders - only orders belonging to the logged-in user"""
    # Optimized query with prefetch to reduce database hits
    orders_queryset = Order.objects.filter(user=request.user).select_related(
        'payment'
    ).prefetch_related(
        'items__menu_item'
    ).order_by('-created_at')
    
    # Get current active orders
    current_orders = orders_queryset.filter(status__in=['pending', 'confirmed', 'preparing', 'ready'])
    
    # Get order history
    order_history = orders_queryset.filter(status__in=['delivered', 'cancelled'])
    
    # Calculate statistics
    total_orders = orders_queryset.count()
    delivered_orders = orders_queryset.filter(status='delivered').count()
    
    context = {
        'current_orders': current_orders,
        'order_history': order_history,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'user_full_name': request.user.get_full_name() or request.user.username
    }
    return render(request, 'bakery/orders.html', context)


@login_required
def payment_view(request):
    return render(request, 'bakery/payment.html')


@login_required
def upi_payment_view(request):
    if request.method != 'POST':
        return render(request, 'bakery/upi-payment.html')
    
    # Get POST data
    cart_data = request.POST.get('cart_data')
    delivery_address = request.POST.get('delivery_address')
    delivery_phone = request.POST.get('delivery_phone')
    delivery_notes = request.POST.get('delivery_notes', '')
    payment_screenshot = request.FILES.get('payment_screenshot')
    upi_transaction_id = request.POST.get('upi_transaction_id', '')
    
    # Validate required fields
    if not all([cart_data, delivery_address, payment_screenshot]):
        messages.error(request, 'Please fill all required fields and upload payment screenshot.')
        return render(request, 'bakery/upi-payment.html')
    
    try:
        # Process cart items
        order_items, total_amount, error = process_cart_items(cart_data)
        if error:
            messages.error(request, error)
            return redirect('cart')
        
        # Create order
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        order = Order.objects.create(
            user=request.user,
            order_id=order_id,
            status='pending',
            total_amount=total_amount,
            delivery_address=delivery_address,
            delivery_phone=delivery_phone,
            delivery_notes=delivery_notes
        )
        
        # Create order items
        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                menu_item=item['menu_item'],
                quantity=item['quantity'],
                price=item['price']
            ) for item in order_items
        ])
        
        # Create payment record
        transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        Payment.objects.create(
            order=order,
            payment_method='upi',
            payment_status='pending',
            transaction_id=transaction_id,
            amount=order.grand_total,
            upi_id=upi_transaction_id,
            payment_screenshot=payment_screenshot
        )
        
        success_message = f'Order placed successfully! Order ID: {order_id}. Your payment will be verified within 24 hours.'
        messages.success(request, success_message)
        
        return render(request, 'bakery/upi-payment.html', {
            'order_placed': True,
            'order_id': order_id,
            'message': success_message
        })
        
    except json.JSONDecodeError:
        messages.error(request, 'Invalid cart data.')
    except Exception as e:
        messages.error(request, f'Error processing order: {str(e)}')
    
    return render(request, 'bakery/upi-payment.html')


# Authentication views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect(request.GET.get('next', 'index'))
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'bakery/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        fullname = request.POST.get('fullname', '')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'bakery/signin.html')
        
        # Parse fullname
        name_parts = fullname.split() if fullname else []
        first_name = name_parts[0] if name_parts else ''
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        
        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('index')
    
    return render(request, 'bakery/signin.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('index')
