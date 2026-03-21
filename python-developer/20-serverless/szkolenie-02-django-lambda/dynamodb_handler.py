"""
Szkolenie 2 – Lambda handler z DynamoDB.

DynamoDB to naturalny partner Lambdy – nie wymaga
zarządzania pulą połączeń jak RDS.
"""

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("users")


def lambda_handler(event, context):
    # Zapis
    table.put_item(Item={
        "user_id": "123",
        "name": "Kacper",
        "email": "kacper@devs-mentoring.pl"
    })

    # Odczyt
    response = table.get_item(Key={"user_id": "123"})
    return response.get("Item")
