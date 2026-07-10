# AWS CLI Deployment - V23 Option A

## Upload frontend

```bash
aws s3 cp frontend/index.html s3://fifa-predictor/index.html
aws s3 cp frontend/error.html s3://fifa-predictor/error.html
aws s3 cp data/country-flags.json s3://fifa-predictor/country-flags.json
```

## Package Lambda

```bash
cd backend/lambda
zip -r ../../lambda-v23-option-a.zip lambda_function.py requirements.txt
cd ../..
```

## Update Lambda code

```bash
aws lambda update-function-code   --function-name fifa-predictor-api   --zip-file fileb://lambda-v23-option-a.zip
```

## Confirm handler

```bash
aws lambda update-function-configuration   --function-name fifa-predictor-api   --handler lambda_function.handler
```

## Validate

```bash
curl https://adsmmknot4.execute-api.us-east-1.amazonaws.com/health
curl https://adsmmknot4.execute-api.us-east-1.amazonaws.com/state
```
