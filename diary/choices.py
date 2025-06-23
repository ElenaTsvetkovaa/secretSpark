from django.db import models


class MoodChoices(models.TextChoices):

    HAPPY = 'Happy', 'Happy'
    IN_PERIOD = 'In Period', 'In Period'
    CALM = 'Calm', 'Calm'
    ANGRY = 'Angry', 'Angry'
    HEARTBROKEN = 'Heartbroken', 'Heartbroken'

