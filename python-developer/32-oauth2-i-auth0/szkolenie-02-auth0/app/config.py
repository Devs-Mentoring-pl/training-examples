from pydantic_settings import BaseSettings, SettingsConfigDict


class Auth0Settings(BaseSettings):
    auth0_domain: str                # np. "moja-firma.eu.auth0.com"
    auth0_client_id: str             # z dashboardu Auth0
    auth0_client_secret: str         # z dashboardu Auth0
    auth0_audience: str              # np. "https://api.moja-firma.com"
    auth0_callback_url: str          # np. "http://localhost:8000/auth/callback"
    app_frontend_url: str = "http://localhost:3000"
    secret_key: str = "zmien-to-w-produkcji"

    model_config = SettingsConfigDict(env_file=".env")


settings = Auth0Settings()
