# Architecture - FIFA Predictor

## AWS Architecture

```text
Users
   ↓
https://d3kucjh82irtfi.cloudfront.net
   ↓
CloudFront Distribution (E10S89UVXWNEFA)
   ↓
Origin Access Control (OAC)
   ↓
Private S3 Bucket (fifa-predictor)
   ↓
API Gateway (fifa-predictor-http-api)
   ↓
Lambda fifaPredictionLambda (lambda_function.handler)
   ↓
DynamoDB (fifa-predictor-table)

This is 100% serverless.
No Route53.
No EC2.
No servers.
No load balancers.
No custom domain.
No SSL certificates to manage.
No Kubernetes.
CloudFront provides HTTPS automatically.

Application can be accessed by the CDN endpoint (https://d3kucjh82irtfi.cloudfront.net/)
http://fifa-predictor.s3-website-us-east-1.amazonaws.com/
```


## Functional Flow

```text
1. Cloudfront (https://d3kucjh82irtfi.cloudfront.net/) setup redirects request to 'fifa-predictor' S3 with index.html as the root object.
2. Frontend code is built in index.html
3. The backend functions defined in index.html calls https://adsmmknot4.execute-api.us-east-1.amazonaws.com/? with different endpoints for the following functions,
   - To refresh the official results
   - To create new users
   - To provide status of all users
3. The API Gateway executes the lambda function defined in the lambda.handler
4. The lambda functions writes data to the Dyanamo DB table.
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
