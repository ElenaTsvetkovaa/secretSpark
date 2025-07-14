from django.db import models
from articles.choices import ArticleCategories
from articles.mixins import TimeStampMixin
from common.models import BaseContent


class Article(BaseContent):

    category = models.CharField(
        max_length=50,
        choices=ArticleCategories.choices
    )

    class Meta:
        ordering =  ('-updated_at', )


    def __str__(self):
        return f"{self.title} - {self.id}"


class ArticleSection(models.Model):

    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE
    )
    section = models.OneToOneField(
        to='common.Section',
        on_delete=models.CASCADE
    )


