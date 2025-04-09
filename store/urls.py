from django.urls import path
from . import views
from .views import ProductListView


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('', views.shop_view, name='shop'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile_view, name='profile'),
]