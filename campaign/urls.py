from django.urls import path
from . import views

urlpatterns = [
    path('', views.camphome, name='camp-home'),
    path('camp-list/', views.CampaignList, name="camp-list"),
]
