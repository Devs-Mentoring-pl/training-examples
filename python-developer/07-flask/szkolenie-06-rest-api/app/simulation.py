"""
Skrypt symulujący klienta REST API.
Uruchom serwer (python run.py), a następnie ten skrypt w osobnym terminalu.
"""
import requests

BASE_URL = 'http://localhost:5000'

# --- 1. Dodanie treningów (POST) ---
print("=== Dodawanie treningów ===")

training_1 = {
    "name": "Bieg poranny",
    "duration": 45,
    "note": "Tempo umiarkowane, 5km"
}

training_2 = {
    "name": "Siłownia",
    "duration": 90,
    "date": "15/03/26",
    "note": "Dzień nóg"
}

response = requests.post(f'{BASE_URL}/training', json=training_1)
print(f"POST /training → {response.status_code}: {response.json()}")

response = requests.post(f'{BASE_URL}/training', json=training_2)
print(f"POST /training → {response.status_code}: {response.json()}")

# --- 2. Pobranie wszystkich treningów (GET) ---
print("\n=== Wszystkie treningi ===")

response = requests.get(f'{BASE_URL}/trainings')
print(f"GET /trainings → {response.status_code}: {response.json()}")

# --- 3. Pobranie treningu po ID (GET) ---
print("\n=== Trening o ID 1 ===")

response = requests.get(f'{BASE_URL}/training/1')
print(f"GET /training/1 → {response.status_code}: {response.json()}")

# --- 4. Aktualizacja treningu (PUT) ---
print("\n=== Aktualizacja treningu ID 2 ===")

updated_training = {
    "name": "Siłownia – pełny trening",
    "duration": 120,
    "note": "Dzień nóg + cardio"
}

response = requests.put(f'{BASE_URL}/training/2', json=updated_training)
print(f"PUT /training/2 → {response.status_code}: {response.json()}")

# --- 5. Usunięcie treningu (DELETE) ---
print("\n=== Usunięcie treningu ID 1 ===")

response = requests.delete(f'{BASE_URL}/training/1')
print(f"DELETE /training/1 → {response.status_code}")

# --- 6. Próba pobrania usuniętego treningu ---
print("\n=== Próba pobrania usuniętego treningu ===")

response = requests.get(f'{BASE_URL}/training/1')
print(f"GET /training/1 → {response.status_code}: {response.json()}")
