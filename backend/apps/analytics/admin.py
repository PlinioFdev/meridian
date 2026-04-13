from django.contrib import admin
from .models import DailyRevenueSnapshot, ProductPerformance, CustomerSegment

@admin.register(DailyRevenueSnapshot)
class DailyRevenueSnapshotAdmin(admin.ModelAdmin):
    list_display = ['store', 'date', 'revenue', 'orders_count', 'aov', 'new_customers']
    list_filter = ['store']

@admin.register(ProductPerformance)
class ProductPerformanceAdmin(admin.ModelAdmin):
    list_display = ['title', 'store', 'units_sold', 'revenue', 'period_start', 'period_end']
    list_filter = ['store']

@admin.register(CustomerSegment)
class CustomerSegmentAdmin(admin.ModelAdmin):
    list_display = ['shopify_customer_id', 'store', 'segment', 'ltv', 'orders_count', 'last_order_date']
    list_filter = ['store', 'segment']
