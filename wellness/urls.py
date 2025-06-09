from django.urls import path, include
from .views import cycle_calendar_view, diary_page, MoodListView

urlpatterns = [
    path('api/cycle-calendar/', cycle_calendar_view, name='cycle-calendar-events'),
    path('diary/', include([
        path('', diary_page, name='diary-page'),
        path('api/moods/', MoodListView.as_view(), name='mood-list'),
    ])),
]
