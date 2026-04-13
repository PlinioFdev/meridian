from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Sum, Count, Avg
from apps.stores.models import ShopifyStore
from apps.analytics.models import DailyRevenueSnapshot, ProductPerformance, CustomerSegment
from apps.ingestion.models import SyncJob
from .serializers import DailyRevenueSerializer, ProductPerformanceSerializer, CustomerSegmentSerializer, SyncJobSerializer


class OverviewView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        store = ShopifyStore.objects.filter(is_active=True).first()
        if not store:
            return Response({'error': 'No active store'}, status=404)
        snapshots = DailyRevenueSnapshot.objects.filter(store=store)
        totals = snapshots.aggregate(
            total_revenue=Sum('revenue'),
            total_orders=Sum('orders_count'),
            avg_aov=Avg('aov'),
        )
        segments = CustomerSegment.objects.filter(store=store)
        return Response({
            'total_revenue': totals['total_revenue'] or 0,
            'total_orders': totals['total_orders'] or 0,
            'avg_aov': totals['avg_aov'] or 0,
            'total_customers': segments.count(),
            'new_customers': segments.filter(segment='new').count(),
            'returning_customers': segments.filter(segment='returning').count(),
            'at_risk_customers': segments.filter(segment='at_risk').count(),
            'last_sync': store.last_sync_at,
        })


class RevenueView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        store = ShopifyStore.objects.filter(is_active=True).first()
        snapshots = DailyRevenueSnapshot.objects.filter(store=store).order_by('date')
        return Response(DailyRevenueSerializer(snapshots, many=True).data)


class ProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        store = ShopifyStore.objects.filter(is_active=True).first()
        products = ProductPerformance.objects.filter(store=store).order_by('-revenue')[:20]
        return Response(ProductPerformanceSerializer(products, many=True).data)


class CustomersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        store = ShopifyStore.objects.filter(is_active=True).first()
        customers = CustomerSegment.objects.filter(store=store).order_by('-ltv')[:50]
        return Response(CustomerSegmentSerializer(customers, many=True).data)


class SyncStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        store = ShopifyStore.objects.filter(is_active=True).first()
        jobs = SyncJob.objects.filter(store=store).order_by('-created_at')[:10]
        return Response(SyncJobSerializer(jobs, many=True).data)
