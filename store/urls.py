from django.urls import path
from . import views
from .views import ProductListView, newsletter_signup_ajax, robots_txt, sitemap_xml

urlpatterns = [
    path('', views.home_view, name='home'),  # Homepage
    path('shop/', ProductListView.as_view(), name='product_list'),  # Shop view
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/<int:size_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap_xml, name="sitemap_xml"),

    # AJAX Newsletter Signup
    path('ajax/newsletter-signup/', newsletter_signup_ajax, name='newsletter_signup_ajax'),

    # Stripe Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
]