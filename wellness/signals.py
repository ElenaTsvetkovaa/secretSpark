from django.db.models.signals import post_migrate
from django.dispatch import receiver

from wellness.choices import Phases
from wellness.models import CyclePhase


@receiver(post_migrate)
def populate_cycle_phases(sender, **kwargs):
    phases_data = [
        {
            "name": Phases.MENSTRUAL,
            "description": (
                "This is the start of your cycle. The menstrual phase involves shedding of the uterine lining, "
                "which results in bleeding. You might feel more tired or emotionally sensitive during this time. "
                "It’s important to rest, stay hydrated, and nourish your body. Hormone levels like estrogen and "
                "progesterone are at their lowest, which can affect energy and mood."
            ),
        },
        {
            "name": Phases.FOLLICULAR,
            "description": (
                "Following your period, the follicular phase begins. Your body is preparing to release an egg, "
                "and estrogen levels start to rise. You may feel more energetic and focused. This is often a great time "
                "for productivity and physical activity. The uterine lining also begins to rebuild in preparation for possible pregnancy."
            ),
        },
        {
            "name": Phases.OVULATION,
            "description": (
                "Ovulation usually occurs mid-cycle and is the time when an egg is released from the ovary. "
                "Estrogen peaks, and you may feel your most confident and vibrant. Some people notice mild pelvic pain or a change in discharge. "
                "This is your most fertile phase, and libido may naturally increase. It’s a powerful time physically and emotionally."
            ),
        },
        {
            "name": Phases.LUTEAL,
            "description": (
                "After ovulation, the luteal phase begins. Progesterone levels rise to prepare the body for a possible pregnancy. "
                "You may start to feel more introspective or emotional as PMS symptoms (like bloating, mood changes, or cravings) can occur. "
                "It's a good time for rest, self-care, and reflecting. Hormone fluctuations are natural and it’s okay to slow down a bit here."
            ),
        },
    ]

    for phase in phases_data:
        CyclePhase.objects.update_or_create(
            name=phase["name"],
            defaults={"description": phase["description"]}
        )



