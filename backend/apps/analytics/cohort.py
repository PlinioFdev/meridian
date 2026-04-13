from django.db import connection
from apps.stores.models import ShopifyStore


def compute_cohort_retention(store_id, months=6):
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH first_orders AS (
                SELECT
                    customer_id,
                    DATE_TRUNC('month', MIN(shopify_created_at)) AS cohort_month
                FROM ingestion_shopifyorder
                WHERE store_id = %s AND customer_id IS NOT NULL
                GROUP BY customer_id
            ),
            order_months AS (
                SELECT
                    o.customer_id,
                    f.cohort_month,
                    DATE_TRUNC('month', o.shopify_created_at) AS order_month
                FROM ingestion_shopifyorder o
                JOIN first_orders f ON o.customer_id = f.customer_id
                WHERE o.store_id = %s
            )
            SELECT
                TO_CHAR(cohort_month, 'YYYY-MM') AS cohort,
                COUNT(DISTINCT customer_id) AS cohort_size,
                COUNT(DISTINCT CASE WHEN order_month = cohort_month THEN customer_id END) AS m0,
                COUNT(DISTINCT CASE WHEN order_month = cohort_month + INTERVAL '1 month' THEN customer_id END) AS m1,
                COUNT(DISTINCT CASE WHEN order_month = cohort_month + INTERVAL '2 months' THEN customer_id END) AS m2,
                COUNT(DISTINCT CASE WHEN order_month = cohort_month + INTERVAL '3 months' THEN customer_id END) AS m3,
                COUNT(DISTINCT CASE WHEN order_month = cohort_month + INTERVAL '4 months' THEN customer_id END) AS m4,
                COUNT(DISTINCT CASE WHEN order_month = cohort_month + INTERVAL '5 months' THEN customer_id END) AS m5,
                COUNT(DISTINCT CASE WHEN order_month = cohort_month + INTERVAL '6 months' THEN customer_id END) AS m6
            FROM order_months
            GROUP BY cohort_month
            ORDER BY cohort_month DESC
            LIMIT 12
        """, [store_id, store_id])

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    result = []
    for row in rows:
        data = dict(zip(columns, row))
        cohort_size = data['cohort_size']
        entry = {
            'cohort': data['cohort'],
            'cohort_size': cohort_size,
            'retention': {}
        }
        for m in range(months + 1):
            key = f'm{m}'
            count = data.get(key, 0) or 0
            entry['retention'][key] = {
                'count': count,
                'rate': round((count / cohort_size * 100), 1) if cohort_size > 0 else 0
            }
        result.append(entry)

    return result
