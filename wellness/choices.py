from django.db import models
from enum import StrEnum


class Phases(models.TextChoices):

    MENSTRUAL = 'M', 'Menstrual'
    FOLLICULAR = 'F', 'Follicular'
    OVULATION = 'O', 'Ovulation'
    LUTEAL = 'L', 'Luteal'

class MoodChoices(models.TextChoices):

    HAPPY = 'Happy', 'Happy'
    IN_PERIOD = 'In Period', 'In Period'
    CALM = 'Calm', 'Calm'
    ANGRY = 'Angry', 'Angry'
    HEARTBROKEN = 'Heartbroken', 'Heartbroken'




