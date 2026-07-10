# AWS Console Deployment

## Deployment Flow

AWS Console
│
├── S3
├── DynamoDB
├── Lambda
├── API Gateway
└── CloudFront (not enabled yet)

## 0. AWS cnfig

1. Login to AWS Console
2. Choose Region: US East (N. Virginia) - us-east-1

## 1. Upload frontend
Stores UI & Error web pages
1. Open S3.
2. Open your `fifa-predictor` bucket.
3. Upload `frontend/index.html` as `index.html`.
4. Upload `frontend/error.html` as `error.html`.
5. Uncheck: Block All Public Access

## 2. Configure Dynamo DB
Stores: Users, Picks & FIFA 2026 Official Results
1. Open Dynamo DB-> Create Table
2. Give Table Name:fifa-predictor-table, Partition Key:pk (String), Sort Key:sk (String)
3. Choose: On-Demand Capacity
   
## 3. Update Lambda
Lambda code handles API response(s): /state, /users, /predictions, /leaderboard, /official-results, /refresh and writes official FIFA 2026 results into DynamoDB.
1. Open Lambda.
2. Open your `fifa-predictor-api` function.
3. Select: Author from Scratch, Runtime: Python 3.12
4. Copy the code with `backend/lambda/lambda_function.py`.
5. Confirm handler is:
```text
lambda_function.handler
```
6. Confirm environment variables:
```text
TABLE_NAME=fifa-predictor-table
TOURNAMENT=FIFA2026
CORS_ORIGIN=*
```
7. Grant DynamoDB Access
```text
Navigate: Configuration->Permissions

Click Lambda Role.
Add inline policy:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Scan",
        "dynamodb:Query"
      ],
      "Resource": "*"
    }
  ]
}

Resource = *
```
8. Click Deploy.

## 4. Create API Gateway
Create HTTP API end points
1. Open API Gateway->Choose: HTTP API->Click Build
2. Add Lambda Integration. Select: fifa-predictor-api, Click:Next
3. Configure Routes
```text
Add: ANY /
Add: ANY /{proxy+}
```
4. Enable CORS: In: API Gateway→ CORS
Configure:
```text
Allowed Origins:*
Allowed Methods:GETPOSTPUTOPTIONS
Allowed Headers:*
5. Save the API endpoint: https://<abcd1234>.execute-api.us-east-1.amazonaws.com

## 5. Configure frontend
1. Update S3:index.html
Search for: REPLACE_WITH_API_GATEWAY_URL
Replace with: https://<abcd1234>.execute-api.us-east-1.amazonaws.com .

## 6. Validate backend
Test the following links: (*Replace abcd1234 with the AWS resource name)
```text
https://<abcd1234>.execute-api.us-east-1.amazonaws.com/health
https://<abcd1234>.execute-api.us-east-1.amazonaws.com/state
https://<abcd1234>.execute-api.us-east-1.amazonaws.com/leaderboard
https://<abcd1234>.execute-api.us-east-1.amazonaws.com/users
https://<abcd1234>.execute-api.us-east-1.amazonaws.com/official-results/refresh
```

## 7. Validate app
1. Open your S3 website endpoint (http://fifa-predictor.s3-website-us-east-1.amazonaws.com/)
2. Select FIFA 2026, and verify flags and updated official progression display correctly.
