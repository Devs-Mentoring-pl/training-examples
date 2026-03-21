# Szkolenie 1: Serverless -- Teoria i AWS Lambda

Przyklady funkcji AWS Lambda w Pythonie: podstawowy handler,
testowanie lokalne, wzorzec keep-warm, inicjalizacja poza handlerem.

## Pliki

- `lambda_function.py` -- handler glowny (obsluga API Gateway + bezposrednie wywolanie)
- `test_lambda.py` -- testy lokalne handlera
- `lambda_dynamodb.py` -- handler z DynamoDB (inicjalizacja poza handlerem)
- `trust-policy.json` -- IAM trust policy dla roli Lambda

## Deployment

```bash
# Spakuj funkcje
zip lambda_function.zip lambda_function.py

# Utwórz role IAM
aws iam create-role \
  --role-name lambda-basic-role \
  --assume-role-policy-document file://trust-policy.json

aws iam attach-role-policy \
  --role-name lambda-basic-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Utwórz funkcje Lambda
aws lambda create-function \
  --function-name my-first-lambda \
  --runtime python3.12 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-basic-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda_function.zip \
  --timeout 30 \
  --memory-size 128

# Wywolaj funkcje
aws lambda invoke \
  --function-name my-first-lambda \
  --payload '{"name": "Kacper"}' \
  --cli-binary-format raw-in-base64-out \
  response.json
```
