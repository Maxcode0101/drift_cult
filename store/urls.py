from django.urls import path
from . import views
from .views import ProductListView, newsletter_signup_ajax
from .views import (
    admin_dashboard,
    product_create,
    product_edit,
    product_delete,
    add_product_sizes,
    admin_order_list,
    admin_order_detail,
    admin_order_delete,
    bulk_order_action,
)

urlpatterns = [
    path('', views.home_view, name='home'),  # Homepage
    path('shop/', ProductListView.as_view(), name='product_list'),  # Shop view
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('cart/', views.view_cart, name='view_cart'),
    path(
        'add-to-cart/<int:product_id>/<int:size_id>/',
        views.add_to_cart, name='add_to_cart'),
    path(
        'remove-from-cart/<int:item_id>/',
        views.remove_from_cart, name='remove_from_cart'),
    path(
        'update_cart_quantity/<int:item_id>/',
        views.update_cart_quantity, name='update_cart_quantity'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path(
        'admin-dashboard/orders/bulk/',
        bulk_order_action, name='bulk_order_action'),


    # Admin Dashboard
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path(
        'admin-dashboard/product/add/',
        product_create, name='product_create'),
    path(
        'admin-dashboard/product/<int:pk>/edit/',
        product_edit, name='product_edit'),
    path(
        'admin-dashboard/product/<int:pk>/delete/',
        product_delete, name='product_delete'),
    path(
        'admin-dashboard/product/<int:product_id>/sizes/',
        add_product_sizes, name='add_product_sizes'),
    path(
        'admin-dashboard/orders/',
        admin_order_list, name='admin_order_list'),
    path(
        'admin-dashboard/orders/<int:order_id>/',
        admin_order_detail, name='admin_order_detail'),
    path(
        'admin-dashboard/orders/<int:order_id>/delete/',
        admin_order_delete, name='admin_order_delete'),


    # AJAX Newsletter Signup
    path(
        'ajax/newsletter-signup/',
        newsletter_signup_ajax, name='newsletter_signup_ajax'),

    # Stripe Checkout
    path('checkout/', views.checkout, name='checkout'),
    path(
        'create-checkout-session/',
        views.create_checkout_session, name='create_checkout_session'),
    path(
        'order-confirmation/',
        views.order_confirmation, name='order_confirmation'),
]
