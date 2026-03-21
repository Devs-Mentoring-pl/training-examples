# Lekki obraz Pythona 3.12
FROM python:3.12-slim

# Katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj i zainstaluj zależności (osobna warstwa – cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj kod aplikacji
COPY src/ .

# Informacja o porcie
EXPOSE 5000

# Uruchom aplikację
CMD ["python", "app.py"]
