from django.urls import path
from .views import cycle_calendar_view

urlpatterns = [
    path('api/cycle-calendar/', cycle_calendar_view, name='cycle-calendar-events'),
]
