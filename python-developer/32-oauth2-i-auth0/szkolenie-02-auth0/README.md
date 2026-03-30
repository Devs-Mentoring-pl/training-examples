# Szkolenie 2: Auth0 – zarządzane uwierzytelnianie (FastAPI)

Kompletna integracja Auth0 z FastAPI: flow logowania, weryfikacja JWT (PyJWT + JWKS), RBAC permissions i klient Machine-to-Machine.

## Wymagania wstępne

1. Utwórz darmowe konto na [auth0.com](https://auth0.com)
2. Utwórz **Application** typu "Regular Web Application":
   - Allowed Callback URLs: `http://localhost:8000/auth/callback`
   - Allowed Logout URLs: `http://localhost:3000`
3. Utwórz **API** z identyfikatorem (audience), np. `https://api.moja-aplikacja.com`
4. Włącz RBAC: APIs → Twoje API → Settings → Enable RBAC + Add Permissions in the Access Token
5. (Opcjonalnie) Utwórz **Application** typu "Machine to Machine" dla M2M endpointu

## Uruchomienie

```bash
cp .env.example .env
# Uzupełnij .env danymi z dashboardu Auth0

pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpointy

### Flow logowania (dla frontendu)

| Endpoint | Opis |
|----------|------|
| `GET /auth/login-url` | Zwraca URL do Auth0 Universal Login |
| `GET /auth/callback` | Callback z Auth0 – wymienia code na token, ustawia cookie |
| `GET /auth/me` | Dane zalogowanego użytkownika (z Auth0 `/userinfo`) |
| `GET /auth/logout-url` | URL do wylogowania z Auth0 |
| `POST /auth/logout` | Usuwa cookie z tokenem |

### API chronione JWT (Bearer token)

| Endpoint | Wymagane uprawnienie |
|----------|---------------------|
| `GET /documents/` | `read:documents` |
| `POST /documents/` | `write:documents` |
| `DELETE /documents/{id}` | `delete:documents` |
| `GET /health` | brak (publiczny) |

### Machine-to-Machine

| Endpoint | Opis |
|----------|------|
| `GET /orders/{id}/inventory` | Wywołuje inny serwis z tokenem M2M |

## RBAC

W dashboardzie Auth0 utwórz permissions (`read:documents`, `write:documents`, `delete:documents`), przypisz je do ról i ról do użytkowników. Bez tego pole `permissions` w JWT będzie puste.

## Testowanie Bearer token

```bash
# Pobierz token z Auth0 (np. przez flow logowania lub Management API)
TOKEN="eyJhbGc..."

curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/documents/
```
