from django.shortcuts import render
from django.http import JsonResponse
from datetime import timedelta, date
from .models import CycleCalendar  # Assuming this is your model


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
    return render(request, 'notes/cycle-calendar-events.html')