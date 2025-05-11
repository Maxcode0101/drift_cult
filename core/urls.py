from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .views import stripe_webhook, test_email, robots_txt, contact_view
from store.views import home_view, about_view, community_view
from store.sitemaps import ProductSitemap, StaticViewSitemap

sitemaps = {
    'products': ProductSitemap(),
    'static': StaticViewSitemap(),
}

urlpatterns = [
    path("", home_view, name="home"),
    path("webhook/stripe/", stripe_webhook, name="stripe_webhook"),
    path("test-email/", test_email, name="test_email"),
    path("about/", about_view, name="about"),
    path('contact/', contact_view, name='contact'),
    path("community/", community_view, name="community"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]