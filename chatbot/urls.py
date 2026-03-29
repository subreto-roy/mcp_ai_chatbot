from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/products/', views.product_list, name='product-list'),
    path('api/products/<int:pk>/', views.product_detail, name='product-detail'),
    path('api/chat/', views.chat, name='chat'),
]