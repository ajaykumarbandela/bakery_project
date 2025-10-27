from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MenuItem, Order, OrderItem, Payment, UserProfile
from decimal import Decimal
import uuid
from django.utils import timezone


# Base Serializers
class TimestampedSerializer(serializers.ModelSerializer):
    """Base serializer with timestamp read-only fields"""
    class Meta:
        read_only_fields = ['created_at', 'updated_at']


class UserProfileSerializer(TimestampedSerializer):
    """Serializer for user profile"""
    class Meta(TimestampedSerializer.Meta):
        model = UserProfile
        fields = ['id', 'phone', 'address', 'city', 'state', 'pincode', 
                  'default_delivery_address', 'created_at', 'updated_at']
        read_only_fields = ['id'] + TimestampedSerializer.Meta.read_only_fields


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user information"""
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'full_name', 'profile', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=6, style={'input_type': 'password'})
    phone = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone']
    
    def create(self, validated_data):
        phone = validated_data.pop('phone', '')
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        UserProfile.objects.create(user=user, phone=phone)
        return user


class MenuItemSerializer(TimestampedSerializer):
    """Serializer for menu items with full CRUD support"""
    class Meta(TimestampedSerializer.Meta):
        model = MenuItem
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items with computed fields"""
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_price = serializers.DecimalField(
        source='menu_item.price', 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_name', 'menu_item_price', 
                  'quantity', 'price', 'subtotal']
        read_only_fields = ['id', 'subtotal']


class PaymentSerializer(TimestampedSerializer):
    """Serializer for payment information"""
    order_id = serializers.CharField(source='order.order_id', read_only=True)
    
    class Meta(TimestampedSerializer.Meta):
        model = Payment
        fields = ['id', 'order', 'order_id', 'payment_method', 'payment_status', 
                  'transaction_id', 'amount', 'upi_id', 'card_last4', 
                  'created_at', 'updated_at', 'paid_at']
        read_only_fields = ['id', 'transaction_id', 'paid_at'] + TimestampedSerializer.Meta.read_only_fields


class OrderSerializer(TimestampedSerializer):
    """Serializer for orders with related data"""
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    grand_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta(TimestampedSerializer.Meta):
        model = Order
        fields = ['id', 'order_id', 'user', 'user_email', 'user_name', 'status', 'status_display',
                  'total_amount', 'delivery_fee', 'grand_total', 'delivery_address', 
                  'delivery_phone', 'delivery_notes', 'items', 'payment',
                  'created_at', 'updated_at', 'confirmed_at', 'delivered_at']
        read_only_fields = ['id', 'order_id', 'grand_total', 'confirmed_at', 
                           'delivered_at'] + TimestampedSerializer.Meta.read_only_fields



class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating new orders with validation"""
    items = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of items: [{'menu_item_id': 1, 'quantity': 2, 'price': 10.50}]"
    )
    delivery_fee = serializers.DecimalField(max_digits=10, decimal_places=2, default=Decimal('5.00'))
    delivery_address = serializers.CharField(required=False, allow_blank=True)
    delivery_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    delivery_notes = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(
        choices=['upi', 'card', 'netbanking', 'cod'],
        default='cod'
    )
    upi_id = serializers.CharField(required=False, allow_blank=True)
    
    def validate_items(self, value):
        """Validate items list structure and data"""
        if not value:
            raise serializers.ValidationError("Order must contain at least one item")
        
        required_fields = ['menu_item_id', 'quantity', 'price']
        for item in value:
            # Check required fields
            for field in required_fields:
                if field not in item:
                    raise serializers.ValidationError(f"Each item must have {field}")
            
            # Validate quantity
            if item['quantity'] < 1:
                raise serializers.ValidationError("Quantity must be at least 1")
            
            # Validate price
            if Decimal(str(item['price'])) <= 0:
                raise serializers.ValidationError("Price must be greater than 0")
        
        return value
    
    def create(self, validated_data):
        """Create order with items and payment"""
        user = self.context['request'].user
        items_data = validated_data['items']
        
        # Calculate total
        total = sum(Decimal(str(item['price'])) * item['quantity'] for item in items_data)
        
        # Create order
        order = Order.objects.create(
            user=user,
            order_id=f"ORD{str(uuid.uuid4())[:8].upper()}",
            total_amount=total,
            delivery_fee=validated_data.get('delivery_fee', Decimal('5.00')),
            delivery_address=validated_data.get('delivery_address', ''),
            delivery_phone=validated_data.get('delivery_phone', ''),
            delivery_notes=validated_data.get('delivery_notes', '')
        )
        
        # Create order items using bulk_create for efficiency
        order_items = [
            OrderItem(
                order=order,
                menu_item_id=item['menu_item_id'],
                quantity=item['quantity'],
                price=Decimal(str(item['price']))
            ) for item in items_data
        ]
        OrderItem.objects.bulk_create(order_items)
        
        # Create payment if method is not COD
        payment_method = validated_data.get('payment_method', 'cod')
        if payment_method != 'cod':
            Payment.objects.create(
                order=order,
                payment_method=payment_method,
                payment_status='pending',
                transaction_id=f"TXN{str(uuid.uuid4())[:12].upper()}",
                amount=order.grand_total,
                upi_id=validated_data.get('upi_id', '')
            )
        
        return order


class PaymentCreateSerializer(serializers.Serializer):
    """Serializer for creating payment records"""
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=['upi', 'card', 'netbanking', 'cod'])
    upi_id = serializers.CharField(required=False, allow_blank=True)
    card_last4 = serializers.CharField(max_length=4, required=False, allow_blank=True)
    
    def validate_order_id(self, value):
        """Validate order exists and belongs to user"""
        user = self.context['request'].user
        try:
            order = Order.objects.get(id=value)
            if order.user != user and not user.is_staff:
                raise serializers.ValidationError("You don't have permission to pay for this order")
            if hasattr(order, 'payment'):
                raise serializers.ValidationError("Payment already exists for this order")
            return value
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found")
    
    def create(self, validated_data):
        """Create payment record"""
        order = Order.objects.get(id=validated_data['order_id'])
        payment = Payment.objects.create(
            order=order,
            payment_method=validated_data['payment_method'],
            payment_status='pending',
            transaction_id=f"TXN{str(uuid.uuid4())[:12].upper()}",
            amount=order.grand_total,
            upi_id=validated_data.get('upi_id', ''),
            card_last4=validated_data.get('card_last4', '')
        )
        return payment
