from django.core.validators import MinLengthValidator
from django.db import models

from articles.choices import ArticleCategories
from articles.mixins import TimeStampMixin


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

    photo = models.ImageField()

    # TODO when I create user roles
    # author =   models.ForeignKey(
    #     to=settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    # )
    # likes = models.ManyToManyField(
    #     to=settings.AUTH_USER_MODEL,
    #     related_name='likes',
    #     blank=True
    # )


class Comment(TimeStampMixin):

    # TODO when I create user roles
    # user = models.ForeignKey(
    #     to=settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE
    # )
    article = models.ManyToManyField(
        to=Article,
    )
    text = models.TextField()





