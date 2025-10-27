import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakery_project.settings')
django.setup()

from bakery.models import MenuItem

# Clear existing items (optional)
# MenuItem.objects.all().delete()

menu_items = [
    # Breads
    {
        'name': 'Milk Bread',
        'description': 'Soft and fluffy milk bread',
        'price': 50.00,
        'category': 'bread',
        'image_url': 'https://plus.unsplash.com/premium_photo-1695028378526-05116fcaae90?w=500&auto=format&fit=crop&q=60'
    },
    {
        'name': 'Brioche',
        'description': 'Rich and buttery French bread',
        'price': 50.00,
        'category': 'bread',
        'image_url': 'https://images.unsplash.com/photo-1608198093002-ad4e005484ec?w=500&auto=format&fit=crop&q=60'
    },
    {
        'name': 'Baguette',
        'description': 'Classic French baguette',
        'price': 50.00,
        'category': 'bread',
        'image_url': 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=500&auto=format&fit=crop&q=60'
    },
    {
        'name': 'Sourdough',
        'description': 'Tangy sourdough bread',
        'price': 50.00,
        'category': 'bread',
        'image_url': 'https://images.unsplash.com/photo-1585478259715-876acc5be8eb?w=500&auto=format&fit=crop&q=60'
    },
    
    # Cakes
    {
        'name': 'Red Velvet Cake',
        'description': 'Classic red velvet with cream cheese frosting',
        'price': 50.00,
        'category': 'cake',
        'image_url': 'https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?w=500&auto=format&fit=crop&q=60'
    },
    {
        'name': 'Fruitcake',
        'description': 'Traditional fruitcake with dried fruits',
        'price': 50.00,
        'category': 'cake',
        'image_url': 'https://images.unsplash.com/photo-1464347744102-11db6282f854?w=500&auto=format&fit=crop&q=60'
    },
    {
        'name': 'Carrot Cake',
        'description': 'Moist carrot cake with cream cheese frosting',
        'price': 50.00,
        'category': 'cake',
        'image_url': 'https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62?w=500&auto=format&fit=crop&q=60'
    },
    {
        'name': 'Chocolate Cake',
        'description': 'Rich chocolate layer cake',
        'price': 50.00,
        'category': 'cake',
        'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500&auto=format&fit=crop&q=60'
    },
    
    # Croissants
    {
        'name': 'Apricot Delight',
        'description': 'Croissant with apricot filling',
        'price': 50.00,
        'category': 'croissant',
        'image_url': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=500&auto=format&fit=crop&q=60'
    },
    {
        'name': 'Plain Butter Croissant',
        'description': 'Classic French butter croissant',
        'price': 50.00,
        'category': 'croissant',
        'image_url': 'https://images.unsplash.com/photo-1530610476181-d83430b64dcd?w=500&auto=format&fit=crop&q=60'
    },
    {
        'name': 'Chocolate Croissant',
        'description': 'Croissant filled with chocolate',
        'price': 50.00,
        'category': 'croissant',
        'image_url': 'https://images.unsplash.com/photo-1623334044303-241021148842?w=500&auto=format&fit=crop&q=60'
    },
    {
        'name': 'Almond Croissant',
        'description': 'Croissant with almond cream filling',
        'price': 50.00,
        'category': 'croissant',
        'image_url': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=500&auto=format&fit=crop&q=60'
    },
    {
        'name': 'Pain aux Raisins',
        'description': 'French pastry with raisins',
        'price': 50.00,
        'category': 'croissant',
        'image_url': 'https://images.unsplash.com/photo-1509365465985-25d11c17e812?w=500&auto=format&fit=crop&q=60'
    },
    
    # Fruit Tarts
    {
        'name': 'Citrus Tarts',
        'description': 'Fresh citrus tarts',
        'price': 50.00,
        'category': 'fruittart',
        'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500&auto=format&fit=crop&q=60'
    },
    {
        'name': 'Tarte Tatin',
        'description': 'Upside-down caramelized apple tart',
        'price': 50.00,
        'category': 'fruittart',
        'image_url': 'https://images.unsplash.com/photo-1519915212116-7cfef71f1d3e?w=500&auto=format&fit=crop&q=60'
    },
]

# Add all items
created_count = 0
for item_data in menu_items:
    item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        defaults=item_data
    )
    if created:
        created_count += 1
        print(f"✓ Added: {item.name}")
    else:
        print(f"- Already exists: {item.name}")

print(f"\n{'='*50}")
print(f"Total items added: {created_count}")
print(f"Total items in database: {MenuItem.objects.count()}")
print(f"{'='*50}")
