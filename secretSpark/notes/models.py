from django.db import models

from secretSpark.notes.choices import CyclePhases, Symptoms


class CycleCalendar(models.Model):

    # user = models.OneToOneField(
    #     to='users.User',
    #     on_delete=models.CASCADE
    # )
    start_date = models.DateField()
    cycle_length = models.SmallIntegerField() # Varying from 28 to 35 days
    period_length = models.SmallIntegerField() # Varying from 3 to 7 days
    last_period_date = models.DateField()
    current_phase = models.CharField(
        max_length=20,
        choices=CyclePhases
    )


class Diary(models.Model):

    # user = models.ForeignKey(
    #     to='users.User',
    #     on_delete=models.CASCADE
    # )
    date = models.DateField(
        auto_now_add=True
    )
    content = models.TextField()
    cycle_day = models.SmallIntegerField()
    symptoms = models.CharField(
        max_length=20,
        choices=Symptoms
    )







