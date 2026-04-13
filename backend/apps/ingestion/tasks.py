import logging
from celery import shared_task
from django.utils import timezone
from apps.stores.models import ShopifyStore
from .models import ShopifyOrder, ShopifyProduct, ShopifyCustomer, SyncJob
from .shopify_client import ShopifyClient

logger = logging.getLogger(__name__)


def _run_sync(store_id, sync_type, sync_fn):
    store = ShopifyStore.objects.get(id=store_id)
    job = SyncJob.objects.create(store=store, sync_type=sync_type, status=SyncJob.Status.RUNNING, started_at=timezone.now())
    try:
        records = sync_fn(store, job)
        job.status = SyncJob.Status.SUCCESS
        job.records_synced = records
        store.last_sync_at = timezone.now()
        store.save(update_fields=['last_sync_at'])
    except Exception as e:
        job.status = SyncJob.Status.FAILED
        job.error_message = str(e)
        logger.exception(f"Sync failed for store {store_id} type {sync_type}")
    finally:
        job.finished_at = timezone.now()
        job.save()


@shared_task
def sync_orders(store_id):
    def _sync(store, job):
        client = ShopifyClient(store)
        count = 0
        for order in client.get_orders():
            ShopifyOrder.objects.update_or_create(
                store=store,
                shopify_id=order['id'],
                defaults={
                    'email': order.get('email', ''),
                    'total_price': order.get('total_price', 0),
                    'subtotal_price': order.get('subtotal_price', 0),
                    'total_tax': order.get('total_tax', 0),
                    'currency': order.get('currency', 'USD'),
                    'financial_status': order.get('financial_status', ''),
                    'fulfillment_status': order.get('fulfillment_status') or '',
                    'customer_id': order.get('customer', {}).get('id'),
                    'line_items': order.get('line_items', []),
                    'shopify_created_at': order['created_at'],
                    'shopify_updated_at': order['updated_at'],
                }
            )
            count += 1
        return count
    _run_sync(store_id, SyncJob.SyncType.ORDERS, _sync)


@shared_task
def sync_products(store_id):
    def _sync(store, job):
        client = ShopifyClient(store)
        count = 0
        for product in client.get_products():
            ShopifyProduct.objects.update_or_create(
                store=store,
                shopify_id=product['id'],
                defaults={
                    'title': product.get('title', ''),
                    'vendor': product.get('vendor', ''),
                    'product_type': product.get('product_type', ''),
                    'status': product.get('status', 'active'),
                    'variants': product.get('variants', []),
                    'shopify_created_at': product['created_at'],
                    'shopify_updated_at': product['updated_at'],
                }
            )
            count += 1
        return count
    _run_sync(store_id, SyncJob.SyncType.PRODUCTS, _sync)


@shared_task
def sync_customers(store_id):
    def _sync(store, job):
        client = ShopifyClient(store)
        count = 0
        for customer in client.get_customers():
            ShopifyCustomer.objects.update_or_create(
                store=store,
                shopify_id=customer['id'],
                defaults={
                    'email': customer.get('email', ''),
                    'first_name': customer.get('first_name', ''),
                    'last_name': customer.get('last_name', ''),
                    'orders_count': customer.get('orders_count', 0),
                    'total_spent': customer.get('total_spent', 0),
                    'currency': customer.get('currency', 'USD'),
                    'shopify_created_at': customer['created_at'],
                    'shopify_updated_at': customer['updated_at'],
                }
            )
            count += 1
        return count
    _run_sync(store_id, SyncJob.SyncType.CUSTOMERS, _sync)


@shared_task
def sync_all(store_id):
    sync_orders.delay(store_id)
    sync_products.delay(store_id)
    sync_customers.delay(store_id)
