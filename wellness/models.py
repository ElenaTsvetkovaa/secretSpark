from django.db import models
from wellness.choices import Phases


class CyclePhase(models.Model):

    phase_name = models.CharField(
        max_length=50,
        choices=Phases
    )
    description = models.TextField()

    def __str__(self):
        return self.phase_name


class CycleCalendar(models.Model):

    last_period_date = models.DateField()
    cycle_length = models.PositiveSmallIntegerField(
        default=28
    )
    period_length = models.PositiveSmallIntegerField(
        default=5
    )







