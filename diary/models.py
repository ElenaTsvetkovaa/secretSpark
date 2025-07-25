from django.contrib.auth import get_user_model
from django.db import models
from diary.choices import MoodChoices


class Diary(models.Model):

    profile = models.ForeignKey(
        to="accounts.Profile",
        on_delete=models.CASCADE
    )
    date = models.DateField()
    content = models.TextField()
    mood = models.ForeignKey(
        to='Moods',
        on_delete=models.SET_DEFAULT,
        default=4,    # This is calm in the db
    )

    def __str__(self):
        return f'{self.profile.user.first_name} - {self.date}'


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

    def __str__(self):
        return f'{self.id} - {self.mood}'
