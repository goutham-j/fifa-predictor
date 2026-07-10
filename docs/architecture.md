# Architecture - FIFA Predictor V23 Option A

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
```

## FIFA 2026 refresh flow

```text
User selects FIFA 2026
   -> frontend calls POST /official-results/refresh
   -> Lambda recomputes official selections from OFFICIAL_RESULTS_TIMELINE
   -> Lambda writes USER#FIFA 2026 / PREDICTION#FIFA2026 to DynamoDB
   -> frontend calls GET /state
   -> bracket, Prediction Matrix, and scores refresh
```

## Why Option A

The live FIFA website parsing enhancement is deferred. This version keeps the backend stable by using a manually updated official timeline.

## No AWS schema change

DynamoDB remains:

```text
pk = USER#<UserId>
sk = PROFILE | PREDICTION#FIFA2026
```
