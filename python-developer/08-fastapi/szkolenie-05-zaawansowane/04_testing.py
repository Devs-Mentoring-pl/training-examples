"""
Przykłady testowania FastAPI.

Uruchom: pytest 04_testing.py -v
"""

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel

# --- Aplikacja do testowania ---

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


# Symulowana baza danych
items_db: list[dict] = []


def get_current_user():
    """Dependency - zwraca aktualnego użytkownika."""
    return {"username": "real_user", "role": "user"}


@app.get("/")
async def root():
    return {"message": "Witaj w API!"}


@app.post("/items", status_code=201)
async def create_item(item: Item):
    item_dict = item.model_dump()
    items_db.append(item_dict)
    return item_dict


@app.get("/protected")
async def protected_endpoint(user: dict = Depends(get_current_user)):
    return {"user": user["username"], "role": user["role"]}


# --- Testy z TestClient ---

client = TestClient(app)


def test_read_root():
    """Test endpointu głównego."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Witaj w API!"}


def test_create_item():
    """Test tworzenia elementu."""
    response = client.post(
        "/items",
        json={"name": "Laptop", "price": 3999.99},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Laptop"


def test_create_item_invalid():
    """Test walidacji – brak wymaganego pola."""
    response = client.post("/items", json={"name": "Laptop"})
    assert response.status_code == 422  # Validation Error


# --- Testy asynchroniczne ---


@pytest.mark.asyncio
async def test_read_root_async():
    """Test asynchroniczny z httpx."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Witaj w API!"}


# --- Override dependencies ---


def override_get_current_user():
    """Zawsze zwraca testowego użytkownika."""
    return {"username": "test_user", "role": "admin"}


app.dependency_overrides[get_current_user] = override_get_current_user

client_with_overrides = TestClient(app)


def test_protected_endpoint():
    """Test chronionego endpointu – dependency podmieniona."""
    response = client_with_overrides.get("/protected")
    assert response.status_code == 200
    assert response.json()["user"] == "test_user"
    assert response.json()["role"] == "admin"


# --- Testowanie WebSocketów ---
# (wymaga endpointu /ws z 02_websocket_chat.py)

# def test_websocket_echo():
#     """Test endpointu WebSocket."""
#     with client.websocket_connect("/ws") as websocket:
#         websocket.send_text("Cześć!")
#         data = websocket.receive_text()
#         assert data == "Echo: Cześć!"
