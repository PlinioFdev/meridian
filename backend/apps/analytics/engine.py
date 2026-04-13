from django.db.models import Sum, Count, Avg, Min, Max
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from apps.ingestion.models import ShopifyOrder, ShopifyCustomer
from .models import DailyRevenueSnapshot, ProductPerformance, CustomerSegment


def compute_daily_revenue(store, days=90):
    cutoff = date.today() - timedelta(days=days)
    qs = (
        ShopifyOrder.objects
        .filter(store=store, shopify_created_at__date__gte=cutoff)
        .annotate(day=TruncDate('shopify_created_at'))
        .values('day')
        .annotate(
            revenue=Sum('total_price'),
            orders_count=Count('id'),
            aov=Avg('total_price'),
        )
        .order_by('day')
    )
    snapshots = []
    for row in qs:
        new_customers = ShopifyOrder.objects.filter(
            store=store,
            shopify_created_at__date=row['day'],
            customer_id__in=ShopifyOrder.objects.filter(
                store=store
            ).values('customer_id').annotate(
                first=Min('shopify_created_at')
            ).filter(first__date=row['day']).values('customer_id')
        ).values('customer_id').distinct().count()

        snap, _ = DailyRevenueSnapshot.objects.update_or_create(
            store=store,
            date=row['day'],
            defaults={
                'revenue': row['revenue'] or 0,
                'orders_count': row['orders_count'],
                'aov': row['aov'] or 0,
                'new_customers': new_customers,
            }
        )
        snapshots.append(snap)
    return len(snapshots)


def compute_product_performance(store, days=30):
    period_start = date.today() - timedelta(days=days)
    period_end = date.today()
    orders = ShopifyOrder.objects.filter(
        store=store,
        shopify_created_at__date__gte=period_start
    )
    product_stats = {}
    for order in orders:
        for item in order.line_items:
            pid = item.get('product_id')
            if not pid:
                continue
            if pid not in product_stats:
                product_stats[pid] = {
                    'title': item.get('title', ''),
                    'units_sold': 0,
                    'revenue': Decimal('0'),
                    'orders_count': 0,
                }
            product_stats[pid]['units_sold'] += item.get('quantity', 0)
            product_stats[pid]['revenue'] += Decimal(str(item.get('price', 0))) * item.get('quantity', 1)
            product_stats[pid]['orders_count'] += 1
    for pid, stats in product_stats.items():
        ProductPerformance.objects.update_or_create(
            store=store,
            shopify_product_id=pid,
            period_start=period_start,
            period_end=period_end,
            defaults=stats
        )
    return len(product_stats)


def compute_customer_segments(store):
    today = date.today()
    customers = ShopifyCustomer.objects.filter(store=store)
    count = 0
    for customer in customers:
        orders = ShopifyOrder.objects.filter(store=store, customer_id=customer.shopify_id)
        orders_count = orders.count()
        ltv = orders.aggregate(total=Sum('total_price'))['total'] or Decimal('0')
        last_order = orders.aggregate(last=Max('shopify_created_at'))['last']
        last_order_date = last_order.date() if last_order else None
        days_since = (today - last_order_date).days if last_order_date else 999
        if orders_count == 1 and days_since <= 30:
            segment = CustomerSegment.Segment.NEW
        elif orders_count > 1 and days_since <= 60:
            segment = CustomerSegment.Segment.RETURNING
        elif days_since <= 120:
            segment = CustomerSegment.Segment.AT_RISK
        else:
            segment = CustomerSegment.Segment.LOST
        CustomerSegment.objects.update_or_create(
            store=store,
            shopify_customer_id=customer.shopify_id,
            defaults={
                'segment': segment,
                'ltv': ltv,
                'orders_count': orders_count,
                'last_order_date': last_order_date,
            }
        )
        count += 1
    return count
