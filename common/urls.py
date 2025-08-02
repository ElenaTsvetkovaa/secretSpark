from django.urls import path
from common.views import index, health_check

urlpatterns = [
    path('', index, name='home'),
    path('health/', health_check, name='health_check'),
]