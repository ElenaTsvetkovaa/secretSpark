from django.urls import path
from secretSpark.home.views import home

urlpatterns = [
    path('', home, name='home'),

]