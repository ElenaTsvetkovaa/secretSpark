from django.db import models
from diary.choices import MoodChoices


class Diary(models.Model):

    date = models.DateField()
    content = models.TextField()
    mood = models.ForeignKey(
        to='Moods',
        on_delete=models.SET_DEFAULT,
        default=4,    # This is calm in the db
    )


class Moods(models.Model):

    mood = models.CharField(
        max_length=50,
        choices=MoodChoices.choices,
        default=MoodChoices.CALM,
        blank=True,
        unique=True
    )
    reminder = models.CharField(
        max_length=200,
    )
    image = models.ImageField(
        upload_to='mood-images/'
    )
