from cloudinary.models import CloudinaryField
from cloudinary.utils import cloudinary_url
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
    profile_picture = CloudinaryField(
        'image',
        folder='profile-pictures',
        blank = True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.id}"

    @property
    def image_url(self):
        if not self.profile_picture:
            return None
        url, _ = cloudinary_url(self.profile_picture.public_id, secure=True)
        return url

