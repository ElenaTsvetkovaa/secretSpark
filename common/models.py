from django.db import models


class BaseContent(models.Model):

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

    class Meta:
        abstract = True


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

    def __str__(self):
        return f"{self.title} - {self.id}"

