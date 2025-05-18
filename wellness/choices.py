from django.db import models
from enum import StrEnum


class Phases(models.TextChoices):

    MENSTRUAL = 'M', 'Menstrual'
    FOLLICULAR = 'F', 'Follicular'
    OVULATION = 'O', 'Ovulation'
    LUTEAL = 'L', 'Luteal'

class MoodChoices(models.TextChoices):

    HAPPY = 'Happy' 'Happy'
    CALM = 'Calm' 'Calm'
    CONFIDENT = 'Confident' 'Confident'
    GRATEFUL = 'Grateful' 'Grateful'
    OPTIMISTIC = 'Optimistic' 'Optimistic'
    SAD = 'Sad' 'Sad'
    INSECURE = 'Insecure' 'Insecure'
    TIRED = 'Tired' 'Tired'
    ANXIOUS = 'Anxious' 'Anxious'
    IRRITABLE = 'Irritable' 'Irritable'
    EXCITED = 'Excited', 'Excited'
    LONELY = 'Lonely', 'Lonely'
    OVERWHELMED = 'Overwhelmed', 'Overwhelmed'
    PEACEFUL = 'Peaceful', 'Peaceful'
    MOTIVATED = 'Motivated', 'Motivated'
    BORED = 'Bored', 'Bored'
    STRESSED = 'Stressed', 'Stressed'
    HOPEFUL = 'Hopeful', 'Hopeful'
    JEALOUS = 'Jealous', 'Jealous'
    CONTENT = 'Content', 'Content'
    FRUSTRATED = 'Frustrated', 'Frustrated'
    NOSTALGIC = 'Nostalgic', 'Nostalgic'
    GUILTY = 'Guilty', 'Guilty'
    RELIEVED = 'Relieved', 'Relieved'
    EMBARRASSED = 'Embarrassed', 'Embarrassed'
    CURIOUS = 'Curious', 'Curious'
    INSPIRED = 'Inspired', 'Inspired'
    APATHETIC = 'Apathetic', 'Apathetic'
    SHY = 'Shy', 'Shy'
    PROUD = 'Proud', 'Proud'





