from django.urls import path
from common.views import index

urlpatterns = [
    path('', index, name='home'),
]