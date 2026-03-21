# Docker - Optymalizacja obrazów

Przykłady różnych podejść do budowania zoptymalizowanych obrazów Docker dla aplikacji Python.

## Porównanie rozmiarów obrazów

| Obraz bazowy | Rozmiar |
|---|---|
| `python:3.12` | ~1020 MB |
| `python:3.12-slim` | ~145 MB |
| `python:3.12-alpine` | ~55 MB |
| Multi-stage z `python:3.12-slim` | ~155 MB |
| Multi-stage z Distroless | ~52 MB |

## Pliki Dockerfile

### 01_basic.Dockerfile
Podstawowy Dockerfile z montowaniem cache pip (`--mount=type=cache`). Wymaga BuildKit.

```bash
docker build -f 01_basic.Dockerfile -t app:basic .
```

### 02_uv.Dockerfile
Wykorzystuje `uv` -- ultraszybki menedżer pakietów napisany w Rust (10-100x szybszy niż pip).

```bash
docker build -f 02_uv.Dockerfile -t app:uv .
```

### 03_multistage.Dockerfile
Multi-stage build z separacją etapu budowania (builder) i uruchamiania (runner). Używa virtualenv i non-root user.

```bash
docker build -f 03_multistage.Dockerfile -t app:multistage .
```

### 04_distroless.Dockerfile
Multi-stage build z obrazem Google Distroless -- absolutne minimum (brak shell, brak menedżera pakietów).

```bash
docker build -f 04_distroless.Dockerfile -t app:distroless .
```
