from rest_framework import serializers
from wellness.models import CycleCalendar, CyclePhase, NutritionPlan, TrainingPlan


class CalendarDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = CycleCalendar
        fields = '__all__'

class CyclePhaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CyclePhase
        fields = '__all__'

class NutritionPlanSerializer(serializers.ModelSerializer):
    phase = CyclePhaseSerializer(read_only=True)

    class Meta:
        model = NutritionPlan
        fields = ['id', 'phase', 'title', 'content', 'meal_suggestions', 'supplements', 'created_at']

class TrainingPlanSerializer(serializers.ModelSerializer):
    phase = CyclePhaseSerializer(read_only=True)

    class Meta:
        model = TrainingPlan
        fields = ['id', 'phase', 'title', 'content', 'exercises', 'workout_tips', 'recovery_tips', 'intensity_level', 'duration_minutes', 'created_at']

class PhasePlansSerializer(serializers.Serializer):
    """Combined serializer for nutrition and training plans by phase"""
    phase = CyclePhaseSerializer(read_only=True)
    nutrition_plan = NutritionPlanSerializer(read_only=True)
    training_plan = TrainingPlanSerializer(read_only=True)
