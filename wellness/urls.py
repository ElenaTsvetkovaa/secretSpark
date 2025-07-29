from django.urls import path, include
from wellness import views

urlpatterns = [
    path('', views.TrackPeriodView.as_view(), name='track-period'),
    path('api/track-period/', views.TrackPeriodAPIView.as_view(), name='api-track-period'),
    path('api/show-results/', views.CyclePhasesResultsView.as_view(), name='api-show-results'),
    path('api/generate-plans/<str:phase_name>/', views.GeneratePlansAPIView.as_view(), name='api-generate-plans'),
]
