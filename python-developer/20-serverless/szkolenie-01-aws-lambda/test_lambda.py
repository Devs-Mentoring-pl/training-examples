# test_lambda.py

from lambda_function import lambda_handler


def test_basic_invocation():
    """Test podstawowego wywołania bez parametrów."""
    event = {}
    result = lambda_handler(event, None)
    assert result["statusCode"] == 200
    assert "Świat" in result["body"]


def test_with_name():
    """Test wywołania z imieniem."""
    event = {"name": "Kacper", "age": 30}
    result = lambda_handler(event, None)
    assert "Kacper" in result["body"]
    assert "30" in result["body"]


def test_api_gateway_format():
    """Test formatu API Gateway (body jako string JSON)."""
    import json
    event = {
        "body": json.dumps({"name": "Anna"})
    }
    result = lambda_handler(event, None)
    assert "Anna" in result["body"]


if __name__ == "__main__":
    test_basic_invocation()
    test_with_name()
    test_api_gateway_format()
    print("Wszystkie testy przeszły!")
