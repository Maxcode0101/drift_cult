from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_view, name='shop'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]