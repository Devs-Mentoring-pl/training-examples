"""
Szkolenie 2 – Lambda handler z SQS.

SQS oddziela producenta od konsumenta – buforuje żądania
i przetwarza je asynchronicznie.
"""

import boto3
import json

sqs = boto3.client("sqs", region_name="eu-central-1")
QUEUE_URL = "https://sqs.eu-central-1.amazonaws.com/123456/my-queue"


def send_to_queue(message: dict):
    """Wyślij wiadomość do kolejki SQS."""
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message)
    )


def lambda_handler(event, context):
    """Handler przetwarzający wiadomości z SQS."""
    for record in event["Records"]:
        body = json.loads(record["body"])
        # Przetwórz wiadomość...
        print(f"Przetwarzam zamówienie: {body}")
