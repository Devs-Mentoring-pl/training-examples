import json


def lambda_handler(event, context):
    """Handler główny – przetwarza żądanie i zwraca odpowiedź."""

    # Pobierz dane z event
    body = event.get("body")
    if body and isinstance(body, str):
        body = json.loads(body)
    elif not body:
        body = event  # bezpośrednie wywołanie (np. z konsoli AWS)

    name = body.get("name", "Świat")
    age = body.get("age")

    # Zbuduj odpowiedź
    message = f"Cześć, {name}!"
    if age:
        message += f" Masz {age} lat."

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": message
        }, ensure_ascii=False)
    }
