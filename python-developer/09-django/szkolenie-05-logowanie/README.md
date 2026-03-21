# Szkolenie 5: Logowanie i autoryzacja

Kod z szkolenia Django nr 5 -- LoginView, LogoutView, @login_required, warunkowy navbar.

## Pliki

- `urls.py` -- routing z LoginView, LogoutView, register, profile
- `views.py` -- widoki register (z redirect na login) i profile (@login_required)
- `settings_auth.py` -- ustawienia LOGIN_REDIRECT_URL, LOGIN_URL, bezpieczenstwo sesji
- `templates/users/login.html` -- formularz logowania z crispy-forms
- `templates/users/logout.html` -- strona po wylogowaniu
- `templates/users/profile.html` -- prosta strona profilu
- `navbar_auth.html` -- fragment navbar-a z user.is_authenticated

## Kluczowe koncepty

- LoginView i LogoutView z django.contrib.auth.views
- LOGIN_REDIRECT_URL i LOGIN_URL w settings.py
- Dekorator @login_required (FBV) i LoginRequiredMixin (CBV)
- user.is_authenticated w szablonach
- Wylogowanie przez POST (Django 5.x) z {% csrf_token %}
- Bezpieczenstwo sesji: SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SECURE
