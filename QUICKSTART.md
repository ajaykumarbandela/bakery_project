# 🎯 Quick Start Guide - Local Development

## Prerequisites
- Python 3.8 or higher
- Git

## Setup Steps

### 1. Clone the Repository
```bash
git clone https://github.com/ajaykumarbandela/bakery_project.git
cd bakery_project
```

### 2. Create Virtual Environment
**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install Django djangorestframework Pillow
```

### 4. Run Migrations
```bash
cd bakery_project
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Populate Sample Data
```bash
python manage.py populate_menu
python manage.py create_sample_data
```

### 7. Run Development Server
```bash
python manage.py runserver
```

### 8. Access the Application
- **Website**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/

### 9. Test Accounts
After running `create_sample_data`:
- **Admin**: admin@bakery.com / admin123
- **Test User**: test@bakery.com / test123

## 🎉 You're Ready!

Explore the features:
- ✅ Browse menu items
- ✅ Add items to cart
- ✅ Place orders
- ✅ View order history (user-specific)
- ✅ Admin panel for management

---

## For Deployment, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
