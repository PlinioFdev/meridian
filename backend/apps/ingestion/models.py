from django.db import models
from apps.stores.models import ShopifyStore


class ShopifyOrder(models.Model):
    store = models.ForeignKey(ShopifyStore, on_delete=models.CASCADE, related_name='orders')
    shopify_id = models.BigIntegerField()
    email = models.EmailField(blank=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='USD')
    financial_status = models.CharField(max_length=50, blank=True)
    fulfillment_status = models.CharField(max_length=50, blank=True, null=True)
    customer_id = models.BigIntegerField(null=True, blank=True)
    line_items = models.JSONField(default=list)
    shopify_created_at = models.DateTimeField()
    shopify_updated_at = models.DateTimeField()
    synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store', 'shopify_id')
        ordering = ['-shopify_created_at']
        indexes = [
            models.Index(fields=['store', 'shopify_created_at']),
            models.Index(fields=['store', 'customer_id']),
        ]

    def __str__(self):
        return f"Order {self.shopify_id} ({self.store})"


class ShopifyProduct(models.Model):
    store = models.ForeignKey(ShopifyStore, on_delete=models.CASCADE, related_name='products')
    shopify_id = models.BigIntegerField()
    title = models.CharField(max_length=500)
    vendor = models.CharField(max_length=255, blank=True)
    product_type = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default='active')
    variants = models.JSONField(default=list)
    shopify_created_at = models.DateTimeField()
    shopify_updated_at = models.DateTimeField()
    synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store', 'shopify_id')
        ordering = ['-shopify_created_at']

    def __str__(self):
        return f"{self.title} ({self.store})"


class ShopifyCustomer(models.Model):
    store = models.ForeignKey(ShopifyStore, on_delete=models.CASCADE, related_name='customers')
    shopify_id = models.BigIntegerField()
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    orders_count = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default='USD')
    shopify_created_at = models.DateTimeField()
    shopify_updated_at = models.DateTimeField()
    synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store', 'shopify_id')
        ordering = ['-shopify_created_at']
        indexes = [
            models.Index(fields=['store', 'shopify_created_at']),
        ]

    def __str__(self):
        return f"{self.email} ({self.store})"


class SyncJob(models.Model):
    class SyncType(models.TextChoices):
        ORDERS = 'orders', 'Orders'
        PRODUCTS = 'products', 'Products'
        CUSTOMERS = 'customers', 'Customers'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        RUNNING = 'running', 'Running'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'

    store = models.ForeignKey(ShopifyStore, on_delete=models.CASCADE, related_name='sync_jobs')
    sync_type = models.CharField(max_length=20, choices=SyncType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    cursor = models.TextField(blank=True)
    records_synced = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sync_type} sync ({self.status}) - {self.store}"
