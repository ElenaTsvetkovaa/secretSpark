from django.db.models import When, Value, Case
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy

from rest_framework.views import APIView

from diary.forms import DiaryForm, MoodsForm
from diary.models import Moods, Diary
from diary.serializers import MoodsSerializer


# def diary_page(request):
#     diary_form = DiaryForm(request.POST or None)
#
#     if request.method == 'POST' and diary_form.is_valid():
#         diary_form.save()
#
#     context = {
#         "diary_form": diary_form,
#     }
#
#     return render(request, 'diary/diary-page.html', context)

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


class DiaryPageView(CreateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary-page.html'
    success_url = reverse_lazy('diary-page')

    def form_valid(self, form):
        mood_id = int(self.request.POST.get("selected_mood"))
        form.instance.mood_id = int(self.request.POST.get("selected_mood"))
        form.instance.date = self.request.POST.get("selected_date")
        return super().form_valid(form)


