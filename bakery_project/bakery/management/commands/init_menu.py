"""
Management command to initialize database with menu items if empty
This runs automatically during deployment
"""
from django.core.management.base import BaseCommand
from bakery.models import MenuItem


class Command(BaseCommand):
    help = 'Initialize database with menu items if empty'

    def handle(self, *args, **options):
        # Check if menu items already exist
        if MenuItem.objects.exists():
            self.stdout.write(self.style.SUCCESS('Menu items already exist. Skipping initialization.'))
            return

        self.stdout.write('Creating menu items...')
        
        menu_items = [
            # Cakes
            {
                'name': 'Chocolate Cake',
                'description': 'Rich, moist chocolate cake with chocolate frosting',
                'price': 450.00,
                'category': 'Cakes',
                'available': True
            },
            {
                'name': 'Vanilla Cake',
                'description': 'Classic vanilla sponge cake with buttercream',
                'price': 400.00,
                'category': 'Cakes',
                'available': True
            },
            {
                'name': 'Red Velvet Cake',
                'description': 'Soft red velvet cake with cream cheese frosting',
                'price': 500.00,
                'category': 'Cakes',
                'available': True
            },
            {
                'name': 'Black Forest Cake',
                'description': 'Chocolate cake layered with cherries and whipped cream',
                'price': 550.00,
                'category': 'Cakes',
                'available': True
            },
            
            # Pastries
            {
                'name': 'Croissant',
                'description': 'Buttery, flaky French pastry',
                'price': 80.00,
                'category': 'Pastries',
                'available': True
            },
            {
                'name': 'Danish Pastry',
                'description': 'Sweet pastry filled with cream or fruit',
                'price': 90.00,
                'category': 'Pastries',
                'available': True
            },
            {
                'name': 'Eclair',
                'description': 'Choux pastry filled with cream and topped with chocolate',
                'price': 100.00,
                'category': 'Pastries',
                'available': True
            },
            
            # Cupcakes
            {
                'name': 'Vanilla Cupcake',
                'description': 'Fluffy vanilla cupcake with buttercream frosting',
                'price': 60.00,
                'category': 'Cupcakes',
                'available': True
            },
            {
                'name': 'Chocolate Cupcake',
                'description': 'Rich chocolate cupcake with chocolate ganache',
                'price': 70.00,
                'category': 'Cupcakes',
                'available': True
            },
            {
                'name': 'Red Velvet Cupcake',
                'description': 'Red velvet cupcake with cream cheese frosting',
                'price': 75.00,
                'category': 'Cupcakes',
                'available': True
            },
            
            # Bread
            {
                'name': 'Sourdough Bread',
                'description': 'Artisan sourdough bread with crispy crust',
                'price': 120.00,
                'category': 'Bread',
                'available': True
            },
            {
                'name': 'Whole Wheat Bread',
                'description': 'Healthy whole wheat bread loaf',
                'price': 80.00,
                'category': 'Bread',
                'available': True
            },
            {
                'name': 'Baguette',
                'description': 'Traditional French baguette',
                'price': 100.00,
                'category': 'Bread',
                'available': True
            },
            
            # Cookies
            {
                'name': 'Chocolate Chip Cookies',
                'description': 'Classic cookies loaded with chocolate chips (6 pieces)',
                'price': 150.00,
                'category': 'Cookies',
                'available': True
            },
            {
                'name': 'Oatmeal Cookies',
                'description': 'Healthy oatmeal cookies with raisins (6 pieces)',
                'price': 140.00,
                'category': 'Cookies',
                'available': True
            },
            {
                'name': 'Sugar Cookies',
                'description': 'Sweet and buttery sugar cookies (6 pieces)',
                'price': 130.00,
                'category': 'Cookies',
                'available': True
            },
        ]

        created_count = 0
        for item_data in menu_items:
            MenuItem.objects.create(**item_data)
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} menu items!'))
