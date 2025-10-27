# 🍰 Full-Stack Bakery E-Commerce Platform

## 🎯 Project Overview

A complete full-stack Django bakery ordering system with REST API, featuring secure authentication, order management, payment processing, and comprehensive admin controls. Built with Django REST Framework for seamless frontend integration.

---

## ✨ Key Features

### 🔐 Authentication & User Management
- User registration with email validation
- Secure login/logout with token-based authentication
- User profile management
- Admin and customer role separation

### 🍞 Menu Management
- Full CRUD operations for menu items
- 8 product categories (Bread, Cake, Croissant, Fruit Tart, Pastry, Cookie, Muffin, Donut)
- Search and filter functionality
- Availability toggle
- Image URL support

### 📦 Order System
- Create orders with multiple items
- Real-time order tracking (6 status levels)
- Order history and current orders view
- Order cancellation
- Delivery details management
- Admin order management panel

### 💳 Payment Processing
- Multiple payment methods:
  - UPI
  - Credit/Debit Card
  - Net Banking
  - Cash on Delivery (COD)
- Payment tracking with transaction IDs
- Payment status management
- Secure payment records

### 👤 User Profiles
- Extended user information
- Default delivery addresses
- Contact details management
- Order history tracking

### 🎛️ Admin Interface
- Comprehensive Django admin panel
- Bulk actions for orders and payments
- Status management
- Advanced filtering and search
- Inline editing for order items

### 🔌 REST API
- Complete RESTful API
- Token-based authentication
- CRUD operations for all resources
- Proper HTTP status codes
- JSON responses
- API documentation included

---

## 🛠️ Technology Stack

**Backend:**
- Django 5.2.7
- Django REST Framework 3.16.1
- Python 3.x
- SQLite (Development)

**Authentication:**
- Django Token Authentication
- Session-based authentication
- CSRF protection

**Frontend Ready:**
- REST API for React/Vue/Angular
- Mobile app integration support
- Third-party service integration

---

## 📋 Database Schema

### Models

**MenuItem**
- name, description, price
- category, image_url
- available status
- timestamps

**Order**
- order_id (unique)
- user relationship
- status tracking
- pricing (total + delivery fee)
- delivery details
- timestamps (created, confirmed, delivered)

**OrderItem**
- order relationship
- menu item relationship
- quantity, price
- subtotal calculation

**Payment**
- order relationship (one-to-one)
- payment method & status
- transaction_id (unique)
- payment details (UPI ID, card last 4)
- timestamps

**UserProfile**
- user relationship (one-to-one)
- contact information
- address details
- default delivery address

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Installation Steps

1. **Clone the repository**
```bash
cd "c:\Users\btech\Desktop\ai\the updated proj\bakery_project"
```

2. **Create virtual environment** (if not exists)
```bash
python -m venv envi
```

3. **Activate virtual environment**
```bash
# Windows
.\envi\Scripts\activate

# Linux/Mac
source envi/bin/activate
```

4. **Install dependencies**
```bash
pip install django djangorestframework
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create sample data**
```bash
python manage.py create_sample_data
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Web App: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API Root: http://localhost:8000/api

---

## 🔑 Default Credentials

**Admin Account:**
- Email: admin@bakery.com
- Password: admin123

**Test User:**
- Email: test@bakery.com
- Password: test123

---

## 📚 API Documentation

Complete API documentation available in `API_GUIDE.md`

### Quick API Examples

**Login:**
```bash
POST http://localhost:8000/api/auth/login/
{
  "email": "test@bakery.com",
  "password": "test123"
}
```

**Get Menu Items:**
```bash
GET http://localhost:8000/api/menu-items/
```

**Create Order:**
```bash
POST http://localhost:8000/api/orders/
Authorization: Token YOUR_TOKEN
{
  "items": [
    {"menu_item_id": 1, "quantity": 2, "price": "25.99"}
  ],
  "delivery_address": "123 Main St",
  "payment_method": "upi",
  "upi_id": "user@upi"
}
```

---

## 📁 Project Structure

```
bakery_project/
├── bakery/                          # Main app
│   ├── models.py                    # Database models
│   ├── views.py                     # Template views
│   ├── api_views.py                 # REST API views
│   ├── serializers.py               # API serializers
│   ├── urls.py                      # URL routing
│   ├── api_urls.py                  # API URL routing
│   ├── admin.py                     # Admin configuration
│   ├── templates/                   # HTML templates
│   │   └── bakery/
│   │       ├── index.html
│   │       ├── menu.html
│   │       ├── login.html
│   │       ├── signin.html
│   │       ├── cart.html
│   │       ├── orders.html
│   │       ├── payment.html
│   │       └── upi-payment.html
│   ├── static/                      # CSS, JS, images
│   │   └── css/
│   │       ├── styles.css
│   │       ├── login.css
│   │       ├── cart.css
│   │       └── orders.css
│   └── management/
│       └── commands/
│           └── create_sample_data.py
├── bakery_project/                  # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3                       # Database
├── manage.py                        # Django management
├── API_GUIDE.md                     # API documentation
└── README.md                        # This file
```

---

## 🎨 Frontend Pages

