# Flask – REST API (Szkolenie 6)

REST API do zarządzania treningami z SQLAlchemy i Marshmallow: pełny CRUD + skrypt testujący.

## Uruchomienie

```bash
pip install -r requirements.txt
python run.py
```

API: http://localhost:5000

## Testowanie

W osobnym terminalu (przy działającym serwerze):

```bash
python -m app.simulation
```

Lub z curl:

```bash
curl -X POST http://localhost:5000/training \
  -H "Content-Type: application/json" \
  -d '{"name": "Bieg poranny", "duration": 45}'

curl http://localhost:5000/trainings
```
