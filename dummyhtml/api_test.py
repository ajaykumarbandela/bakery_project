"""
API Testing Script for Bakery Project
Run with: python api_test.py
"""

import requests
import json

BASE_URL = 'http://localhost:8000/api'

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)
    print(f"{'='*60}\n")

def test_authentication():
    """Test authentication endpoints"""
    print("\n🔐 TESTING AUTHENTICATION")
    
    # Login
    response = requests.post(f'{BASE_URL}/auth/login/', json={
        'email': 'test@bakery.com',
        'password': 'test123'
    })
    print_response("Login Test User", response)
    
    if response.status_code == 200:
        token = response.json()['token']
        
        # Get current user
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(f'{BASE_URL}/auth/user/', headers=headers)
        print_response("Get Current User", response)
        
        return token
    return None

def test_menu_items(token=None):
    """Test menu items endpoints"""
    print("\n🍰 TESTING MENU ITEMS")
    
    # List all items
    response = requests.get(f'{BASE_URL}/menu-items/')
    print_response("List All Menu Items", response)
    
    # Get categories
    response = requests.get(f'{BASE_URL}/menu-items/categories/')
    print_response("Get Categories", response)
    
    # Filter by category
    response = requests.get(f'{BASE_URL}/menu-items/?category=cake')
    print_response("Filter by Category (Cake)", response)
    
    # Search
    response = requests.get(f'{BASE_URL}/menu-items/?search=chocolate')
    print_response("Search (Chocolate)", response)
    
    # Get single item
    response = requests.get(f'{BASE_URL}/menu-items/1/')
    print_response("Get Single Menu Item (ID=1)", response)

def test_orders(token):
    """Test orders endpoints"""
    print("\n📦 TESTING ORDERS")
    
    headers = {'Authorization': f'Token {token}'}
    
    # List orders
    response = requests.get(f'{BASE_URL}/orders/', headers=headers)
    print_response("List My Orders", response)
    
    # Create order
    order_data = {
        'items': [
            {'menu_item_id': 1, 'quantity': 1, 'price': '25.99'},
            {'menu_item_id': 7, 'quantity': 2, 'price': '3.50'}
        ],
        'delivery_fee': '5.00',
        'delivery_address': '789 Test Street, New York, NY 10001',
        'delivery_phone': '+1234567890',
        'delivery_notes': 'Please call on arrival',
        'payment_method': 'upi',
        'upi_id': 'testuser@upi'
    }
    response = requests.post(f'{BASE_URL}/orders/', json=order_data, headers=headers)
    print_response("Create New Order", response)
    
    if response.status_code == 201:
        order_id = response.json()['id']
        
        # Get single order
        response = requests.get(f'{BASE_URL}/orders/{order_id}/', headers=headers)
        print_response(f"Get Order Details (ID={order_id})", response)
    
    # Get current orders
    response = requests.get(f'{BASE_URL}/orders/current/', headers=headers)
    print_response("Get Current Orders", response)
    
    # Get order history
    response = requests.get(f'{BASE_URL}/orders/history/', headers=headers)
    print_response("Get Order History", response)

def test_payments(token):
    """Test payments endpoints"""
    print("\n💳 TESTING PAYMENTS")
    
    headers = {'Authorization': f'Token {token}'}
    
    # List payments
    response = requests.get(f'{BASE_URL}/payments/', headers=headers)
    print_response("List My Payments", response)

def test_profile(token):
    """Test user profile endpoints"""
    print("\n👤 TESTING USER PROFILE")
    
    headers = {'Authorization': f'Token {token}'}
    
    # Get profile
    response = requests.get(f'{BASE_URL}/profiles/me/', headers=headers)
    print_response("Get My Profile", response)
    
    # Update profile
    profile_data = {
        'phone': '+1999888777',
        'city': 'San Francisco',
        'state': 'CA',
        'address': '123 Updated Address'
    }
    response = requests.patch(f'{BASE_URL}/profiles/me/', json=profile_data, headers=headers)
    print_response("Update Profile", response)

def test_dashboard(token):
    """Test dashboard endpoints"""
    print("\n📊 TESTING DASHBOARD")
    
    headers = {'Authorization': f'Token {token}'}
    
    # Get stats
    response = requests.get(f'{BASE_URL}/dashboard/stats/', headers=headers)
    print_response("Get Dashboard Statistics", response)

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 BAKERY API TEST SUITE")
    print("="*60)
    print("\nMake sure the Django server is running on http://localhost:8000")
    print("Run with: python manage.py runserver")
    
    try:
        # Test authentication
        token = test_authentication()
        
        if token:
            # Test menu items
            test_menu_items(token)
            
            # Test orders
            test_orders(token)
            
            # Test payments
            test_payments(token)
            
            # Test profile
            test_profile(token)
            
            # Test dashboard
            test_dashboard(token)
            
            print("\n" + "="*60)
            print("✅ ALL TESTS COMPLETED!")
            print("="*60)
        else:
            print("\n❌ Authentication failed. Cannot proceed with tests.")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to the server!")
        print("Make sure Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == '__main__':
    main()
