# --- Etap 1: budowanie ---
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Etap 2: obraz końcowy ---
FROM python:3.12-slim

WORKDIR /app

# Kopiujemy tylko zainstalowane pakiety (bez kompilatora, pip cache itp.)
COPY --from=builder /install /usr/local

COPY . .

# Użytkownik nie-root (bezpieczeństwo)
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
