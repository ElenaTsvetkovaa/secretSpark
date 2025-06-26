from django.urls import reverse_lazy
from django.views.generic import CreateView
from wellness.forms import CalendarCycleForm
from wellness.models import CycleCalendar

class TrackPeriodView(CreateView):
    model = CycleCalendar
    template_name = "wellness/track-period.html"
    form_class = CalendarCycleForm
    success_url = reverse_lazy('track-period')




