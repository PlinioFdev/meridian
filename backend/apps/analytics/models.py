from django.db import models
from apps.stores.models import ShopifyStore


class DailyRevenueSnapshot(models.Model):
    store = models.ForeignKey(ShopifyStore, on_delete=models.CASCADE, related_name='revenue_snapshots')
    date = models.DateField()
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    orders_count = models.IntegerField(default=0)
    new_customers = models.IntegerField(default=0)
    returning_customers = models.IntegerField(default=0)
    aov = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store', 'date')
        ordering = ['-date']
        indexes = [models.Index(fields=['store', 'date'])]

    def __str__(self):
        return f"{self.store} - {self.date} - ${self.revenue}"


class ProductPerformance(models.Model):
    store = models.ForeignKey(ShopifyStore, on_delete=models.CASCADE, related_name='product_performances')
    shopify_product_id = models.BigIntegerField()
    title = models.CharField(max_length=500)
    period_start = models.DateField()
    period_end = models.DateField()
    units_sold = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    orders_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store', 'shopify_product_id', 'period_start', 'period_end')
        ordering = ['-revenue']

    def __str__(self):
        return f"{self.title} - {self.period_start} to {self.period_end}"


class CustomerSegment(models.Model):
    class Segment(models.TextChoices):
        NEW = 'new', 'New'
        RETURNING = 'returning', 'Returning'
        AT_RISK = 'at_risk', 'At Risk'
        LOST = 'lost', 'Lost'

    store = models.ForeignKey(ShopifyStore, on_delete=models.CASCADE, related_name='customer_segments')
    shopify_customer_id = models.BigIntegerField()
    segment = models.CharField(max_length=20, choices=Segment.choices)
    ltv = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    orders_count = models.IntegerField(default=0)
    last_order_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store', 'shopify_customer_id')
        ordering = ['-ltv']

    def __str__(self):
        return f"Customer {self.shopify_customer_id} - {self.segment}"
