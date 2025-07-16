from django.db import models
from enum import StrEnum


class Phases(models.TextChoices):

    MENSTRUAL = 'menstrual', 'menstrual'
    FOLLICULAR = 'follicular', 'follicular'
    OVULATION = 'ovulation', 'ovulation'
    LUTEAL = 'luteal', 'luteal'



