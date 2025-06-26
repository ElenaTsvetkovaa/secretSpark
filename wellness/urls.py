from django.urls import path, include
from wellness import views

urlpatterns = [
    path('track-period/', views.TrackPeriodView.as_view(), name='track-period'),
]
