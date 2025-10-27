from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bakery.models import MenuItem, Order, OrderItem, Payment, UserProfile
from django.utils import timezone
from decimal import Decimal
import uuid


class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create admin user
        if not User.objects.filter(username='admin@bakery.com').exists():
            admin = User.objects.create_superuser(
                username='admin@bakery.com',
                email='admin@bakery.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            UserProfile.objects.create(
                user=admin,
                phone='+1234567890',
                city='New York',
                state='NY',
                address='123 Admin Street'
            )
            self.stdout.write(self.style.SUCCESS('✓ Admin user created'))
        
        # Create test user
        if not User.objects.filter(username='test@bakery.com').exists():
            test_user = User.objects.create_user(
                username='test@bakery.com',
                email='test@bakery.com',
                password='test123',
                first_name='Test',
                last_name='Customer'
            )
            UserProfile.objects.create(
                user=test_user,
                phone='+1987654321',
                city='Los Angeles',
                state='CA',
                address='456 Test Avenue'
            )
            self.stdout.write(self.style.SUCCESS('✓ Test user created'))
        
        # Create menu items
        menu_items_data = [
            # Breads
            {'name': 'Sourdough Bread', 'description': 'Artisan sourdough with crispy crust', 'price': 5.99, 'category': 'bread', 'image_url': 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73'},
            {'name': 'Whole Wheat Bread', 'description': 'Healthy whole grain bread', 'price': 4.99, 'category': 'bread', 'image_url': 'https://images.unsplash.com/photo-1586444248902-2f64eddc13df'},
            {'name': 'French Baguette', 'description': 'Classic French baguette', 'price': 3.99, 'category': 'bread', 'image_url': 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73'},
            
            # Cakes
            {'name': 'Chocolate Cake', 'description': 'Rich chocolate layer cake', 'price': 25.99, 'category': 'cake', 'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587'},
            {'name': 'Vanilla Cake', 'description': 'Classic vanilla birthday cake', 'price': 22.99, 'category': 'cake', 'image_url': 'https://images.unsplash.com/photo-1464349095431-e9a21285b5f3'},
            {'name': 'Red Velvet Cake', 'description': 'Smooth red velvet with cream cheese', 'price': 27.99, 'category': 'cake', 'image_url': 'https://images.unsplash.com/photo-1586788680434-30d324b2d46f'},
            
            # Croissants
            {'name': 'Butter Croissant', 'description': 'Flaky French butter croissant', 'price': 3.50, 'category': 'croissant', 'image_url': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a'},
            {'name': 'Almond Croissant', 'description': 'Croissant filled with almond cream', 'price': 4.50, 'category': 'croissant', 'image_url': 'https://images.unsplash.com/photo-1623334044303-241021148842'},
            {'name': 'Chocolate Croissant', 'description': 'Pain au chocolat with dark chocolate', 'price': 4.25, 'category': 'croissant', 'image_url': 'https://images.unsplash.com/photo-1623334044303-241021148842'},
            
            # Fruit Tarts
            {'name': 'Strawberry Tart', 'description': 'Fresh strawberries on custard', 'price': 8.99, 'category': 'fruittart', 'image_url': 'https://images.unsplash.com/photo-1519915028121-7d3463d20b13'},
            {'name': 'Mixed Berry Tart', 'description': 'Assorted berries with glaze', 'price': 9.99, 'category': 'fruittart', 'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777'},
            {'name': 'Lemon Tart', 'description': 'Tangy lemon curd tart', 'price': 7.99, 'category': 'fruittart', 'image_url': 'https://images.unsplash.com/photo-1519915028121-7d3463d20b13'},
            
            # Pastries
            {'name': 'Apple Turnover', 'description': 'Flaky pastry with apple filling', 'price': 3.75, 'category': 'pastry', 'image_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff'},
            {'name': 'Cheese Danish', 'description': 'Sweet cheese filled Danish', 'price': 3.99, 'category': 'pastry', 'image_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff'},
            
            # Cookies
            {'name': 'Chocolate Chip Cookies', 'description': 'Classic chocolate chip (6 pack)', 'price': 6.99, 'category': 'cookie', 'image_url': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e'},
            {'name': 'Oatmeal Raisin Cookies', 'description': 'Healthy oatmeal cookies (6 pack)', 'price': 5.99, 'category': 'cookie', 'image_url': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e'},
            
            # Muffins
            {'name': 'Blueberry Muffin', 'description': 'Fresh blueberry muffin', 'price': 3.25, 'category': 'muffin', 'image_url': 'https://images.unsplash.com/photo-1607958996333-41aef7caefaa'},
            {'name': 'Chocolate Chip Muffin', 'description': 'Double chocolate muffin', 'price': 3.50, 'category': 'muffin', 'image_url': 'https://images.unsplash.com/photo-1607958996333-41aef7caefaa'},
            
            # Donuts
            {'name': 'Glazed Donut', 'description': 'Classic glazed donut', 'price': 2.50, 'category': 'donut', 'image_url': 'https://images.unsplash.com/photo-1551024506-0bccd828d307'},
            {'name': 'Chocolate Donut', 'description': 'Chocolate frosted donut', 'price': 2.75, 'category': 'donut', 'image_url': 'https://images.unsplash.com/photo-1551024506-0bccd828d307'},
        ]
        
        created_items = 0
        for item_data in menu_items_data:
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
            if created:
                created_items += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ {created_items} menu items created'))
        
        # Create sample orders with different statuses
        test_user = User.objects.get(username='test@bakery.com')
        if not Order.objects.filter(user=test_user).exists():
            # Order 1 - Current order (confirmed)
            order1 = Order.objects.create(
                user=test_user,
                order_id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                total_amount=Decimal('35.48'),
                delivery_fee=Decimal('50.00'),
                status='confirmed',
                delivery_address='456 Test Avenue, Los Angeles, CA 90210',
                delivery_phone='+1987654321',
                delivery_notes='Please ring the doorbell'
            )
            
            # Add items to order 1
            items1 = [
                {'menu_item': MenuItem.objects.get(name='Chocolate Cake'), 'quantity': 1, 'price': Decimal('25.99')},
                {'menu_item': MenuItem.objects.get(name='Butter Croissant'), 'quantity': 2, 'price': Decimal('3.50')},
                {'menu_item': MenuItem.objects.get(name='Glazed Donut'), 'quantity': 1, 'price': Decimal('2.50')},
            ]
            
            for item_data in items1:
                OrderItem.objects.create(
                    order=order1,
                    menu_item=item_data['menu_item'],
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )
            
            # Create payment for order 1
            Payment.objects.create(
                order=order1,
                payment_method='upi',
                payment_status='completed',
                transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
                amount=order1.grand_total,
                upi_id='test@upi'
            )
            
            # Order 2 - Current order (preparing)
            order2 = Order.objects.create(
                user=test_user,
                order_id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                total_amount=Decimal('18.48'),
                delivery_fee=Decimal('50.00'),
                status='preparing',
                delivery_address='456 Test Avenue, Los Angeles, CA 90210',
                delivery_phone='+1987654321'
            )
            
            # Add items to order 2
            items2 = [
                {'menu_item': MenuItem.objects.get(name='Strawberry Tart'), 'quantity': 2, 'price': Decimal('8.99')},
                {'menu_item': MenuItem.objects.get(name='Chocolate Chip Cookies'), 'quantity': 1, 'price': Decimal('6.99')},
            ]
            
            for item_data in items2:
                OrderItem.objects.create(
                    order=order2,
                    menu_item=item_data['menu_item'],
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )
            
            # Create payment for order 2
            Payment.objects.create(
                order=order2,
                payment_method='upi',
                payment_status='pending',
                transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
                amount=order2.grand_total,
                upi_id='test@upi'
            )
            
            # Order 3 - Delivered order (history)
            order3 = Order.objects.create(
                user=test_user,
                order_id=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                total_amount=Decimal('12.24'),
                delivery_fee=Decimal('50.00'),
                status='delivered',
                delivery_address='456 Test Avenue, Los Angeles, CA 90210',
                delivery_phone='+1987654321',
                delivered_at=timezone.now() - timezone.timedelta(days=3)
            )
            
            # Add items to order 3
            items3 = [
                {'menu_item': MenuItem.objects.get(name='Almond Croissant'), 'quantity': 2, 'price': Decimal('4.50')},
                {'menu_item': MenuItem.objects.get(name='Blueberry Muffin'), 'quantity': 1, 'price': Decimal('3.25')},
            ]
            
            for item_data in items3:
                OrderItem.objects.create(
                    order=order3,
                    menu_item=item_data['menu_item'],
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )
            
            # Create payment for order 3
            Payment.objects.create(
                order=order3,
                payment_method='upi',
                payment_status='completed',
                transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
                amount=order3.grand_total,
                upi_id='test@upi'
            )
            
            self.stdout.write(self.style.SUCCESS('✓ Sample orders created (confirmed, preparing, delivered)'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Sample Data Created Successfully ==='))
        self.stdout.write(self.style.SUCCESS('\nCredentials:'))
        self.stdout.write(self.style.SUCCESS('Admin: admin@bakery.com / admin123'))
        self.stdout.write(self.style.SUCCESS('Test User: test@bakery.com / test123'))