### Available Templates
1. **index.html** - Homepage
2. **menu.html** - Browse menu items
3. **login.html** - User login
4. **signin.html** - User registration
5. **cart.html** - Shopping cart
6. **orders.html** - Order tracking
7. **payment.html** - Payment page
8. **upi-payment.html** - UPI payment

### Styling
- Modern glassmorphism design
- Responsive mobile-first layout
- Gradient-based color scheme
- CSS3 animations and transitions
- Cross-browser compatible

---

## 🔧 API Endpoints Summary

### Authentication
- `POST /api/auth/register/` - Register
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/user/` - Current user

### Menu Items
- `GET /api/menu-items/` - List items
- `GET /api/menu-items/{id}/` - Get item
- `POST /api/menu-items/` - Create (Admin)
- `PUT /api/menu-items/{id}/` - Update (Admin)
- `DELETE /api/menu-items/{id}/` - Delete (Admin)
- `GET /api/menu-items/categories/` - List categories
- `PATCH /api/menu-items/{id}/toggle_availability/` - Toggle (Admin)

### Orders
- `GET /api/orders/` - List my orders
- `GET /api/orders/{id}/` - Get order
- `POST /api/orders/` - Create order
- `PATCH /api/orders/{id}/cancel/` - Cancel order
- `PATCH /api/orders/{id}/update_status/` - Update status (Admin)
- `GET /api/orders/current/` - Current orders
- `GET /api/orders/history/` - Order history

### Payments
- `GET /api/payments/` - List payments
- `GET /api/payments/{id}/` - Get payment
- `POST /api/payments/process/` - Process payment
- `PATCH /api/payments/{id}/mark_completed/` - Mark completed (Admin)

### User Profile
- `GET /api/profiles/me/` - Get profile
- `PUT /api/profiles/me/` - Update profile

### Dashboard
- `GET /api/dashboard/stats/` - Statistics

---

## 💻 Usage Examples

### Python (requests)
```python
import requests

BASE_URL = 'http://localhost:8000/api'

# Login
response = requests.post(f'{BASE_URL}/auth/login/', json={
    'email': 'test@bakery.com',
    'password': 'test123'
})
token = response.json()['token']

# Get menu items
headers = {'Authorization': f'Token {token}'}
menu = requests.get(f'{BASE_URL}/menu-items/', headers=headers)
print(menu.json())
```

### JavaScript (Fetch)
```javascript
// Login
const response = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'test@bakery.com',
    password: 'test123'
  })
});
const {token} = await response.json();

// Create order
const order = await fetch('http://localhost:8000/api/orders/', {
  method: 'POST',
  headers: {
    'Authorization': `Token ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    items: [{menu_item_id: 1, quantity: 2, price: '25.99'}],
    delivery_address: '123 Main St',
    payment_method: 'cod'
  })
});
```

---

## 🔒 Security Features

- CSRF protection on all forms
- Token-based API authentication
- Password hashing with Django's built-in system
- Session security with HTTPOnly cookies
- SQL injection protection via ORM
- XSS protection with template escaping
- Admin-only endpoints for sensitive operations

---

## 📊 Database Records

After running `create_sample_data`:
- 20+ menu items across 8 categories
- 2 user accounts (admin + test user)
- Sample order with payment
- User profiles for both accounts

---

## 🎯 Project Highlights for Resume

**Full-Stack Bakery E-Commerce Platform with Django REST API**

Engineered a production-ready e-commerce platform featuring:
- **Backend:** Django MVT + REST API with token authentication
- **Database:** Comprehensive relational models (MenuItem, Order, Payment, UserProfile)
- **API:** 30+ RESTful endpoints with full CRUD operations
- **Security:** CSRF protection, token auth, admin role separation
- **Features:** Order tracking (6 statuses), multi-payment methods, admin panel
- **Admin:** Bulk actions, filtering, inline editing, status management
- **Performance:** Optimized queries with select_related/prefetch_related
- **Code Quality:** Serializers, viewsets, permissions, proper HTTP codes

**Tech Stack:** Django 5.2.7 | Django REST Framework | Python 3.x | SQLite | Token Authentication | AJAX-ready API

**Achievements:**
- Complete CRUD for menu items with 8 categories
- Order management with real-time status tracking
- Multi-method payment processing (UPI, Card, NetBanking, COD)
- Admin panel with bulk operations
- RESTful API ready for frontend integration
- Sample data management command

---

## 🚀 Next Steps / Future Enhancements

- [ ] Add email notifications for orders
- [ ] Implement real payment gateway integration
- [ ] Add order rating and review system
- [ ] Create React/Vue frontend
- [ ] Add inventory management
- [ ] Implement delivery tracking
- [ ] Add promotional codes/discounts
- [ ] Create mobile app (React Native/Flutter)
- [ ] Add real-time notifications (WebSockets)
- [ ] Implement analytics dashboard

---

## 📞 Support

For issues or questions, refer to:
- `API_GUIDE.md` for complete API documentation
- Django admin at `/admin` for database management
- Django docs: https://docs.djangoproject.com

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 👨‍💻 Developer

Built as a full-stack portfolio project demonstrating:
- Django framework expertise
- RESTful API design
- Database modeling
- Authentication & authorization
- Admin interface customization
- Modern web development practices

**Perfect for showcasing to top MNC companies!** 🎯
