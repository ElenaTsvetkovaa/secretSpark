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

    # user = models.OneToOneField(
    #     to='users.User',
    #     on_delete=models.CASCADE
    # )
    start_date = models.DateField()
    cycle_length = models.SmallIntegerField() # Varying from 28 to 35 days
    period_length = models.SmallIntegerField() # Varying from 3 to 7 days
    last_period_date = models.DateField()

class CyclePhaseOccurrence(models.Model):
    calendar = models.ForeignKey(CycleCalendar, on_delete=models.CASCADE)  # One calendar has multiple phase occurrences
    phase = models.ForeignKey(CyclePhase, on_delete=models.CASCADE)  # Links to a specific phase
    start_date = models.DateField()
    end_date = models.DateField()

#     def __str__(self):
#         return f"{self.calendar.user.username}'s {self.phase.name} Phase ({self.start_date} - {self.end_date})"
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






