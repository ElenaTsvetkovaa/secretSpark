from django.db.models import When, Value, Case
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView
from diary.forms import DiaryForm
from diary.mixins import DiaryFormMixin
from diary.models import Moods, Diary
from diary.serializers import MoodsSerializer



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


class DiaryPageCreateView(DiaryFormMixin, CreateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary-page.html'

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({"success": True, "diary_id": self.object.id})


class DiaryPageUpdateView(DiaryFormMixin, UpdateView):
    model = Diary
    form_class = DiaryForm
    template_name = 'diary/diary-page.html'

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({"success": True, "diary_id": self.object.id})


def get_entry_by_date(request):
    selected_date = request.GET.get("date")
    try:
        diary = Diary.objects.get(date=selected_date)
        return JsonResponse(data={
            "exists": True,
            "diary_id": diary.id,  # ← used for redirecting to update view
            "content": diary.content,
            "mood_id": diary.mood_id,
        })
    except Diary.DoesNotExist:
        return JsonResponse(data={
            "exists": False,
        })

