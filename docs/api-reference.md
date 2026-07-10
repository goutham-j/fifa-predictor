# API Reference

## GET /health
Returns backend health and configured DynamoDB table.

## GET /state
Refreshes FIFA 2026 official results from the static timeline, then returns users, leaderboard and official results.

## GET /users
Returns all users.

## POST /users
Creates a user.

## GET /predictions/{userId}
Returns a user's predictions.

## POST /predictions/{userId}
Stores a user's predictions.

## GET or POST /official-results/refresh
Refreshes the read-only FIFA 2026 user from the static backend timeline.

## PUT /official-results
Manual override endpoint for official results.

## API Examples
https://{abc123}.execute-api.us-east-1.amazonaws.com
https://{abc123}.execute-api.us-east-1.amazonaws.com/health
https://{abc123}.execute-api.us-east-1.amazonaws.com/state
https://{abc123}.execute-api.us-east-1.amazonaws.com/leaderboard
https://{abc123}.execute-api.us-east-1.amazonaws.com/users
https://{abc123}.execute-api.us-east-1.amazonaws.com/official-results/refresh
