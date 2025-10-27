#!/bin/bash
# Quick Deployment Script

echo "🚀 Bakery Project Deployment Setup"
echo "=================================="
echo ""

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Load menu items
echo "🍰 Loading menu items..."
python update_images.py

echo ""
echo "✅ Deployment setup complete!"
echo ""
echo "Next steps:"
echo "1. Set environment variables on your hosting platform"
echo "2. Deploy your code"
echo "3. Run this script on the server"
echo "4. Create superuser: python manage.py createsuperuser"
echo ""
echo "See DEPLOYMENT_GUIDE.md for detailed instructions"
