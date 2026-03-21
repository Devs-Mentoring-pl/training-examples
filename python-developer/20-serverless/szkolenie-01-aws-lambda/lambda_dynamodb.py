"""
Lambda z DynamoDB – inicjalizacja poza handlerem (cold start optimization).
Kod poza handlerem wykonuje się RAZ (przy cold starcie)
i jest reużywany w warm startach.
"""

import json
import boto3

# To wykonuje się RAZ – przy cold starcie
# Kolejne wywołania reużywają ten sam klient
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("users")


def lambda_handler(event, context):
    """Handler z obsługą keep-warm ping."""

    # Ignoruj pingi keep-warm
    if event.get("warm"):
        return {"statusCode": 200, "body": "warm"}

    # To wykonuje się PRZY KAŻDYM wywołaniu
    user_id = event.get("user_id")
    response = table.get_item(Key={"id": user_id})
    return {
        "statusCode": 200,
        "body": json.dumps(response.get("Item", {}))
    }
