from functools import lru_cache

from fastapi import FastAPI, Depends
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.routers.auth import router as auth_router
from app.routers.documents import router as documents_router
from app.services.m2m_client import Auth0M2MClient, M2MSettings

app = FastAPI(title="Auth0 – FastAPI Integration")

# SessionMiddleware przechowuje state między /login-url a /callback
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

app.include_router(auth_router)
app.include_router(documents_router)


# --- M2M: przykład wywołania innego serwisu ---

@lru_cache
def get_m2m_client() -> Auth0M2MClient:
    return Auth0M2MClient(M2MSettings())


@app.get("/orders/{order_id}/inventory")
async def get_order_inventory(
    order_id: int,
    m2m_client: Auth0M2MClient = Depends(get_m2m_client),
):
    """
    Przykład Machine-to-Machine: pobierz dane z innego serwisu.
    Wymaga skonfigurowania AUTH0_M2M_* w .env.
    """
    data = await m2m_client.call_api(
        f"https://inventory-service.internal/items/{order_id}"
    )
    return {"order_id": order_id, "inventory": data}


@app.get("/health")
async def health():
    """Publiczny endpoint – nie wymaga tokena."""
    return {"status": "ok"}
