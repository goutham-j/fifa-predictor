# AWS CLI Deployment

## Upload frontend

```bash
aws s3 cp frontend/index.html s3://fifa-predictor/index.html
aws s3 cp frontend/error.html s3://fifa-predictor/error.html
```

## Update Lambda code

```bash
aws lambda update-function-code   --function-name fifa-predictor-api   fileb://lambda_function.py
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
