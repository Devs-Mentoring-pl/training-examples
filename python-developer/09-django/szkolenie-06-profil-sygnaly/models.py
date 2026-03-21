# users/models.py

from django.db import models
from django.contrib.auth.models import User
from .validators import validate_image_size


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='default.jpg',
        upload_to='profile_pics',
        validators=[validate_image_size],
    )

    def __str__(self):
        return f"Profil uzytkownika {self.user.username}"
