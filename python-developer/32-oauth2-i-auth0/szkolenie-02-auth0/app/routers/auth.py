import secrets
import urllib.parse

import httpx
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse

from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login-url")
async def get_login_url(request: Request):
    """
    Zwraca URL do Auth0 Universal Login.
    Frontend przekierowuje tam użytkownika.
    """
    state = secrets.token_urlsafe(32)
    request.session["oauth_state"] = state

    params = {
        "response_type": "code",
        "client_id": settings.auth0_client_id,
        "redirect_uri": settings.auth0_callback_url,
        "scope": "openid profile email",
        "audience": settings.auth0_audience,
        "state": state,
    }

    url = f"https://{settings.auth0_domain}/authorize?{urllib.parse.urlencode(params)}"
    return {"url": url}


@router.get("/callback")
async def auth_callback(request: Request, code: str, state: str):
    """
    Obsługuje redirect z Auth0 po zalogowaniu.
    Wymienia authorization code na tokeny.
    """
    stored_state = request.session.pop("oauth_state", "")
    if not secrets.compare_digest(state, stored_state):
        raise HTTPException(status_code=400, detail="Nieprawidłowy state – możliwy atak CSRF")

    # Wymień code na tokeny (server-to-server)
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            f"https://{settings.auth0_domain}/oauth/token",
            json={
                "grant_type": "authorization_code",
                "client_id": settings.auth0_client_id,
                "client_secret": settings.auth0_client_secret,
                "code": code,
                "redirect_uri": settings.auth0_callback_url,
            },
            timeout=10.0,
        )

    if token_response.status_code != 200:
        raise HTTPException(status_code=502, detail="Błąd wymiany code na token")

    tokens = token_response.json()

    # Ustaw access_token jako HttpOnly cookie i przekieruj do frontendu
    response = RedirectResponse(url=settings.app_frontend_url)
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,       # True na produkcji (wymaga HTTPS)
        samesite="lax",
        max_age=tokens.get("expires_in", 3600),
        path="/",
    )
    return response


@router.get("/me")
async def get_current_user(request: Request):
    """
    Zwraca dane zalogowanego użytkownika.
    Pobiera profil z Auth0 /userinfo.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Brak tokenu – zaloguj się")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://{settings.auth0_domain}/userinfo",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Token nieprawidłowy lub wygasł")

    return response.json()


@router.get("/logout-url")
async def get_logout_url():
    """
    Zwraca URL do wylogowania z Auth0.
    Auth0 unieważnia sesję i przekierowuje z powrotem do frontendu.
    """
    params = {
        "client_id": settings.auth0_client_id,
        "returnTo": settings.app_frontend_url,
    }
    url = f"https://{settings.auth0_domain}/v2/logout?{urllib.parse.urlencode(params)}"
    return {"url": url}


@router.post("/logout")
async def logout(response: Response):
    """Usuwa cookie z tokenem po stronie backendu."""
    response.delete_cookie("access_token", path="/")
    return {"message": "Wylogowano"}
