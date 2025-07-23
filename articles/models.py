from cloudinary.utils import cloudinary_url
from django.db import models
from articles.choices import ArticleCategories
from articles.mixins import TimeStampMixin
from cloudinary.models import CloudinaryField


class Article(models.Model):

    title = models.CharField(
        max_length=200
    )
    banner = CloudinaryField(
        'image',
        folder='section-images'
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

    @property
    def banner_url(self):
        if not self.banner:
            return None
        url, _ = cloudinary_url(self.banner.public_id, secure=True)
        return url


class Section(models.Model):

    title = models.CharField(
        max_length=150
    )
    content = models.TextField()
    image = CloudinaryField(
        'image',
        folder='section-images',
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

    @property
    def image_url(self):
        if not self.image:
            return None
        url, _ = cloudinary_url(self.image.public_id, secure=True)
        return url



