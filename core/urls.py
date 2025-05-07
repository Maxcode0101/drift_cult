from django.urls import path
from .views import test_email
from store.views import home_view, about_view, community_view, robots_txt

urlpatterns = [
    path("test-email/", test_email, name="test_email"),
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("community/", community_view, name="community"),
    path("robots.txt", robots_txt, name="robots_txt"),
]
