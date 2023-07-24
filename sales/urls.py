from django.urls import path
from . import views


urlpatterns = [
    path('sale-list/', views.SalesList, name="sale-list"),
    path('', views.home, name='sales-home'),
    path('sale/<int:pk>/', views.saleListDetail, name='saleListDetail'),
    
]

