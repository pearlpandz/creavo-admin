from django.urls import re_path
from api.views import index

urlpatterns = [
    re_path(r'^.*$', index),
]
