# Bank Adapter Service

Service for integrating with banks and payment providers in the Mindbots Personal Finance Management system.

## Overview

The Bank Adapter Service provides a unified interface for connecting to various banking providers (Plaid, Yodlee, etc.) to:
- Connect to bank accounts
- Sync transactions
- Monitor balances
- Initiate payments

## Architecture

This service follows the Mindbots microservice architecture:
- FastAPI for REST API
- Async/await for high performance
- PostgreSQL for data persistence
- Redis for caching
- Docker for containerization

## Development Setup

### Prerequisites

- Python 3.12+
- Poetry 1.7.0+
- Docker and Docker Compose
- PostgreSQL 14+
- Redis

### Installation

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run database migrations:
```bash
poetry run alembic upgrade head
```

4. Start the service:
```bash
poetry run uvicorn bank_adapter.main:app --reload --host 0.0.0.0 --port 8001
```

## API Documentation

Once the service is running, you can access:
- API Documentation: http://localhost:8001/docs
- OpenAPI Schema: http://localhost:8001/openapi.json

## Testing

Run tests with:
```bash
poetry run pytest
```

With coverage:
```bash
poetry run pytest --cov=bank_adapter --cov-report=html
```

## Configuration

Key environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `PLAID_CLIENT_ID`: Plaid API client ID
- `PLAID_SECRET`: Plaid API secret
- `YODLEE_CLIENT_ID`: Yodlee API client ID
- `YODLEE_CLIENT_SECRET`: Yodlee API secret

## License

Proprietary - Mindbots Inc. All rights reserved.