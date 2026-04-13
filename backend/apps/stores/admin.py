from django.contrib import admin
from .models import ShopifyStore

@admin.register(ShopifyStore)
class ShopifyStoreAdmin(admin.ModelAdmin):
    list_display = ['shop_domain', 'name', 'is_active', 'last_sync_at', 'created_at']
    list_filter = ['is_active']
    search_fields = ['shop_domain', 'name']
