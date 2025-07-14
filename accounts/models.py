from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username} - {self.id}"


UserModel = get_user_model()


class Profile(models.Model):

    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(
        upload_to='profile-pictures/',
        blank=True,
        null=True
    )


    def __str__(self):
        return f"{self.user.username} - {self.id}"
