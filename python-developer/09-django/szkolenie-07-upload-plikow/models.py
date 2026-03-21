# users/models.py

from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .validators import validate_file_size


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='default.jpg',
        upload_to='profile_pics',
        validators=[validate_file_size],
    )

    def __str__(self):
        return f'Profil uzytkownika {self.user.username}'

    def save(self, *args, **kwargs):
        # Najpierw zapisz profil (i plik na dysk)
        super().save(*args, **kwargs)

        # Nastepnie przeskaluj obraz, jesli jest za duzy
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
