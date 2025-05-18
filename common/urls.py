from django.urls import path
from common.views import home, index

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),

]