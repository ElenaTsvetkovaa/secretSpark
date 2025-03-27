from django.core.validators import MinValueValidator
from django.db import models

from secretSpark.notes.choices import Phases, Symptoms

class CyclePhase(models.Model):

    phase_name = models.CharField(
        max_length=50,
        choices=Phases
    )
    description = models.TextField(
        validators=[
            MinValueValidator(100, message='Enter at least 100 words!')
        ]
    )

    def __str__(self):
        return self.phase_name


class CycleCalendar(models.Model):

    start_date = models.DateField()
    cycle_length = models.SmallIntegerField() # Varying from 28 to 35 days
    period_length = models.SmallIntegerField() # Varying from 3 to 7 days
    last_period_date = models.DateField()


# #
# class Diary(models.Model):
#
#     # user = models.ForeignKey(
#     #     to='users.User',
#     #     on_delete=models.CASCADE
#     # )
#     date = models.DateField(
#         auto_now_add=True
#     )
#     content = models.TextField()
#     cycle_day = models.SmallIntegerField()
#     symptoms = models.CharField(
#         max_length=20,
#     )
#






