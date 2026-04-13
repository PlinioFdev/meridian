from django.contrib import admin
from .models import ShopifyOrder, ShopifyProduct, ShopifyCustomer, SyncJob

@admin.register(ShopifyOrder)
class ShopifyOrderAdmin(admin.ModelAdmin):
    list_display = ['shopify_id', 'store', 'email', 'total_price', 'financial_status', 'shopify_created_at']
    list_filter = ['store', 'financial_status']
    search_fields = ['shopify_id', 'email']

@admin.register(ShopifyProduct)
class ShopifyProductAdmin(admin.ModelAdmin):
    list_display = ['shopify_id', 'store', 'title', 'vendor', 'status']
    list_filter = ['store', 'status']
    search_fields = ['title', 'vendor']

@admin.register(ShopifyCustomer)
class ShopifyCustomerAdmin(admin.ModelAdmin):
    list_display = ['shopify_id', 'store', 'email', 'orders_count', 'total_spent']
    list_filter = ['store']
    search_fields = ['email']

@admin.register(SyncJob)
class SyncJobAdmin(admin.ModelAdmin):
    list_display = ['store', 'sync_type', 'status', 'records_synced', 'started_at', 'finished_at']
    list_filter = ['store', 'sync_type', 'status']
