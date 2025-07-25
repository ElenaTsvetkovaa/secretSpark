from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import When, Value, Case
from django.views.generic import TemplateView
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from diary.models import Moods, Diary
from diary.serializers import MoodsSerializer, DiarySerializer


class DiaryPageView(LoginRequiredMixin, TemplateView):
    template_name = 'diary/diary-page.html'

class MoodListView(generics.ListAPIView):
    """API endpoint to list all moods in custom order"""
    permission_classes = [IsAuthenticated]
    serializer_class = MoodsSerializer
    
    def get_queryset(self):
        return Moods.objects.annotate(
            custom_order=Case(
                When(mood='Heartbroken', then=Value(0)),
                When(mood='Angry', then=Value(1)),
                When(mood='In Period', then=Value(2)),
                When(mood='Calm', then=Value(3)),
                When(mood='Happy', then=Value(4)),
            )
        ).order_by('custom_order')


class DiaryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for diary entries with full CRUD operations and custom date lookup.
    Custom endpoint: GET /diary/by-date/?date=2023-01-01
    """
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Diary.objects.filter(profile=self.request.user.profile)
        return queryset

    def perform_update(self, serializer):
        serializer.save(profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @action(detail=False, methods=['get'], url_path='by-date')
    def get_by_date(self, request):
        selected_date = request.query_params.get('date')
        if not selected_date:
            return Response(
                {'error': 'Date parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            diary = Diary.objects.get(profile=self.request.user.profile, date=selected_date)
            serializer = self.get_serializer(diary)
            return Response({
                'exists': True,
                'data': serializer.data
            })
        except Diary.DoesNotExist:
            return Response({'exists': False})