from rest_framework import serializers
from wellness.models import CycleCalendar


class CalendarDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = CycleCalendar
        fields = '__all__'

