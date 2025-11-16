from django.urls import path
from .views import retailer_dashboard

urlpatterns = [
    path('dashboard/', retailer_dashboard, name='retailer_dashboard'),
]
