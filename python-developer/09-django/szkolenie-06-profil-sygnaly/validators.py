# users/validators.py

from django.core.exceptions import ValidationError


def validate_image_size(image):
    """Odrzuca obrazy wieksze niz 5 MB."""
    max_size_mb = 5
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Maksymalny rozmiar pliku to {max_size_mb} MB.")
