from rest_framework import serializers
from apps.analytics.models import DailyRevenueSnapshot, ProductPerformance, CustomerSegment
from apps.ingestion.models import SyncJob


class DailyRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRevenueSnapshot
        fields = ['date', 'revenue', 'orders_count', 'aov', 'new_customers', 'returning_customers']


class ProductPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPerformance
        fields = ['shopify_product_id', 'title', 'units_sold', 'revenue', 'orders_count', 'period_start', 'period_end']


class CustomerSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSegment
        fields = ['shopify_customer_id', 'segment', 'ltv', 'orders_count', 'last_order_date']


class SyncJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyncJob
        fields = ['sync_type', 'status', 'records_synced', 'started_at', 'finished_at', 'error_message']
