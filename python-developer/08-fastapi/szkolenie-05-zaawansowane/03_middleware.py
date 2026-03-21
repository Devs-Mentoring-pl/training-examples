import logging
import time

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI(title="Middleware Examples")

logger = logging.getLogger("api")


# --- TimingMiddleware ---


class TimingMiddleware(BaseHTTPMiddleware):
    """Mierzy czas przetwarzania żądania i dodaje nagłówek X-Process-Time."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()

        # Przekaż żądanie dalej (do endpointu lub kolejnego middleware)
        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"

        return response


# --- LoggingMiddleware ---


class LoggingMiddleware(BaseHTTPMiddleware):
    """Loguje każde żądanie przychodzące do API."""

    async def dispatch(self, request: Request, call_next) -> Response:
        logger.info(f"{request.method} {request.url.path}")

        response = await call_next(request)

        logger.info(f"Status: {response.status_code} | {request.method} {request.url.path}")

        return response


# --- Middleware jako funkcja ---


@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    """Dodaje niestandardowy nagłówek do każdej odpowiedzi."""
    response = await call_next(request)
    response.headers["X-Powered-By"] = "FastAPI + Devs-Mentoring"
    return response


# Kolejność: LoggingMiddleware wykonuje się PIERWSZY, TimingMiddleware DRUGI
app.add_middleware(TimingMiddleware)
app.add_middleware(LoggingMiddleware)


# --- Przykładowe endpointy ---


@app.get("/")
async def root():
    return {"message": "Witaj w API!"}


@app.get("/slow")
async def slow_endpoint():
    """Endpoint z opóźnieniem – do testowania TimingMiddleware."""
    import asyncio
    await asyncio.sleep(1)
    return {"message": "Wolna odpowiedź"}
