# AWS Console Deployment

## 1. Upload frontend

1. Open S3.
2. Open your `fifa-predictor` bucket.
3. Upload `frontend/index.html` as `index.html`.
4. Upload `frontend/error.html` as `error.html`.
5. Upload `data/country-flags.json` if you want to keep the data file with the frontend assets.

## 2. Update Lambda

1. Open Lambda.
2. Open your `fifa-predictor-api` function.
3. Replace the current code with `backend/lambda/lambda_function.py`.
4. Confirm handler is:

```text
lambda_function.handler
```

5. Confirm environment variables:

```text
TABLE_NAME=fifa-predictor-table
TOURNAMENT=FIFA2026
CORS_ORIGIN=*
```

6. Click Deploy.

## 3. Validate backend

Open:

```text
https://adsmmknot4.execute-api.us-east-1.amazonaws.com/health
```

Then open:

```text
https://adsmmknot4.execute-api.us-east-1.amazonaws.com/state
```

## 4. Validate app

Open your S3 website endpoint, select FIFA 2026, and verify flags and updated official progression display correctly.
