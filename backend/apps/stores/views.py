import hmac
import hashlib
import binascii
import urllib.parse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views import View
from django.utils import timezone
import requests
from .models import ShopifyStore


class ShopifyInstallView(View):
    def get(self, request):
        shop = request.GET.get('shop')
        if not shop:
            return HttpResponseBadRequest('Missing shop parameter')
        scopes = settings.SHOPIFY_SCOPES
        redirect_uri = request.build_absolute_uri('/shopify/callback/')
        state = binascii.b2a_hex(open('/dev/urandom', 'rb').read(16)).decode()
        request.session['shopify_oauth_state'] = state
        params = {
            'client_id': settings.SHOPIFY_API_KEY,
            'scope': scopes,
            'redirect_uri': redirect_uri,
            'state': state,
        }
        auth_url = f"https://{shop}/admin/oauth/authorize?{urllib.parse.urlencode(params)}"
        return HttpResponseRedirect(auth_url)


class ShopifyCallbackView(View):
    def get(self, request):
        shop = request.GET.get('shop')
        code = request.GET.get('code')
        state = request.GET.get('state')
        if not all([shop, code, state]):
            return HttpResponseBadRequest('Missing parameters')
        if state != request.session.get('shopify_oauth_state'):
            return HttpResponseBadRequest('Invalid state')
        if not self._verify_hmac(request):
            return HttpResponseBadRequest('Invalid HMAC')
        access_token = self._exchange_token(shop, code)
        if not access_token:
            return HttpResponseBadRequest('Failed to get access token')
        store, _ = ShopifyStore.objects.update_or_create(
            shop_domain=shop,
            defaults={
                'access_token': access_token,
                'is_active': True,
                'scopes': settings.SHOPIFY_SCOPES,
                'installed_at': timezone.now(),
            }
        )
        return HttpResponse(f'<h1>Meridian connected to {shop}</h1><p>Store ID: {store.id}</p>')

    def _verify_hmac(self, request):
        params = dict(request.GET)
        hmac_value = params.pop('hmac', [None])[0]
        if not hmac_value:
            return False
        sorted_params = '&'.join(
            f"{k}={v[0]}" for k, v in sorted(params.items())
        )
        digest = hmac.new(
            settings.SHOPIFY_API_SECRET.encode(),
            sorted_params.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(digest, hmac_value)

    def _exchange_token(self, shop, code):
        response = requests.post(
            f"https://{shop}/admin/oauth/access_token",
            json={
                'client_id': settings.SHOPIFY_API_KEY,
                'client_secret': settings.SHOPIFY_API_SECRET,
                'code': code,
            }
        )
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
