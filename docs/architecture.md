# Architecture - FIFA Predictor

## Current architecture

```text
User Browser
   |
   v
S3 Static Website Hosting
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
[(http://fifa-predictor.s3-website-us-east-1.amazonaws.com/)]
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
