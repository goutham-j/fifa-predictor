# FIFA 2026 World Cup Predictor - V23 Option A

A browser-based FIFA 2026 World Cup knockout predictor with AWS-backed user persistence.

## What this version includes

- Round of 32 prediction bracket.
- User creation and color-coded prediction paths.
- Drag-and-drop picks with drag-back undo support.
- FIFA 2026 read-only official profile.
- Prediction Matrix and score calculation against FIFA 2026 official results.
- AWS backend integration using API Gateway, Lambda, and DynamoDB.
- Country flag display in team and winner boxes.
- Static/manual official results timeline maintained in `lambda_function.py` and mirrored in `data/official-results-timeline.json`.

## V23 Option A decision

This version intentionally does not scrape FIFA.com live at runtime. The official results are refreshed from the backend static/manual timeline. To update future match results, add new entries to `backend/lambda/lambda_function.py` and redeploy Lambda.

## Key deployment files

- `frontend/index.html` - main app UI.
- `frontend/error.html` - S3 static website error page.
- `backend/lambda/lambda_function.py` - production Lambda backend.
- `data/country-flags.json` - country flag mapping.
- `data/official-results-timeline.json` - reference copy of official timeline.

## Runtime architecture

S3 Website -> API Gateway -> Lambda -> DynamoDB.

CloudFront is optional and can be added later after V23 is stable.
