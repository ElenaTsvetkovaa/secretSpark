from django.db import models


class ArticleCategories(models.TextChoices):

    SELF_IMPROVEMENT = 'self-improvement', 'Self Improvement'
    WORK_AND_MONEY = 'work-and-money', 'Work and Money'
    STYLE = 'style', 'Style'


