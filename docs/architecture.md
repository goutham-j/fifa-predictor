# Architecture - FIFA Predictor

## AWS Architecture

```text
User Browser
   |
   v
S3 Static Website Hosting  (https://fifa-predictor.s3.us-east-1.amazonaws.com/index.html)
   |
   v
API Gateway HTTP API 
   |
   v
Lambda: lambda_function.handler
   |
   v
DynamoDB: fifa-predictor-table

This is 100% serverless.
No Route53.
No EC2.
No servers.
No load balancers.
No custom domain.
No SSL certificates to manage.
No Kubernetes.
CloudFront provides HTTPS automatically.

And you'll access the application through S3 public endpoint. CloudFront can be added later.
http://fifa-predictor.s3-website-us-east-1.amazonaws.com/
```

## Functional Flow

```text
1. index.html -> Calls https://adsmmknot4.execute-api.us-east-1.amazonaws.com/? different endpoints for the following functions,
   - To refresh the official results
   - To create new users
   - To provide status of all users

2. 

```

## FIFA 2026 User Flow

```text
User selects FIFA 2026
   -> frontend calls POST /official-results/refresh
   -> Lambda recomputes official selections from OFFICIAL_RESULTS_TIMELINE
   -> Lambda writes USER#FIFA 2026 / PREDICTION#FIFA2026 to DynamoDB
   -> frontend calls GET /state
   -> bracket, Prediction Matrix, and scores refresh
```
