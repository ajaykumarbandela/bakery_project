# 🚀 Deployment Guide for Bakery Project

This guide will help you deploy your Django bakery project to various hosting platforms.

---

## 📋 Table of Contents
1. [Render (Recommended - Free)](#option-1-render-free--easy)
2. [PythonAnywhere (Easy for Beginners)](#option-2-pythonanywhere)
3. [Heroku](#option-3-heroku)
4. [Railway](#option-4-railway)
5. [AWS EC2 (Advanced)](#option-5-aws-ec2)

---

## Option 1: Render (Free & Easy) ⭐ RECOMMENDED

### Step 1: Prepare Your Repository
Your code is already pushed to GitHub! ✅

### Step 2: Sign Up on Render
1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with your GitHub account

### Step 3: Create a New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `ajaykumarbandela/bakery_project`
3. Configure the service:
   - **Name**: `bakery-project`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Environment**: `Python 3`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && python bakery_project/manage.py collectstatic --no-input && python bakery_project/manage.py migrate
     ```
   - **Start Command**:
     ```bash
     gunicorn --chdir bakery_project bakery_project.wsgi:application
     ```

### Step 4: Add Environment Variables
In the Render dashboard, add these environment variables:
- `SECRET_KEY`: Generate a random key (use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: Your Render URL (e.g., `bakery-project.onrender.com`)
- `PYTHON_VERSION`: `3.11.0`

### Step 5: Create PostgreSQL Database (Optional but Recommended)
1. Click "New +" → "PostgreSQL"
2. Name it `bakery-db`
3. Choose the Free plan
4. Once created, copy the "Internal Database URL"
5. Add it as environment variable `DATABASE_URL` in your web service

### Step 6: Deploy! 🎉
Click "Create Web Service" and wait for deployment (5-10 minutes)

Your site will be live at: `https://your-app-name.onrender.com`

---

## Option 2: PythonAnywhere

### Step 1: Sign Up
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free "Beginner" account

### Step 2: Clone Your Repository
In the PythonAnywhere Bash console:
```bash
cd ~
git clone https://github.com/ajaykumarbandela/bakery_project.git
cd bakery_project
```

### Step 3: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 bakery-env
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration" → Python 3.10
4. Configure:
   - **Source code**: `/home/yourusername/bakery_project`
   - **Working directory**: `/home/yourusername/bakery_project`
   - **WSGI file**: Edit and update with Django WSGI config

### Step 5: Set Environment Variables
In the web tab, add:
```python
SECRET_KEY = 'your-secret-key-here'
DEBUG = False
```

### Step 6: Static Files
- URL: `/static/`
- Directory: `/home/yourusername/bakery_project/bakery_project/staticfiles`

### Step 7: Reload
Click "Reload" button

Your site will be at: `https://yourusername.pythonanywhere.com`

---

## Option 3: Heroku

### Prerequisites
Install Heroku CLI from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

### Deployment Steps
```bash
# Login to Heroku
heroku login

# Create app
heroku create bakery-project-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='.herokuapp.com'

# Deploy
git push heroku main

# Run migrations
heroku run python bakery_project/manage.py migrate

# Create superuser
heroku run python bakery_project/manage.py createsuperuser

# Open app
heroku open
```

---

## Option 4: Railway

### Step 1: Sign Up
Go to [railway.app](https://railway.app) and sign up with GitHub

### Step 2: New Project
1. Click "New Project"
2. Choose "Deploy from GitHub repo"
3. Select `bakery_project`

### Step 3: Add PostgreSQL
1. Click "New" → "Database" → "Add PostgreSQL"
2. Railway will automatically set `DATABASE_URL`

### Step 4: Environment Variables
Add these in the Variables tab:
- `SECRET_KEY`: Your secret key
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: `.railway.app`

### Step 5: Deploy Settings
Railway will auto-detect Django and deploy!

---

## Option 5: AWS EC2 (Advanced)

### Prerequisites
- AWS Account
- Basic Linux knowledge

### High-Level Steps
1. Launch EC2 instance (Ubuntu 22.04)
2. Install Python, Nginx, and PostgreSQL
3. Clone repository
4. Set up Gunicorn as application server
5. Configure Nginx as reverse proxy
6. Set up SSL with Let's Encrypt

**Detailed guide**: This requires advanced setup. Consider Render or Railway for easier deployment.

---

## 🔧 Post-Deployment Checklist

After deploying to any platform:

1. **Create Superuser**
   ```bash
   python bakery_project/manage.py createsuperuser
   ```

2. **Populate Sample Data**
   ```bash
   python bakery_project/manage.py populate_menu
   python bakery_project/manage.py create_sample_data
   ```

3. **Test Your Site**
   - Visit the home page
   - Try logging in
   - Place a test order
   - Check the admin panel at `/admin/`

4. **Set Up Custom Domain** (Optional)
   - Buy a domain (e.g., from Namecheap, GoDaddy)
   - Configure DNS to point to your hosting provider
   - Update `ALLOWED_HOSTS` in settings

5. **Monitor Your App**
   - Check logs regularly
   - Set up error tracking (e.g., Sentry)
   - Monitor database usage

---

## 🆘 Troubleshooting

### Static Files Not Loading
```bash
python manage.py collectstatic --no-input
```

### Database Errors
Make sure `DATABASE_URL` is set correctly in environment variables

### 500 Internal Server Error
Check logs:
- Render: View logs in dashboard
- Heroku: `heroku logs --tail`
- Railway: View logs in deployment tab

### ALLOWED_HOSTS Error
Add your domain to `ALLOWED_HOSTS` environment variable

---

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Render Django Guide](https://render.com/docs/deploy-django)
- [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)

---

## 🎉 Success!

Once deployed, share your live URL:
- Home: `https://your-app.onrender.com/`
- Admin: `https://your-app.onrender.com/admin/`
- API: `https://your-app.onrender.com/api/`

**Need help?** Open an issue on GitHub or contact support of your hosting provider.
