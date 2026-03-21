# Szkolenie 4: FastAPI - Autentykacja i bezpieczenstwo

Kompletna aplikacja demonstrująca autentykację i autoryzację w FastAPI z JWT, hashowaniem haseł i RBAC.

## Endpointy

| Metoda | Endpoint              | Opis                              | Autoryzacja        |
|--------|-----------------------|-----------------------------------|---------------------|
| POST   | `/token`              | Logowanie (zwraca access + refresh token) | Publiczny          |
| POST   | `/token/refresh`      | Odświeżanie access tokena         | Wymaga refresh token |
| GET    | `/me`                 | Dane zalogowanego użytkownika     | Wymaga tokena       |
| GET    | `/my-items`           | Przedmioty użytkownika            | Wymaga tokena       |
| GET    | `/admin/dashboard`    | Panel admina                      | Rola: admin         |
| DELETE | `/admin/users/{username}` | Usunięcie użytkownika         | Rola: admin         |
| GET    | `/reports`            | Raporty                           | Rola: admin lub moderator |

## Użytkownicy testowi

| Username | Hasło     | Rola  |
|----------|-----------|-------|
| kacper   | admin123  | admin |
| jan      | user123   | user  |

## Jak uruchomić

```bash
pip install -r requirements.txt
fastapi dev main.py
```

Swagger UI: http://localhost:8000/docs

## Przykłady curl

```bash
# Logowanie
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=kacper&password=admin123"

# Pobranie danych użytkownika (wstaw token z odpowiedzi logowania)
curl http://localhost:8000/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Pobranie przedmiotów użytkownika
curl http://localhost:8000/my-items \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Panel admina (wymaga roli admin)
curl http://localhost:8000/admin/dashboard \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Odświeżenie tokena
curl -X POST "http://localhost:8000/token/refresh?refresh_token=<REFRESH_TOKEN>"
```
