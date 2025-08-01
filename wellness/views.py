from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from django.views.generic import CreateView, TemplateView
from rest_framework import generics, permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from wellness.models import CycleCalendar, CyclePhase, NutritionPlan, TrainingPlan
from wellness.serializers import CalendarDataSerializer, NutritionPlanSerializer, TrainingPlanSerializer, PhasePlansSerializer
from wellness.services import PlanGeneratorService


class TrackPeriodView(TemplateView):
    template_name = "wellness/period-tracker.html"


class TrackPeriodAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CalendarDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return CycleCalendar.objects.get(profile=self.request.user.profile)
        except CycleCalendar.DoesNotExist:
            return None
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save(profile=request.user.profile)
        return Response(serializer.data)


def calculate_phases(start_date, period_length, cycle_length):
    """
    Perform calculations for the relative time frames of each phase.
    Example: {
        'menstrual': (2025-07-01, 2025-07-05),
        'follicular': (2025-07-01, 2025-07-13),
        'ovulation': (2025-07-14, 2025-07-14),
        'luteal': (2025-07-15, 2025-07-28)
    }
    """
    menstrual = (start_date, start_date + timedelta(days=period_length - 1)) # From first bleeding until the end of it(period length)
    ovulation = start_date + timedelta(days=cycle_length - 14) # Always around 14 days of the whole cycle
    follicular = (start_date, ovulation - timedelta(days=1)) # From bleeding until 1 day before ovulation
    luteal = (ovulation + timedelta(days=1), start_date + timedelta(days=cycle_length - 1)) # After ovulation until the end of the cycle length

    return {
        "menstrual": menstrual,
        "follicular": follicular,
        "ovulation": (ovulation, ovulation),
        "luteal": luteal
    }


def generate_phases_around_date(last_period_date, period_length, cycle_length, window_start, window_end):
    """
    Generating phases based on given date for 3 months ahead
    """
    phases_list = []

    # Days between window start and window end considering the period date
    days_before = (last_period_date - window_start).days
    days_after = (window_end - last_period_date).days

    # Calculating full cycles between these days
    cycles_before = max(0, (days_before // cycle_length) + 1)
    cycles_after = max(0, (days_after // cycle_length) + 1)

    for i in range(-cycles_before, cycles_after + 1):
        cycle_start = last_period_date + timedelta(days=i * cycle_length)
        phases = calculate_phases(cycle_start, period_length, cycle_length)

        for phase_name, (phase_start, phase_end) in phases.items():
            if phase_end >= window_start and phase_start <= window_end:
                phases_list.append({
                    "name": phase_name,
                    "start": phase_start,
                    "end": phase_end
                })

    return phases_list


class CyclePhasesResultsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        profile = request.user.profile
        cycle_data = CycleCalendar.objects.get(profile=profile)

        offset = int(request.GET.get("offset", 0))

        today = datetime.today().date()
        base_month = datetime(today.year, today.month, 1).date()
        window_start = base_month + relativedelta(months=offset)
        window_end = window_start + relativedelta(months=3) - timedelta(days=1)

        all_phases = generate_phases_around_date(
            last_period_date=cycle_data.last_period_date,
            period_length=cycle_data.period_length,
            cycle_length=cycle_data.cycle_length,
            window_start=window_start,
            window_end=window_end
        )

        # Calculate current phase independently of offset
        current_phase_data = calculate_current_phase_and_plans(
            last_period_date=cycle_data.last_period_date,
            period_length=cycle_data.period_length,
            cycle_length=cycle_data.cycle_length
        )

        # Converting date objects to strings
        for phase in all_phases:
            phase["start"] = phase["start"].isoformat()
            phase["end"] = phase["end"].isoformat()

        return Response({
            "phases": all_phases,
            "current_phase": current_phase_data
        })


def calculate_current_phase_and_plans(last_period_date, period_length, cycle_length):
    """
    Calculate the current phase based on today's date and cycle data.
    Returns a dict with current phase info and related plans.
    """
    today = datetime.today().date()
    
    # Calculate how many days since the last period started
    days_since_period = (today - last_period_date).days
    
    # Find the current cycle position
    current_cycle_day = (days_since_period % cycle_length) + 1
    
    # Calculate phase boundaries for current cycle
    cycle_start = last_period_date + timedelta(days=(days_since_period // cycle_length) * cycle_length)
    phases = calculate_phases(cycle_start, period_length, cycle_length)
    
    # Find which phase today falls into
    current_phase_name = None
    for phase_name, (phase_start, phase_end) in phases.items():
        if phase_start <= today <= phase_end:
            current_phase_name = phase_name
            break
    
    # Get phase description and plans from database
    if current_phase_name:
        current_phase_obj = CyclePhase.objects.filter(name=current_phase_name).first()
        if current_phase_obj:
            nutrition_plan = NutritionPlan.objects.filter(phase=current_phase_obj).order_by('-created_at').first()
            training_plan = TrainingPlan.objects.filter(phase=current_phase_obj).order_by('-created_at').first()

            if not nutrition_plan or not training_plan:
                try:
                    service = PlanGeneratorService()
                    
                    if not nutrition_plan:
                        nutrition_plan = service.generate_nutrition_plans(current_phase_name)
                    
                    if not training_plan:
                        training_plan = service.generate_training_plans(current_phase_name)
                except Exception as e:
                    print(f"Error generating plans: {e}")
            
            return {
                "name": current_phase_obj.name.capitalize(),
                "description": current_phase_obj.description,
                "nutrition_plan": NutritionPlanSerializer(nutrition_plan).data if nutrition_plan else None,
                "training_plan": TrainingPlanSerializer(training_plan).data if training_plan else None
            }
    
    # Fallback if no phase found
    return {
        "name": "Unknown",
        "description": "Unable to determine current phase.",
        "nutrition_plan": None,
        "training_plan": None
    }


class GeneratePlansAPIView(generics.CreateAPIView):
    VALID_PHASES =  ['menstrual', 'follicular', 'ovulation', 'luteal']
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        phase_name = kwargs['phase_name']
        if phase_name not in self.VALID_PHASES:
            return Response(
                {"error": f"Invalid phase. Must be one of: {self.VALID_PHASES}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            service = PlanGeneratorService()

            nutrition_plan = service.generate_nutrition_plans(phase_name)
            training_plan = service.generate_training_plans(phase_name)

            nutrition_data = NutritionPlanSerializer(nutrition_plan).data
            training_data = TrainingPlanSerializer(training_plan).data

            return Response({
                "nutrition_plan": nutrition_data,
                "training_plan": training_data,
                "message": f"Plans generated successfully for {phase_name} phase"
            },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": f"Failed to generate plans: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


