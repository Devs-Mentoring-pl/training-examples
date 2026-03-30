import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

from app.auth.jwt_utils import decode_access_token
from app.routers.auth import router as auth_router

load_dotenv()

app = FastAPI(title="Social Auth – FastAPI + Authlib")

# SessionMiddleware przechowuje state OAuth2 między redirect a callback
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ.get("SECRET_KEY", "zmien-to"),
)

app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Strona główna z przyciskami logowania."""
    token = request.cookies.get("access_token")
    if token:
        try:
            payload = decode_access_token(token)
            name = payload.get("name", payload["sub"])
            return f"""
            <h1>Witaj, {name}!</h1>
            <p><a href="/auth/me">Moje dane (JSON)</a></p>
            <form action="/auth/logout" method="post">
                <button type="submit">Wyloguj</button>
            </form>
            """
        except ValueError:
            pass

    return """
    <h1>Social Auth – FastAPI + Authlib</h1>
    <p><a href="/auth/google/login">Zaloguj przez Google</a></p>
    <p><a href="/auth/github/login">Zaloguj przez GitHub</a></p>
    """


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Strona po zalogowaniu."""
    token = request.cookies.get("access_token")
    if not token:
        return HTMLResponse("<p>Nie jesteś zalogowany. <a href='/'>Wróć</a></p>", status_code=401)

    try:
        payload = decode_access_token(token)
    except ValueError:
        return HTMLResponse("<p>Token wygasł. <a href='/'>Zaloguj ponownie</a></p>", status_code=401)

    name = payload.get("name", payload["sub"])
    return f"""
    <h1>Dashboard</h1>
    <p>Zalogowany jako: <strong>{name}</strong> ({payload['sub']})</p>
    <p><a href="/auth/me">Moje dane (JSON)</a></p>
    <form action="/auth/logout" method="post">
        <button type="submit">Wyloguj</button>
    </form>
    """
