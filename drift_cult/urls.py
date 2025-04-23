from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home
from store.views import stripe_webhook


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('product/', include('store.urls')),
    path('store/', include('store.urls')),
    path('', include('store.urls')),
    path('', include('core.urls')),
    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)