from datetime import timedelta

from django.db.models import Case, When, Value
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from wellness.forms import DiaryForm, MoodsForm
from wellness.models import Moods
from wellness.serializers import MoodsSerializer


def generate_cycle_events(cycle):
    """Generate cycle phases based on start date and cycle length."""
    start_date = cycle.start_date
    period_length = cycle.period_length
    cycle_length = cycle.cycle_length

    events = [
        {"title": "Menstrual", "start": start_date, "end": start_date + timedelta(days=period_length - 1),
         "className": "menstrual-phase"},
        {"title": "Follicular", "start": start_date + timedelta(days=period_length),
         "end": start_date + timedelta(days=cycle_length - 14), "className": "follicular-phase"},
        {"title": "Ovulation", "start": start_date + timedelta(days=cycle_length - 14),
         "end": start_date + timedelta(days=cycle_length - 10), "className": "ovulatory-phase"},
        {"title": "Luteal", "start": start_date + timedelta(days=cycle_length - 10),
         "end": start_date + timedelta(days=cycle_length - 1), "className": "luteal-phase"},
    ]

    return events


# def cycle_calendar_events(request):
#     """Django view to return cycle events as JSON."""
#     cycle = CycleCalendar.objects.first()  # Get the first cycle (for now)
#
#     if cycle:
#         events = generate_cycle_events(cycle)
#         return JsonResponse(events, safe=False)
#
#     return JsonResponse([], safe=False)

def cycle_calendar_view(request):
    return render(request, 'wellness/cycle-calendar-events.html')


def diary_page(request):
    diary_form = DiaryForm(request.POST or None)
    mood_form = MoodsForm(request.POST or None)

    if diary_form.is_valid():
        diary_form.save()

    if mood_form.is_valid():
        mood_form.save()

    context = {
        "diary_form": diary_form,
        "mood_form": mood_form,
    }

    return render(request, 'wellness/diary-page.html', context)

class MoodListView(APIView):

    def get(self, request):
        moods = Moods.objects.annotate(
            custom_order=Case(
                When(mood='Heartbroken', then=Value(0)),
                When(mood='Angry', then=Value(1)),
                When(mood='In Period', then=Value(2)),
                When(mood='Calm', then=Value(3)),
                When(mood='Happy', then=Value(4)),
            )
        ).order_by('custom_order')
        serializer = MoodsSerializer(moods, many=True)

        return Response(serializer.data)


