from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_list, name='community_list'),
    path('<slug:slug>/', views.community_detail, name='community_detail'),
]