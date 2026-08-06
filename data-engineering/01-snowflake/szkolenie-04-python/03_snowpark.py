"""Snowpark – DataFrame API wykonywane po stronie Snowflake.

Kod wygląda jak pandas, ale dane nie są ściągane na lokalną maszynę:
Snowpark tłumaczy operacje na SQL i wykonuje je w hurtowni.

Uruchomienie:
    python 03_snowpark.py
"""

from __future__ import annotations

from snowflake.snowpark import Session
from snowflake.snowpark.functions import avg, col, count, datediff, lit
from snowflake.snowpark.functions import sum as sum_
from snowflake.snowpark.functions import current_date, when

from connection import connection_params


def build_session() -> Session:
    """Tworzy sesję Snowparku na podstawie tej samej konfiguracji, co connector."""
    params = connection_params()
    # Snowpark nie przyjmuje parametrów sieciowych connectora
    for key in ("login_timeout", "network_timeout", "session_parameters"):
        params.pop(key, None)
    return Session.builder.configs(params).create()


def revenue_by_country(session: Session):
    """Przychód według krajów – odpowiednik zapytania SQL z 01_queries.py."""
    orders = session.table("SHOP_DB.RAW.ORDERS")
    customers = session.table("SHOP_DB.RAW.CUSTOMERS")

    return (
        orders.join(customers, orders["CUSTOMER_ID"] == customers["CUSTOMER_ID"])
        .filter(col("STATUS") != "CANCELLED")
        .group_by(customers["COUNTRY_CODE"])
        .agg(
            count(orders["ORDER_ID"]).alias("ORDERS_COUNT"),
            sum_(orders["TOTAL_AMOUNT"]).alias("REVENUE"),
            avg(orders["TOTAL_AMOUNT"]).alias("AVG_ORDER_VALUE"),
        )
        .sort(col("REVENUE").desc())
    )


def customer_segments(session: Session):
    """Segmentacja klientów według stażu – przykład with_column i when/otherwise."""
    customers = session.table("SHOP_DB.RAW.CUSTOMERS")

    return (
        customers.with_column(
            "DAYS_SINCE_SIGNUP", datediff("day", col("SIGNUP_DATE"), current_date())
        )
        .with_column(
            "SEGMENT",
            when(col("DAYS_SINCE_SIGNUP") < 90, lit("NOWY"))
            .when(col("DAYS_SINCE_SIGNUP") < 365, lit("AKTYWNY"))
            .otherwise(lit("WETERAN")),
        )
        .group_by(col("SEGMENT"))
        .agg(count(col("CUSTOMER_ID")).alias("CUSTOMERS"))
        .sort(col("CUSTOMERS").desc())
    )


if __name__ == "__main__":
    session = build_session()
    try:
        revenue = revenue_by_country(session)

        # DataFrame to na razie tylko opis operacji – nic się jeszcze nie wykonało
        print("Wygenerowany SQL:")
        for query in revenue.queries["queries"]:
            print(f"  {query}\n")

        print("Przychód według krajów:")
        revenue.show()

        print("Segmenty klientów:")
        customer_segments(session).show()

        # Zapis wyniku jako tabela – dane nie wracają do Pythona
        revenue.write.mode("overwrite").save_as_table("SHOP_DB.ANALYTICS.REVENUE_BY_COUNTRY")
        print("Zapisano SHOP_DB.ANALYTICS.REVENUE_BY_COUNTRY")
    finally:
        session.close()
