from django.contrib.auth import get_user_model
from django.db import models
from wellness.choices import Phases


class CyclePhase(models.Model):
    # Uses signal to populate the db with pre-defined phases

    name = models.CharField(
        max_length=50,
        choices=Phases
    )
    description = models.TextField()

    def __str__(self):
        return self.name


class CycleCalendar(models.Model):

    profile = models.ForeignKey(
        to="accounts.Profile",
        on_delete=models.CASCADE
    )
    last_period_date = models.DateField(
    )
    cycle_length = models.PositiveSmallIntegerField(
        default=28,
    )
    period_length = models.PositiveSmallIntegerField(
        default=5,
    )







