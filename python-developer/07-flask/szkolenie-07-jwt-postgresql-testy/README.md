# Flask – JWT, PostgreSQL, testy integracyjne (Szkolenie 7)

REST API z autoryzacją JWT (access + refresh token), hashowaniem haseł i testami integracyjnymi pytest.

## Uruchomienie

```bash
pip install -r requirements.txt
python app.py
```

API: http://localhost:5000

## Testowanie

```bash
pytest test_app.py -v
```

## Endpointy

| Metoda | Endpoint   | Opis                    | Autoryzacja |
|--------|-----------|-------------------------|-------------|
| POST   | /register | Rejestracja użytkownika | Nie         |
| POST   | /login    | Logowanie (zwraca JWT)  | Nie         |
| POST   | /refresh  | Odświeżanie tokenu      | Nie         |
| GET    | /profile  | Profil użytkownika      | Bearer JWT  |
| GET    | /users    | Lista użytkowników      | Bearer JWT  |

## Przykład użycia z curl

```bash
# Rejestracja
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "jan", "password": "haslo123"}'

# Logowanie
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "jan", "password": "haslo123"}'

# Profil (wstaw token z odpowiedzi login)
curl http://localhost:5000/profile \
  -H "Authorization: Bearer <TOKEN>"
```

## PostgreSQL (opcjonalnie)

Domyślnie używa SQLite. Aby przełączyć na PostgreSQL:

```bash
export DATABASE_URL="postgresql://flask_user:flask_password@localhost:5432/flask_app"
export SECRET_KEY="twoj-sekretny-klucz"
python app.py
```
