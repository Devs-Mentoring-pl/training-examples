# Obraz bazowy – oficjalny Python 3.12
FROM python:3.12-slim

# Zmienna środowiskowa – Python nie buforuje stdout/stderr
ENV PYTHONUNBUFFERED=1

# Katalog roboczy wewnątrz kontenera
WORKDIR /app

# Kopiujemy requirements najpierw – cache warstw Dockera
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę kodu aplikacji
COPY . .

# Port, na którym nasłuchuje Django
EXPOSE 8000

# Komenda uruchamiająca serwer developerski
CMD ["python", "myapp/manage.py", "runserver", "0.0.0.0:8000"]
