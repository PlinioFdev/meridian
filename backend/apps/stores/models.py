from django.db import models


class ShopifyStore(models.Model):
    name = models.CharField(max_length=255)
    shop_domain = models.CharField(max_length=255, unique=True)
    access_token = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)
    scopes = models.TextField(blank=True)
    installed_at = models.DateTimeField(null=True, blank=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.shop_domain
