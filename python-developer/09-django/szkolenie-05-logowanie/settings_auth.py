# first_project/settings.py -- ustawienia autoryzacji (dodaj na koncu pliku)

LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'login'

# Ustawienia bezpieczenstwa sesji
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1209600  # 2 tygodnie w sekundach
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # False na localhost
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True  # False na localhost
