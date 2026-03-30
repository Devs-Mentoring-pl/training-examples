from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError, PyJWKClient
from pydantic import BaseModel, Field

from app.config import settings

CLAIMS_NAMESPACE = "https://moja-firma.com"

security = HTTPBearer()

# PyJWKClient cachuje klucze JWKS automatycznie
jwks_client = PyJWKClient(
    f"https://{settings.auth0_domain}/.well-known/jwks.json",
    cache_keys=True,
    lifespan=300,  # odświeżaj klucze co 5 minut
)


class TokenPayload(BaseModel):
    """Reprezentacja payload JWT z Auth0."""
    sub: str                         # Identyfikator użytkownika (np. "google-oauth2|123")
    email: str | None = None
    email_verified: bool | None = None
    permissions: list[str] = []      # Z RBAC (wymaga włączenia w dashboardzie Auth0)
    roles: list[str] = Field(        # Z custom Action (wymaga dodania Action w Auth0)
        default=[],
        alias=f"{CLAIMS_NAMESPACE}/roles",
    )
    scope: str = ""                  # Scopes jako string rozdzielony spacją
    org_id: str | None = None        # Z Auth0 Organizations (jeśli skonfigurowane)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> TokenPayload:
    """
    FastAPI dependency – weryfikuje Bearer token i zwraca payload.
    Wrzuć do Depends() na dowolnym endpoincie.
    """
    token = credentials.credentials

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=settings.auth0_audience,
            issuer=f"https://{settings.auth0_domain}/",
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Nieprawidłowy token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenPayload(**payload)


# Typ dla type hints w routerach
CurrentUser = Annotated[TokenPayload, Depends(get_current_user)]
