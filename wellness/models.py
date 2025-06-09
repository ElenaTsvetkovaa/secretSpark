from django.contrib.postgres.fields import ArrayField
from django.db import models
from wellness.choices import Phases, MoodChoices


class CyclePhase(models.Model):

    phase_name = models.CharField(
        max_length=50,
        choices=Phases
    )
    description = models.TextField()

    def __str__(self):
        return self.phase_name


class CycleProfile(models.Model):

    # TODO when I create user roles
    # user = models.ForeignKey(
    #     'User',
    #     on_delete=models.CASCADE
    # )
    cycle_length = models.PositiveSmallIntegerField(
        default=28
    )
    period_length = models.PositiveSmallIntegerField(
        default=5
    )
    last_period_date = models.DateField()


class Diary(models.Model):

    # TODO when I create user roles
    # user = models.ForeignKey(
    #     to='User',
    #     on_delete=models.CASCADE
    # )
    date = models.DateField(
        auto_now=True,
    )
    content = models.TextField()


class Moods(models.Model):

    mood = models.CharField(
        max_length=50,
        choices=MoodChoices.choices,
        blank=True,
        unique=True
    )
    reminder = models.CharField(
        max_length=200,
    )
    image = models.ImageField(
        upload_to='static/images/moods/'
    )







