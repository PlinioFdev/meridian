import logging
from celery import shared_task
from apps.stores.models import ShopifyStore
from .engine import compute_daily_revenue, compute_product_performance, compute_customer_segments

logger = logging.getLogger(__name__)


@shared_task
def compute_metrics(store_id):
    store = ShopifyStore.objects.get(id=store_id)
    r1 = compute_daily_revenue(store)
    r2 = compute_product_performance(store)
    r3 = compute_customer_segments(store)
    logger.info(f"Metrics computed: {r1} snapshots, {r2} products, {r3} customers")
    return {'snapshots': r1, 'products': r2, 'customers': r3}
