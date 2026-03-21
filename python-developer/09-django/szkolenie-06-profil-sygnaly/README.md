# Szkolenie 6: Profil uzytkownika i sygnaly

Kod z szkolenia Django nr 6 -- model Profile z OneToOneField, sygnaly post_save, ImageField, konfiguracja mediow.

## Pliki

- `models.py` -- model Profile z OneToOneField do User i ImageField
- `signals.py` -- create_profile i save_profile z dekoratorem @receiver(post_save)
- `apps.py` -- rejestracja sygnalow w metodzie ready()
- `admin.py` -- rejestracja modelu Profile w panelu admina
- `validators.py` -- walidator rozmiaru obrazu (max 5 MB)
- `urls.py` -- routing z serwowaniem mediow w trybie DEBUG
- `settings_media.py` -- MEDIA_ROOT i MEDIA_URL
- `templates/users/profile.html` -- szablon profilu z awatarem

## Kluczowe koncepty

- OneToOneField -- relacja 1:1 miedzy User a Profile
- ImageField z Pillow -- przechowywanie obrazow
- Sygnaly Django (post_save) -- automatyczne tworzenie profilu przy rejestracji
- MEDIA_ROOT / MEDIA_URL -- konfiguracja przechowywania plikow
- Serwowanie mediow w trybie deweloperskim (if settings.DEBUG)
- Walidatory na poziomie modelu
