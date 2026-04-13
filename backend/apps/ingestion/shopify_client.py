import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class ShopifyClient:
    def __init__(self, store):
        self.store = store
        self.base_url = f"https://{store.shop_domain}/admin/api/{settings.SHOPIFY_API_VERSION}"
        self.headers = {
            'X-Shopify-Access-Token': store.access_token,
            'Content-Type': 'application/json',
        }

    def _get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}.json"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response

    def _paginate(self, endpoint, key, params=None):
        params = params or {}
        params['limit'] = 250
        while True:
            response = self._get(endpoint, params)
            data = response.json().get(key, [])
            yield from data
            link = response.headers.get('Link', '')
            if 'rel="next"' not in link:
                break
            next_url = [p.split(';')[0].strip('<> ') for p in link.split(',') if 'rel="next"' in p][0]
            cursor = next_url.split('page_info=')[-1].split('&')[0]
            params = {'limit': 250, 'page_info': cursor}

    def get_orders(self):
        return self._paginate('orders', 'orders', {'status': 'any'})

    def get_products(self):
        return self._paginate('products', 'products')

    def get_customers(self):
        return self._paginate('customers', 'customers')
