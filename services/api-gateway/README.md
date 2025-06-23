# API Gateway Service

Central API gateway for external access to Personal Finance Management services.

## Overview

The API Gateway provides:
- Unified entry point for all PFM services
- JWT-based authentication and authorization
- Request routing to backend services
- Rate limiting and throttling
- Response caching
- Monitoring and metrics

## Architecture

- FastAPI for high-performance async API
- Redis for caching and rate limiting
- JWT for stateless authentication
- Prometheus metrics and OpenTelemetry tracing
- Smart routing to microservices

## Development Setup

### Prerequisites

- Python 3.12+
- Poetry 1.7.0+
- Redis
- Docker and Docker Compose

### Installation

1. Install dependencies:
```bash
poetry install
```

2. Set up environment:
```bash
cp .env.example .env
# Configure service URLs and secrets
```

3. Start the gateway:
```bash
poetry run uvicorn api_gateway.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI: http://localhost:8000/openapi.json

## Configuration

Key environment variables:
- `JWT_SECRET_KEY`: Secret for JWT signing
- `REDIS_URL`: Redis connection URL
- `BANK_ADAPTER_URL`: Bank adapter service URL
- `RATE_LIMIT`: Rate limit configuration

## Testing

```bash
# Run all tests
poetry run pytest

# With coverage
poetry run pytest --cov=api_gateway
```

## License

Proprietary - Mindbots Inc. All rights reserved.