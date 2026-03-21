# users/validators.py

import os
from django.core.exceptions import ValidationError


def validate_file_size(value):
    """Walidator ograniczajacy rozmiar przesylanego pliku do 5 MB."""
    max_size = 5 * 1024 * 1024  # 5 MB w bajtach

    if value.size > max_size:
        raise ValidationError(
            f'Rozmiar pliku ({value.size / 1024 / 1024:.1f} MB) '
            f'przekracza dozwolony limit 5 MB.'
        )


def validate_image_extension(value):
    """Walidator sprawdzajacy rozszerzenie przesylanego pliku."""
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    ext = os.path.splitext(value.name)[1].lower()

    if ext not in valid_extensions:
        raise ValidationError(
            f'Niedozwolone rozszerzenie pliku: {ext}. '
            f'Dozwolone formaty: {", ".join(valid_extensions)}'
        )
