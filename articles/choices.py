from django.db import models


class ArticleCategories(models.TextChoices):

    SELF_IMPROVEMENT = 'SIM', 'Self Improvement'
    WORK_AND_MONEY = 'WAM', 'Work and Money'
    STYLE = 'STY', 'Style'


