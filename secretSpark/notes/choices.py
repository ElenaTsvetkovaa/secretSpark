from django.db import models
from enum import StrEnum


class Phases(models.TextChoices):

    MENSTRUAL = 'M, Menstrual'
    FOLLICULAR = 'F, Follicular'
    OVULATION = 'O, Ovulation'
    LUTEAL = 'L, Luteal'


class Symptoms(StrEnum):
    CRAMPS = "Cramps"
    HEADACHE = "Headache"
    FATIGUE = "Fatigue"
    BLOATING = "Bloating"
    MOOD_SWINGS = "Mood Swings"
    NAUSEA = "Nausea"
    BACK_PAIN = "Back Pain"
    ACNE = "Acne"
    INSOMNIA = "Insomnia"
    APPETITE_CHANGES = "Appetite Changes"





