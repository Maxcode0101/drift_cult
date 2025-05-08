from django.http import HttpResponsePermanentRedirect
import os

class CanonicalDomainRedirectMiddleware:
    """
    Redirects all traffic from www.driftcult.art to driftcult.art (only in production).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        is_production = not os.environ.get("DEBUG", "False") == "True"

        if is_production and host.startswith('www.'):
            new_url = request.build_absolute_uri().replace('://www.', '://', 1)
            return HttpResponsePermanentRedirect(new_url)

        return self.get_response(request)
