from django.urls import path
from secretSpark.common.views import home

urlpatterns = [
    path('', home, name='common'),

]