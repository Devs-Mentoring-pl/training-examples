# first_project/settings.py -- konfiguracja mediow (dodaj na koncu pliku)

import os

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Alternatywnie w Django 5.x (pathlib):
# MEDIA_ROOT = BASE_DIR / 'media'
