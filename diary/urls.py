from django.urls import path, include
from diary import views

urlpatterns = [
    path('', views.DiaryPageCreateView.as_view(), name='diary-page'),
    path('<int:pk>/', views.DiaryPageUpdateView.as_view() , name='diary-update'),
    path('entry/', views.get_entry_by_date, name='diary-entry'),
    path('moods/', views.MoodListView.as_view(), name='moods-tracker'),
]
