# lifehub-lambda

日常の細々した作業をaws lambdaから、GPTに叩いてもらって各アプリに自動反映するシステム群

A minimal serverless backend for personal data integration using AWS Lambda and API Gateway.

## Features

- AWS Lambda (Python 3.11) with HTTP API Gateway
- POST /recipe endpoint for storing recipe data
- Simple JSON-based API
- Easy deployment using AWS SAM

## Prerequisites

- AWS CLI configured with appropriate credentials
- AWS SAM CLI installed ([Installation guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html))
- Python 3.11

## API Endpoint

### POST /recipe

Accepts a JSON body with the following fields:
- `name` (string): Recipe name
- `ingredients` (array): List of ingredients
- `calories` (number): Calorie count
- `date` (string): Date of the recipe

**Example Request:**
```bash
curl -X POST https://your-api-endpoint/recipe \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pasta Carbonara",
    "ingredients": ["pasta", "eggs", "bacon", "parmesan"],
    "calories": 450,
    "date": "2025-10-20"
  }'
```

**Response:**
```json
{
  "status": "ok"
}
```

## Deployment

### Option 1: Using Makefile

```bash
# Build the application
make build

# Deploy (first time - will guide you through configuration)
make deploy

# Deploy (subsequent times)
make deploy-fast
```

### Option 2: Using SAM CLI directly

```bash
# Build the application
sam build

# Deploy with guided prompts
sam deploy --guided

# Deploy with saved configuration
sam deploy
```

## Local Development

To test the API locally:

```bash
# Start local API
make local-api

# Or using SAM CLI
sam local start-api
```

Then test with:
```bash
curl -X POST http://127.0.0.1:3000/recipe \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Recipe",
    "ingredients": ["test"],
    "calories": 100,
    "date": "2025-10-20"
  }'
```

## Project Structure

```
lifehub-lambda/
├── app.py              # Lambda function handler
├── template.yaml       # SAM/CloudFormation template
├── requirements.txt    # Python dependencies
├── Makefile           # Easy deployment commands
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Cleaning Up

To delete the deployed stack:

```bash
aws cloudformation delete-stack --stack-name lifehub-lambda
```

## License

MIT License - see LICENSE file for details
