from django.urls import path
from .views import distributor_dashboard

urlpatterns = [
    path('dashboard/', distributor_dashboard, name='distributor_dashboard'),
]
