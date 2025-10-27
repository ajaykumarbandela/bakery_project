# Django Bakery Setup Script
# Run this script to set up the project

Write-Host "=== Heavenly Bakery Django Setup ===" -ForegroundColor Green

# Navigate to project directory
Set-Location "c:\Users\btech\Desktop\ai\the updated proj\bakery_project"

Write-Host "`nStep 1: Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`nStep 2: Running migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

Write-Host "`nStep 3: Creating superuser (admin)..." -ForegroundColor Yellow
Write-Host "Please enter admin credentials:" -ForegroundColor Cyan
python manage.py createsuperuser

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "`nTo run the server, execute: python manage.py runserver" -ForegroundColor Cyan
Write-Host "Then visit: http://localhost:8000/" -ForegroundColor Cyan
Write-Host "Admin panel: http://localhost:8000/admin/" -ForegroundColor Cyan
