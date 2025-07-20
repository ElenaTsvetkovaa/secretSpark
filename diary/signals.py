from django.db.models.signals import post_migrate
from django.dispatch import receiver

from diary.models import Moods


@receiver(post_migrate)
def populate_moods(sender, **kwargs):
    moods = [
        {
            "mood": "Happy",
            "reminder": "Stay present in your joy — you're glowing for a reason!",
            "image": "moods/happy.png"
        },
        {
            "mood": "Angry",
            "reminder": "It’s okay to feel this. Breathe deeply and respond, not react.",
            "image": "moods/anger.png"
        },
        {
            "mood": "In Period",
            "reminder": "Take it easy today. Rest, hydrate, and honor your body.",
            "image": "moods/in_period.png"
        },
        {
            "mood": "Calm",
            "reminder": "Protect your peace — you’ve earned this calm.",
            "image": "moods/calm.png"
        },
        {
            "mood": "Heartbroken",
            "reminder": "Healing takes time. Let yourself feel and trust that better days are coming.",
            "image": "moods/heartbroken.png"
        },
    ]

    for mood in moods:
        Moods.objects.update_or_create(
            mood=mood['mood'],
            defaults={
                'reminder': mood['reminder'],
                'image': mood['image']
            }
        )
