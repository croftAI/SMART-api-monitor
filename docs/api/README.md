# SMART API Documentation

## Endpoints

### Analysis Endpoints
- `POST /v1/analysis/metrics/{api_name}`
- `GET /v1/analysis/history/{api_name}`
- `GET /v1/analysis/trends/{api_name}`

### Context Endpoints
- `GET /v1/context/{api_name}`
- `PUT /v1/context/{api_name}`
- `GET /v1/context/{api_name}/dependencies`

### Prediction Endpoints
- `POST /v1/prediction/traffic/{api_name}`
- `POST /v1/prediction/thresholds/{api_name}`
- `GET /v1/prediction/patterns/{api_name}`

## Authentication
Requires API key in header: `X-API-Key`

## Request/Response Examples
[Include examples for each endpoint]