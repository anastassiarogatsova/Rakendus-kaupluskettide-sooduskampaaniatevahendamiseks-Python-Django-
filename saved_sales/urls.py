from django.urls import path
from . import views


urlpatterns = [
    path('saved-sales/', views.SendSaved, name="SendSaved"),
    path('saved/', views.about, name="about"),
    
]
