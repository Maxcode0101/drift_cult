from django.conf import settings
from django.http import HttpResponsePermanentRedirect

class CanonicalDomainRedirectMiddleware:
    """
    Redirects all traffic from www.driftcult.art to driftcult.art — only in production.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG:
            host = request.get_host()
            if host.startswith('www.'):
                new_url = request.build_absolute_uri().replace('://www.', '://', 1)
                return HttpResponsePermanentRedirect(new_url)
        return self.get_response(request)