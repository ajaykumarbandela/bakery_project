from django.core.management.base import BaseCommand
from bakery.models import MenuItem


class Command(BaseCommand):
    help = 'Populate database with sample menu items'

    def handle(self, *args, **kwargs):
        menu_items = [
            {
                'name': 'Sourdough Bread',
                'description': 'Freshly baked sourdough with a crispy crust',
                'price': 499.00,
                'category': 'bread',
                'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCk81MUCJH0ENqwi8y7midIrNBW7O_hVp0yA&s',
            },
            {
                'name': 'Croissant',
                'description': 'Buttery, flaky French croissant',
                'price': 329.00,
                'category': 'croissant',
                'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgiqw1-Ee1hgrio3bJ44ki9eT91tgqHOzqLQ&s',
            },
            {
                'name': 'Chocolate Cake',
                'description': 'Rich chocolate cake with ganache',
                'price': 2075.00,
                'category': 'cake',
                'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwEuDw3mdCJyGJ3wM1uIngWezPpcPFYElNAg&s',
            },
            {
                'name': 'Fruit Tart',
                'description': 'Fresh seasonal fruits on pastry cream',
                'price': 579.00,
                'category': 'fruittart',
                'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCk81MUCJH0ENqwi8y7midIrNBW7O_hVp0yA&s',
            },
            {
                'name': 'Milk Bread',
                'description': 'Soft and fluffy Japanese milk bread',
                'price': 414.00,
                'category': 'bread',
                'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoRUQi2KN_SuVyXqAXdFZZa-kVTk4JmXOi3A&s',
            },
            {
                'name': 'Brioche',
                'description': 'Rich and tender French brioche',
                'price': 579.00,
                'category': 'bread',
                'image_url': 'https://example.com/brioche.jpg',
            },
            {
                'name': 'Baguette',
                'description': 'Classic French baguette',
                'price': 329.00,
                'category': 'bread',
                'image_url': 'https://example.com/baguette.jpg',
            },
        ]

        for item_data in menu_items:
            item, created = MenuItem.objects.get_or_create(
                name=item_data['name'],
                defaults=item_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created menu item: {item.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Menu item already exists: {item.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated menu items!')
        )
