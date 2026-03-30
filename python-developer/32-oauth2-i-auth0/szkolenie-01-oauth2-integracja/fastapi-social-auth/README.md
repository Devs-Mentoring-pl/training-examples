# Szkolenie 1: Social auth w FastAPI (Google + GitHub)

Przykładowa aplikacja FastAPI z logowaniem przez Google i GitHub za pomocą biblioteki Authlib.

## Wymagania wstępne

1. **Google:** Utwórz OAuth 2.0 Client w [Google Cloud Console](https://console.cloud.google.com) → APIs & Services → Credentials. Authorized redirect URI: `http://localhost:8000/auth/google/callback`
2. **GitHub:** Utwórz OAuth App w GitHub → Settings → Developer settings → OAuth Apps. Authorization callback URL: `http://localhost:8000/auth/github/callback`

## Uruchomienie

```bash
cp .env.example .env
# Uzupełnij .env danymi z Google Cloud Console i GitHub OAuth Apps

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Otwórz http://localhost:8000 – zobaczysz przyciski logowania.

## Endpointy

| Endpoint | Opis |
|----------|------|
| `GET /` | Strona główna z przyciskami logowania |
| `GET /auth/google/login` | Inicjuje OAuth2 flow z Google |
| `GET /auth/google/callback` | Callback od Google (redirect URI) |
| `GET /auth/github/login` | Inicjuje OAuth2 flow z GitHub |
| `GET /auth/github/callback` | Callback od GitHub (redirect URI) |
| `GET /auth/me` | Dane zalogowanego użytkownika (JSON) |
| `POST /auth/logout` | Wylogowanie (usunięcie cookie) |
| `GET /dashboard` | Strona po zalogowaniu |
