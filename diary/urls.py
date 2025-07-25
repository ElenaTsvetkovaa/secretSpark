
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from diary import views

# REST API router for diary CRUD operations
router = DefaultRouter()
router.register(r'', views.DiaryViewSet, basename='diary')

urlpatterns = [
    path('page/', views.DiaryPageView.as_view(), name='diary-page'),
    path('moods/', views.MoodListView.as_view(), name='moods-tracker'),
    path('', include(router.urls)),  # /diary/, /diary/{id}/, /diary/by-date/
]
