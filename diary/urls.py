from django.urls import path, include
from diary import views

urlpatterns = [
    path('', views.DiaryPageView.as_view(), name='diary-page'),
    path('moods/', views.MoodListView.as_view(), name='moods-tracker'),
]
