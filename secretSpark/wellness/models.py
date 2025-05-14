from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from secretSpark.wellness.choices import Phases, Symptoms

class CyclePhase(models.Model):

    phase_name = models.CharField(
        max_length=50,
        choices=Phases
    )
    description = models.TextField()

    def __str__(self):
        return self.phase_name


class CycleCalendar(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )
    cycle_length = models.SmallIntegerField() # Varying from 28 to 35 days
    period_length = models.SmallIntegerField() # Varying from 3 to 7 days
    last_period_date = models.DateField()


class Diary(models.Model):

    user = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE
    )
    created_at = models.DateField(
        auto_now_add=True
    )
    content = models.TextField()
    symptoms = ArrayField(
        base_field=models.CharField(max_length=30, choices=Symptoms.choices()),
        blank=True,
        default=list
    )


    class Meta:
        unique_together = ('user', 'created_at')







