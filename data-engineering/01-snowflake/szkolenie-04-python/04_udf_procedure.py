"""UDF i procedury składowane w Pythonie – kod działający wewnątrz Snowflake.

UDF (User Defined Function) – funkcja wywoływana w SELECT, działa na wierszu.
Procedura – może wykonywać zapytania i modyfikować dane, dostaje sesję Snowparku.

Uruchomienie:
    python 04_udf_procedure.py
"""

from __future__ import annotations

from snowflake.snowpark import Session
from snowflake.snowpark.functions import call_udf, col, lit, udf
from snowflake.snowpark.types import FloatType, StringType

from connection import connection_params


def build_session() -> Session:
    params = connection_params()
    for key in ("login_timeout", "network_timeout", "session_parameters"):
        params.pop(key, None)
    return Session.builder.configs(params).create()


def register_udfs(session: Session) -> None:
    """Rejestruje UDF-y w Snowflake (trwałe, przechowywane na stage'u)."""
    session.sql("CREATE STAGE IF NOT EXISTS SHOP_DB.RAW.UDF_STAGE").collect()

    @udf(
        name="SHOP_DB.RAW.MASK_EMAIL",
        is_permanent=True,
        stage_location="@SHOP_DB.RAW.UDF_STAGE",
        replace=True,
        return_type=StringType(),
        input_types=[StringType()],
    )
    def mask_email(email: str) -> str:
        """Maskuje część lokalną adresu: jan.kowalski@x.pl -> j***@x.pl"""
        if not email or "@" not in email:
            return email
        local, domain = email.split("@", 1)
        return f"{local[0]}***@{domain}"

    @udf(
        name="SHOP_DB.RAW.CALCULATE_VAT",
        is_permanent=True,
        stage_location="@SHOP_DB.RAW.UDF_STAGE",
        replace=True,
        return_type=FloatType(),
        input_types=[FloatType(), FloatType()],
    )
    def calculate_vat(net_amount: float, rate: float) -> float:
        """Liczy kwotę brutto na podstawie kwoty netto i stawki VAT."""
        if net_amount is None:
            return None
        return round(net_amount * (1 + rate), 2)


def create_procedure(session: Session) -> None:
    """Tworzy procedurę przeliczającą podsumowanie klientów."""
    session.sql("""
        CREATE OR REPLACE PROCEDURE SHOP_DB.RAW.REFRESH_CUSTOMER_SUMMARY()
        RETURNS VARCHAR
        LANGUAGE PYTHON
        RUNTIME_VERSION = '3.11'
        PACKAGES = ('snowflake-snowpark-python')
        HANDLER = 'run'
        AS
        $$
def run(session):
    # Przelicza podsumowanie klientow i zwraca liczbe przetworzonych wierszy
    orders = session.table("SHOP_DB.RAW.ORDERS")
    customers = session.table("SHOP_DB.RAW.CUSTOMERS")

    summary = (
        customers
        .join(orders, customers["CUSTOMER_ID"] == orders["CUSTOMER_ID"], how="left")
        .group_by(customers["CUSTOMER_ID"], customers["EMAIL"])
        .agg({"TOTAL_AMOUNT": "sum"})
    )

    summary.write.mode("overwrite").save_as_table("SHOP_DB.ANALYTICS.CUSTOMER_SUMMARY_PROC")
    return f"Przetworzono {summary.count()} klientow"
        $$
    """).collect()


if __name__ == "__main__":
    session = build_session()
    try:
        print("Rejestruję UDF-y...")
        register_udfs(session)

        # Użycie UDF w Snowparku
        print("\nZamaskowane adresy (Snowpark):")
        session.table("SHOP_DB.RAW.CUSTOMERS").select(
            col("CUSTOMER_ID"),
            call_udf("SHOP_DB.RAW.MASK_EMAIL", col("EMAIL")).alias("EMAIL_MASKED"),
            call_udf("SHOP_DB.RAW.CALCULATE_VAT", lit(100.0), lit(0.23)).alias("VAT_DEMO"),
        ).limit(5).show()

        # Użycie UDF w zwykłym SQL
        print("Zamaskowane adresy (SQL):")
        session.sql("""
            SELECT customer_id, SHOP_DB.RAW.MASK_EMAIL(email) AS email_masked
            FROM SHOP_DB.RAW.CUSTOMERS
            LIMIT 5
        """).show()

        print("Kwoty brutto:")
        session.sql("""
            SELECT
                order_id,
                total_amount,
                SHOP_DB.RAW.CALCULATE_VAT(total_amount, 0.23) AS gross_amount
            FROM SHOP_DB.RAW.ORDERS
            LIMIT 5
        """).show()

        print("Tworzę i wywołuję procedurę...")
        create_procedure(session)
        result = session.sql("CALL SHOP_DB.RAW.REFRESH_CUSTOMER_SUMMARY()").collect()
        print(f"  {result[0][0]}")
    finally:
        session.close()
