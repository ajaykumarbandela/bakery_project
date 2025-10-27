# Django Test File
from django.test import TestCase
from django.contrib.auth.models import User
from .models import MenuItem, Order, OrderItem


class MenuItemTestCase(TestCase):
    def setUp(self):
        MenuItem.objects.create(
            name="Test Bread",
            price=5.99,
            category="bread",
            available=True
        )
    
    def test_menu_item_creation(self):
        """Test that menu items are created correctly"""
        item = MenuItem.objects.get(name="Test Bread")
        self.assertEqual(item.price, 5.99)
        self.assertEqual(item.category, "bread")
        self.assertTrue(item.available)


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser@test.com',
            email='testuser@test.com',
            password='testpass123'
        )
        self.menu_item = MenuItem.objects.create(
            name="Test Cake",
            price=25.00,
            category="cake",
            available=True
        )
    
    def test_order_creation(self):
        """Test that orders are created correctly"""
        order = Order.objects.create(
            user=self.user,
            order_id="TEST123",
            total_amount=30.00,
            delivery_fee=5.00
        )
        
        OrderItem.objects.create(
            order=order,
            menu_item=self.menu_item,
            quantity=1,
            price=25.00
        )
        
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_amount, 30.00)
