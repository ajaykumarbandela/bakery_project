# 🍞 Bakery Project - Complete REST API Guide

## 📋 Table of Contents
1. [Authentication](#authentication)
2. [Menu Items](#menu-items)
3. [Orders](#orders)
4. [Payments](#payments)
5. [User Profile](#user-profile)
6. [Dashboard](#dashboard)

---

## 🔐 Authentication

### Register New User
**POST** `/api/auth/register/`

```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "token": "abc123...",
  "user": {
    "id": 1,
    "username": "user@example.com",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "message": "Registration successful"
}
```

### Login
**POST** `/api/auth/login/`

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "token": "abc123...",
  "user": {...},
  "message": "Login successful"
}
```

### Logout
**POST** `/api/auth/logout/`
**Headers:** `Authorization: Token abc123...`

### Get Current User
**GET** `/api/auth/user/`
**Headers:** `Authorization: Token abc123...`

---

## 🍰 Menu Items

### List All Menu Items
**GET** `/api/menu-items/`

**Query Parameters:**
- `category` - Filter by category (bread, cake, croissant, etc.)
- `search` - Search in name/description
- `ordering` - Sort by field (name, price, created_at)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Chocolate Cake",
    "description": "Rich chocolate layer cake",
    "price": "25.99",
    "category": "cake",
    "image_url": "https://...",
    "available": true,
    "created_at": "2025-10-20T10:00:00Z",
    "updated_at": "2025-10-20T10:00:00Z"
  }
]
```

### Get Single Menu Item
**GET** `/api/menu-items/{id}/`

### Get Categories
**GET** `/api/menu-items/categories/`

**Response:**
```json
{
  "categories": ["bread", "cake", "croissant", "fruittart", "pastry", "cookie", "muffin", "donut"]
}
```

### Create Menu Item (Admin Only)
**POST** `/api/menu-items/`
**Headers:** `Authorization: Token admin_token...`

```json
{
  "name": "New Item",
  "description": "Description",
  "price": "10.99",
  "category": "bread",
  "image_url": "https://...",
  "available": true
}
```

### Update Menu Item (Admin Only)
**PUT/PATCH** `/api/menu-items/{id}/`
**Headers:** `Authorization: Token admin_token...`

### Delete Menu Item (Admin Only)
**DELETE** `/api/menu-items/{id}/`
**Headers:** `Authorization: Token admin_token...`

### Toggle Item Availability (Admin Only)
**PATCH** `/api/menu-items/{id}/toggle_availability/`
**Headers:** `Authorization: Token admin_token...`

---

## 📦 Orders

### List My Orders
**GET** `/api/orders/`
**Headers:** `Authorization: Token abc123...`

**Query Parameters:**
- `status` - Filter by status (pending, confirmed, preparing, ready, delivered, cancelled)
- `ordering` - Sort by field (created_at, total_amount, status)

**Response:**
```json
[
  {
    "id": 1,
    "order_id": "ORD12345",
    "user": 1,
    "user_email": "user@example.com",
    "user_name": "John Doe",
    "status": "confirmed",
    "total_amount": "35.48",
    "delivery_fee": "5.00",
    "grand_total": "40.48",
    "delivery_address": "123 Main St",
    "delivery_phone": "+1234567890",
    "delivery_notes": "Ring doorbell",
    "items": [
      {
        "id": 1,
        "menu_item": 1,
        "menu_item_name": "Chocolate Cake",
        "menu_item_price": "25.99",
        "quantity": 1,
        "price": "25.99",
        "subtotal": "25.99"
      }
    ],
    "payment": {
      "id": 1,
      "payment_method": "upi",
      "payment_status": "completed",
      "transaction_id": "TXN123456",
      "amount": "40.48"
    },
    "created_at": "2025-10-20T10:00:00Z",
    "updated_at": "2025-10-20T10:00:00Z"
  }
]
```

### Get Single Order
**GET** `/api/orders/{id}/`
**Headers:** `Authorization: Token abc123...`

### Create New Order
**POST** `/api/orders/`
**Headers:** `Authorization: Token abc123...`

```json
{
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2,
      "price": "25.99"
    },
    {
      "menu_item_id": 5,
      "quantity": 1,
      "price": "3.50"
    }
  ],
  "delivery_fee": "5.00",
  "delivery_address": "123 Main Street, City, State",
  "delivery_phone": "+1234567890",
  "delivery_notes": "Please ring doorbell",
  "payment_method": "upi",
  "upi_id": "user@upi"
}
```

**Response:** Returns created order with all details

### Cancel Order
**PATCH** `/api/orders/{id}/cancel/`
**Headers:** `Authorization: Token abc123...`

**Response:**
```json
{
  "message": "Order cancelled successfully",
  "order": {...}
}
```

### Update Order Status (Admin Only)
**PATCH** `/api/orders/{id}/update_status/`
**Headers:** `Authorization: Token admin_token...`

```json
{
  "status": "preparing"
}
```

### Get Current Orders
**GET** `/api/orders/current/`
**Headers:** `Authorization: Token abc123...`

Returns orders with status: pending, confirmed, preparing, ready

### Get Order History
**GET** `/api/orders/history/`
**Headers:** `Authorization: Token abc123...`

Returns orders with status: delivered, cancelled

---

## 💳 Payments

### List My Payments
**GET** `/api/payments/`
**Headers:** `Authorization: Token abc123...`

**Response:**
```json
[
  {
    "id": 1,
    "order": 1,
    "order_id": "ORD12345",
    "payment_method": "upi",
    "payment_status": "completed",
    "transaction_id": "TXN123456",
    "amount": "40.48",
    "upi_id": "user@upi",
    "card_last4": "",
    "created_at": "2025-10-20T10:00:00Z",
    "updated_at": "2025-10-20T10:00:00Z",
    "paid_at": "2025-10-20T10:05:00Z"
  }
]
```

### Get Single Payment
**GET** `/api/payments/{id}/`
**Headers:** `Authorization: Token abc123...`

### Process Payment
**POST** `/api/payments/process/`
**Headers:** `Authorization: Token abc123...`

```json
{
  "order_id": "ORD12345",
  "payment_method": "upi",
  "upi_id": "user@upi"
}
```

### Mark Payment as Completed (Admin Only)
**PATCH** `/api/payments/{id}/mark_completed/`
**Headers:** `Authorization: Token admin_token...`

---

## 👤 User Profile

### Get My Profile
**GET** `/api/profiles/me/`
**Headers:** `Authorization: Token abc123...`

**Response:**
```json
{
  "id": 1,
  "phone": "+1234567890",
  "address": "123 Main Street",
  "city": "New York",
  "state": "NY",
  "pincode": "10001",
  "default_delivery_address": "123 Main Street, New York, NY 10001",
  "created_at": "2025-10-20T10:00:00Z",
  "updated_at": "2025-10-20T10:00:00Z"
}
```

### Update My Profile
**PUT/PATCH** `/api/profiles/me/`
**Headers:** `Authorization: Token abc123...`

```json
{
  "phone": "+1234567890",
  "address": "456 New Street",
  "city": "Los Angeles",
  "state": "CA",
  "pincode": "90001",
  "default_delivery_address": "456 New Street, Los Angeles, CA 90001"
}
```

---

## 📊 Dashboard

### Get Dashboard Statistics
**GET** `/api/dashboard/stats/`
**Headers:** `Authorization: Token abc123...`

**Response:**
```json
{
  "total_orders": 15,
  "pending_orders": 2,
  "completed_orders": 10,
  "cancelled_orders": 3,
  "total_spent": "450.75",
  "recent_orders": [...]
}
```

---

## 🔧 Status Codes

- **200 OK** - Successful GET/PUT/PATCH
- **201 Created** - Successful POST
- **204 No Content** - Successful DELETE
- **400 Bad Request** - Invalid data
- **401 Unauthorized** - Missing/invalid token
- **403 Forbidden** - No permission
- **404 Not Found** - Resource not found

---

## 📝 Testing Credentials

**Admin Account:**
- Email: admin@bakery.com
- Password: admin123

**Test User:**
- Email: test@bakery.com
- Password: test123

---

## 🚀 Quick Start Examples

### Using cURL

**Register:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"newuser@example.com","password":"pass123","first_name":"New","last_name":"User"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@bakery.com","password":"test123"}'
```

**Get Menu Items:**
```bash
curl http://localhost:8000/api/menu-items/
```

**Create Order:**
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"menu_item_id":1,"quantity":2,"price":"25.99"}],"delivery_address":"123 Main St","payment_method":"cod"}'
```

### Using JavaScript (Fetch API)

```javascript
// Login
const login = async () => {
  const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      email: 'test@bakery.com',
      password: 'test123'
    })
  });
  const data = await response.json();
  localStorage.setItem('token', data.token);
  return data;
};

// Get Menu Items
const getMenuItems = async () => {
  const response = await fetch('http://localhost:8000/api/menu-items/');
  return await response.json();
};

// Create Order
const createOrder = async (orderData) => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://localhost:8000/api/orders/', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(orderData)
  });
  return await response.json();
};
```

### Using Python (requests)

```python
import requests

BASE_URL = 'http://localhost:8000/api'

# Login
response = requests.post(f'{BASE_URL}/auth/login/', json={
    'email': 'test@bakery.com',
    'password': 'test123'
})
token = response.json()['token']

# Get Menu Items
response = requests.get(f'{BASE_URL}/menu-items/')
menu_items = response.json()

# Create Order
headers = {'Authorization': f'Token {token}'}
order_data = {
    'items': [
        {'menu_item_id': 1, 'quantity': 2, 'price': '25.99'}
    ],
    'delivery_address': '123 Main St',
    'payment_method': 'cod'
}
response = requests.post(f'{BASE_URL}/orders/', json=order_data, headers=headers)
order = response.json()
```

---

## 🎯 Project Features Completed

✅ **User Authentication**
- Registration with email validation
- Login/Logout with token-based auth
- User profile management

✅ **Menu Management**
- Full CRUD operations (Admin)
- Category filtering
- Search functionality
- Availability toggle

✅ **Order Management**
- Create orders with multiple items
- Track order status
- View current/historical orders
- Cancel orders
- Admin order management

✅ **Payment Processing**
- Multiple payment methods (UPI, Card, Net Banking, COD)
- Payment tracking
- Transaction history
- Payment status management

✅ **Database Models**
- MenuItem - Store all bakery items
- Order - Customer orders with tracking
- OrderItem - Individual items in orders
- Payment - Payment transactions
- UserProfile - Extended user information

✅ **Admin Interface**
- Complete admin panel
- Bulk actions for orders/payments
- Filtering and search
- Inline editing

✅ **REST API**
- Token authentication
- CRUD operations
- Filtering and pagination
- Proper error handling
- Admin-only endpoints

---

## 📱 Frontend Integration Ready

The API is ready to integrate with:
- React/Vue/Angular applications
- Mobile apps (iOS/Android)
- Desktop applications
- Third-party services

All endpoints follow REST best practices and return consistent JSON responses.
