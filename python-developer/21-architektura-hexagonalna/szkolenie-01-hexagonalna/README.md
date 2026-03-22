# Architektura hexagonalna – system zamówień (Szkolenie 1)

Kompletny przykład architektury hexagonalnej (Ports & Adapters) z systemem zamówień.

## Struktura

- `domain/` — encje i wyjątki (zero zależności zewnętrznych)
- `ports/` — interfejsy (ABC/Protocol)
- `application/` — use cases (serwisy aplikacyjne)
- `adapters/` — implementacje portów (SQLAlchemy, in-memory, fake)
- `entrypoints/` — adaptery wejściowe (FastAPI, Django)
- `infrastructure/` — DI, konfiguracja
- `tests/` — testy z in-memory adapterami

## Uruchomienie testów

```bash
pip install pytest
pytest tests/ -v
```
