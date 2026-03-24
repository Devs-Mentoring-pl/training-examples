import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="Order Service", version="1.0.0")

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8002")

orders_db: dict[int, dict] = {}
next_order_id = 1


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class OrderResponse(BaseModel):
    order_id: int
    user_name: str
    product_name: str
    quantity: int
    total_price: float
    status: str


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "service": "order-service"}


@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate) -> OrderResponse:
    """
    Tworzy zamówienie:
    1. Weryfikuje użytkownika (user-service)
    2. Weryfikuje produkt i dostępność (product-service)
    3. Aktualizuje stan magazynowy (product-service)
    4. Zapisuje zamówienie lokalnie
    """
    global next_order_id

    async with httpx.AsyncClient(timeout=5.0) as client:
        # Krok 1 – weryfikacja użytkownika
        user_resp = await client.get(f"{USER_SERVICE_URL}/users/{order.user_id}")
        if user_resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Użytkownik nie istnieje")
        if user_resp.status_code != 200:
            raise HTTPException(status_code=503, detail="User service niedostępny")

        user = user_resp.json()

        if not user["is_active"]:
            raise HTTPException(status_code=403, detail="Konto użytkownika jest nieaktywne")

        # Krok 2 – weryfikacja produktu
        product_resp = await client.get(
            f"{PRODUCT_SERVICE_URL}/products/{order.product_id}"
        )
        if product_resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Produkt nie istnieje")
        if product_resp.status_code != 200:
            raise HTTPException(status_code=503, detail="Product service niedostępny")

        product = product_resp.json()

        if product["stock"] < order.quantity:
            raise HTTPException(
                status_code=409,
                detail=f"Niewystarczający stan. Dostępne: {product['stock']}"
            )

        # Krok 3 – rezerwacja stanu magazynowego
        stock_resp = await client.patch(
            f"{PRODUCT_SERVICE_URL}/products/{order.product_id}/stock",
            json={"quantity": -order.quantity}  # ujemna wartość = zmniejsz
        )
        if stock_resp.status_code != 200:
            raise HTTPException(
                status_code=503,
                detail="Nie udało się zarezerwować produktu"
            )

    # Krok 4 – zapis zamówienia
    total_price = product["price"] * order.quantity
    new_order = {
        "order_id": next_order_id,
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_price": total_price,
        "status": "confirmed",
    }
    orders_db[next_order_id] = new_order
    next_order_id += 1

    return OrderResponse(
        order_id=new_order["order_id"],
        user_name=user["name"],
        product_name=product["name"],
        quantity=order.quantity,
        total_price=total_price,
        status="confirmed",
    )


@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int) -> OrderResponse:
    """Pobiera szczegóły zamówienia."""
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Zamówienie {order_id} nie istnieje")

    # Pobieramy aktualne dane z serwisów (mogły się zmienić)
    async with httpx.AsyncClient(timeout=5.0) as client:
        user_resp = await client.get(f"{USER_SERVICE_URL}/users/{order['user_id']}")
        product_resp = await client.get(
            f"{PRODUCT_SERVICE_URL}/products/{order['product_id']}"
        )

    user = user_resp.json() if user_resp.status_code == 200 else {"name": "Nieznany"}
    product = product_resp.json() if product_resp.status_code == 200 else {"name": "Nieznany"}

    return OrderResponse(
        order_id=order["order_id"],
        user_name=user["name"],
        product_name=product["name"],
        quantity=order["quantity"],
        total_price=order["total_price"],
        status=order["status"],
    )
