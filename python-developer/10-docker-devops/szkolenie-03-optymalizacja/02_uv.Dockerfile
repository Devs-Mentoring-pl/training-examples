# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

# Zainstaluj uv
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /usr/local/bin/uv

# Kopiuj pliki zależności
COPY pyproject.toml uv.lock ./

# Instalacja zależności – błyskawiczna!
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY . .

CMD ["uv", "run", "python", "app.py"]
