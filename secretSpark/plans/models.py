from django.db import models


class BasePlan(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=50,
        unique=True
    )
    description = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


class NutritionPlan(BasePlan):

    meals =










