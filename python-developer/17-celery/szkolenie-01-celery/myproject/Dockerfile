FROM python:3.12-slim

WORKDIR /app

# Kopiujemy zależności i instalujemy je
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy kod aplikacji
COPY . .

# Domyślna komenda – uruchomienie Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
