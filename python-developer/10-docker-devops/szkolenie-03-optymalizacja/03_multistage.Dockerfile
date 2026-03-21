# ---- Etap 1: Builder ----
FROM python:3.12-slim AS builder

WORKDIR /app

RUN python -m venv /opt/venv
# Aktywacja venv – wszystkie pakiety trafiają do /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Etap 2: Runner ----
FROM python:3.12-slim AS runner

WORKDIR /app

# Kopiuj TYLKO środowisko wirtualne z pierwszego etapu
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

# Uruchom jako non-root (bezpieczeństwo!)
RUN useradd --create-home appuser
USER appuser

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
