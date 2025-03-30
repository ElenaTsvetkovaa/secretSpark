from django.urls import path
from secretSpark.common.views import home, index

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),

]