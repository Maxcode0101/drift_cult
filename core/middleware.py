from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalDomainRedirectMiddleware:
    """
    Redirect www.driftcult.art to driftcult.art in production only.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if (
            not settings.DEBUG
            and host.startswith("www.")
        ):
            new_url = request.build_absolute_uri().replace("://www.", "://", 1)
            return HttpResponsePermanentRedirect(new_url)
        return self.get_response(request)