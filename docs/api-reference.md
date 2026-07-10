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
