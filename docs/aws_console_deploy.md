# AWS Console Deployment

## Deployment Flow

```text
AWS Console
│
├── S3
├── DynamoDB
├── Lambda
├── API Gateway
```


## 0. AWS config

1. Login to AWS Console
2. Choose Region: US East (N. Virginia) - us-east-1

## 1. Create S3 & Upload Frontend Files

Creates UI & Error web pages
1. Open S3.
2. Create `fifa-predictor` bucket.
3. Upload `frontend/index.html` as `index.html`.
4. Upload `frontend/error.html` as `error.html`.
5. Uncheck: Block All Public Access & Enable: Bucket Versioning

## 2. Setup Dynamo DB

Stores Users, Picks & FIFA 2026 Official Results
1. Open Dynamo DB
2. Create Table
3. Give Table Name: fifa-predictor-table, Partition Key: pk (String), Sort Key: sk (String)
4. Choose: On-Demand Capacity
   
## 3. Configure Lambda

Lambda code handles API response(s): /state, /users, /predictions, /leaderboard, /official-results, /refresh and writes official FIFA 2026 results into DynamoDB.
1. Open Lambda.
2. Create `fifaPredictorLambda` function.
3. Select: Author from Scratch, Runtime: Python 3.14 or latest
4. Create Function
5. Select `fifaPredictorLambda` function, goto "Code" and copy the code from `backend/lambda_function.py`.
6. Setup Runtime Handler

Navigate: Under the code editor, "Runtime settings", Edit, under "Handler" add the actual lambda handler name as <file_name>.<handler_name>
   e.g: lambda_function.handler  or my_file.lambda_handler

7. Configure Environment Variables

Navigate: Configuration->Environment Settings. Add the below environment variables as key-value pairs.

```text
TABLE_NAME=fifa-predictor-table
TOURNAMENT=FIFA2026
CORS_ORIGIN=*
```

8. Grant DynamoDB Access

Navigate: Configuration->Permissions
Select the available lambda Role (e.g fifaPredictorAPI-role-ad55k0km). 
Under "Permissions", "Add Permissions"->Create Inline Policy
On the policy editor, select "JSON" and copy the below policy.

```text
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
```
Click on Next, enter a policy name like "DynamoDBInlinePolicy"

9. Deploy Code

Open Lambda->Select the lambda function->Code
Click "Deploy".

## 4. Create API Gateway

Create HTTP API end points
1. Open API Gateway->Choose: HTTP API->Click Build
2. API Name: fifa-predictor-http-api, Click: Next
3. Configure: Routes
   
```text
Add: ANY /
Add: ANY /{proxy+}
```

4. Configure: Integrations
   
```text
Select {proxy+}->Any. Create and Attach an Integration
Integration Target: Lambda function
Integration Details: Select AWS Region & Select Lambda Function
```

5. Configure: CORS
   
Add the following under each sub-sections,
```text
Allow Origins: *
Allow Methods: GET, POST, PUT, OPTIONS
Allow Headers: *
```
6. Remember the API Default endpoint: [https://adsmmknot4.execute-api.us-east-1.amazonaws.com]

## 5. Update Frontend to use API

1. Open S3: index.html
2. Search for: REPLACE_WITH_API_GATEWAY_URL
3. Replace with: [https://adsmmknot4.execute-api.us-east-1.amazonaws.com]

## 6. Configure Cloudfront

1. Open Cloudfront
2. Create Distributions->Choose a plan (Select the free plan)
3. Give a name "fifa-predictor-cf", Select a "Single website or app"
4. Specify Origin. Select Amazon S3 & the S3 origin bucket (fifa-predictor)
5. Create Distribution
6. Open the Distribution
7. Goto "General"->Edit
   Default root object, Enter "index.html"
8. Goto "Origins"
   Create Origin. Choosing Origin Domian as S3 and select "fifa-predictor"
   Under "Origin Access", select "Origin access control settings (recommended)"
   Will create a OAC like - "fifa-predictor.s3.us-east-1.amazonaws.com"
10. Save Changes
11. Remember the CloudFront Distribution domain name, "d3kucjh82irtfi.cloudfront.net"

## 7. Update S3 Permission
1. Open S3: fifa-predictor bucket
2. Allow Cloudfront to access S3. Update "Permissions"

```text
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::fifa-predictor/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::950755621885:distribution/E10S89UVXWNEFA"
                }
            }
        }
    ]
}
```
Note: 950755621885 is <account id> and E10S89UVXWNEFA is <distribution name>

## 8. Validate Backend

Test the following links: (*Replace adsmmknot4 with the AWS API Endpoint)

```text
https://adsmmknot4.execute-api.us-east-1.amazonaws.com/health
https://adsmmknot4.execute-api.us-east-1.amazonaws.com/state
https://adsmmknot4.execute-api.us-east-1.amazonaws.com/leaderboard
https://adsmmknot4.execute-api.us-east-1.amazonaws.com/users
https://adsmmknot4.execute-api.us-east-1.amazonaws.com/official-results/refresh
```

## 8. Validate app
1. Open your S3 website endpoint (http://fifa-predictor.s3-website-us-east-1.amazonaws.com/)
2. Select "FIFA 2026" user, and verify if the match results are showing correctly.
3. Select "Default User" and try to predict matches, try "Clear Selections"
4. Create a new user and try to predict matches, try "Clear Selections"
5. In the "Prediction Matrix" at the bottom, all users should be listed with their details & a score.

https://d3kucjh82irtfi.cloudfront.net/
