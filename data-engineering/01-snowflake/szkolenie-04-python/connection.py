"""Wspólna konfiguracja połączenia ze Snowflake.

Obsługuje trzy metody uwierzytelniania:
- hasło (tylko dla kont osobowych, wymaga MFA)
- klucz RSA (zalecane dla skryptów i CI/CD)
- przeglądarka (wygodne przy pracy interaktywnej z MFA)
"""

from __future__ import annotations

import os
from pathlib import Path

import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

load_dotenv()


def load_private_key(path: str, passphrase: str | None = None) -> bytes:
    """Wczytuje klucz prywatny RSA i zwraca go w formacie DER (wymaganym przez connector)."""
    with Path(path).expanduser().open("rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=passphrase.encode() if passphrase else None,
            backend=default_backend(),
        )

    return private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def connection_params() -> dict:
    """Buduje parametry połączenia na podstawie zmiennych środowiskowych."""
    params = {
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "LEARN_WH"),
        "database": os.getenv("SNOWFLAKE_DATABASE", "SHOP_DB"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA", "RAW"),
        "role": os.getenv("SNOWFLAKE_ROLE", "SYSADMIN"),
        # Limity ochronne – bez nich zapytanie może działać nawet 48 godzin
        "login_timeout": 30,
        "network_timeout": 60,
        "session_parameters": {
            "STATEMENT_TIMEOUT_IN_SECONDS": 300,
            "QUERY_TAG": os.getenv("SNOWFLAKE_QUERY_TAG", "training-examples"),
        },
    }

    key_path = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
    password = os.getenv("SNOWFLAKE_PASSWORD")

    if key_path:
        # Zalecane dla wszystkiego, co działa bez człowieka przy klawiaturze
        params["private_key"] = load_private_key(
            key_path, os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")
        )
    elif password:
        params["password"] = password
    else:
        # Otwiera okno logowania w przeglądarce – wspiera MFA i SSO
        params["authenticator"] = "externalbrowser"

    return params


def get_connection() -> snowflake.connector.SnowflakeConnection:
    """Zwraca nowe połączenie ze Snowflake."""
    return snowflake.connector.connect(**connection_params())


if __name__ == "__main__":
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT CURRENT_VERSION(), CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()"
            )
            version, user, role, warehouse = cur.fetchone()
            print(f"Snowflake {version}")
            print(f"Użytkownik: {user}, rola: {role}, warehouse: {warehouse}")
