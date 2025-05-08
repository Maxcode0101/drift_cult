from django.urls import path
from .views import test_email, robots_txt
from store.views import home_view, about_view, community_view

urlpatterns = [
    path("", home_view, name="home"),
    path("test-email/", test_email, name="test_email"),
    path("about/", about_view, name="about"),
    path("community/", community_view, name="community"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("test-middleware/", test_middleware, name="test_middleware"),
]
