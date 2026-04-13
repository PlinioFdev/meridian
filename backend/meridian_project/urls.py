from django.contrib import admin
from django.urls import path
from apps.stores.views import ShopifyInstallView, ShopifyCallbackView
from apps.api.views import OverviewView, RevenueView, ProductsView, CustomersView, SyncStatusView, CohortView, GrowthView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shopify/install/', ShopifyInstallView.as_view()),
    path('shopify/callback/', ShopifyCallbackView.as_view()),
    path('api/metrics/overview/', OverviewView.as_view()),
    path('api/metrics/revenue/', RevenueView.as_view()),
    path('api/metrics/products/', ProductsView.as_view()),
    path('api/metrics/customers/', CustomersView.as_view()),
    path('api/metrics/cohort/', CohortView.as_view()),
    path('api/metrics/growth/', GrowthView.as_view()),
    path('api/sync/status/', SyncStatusView.as_view()),
]
