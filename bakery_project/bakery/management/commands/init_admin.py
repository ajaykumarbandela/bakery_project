"""
Management command to create default admin user if none exists
IMPORTANT: Change the password after first login!
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Create default admin user if no superuser exists'

    def handle(self, *args, **options):
        # Check if any superuser exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Admin user already exists. Skipping creation.'))
            return

        # Get credentials from environment or use defaults
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@bakery.com')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')  # CHANGE THIS!

        # Create superuser
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS(f'✅ Admin user created successfully!'))
        self.stdout.write(self.style.WARNING(f'Username: {username}'))
        self.stdout.write(self.style.WARNING(f'Email: {email}'))
        self.stdout.write(self.style.WARNING('⚠️  IMPORTANT: Change the password after first login!'))
