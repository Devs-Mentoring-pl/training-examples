# Szkolenie 7: Edycja profilu i upload plikow

Kod z szkolenia Django nr 7 -- formularze aktualizacji, upload plikow, skalowanie obrazow z Pillow.

## Pliki

- `forms.py` -- UserRegisterForm, UserUpdateForm, ProfileUpdateForm (ModelForm)
- `views.py` -- widok profile z obsluga GET/POST, request.FILES, wzorzec POST/Redirect/GET
- `models.py` -- model Profile z nadpisana metoda save() i skalowaniem Pillow
- `validators.py` -- validate_file_size (max 5 MB) i validate_image_extension
- `templates/users/profile.html` -- formularz edycji z enctype="multipart/form-data"
- `templates/blog/home.html` -- fragment z awatarem autora przy artykule

## Kluczowe koncepty

- ModelForm -- formularz powiazany z modelem, automatyczny save()
- Parametr instance= -- pre-populacja formularzy i UPDATE zamiast INSERT
- enctype="multipart/form-data" -- niezbedne do przesylania plikow
- request.FILES -- obiekt z przeslanymi plikami
- Pillow thumbnail() -- skalowanie z zachowaniem proporcji
- Nadpisywanie save() -- super().save(*args, **kwargs) przed przetwarzaniem
- Wzorzec POST/Redirect/GET -- zapobieganie duplikatom
