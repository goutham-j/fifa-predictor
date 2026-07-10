# Data Model

## DynamoDB Table

Table: `fifa-predictor-table`

Primary key:

```text
pk string
sk string
```

## User profile item

```json
{
  "pk":"USER#Goutham",
  "sk":"PROFILE",
  "userId":"Goutham",
  "displayName":"Goutham",
  "color":"#32d583"
}
```

## Prediction item

```json
{
  "pk":"USER#Goutham",
  "sk":"PREDICTION#FIFA2026",
  "selections": {}
}
```

## Official FIFA 2026 profile

```text
pk = USER#FIFA 2026
sk = PREDICTION#FIFA2026
```

Updated by `/official-results/refresh`.
