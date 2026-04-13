import os
import sys
import django
import random
from decimal import Decimal
from datetime import datetime, timedelta

sys.path.insert(0, '/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meridian_project.settings')
django.setup()

from django.utils import timezone
from apps.stores.models import ShopifyStore
from apps.ingestion.models import ShopifyOrder, ShopifyProduct, ShopifyCustomer
from apps.analytics.engine import compute_daily_revenue, compute_product_performance, compute_customer_segments

store = ShopifyStore.objects.filter(is_active=True).first()
if not store:
    print("No active store found.")
    sys.exit(1)

print("Seeding products...")
products = []
product_names = [
    "Premium Wireless Headphones", "Ergonomic Office Chair", "Mechanical Keyboard",
    "4K Monitor Stand", "USB-C Hub", "Noise Cancelling Earbuds", "Laptop Sleeve",
    "Desk Organizer Set", "LED Desk Lamp", "Webcam HD 1080p"
]
for i, name in enumerate(product_names):
    p, _ = ShopifyProduct.objects.update_or_create(
        store=store, shopify_id=9000000000 + i,
        defaults={
            'title': name,
            'vendor': random.choice(['TechBrand', 'OfficeMax', 'DeskCo']),
            'product_type': 'Electronics',
            'status': 'active',
            'variants': [{'id': 9000000000 + i, 'price': str(round(random.uniform(29, 299), 2))}],
            'shopify_created_at': timezone.now() - timedelta(days=random.randint(30, 180)),
            'shopify_updated_at': timezone.now(),
        }
    )
    products.append(p)
print(f"  {len(products)} products created.")

print("Seeding customers...")
customers = []
first_names = ["Alice", "Bob", "Carol", "David", "Eva", "Frank", "Grace", "Henry", "Iris", "Jack",
               "Kate", "Leo", "Mia", "Noah", "Olivia", "Paul", "Quinn", "Rose", "Sam", "Tina"]
for i, name in enumerate(first_names):
    c, _ = ShopifyCustomer.objects.update_or_create(
        store=store, shopify_id=8000000000 + i,
        defaults={
            'email': f'{name.lower()}@example.com',
            'first_name': name,
            'last_name': 'Test',
            'orders_count': 0,
            'total_spent': Decimal('0'),
            'shopify_created_at': timezone.now() - timedelta(days=random.randint(1, 120)),
            'shopify_updated_at': timezone.now(),
        }
    )
    customers.append(c)
print(f"  {len(customers)} customers created.")

print("Seeding orders...")
order_count = 0
for day_offset in range(60):
    date = timezone.now() - timedelta(days=day_offset)
    orders_today = random.randint(1, 8)
    for _ in range(orders_today):
        customer = random.choice(customers)
        product = random.choice(products)
        price = Decimal(str(round(random.uniform(29, 299), 2)))
        qty = random.randint(1, 3)
        ShopifyOrder.objects.create(
            store=store,
            shopify_id=7000000000 + order_count,
            email=customer.email,
            total_price=price * qty,
            subtotal_price=price * qty,
            currency='USD',
            financial_status='paid',
            customer_id=customer.shopify_id,
            line_items=[{
                'product_id': product.shopify_id,
                'title': product.title,
                'quantity': qty,
                'price': str(price),
            }],
            shopify_created_at=date,
            shopify_updated_at=date,
        )
        order_count += 1
print(f"  {order_count} orders created.")

print("Computing metrics...")
compute_daily_revenue(store, days=90)
compute_product_performance(store, days=60)
compute_customer_segments(store)
print("Done! Meridian seeded successfully.")
