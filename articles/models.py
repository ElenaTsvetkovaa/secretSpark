from django.db import models
from articles.choices import ArticleCategories
from articles.mixins import TimeStampMixin


class Article(models.Model):

    title = models.CharField(
        max_length=200
    )
    banner = models.ImageField(
        upload_to='section-images/'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    category = models.CharField(
        max_length=50,
        choices=ArticleCategories.choices
    )

    class Meta:
        ordering =  ('-updated_at', )


    def __str__(self):
        return f"{self.title} - {self.id}"


class Section(models.Model):

    title = models.CharField(
        max_length=150
    )
    content = models.TextField()
    image = models.ImageField(
        upload_to='section-images/',
        blank=True,
        null=True
    )
    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        related_name='sections'
    )

    def __str__(self):
        return f"{self.title} - {self.id}"



