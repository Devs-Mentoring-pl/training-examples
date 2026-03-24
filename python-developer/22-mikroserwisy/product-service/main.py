from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Product Service", version="1.0.0")

products_db: dict[int, dict] = {
    1: {"id": 1, "name": "Laptop", "price": 3499.99, "stock": 10},
    2: {"id": 2, "name": "Słuchawki", "price": 299.99, "stock": 50},
    3: {"id": 3, "name": "Mysz", "price": 89.99, "stock": 0},
}


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int


class StockUpdate(BaseModel):
    quantity: int  # ujemna wartość = zmniejsz stan, dodatnia = zwiększ


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "service": "product-service"}


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int) -> ProductResponse:
    """Pobiera produkt po ID."""
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Produkt {product_id} nie istnieje")
    return ProductResponse(**product)


@app.patch("/products/{product_id}/stock")
async def update_stock(product_id: int, update: StockUpdate) -> dict:
    """Aktualizuje stan magazynowy produktu."""
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Produkt {product_id} nie istnieje")

    new_stock = product["stock"] + update.quantity
    if new_stock < 0:
        raise HTTPException(
            status_code=409,
            detail=f"Niewystarczający stan magazynowy. Dostępne: {product['stock']}"
        )

    products_db[product_id]["stock"] = new_stock
    return {
        "product_id": product_id,
        "previous_stock": product["stock"],
        "new_stock": new_stock
    }
