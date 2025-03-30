from django.core.validators import MinLengthValidator
from django.db import models

from secretSpark.articles.choices import ArticleCategories
from secretSpark.articles.mixins import TimeStampMixin


class Article(TimeStampMixin):

    title = models.CharField(
        max_length=100
    )
    content = models.TextField(
        validators=[
            MinLengthValidator(200, message='The content must be longer.')
        ]
    )
    category = models.CharField(
        max_length=50,
        choices=ArticleCategories
    )










