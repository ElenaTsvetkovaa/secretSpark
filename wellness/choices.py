from django.db import models
from enum import StrEnum


class Phases(models.TextChoices):

    MENSTRUAL = 'M', 'Menstrual'
    FOLLICULAR = 'F', 'Follicular'
    OVULATION = 'O', 'Ovulation'
    LUTEAL = 'L', 'Luteal'



