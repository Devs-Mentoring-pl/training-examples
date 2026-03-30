import time
from dataclasses import dataclass

import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict


class M2MSettings(BaseSettings):
    auth0_domain: str
    auth0_m2m_client_id: str        # Client ID aplikacji M2M
    auth0_m2m_client_secret: str    # Client Secret aplikacji M2M
    auth0_m2m_audience: str         # Audience docelowego API

    model_config = SettingsConfigDict(env_file=".env")


@dataclass
class TokenCache:
    """Prosty cache tokenu M2M – żeby nie odpytywać Auth0 przy każdym requescie."""
    access_token: str = ""
    expires_at: float = 0.0

    def is_valid(self) -> bool:
        """Sprawdź czy token jest ważny (z 60s buforem)."""
        return bool(self.access_token) and time.time() < self.expires_at - 60


class Auth0M2MClient:
    """
    Klient do pobierania i cachowania tokenów M2M z Auth0.
    Używa Client Credentials Flow.
    """

    def __init__(self, m2m_settings: M2MSettings):
        self._settings = m2m_settings
        self._cache = TokenCache()

    async def get_access_token(self) -> str:
        """Zwróć ważny access token, pobierając nowy jeśli wygasł."""
        if self._cache.is_valid():
            return self._cache.access_token

        return await self._fetch_new_token()

    async def _fetch_new_token(self) -> str:
        """Pobierz nowy token z Auth0 (Client Credentials Flow)."""
        payload = {
            "client_id": self._settings.auth0_m2m_client_id,
            "client_secret": self._settings.auth0_m2m_client_secret,
            "audience": self._settings.auth0_m2m_audience,
            "grant_type": "client_credentials",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://{self._settings.auth0_domain}/oauth/token",
                json=payload,
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()

        self._cache.access_token = data["access_token"]
        self._cache.expires_at = time.time() + data["expires_in"]

        return self._cache.access_token

    async def call_api(self, url: str, method: str = "GET", **kwargs) -> dict:
        """Wywołaj chronione API z automatycznym dodaniem tokenu Bearer."""
        token = await self.get_access_token()
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method, url, headers=headers, timeout=30.0, **kwargs
            )
            response.raise_for_status()
            return response.json()
