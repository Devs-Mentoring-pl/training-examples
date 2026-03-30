# Szkolenie 1: Własny OAuth2 provider (django-oauth-toolkit)

Przykładowy projekt Django, który działa jako OAuth2 Authorization Server – wydaje tokeny i chroni endpointy API.

## Uruchomienie

```bash
cd provider_project
pip install -r ../requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Testowanie

1. Zaloguj się do panelu admina: http://localhost:8000/admin/
2. Przejdź do http://localhost:8000/o/applications/ i utwórz nową aplikację OAuth2:
   - **Client type:** Confidential
   - **Authorization grant type:** Authorization code
   - **Redirect uris:** `http://localhost:8000/o/callback/`
3. Skopiuj `Client ID` i `Client Secret`
4. Pobierz token:

```bash
# Authorization Code Flow (otwórz w przeglądarce):
http://localhost:8000/o/authorize/?response_type=code&client_id=TWOJ_CLIENT_ID&redirect_uri=http://localhost:8000/o/callback/&scope=read

# Wymień code na token:
curl -X POST http://localhost:8000/o/token/ \
  -d "grant_type=authorization_code" \
  -d "code=OTRZYMANY_CODE" \
  -d "redirect_uri=http://localhost:8000/o/callback/" \
  -d "client_id=TWOJ_CLIENT_ID" \
  -d "client_secret=TWOJ_CLIENT_SECRET"
```

5. Wywołaj chroniony endpoint:

```bash
curl -H "Authorization: Bearer TWOJ_ACCESS_TOKEN" http://localhost:8000/api/protected/
```

## Endpointy

| Endpoint | Opis |
|----------|------|
| `GET /api/public/` | Publiczny – bez tokena |
| `GET /api/protected/` | Chroniony – wymaga OAuth2 access token ze scope `read` |
| `/o/authorize/` | Ekran zgody OAuth2 |
| `/o/token/` | Wymiana code/credentials na token |
| `/o/revoke_token/` | Unieważnianie tokenów |
| `/o/applications/` | Zarządzanie aplikacjami OAuth2 |
