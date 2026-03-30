import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.auth.jwt_utils import create_access_token, decode_access_token
from app.auth.oauth import oauth

router = APIRouter(prefix="/auth", tags=["auth"])

# Prosty in-memory store użytkowników (na potrzeby przykładu, bez bazy danych)
users_db: dict[str, dict] = {}


@router.get("/google/login")
async def google_login(request: Request):
    """Inicjuje OAuth2 flow z Google – przekierowuje do ekranu logowania."""
    redirect_uri = str(request.url_for("google_callback"))
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request):
    """Obsługuje callback od Google – wymienia code na token."""
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd autoryzacji: {e}")

    # id_token zawiera dane użytkownika (OIDC)
    user_info = token.get("userinfo")
    if not user_info:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://openidconnect.googleapis.com/v1/userinfo",
                headers={"Authorization": f"Bearer {token['access_token']}"},
            )
            user_info = response.json()

    email = user_info["email"]
    users_db[email] = {
        "email": email,
        "name": user_info.get("name", ""),
        "provider": "google",
    }

    jwt_token = create_access_token({"sub": email, "name": users_db[email]["name"]})

    response = RedirectResponse(url="/dashboard")
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,  # True na produkcji (wymaga HTTPS)
        samesite="lax",
    )
    return response


@router.get("/github/login")
async def github_login(request: Request):
    """Inicjuje OAuth2 flow z GitHub."""
    redirect_uri = str(request.url_for("github_callback"))
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback", name="github_callback")
async def github_callback(request: Request):
    """Obsługuje callback od GitHub – wymienia code na token."""
    try:
        token = await oauth.github.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Błąd autoryzacji: {e}")

    # GitHub wymaga osobnych zapytań o dane użytkownika i email
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {token['access_token']}",
                "Accept": "application/vnd.github+json",
            },
        )
        user_data = user_response.json()

        # GitHub może nie zwracać emaila jeśli jest prywatny
        emails_response = await client.get(
            "https://api.github.com/user/emails",
            headers={
                "Authorization": f"Bearer {token['access_token']}",
                "Accept": "application/vnd.github+json",
            },
        )
        emails = emails_response.json()

    # Wybierz główny, zweryfikowany email
    primary_email = next(
        (e["email"] for e in emails if e["primary"] and e["verified"]),
        None,
    )
    if not primary_email:
        raise HTTPException(
            status_code=400,
            detail="Nie udało się pobrać emaila z GitHub. Upewnij się że email jest zweryfikowany.",
        )

    name = user_data.get("name") or user_data.get("login", "")
    users_db[primary_email] = {
        "email": primary_email,
        "name": name,
        "provider": "github",
        "avatar_url": user_data.get("avatar_url", ""),
    }

    jwt_token = create_access_token({"sub": primary_email, "name": name})

    response = RedirectResponse(url="/dashboard")
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )
    return response


@router.get("/me")
async def get_me(request: Request):
    """Zwraca dane zalogowanego użytkownika z JWT cookie."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Brak tokenu – zaloguj się")

    try:
        payload = decode_access_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    email = payload["sub"]
    user = users_db.get(email)
    if not user:
        return {"email": email, "name": payload.get("name", "")}

    return user


@router.post("/logout")
async def logout():
    """Usuwa cookie z tokenem."""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token", path="/")
    return response
