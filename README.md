# Mindbots Personal Finance Management (PFM)

Intelligent Personal Finance Management Service - A comprehensive financial management system integrating AI agents, bank adapters, and Odoo ERP.

## 🎯 Overview

Mindbots PFM is an AI-powered personal finance management system that helps users:
- Connect and manage multiple bank accounts
- Automatically categorize transactions using AI
- Match receipts to transactions
- Generate financial insights and recommendations
- Manage budgets and track spending
- Integrate with accounting systems

## 🏗️ Architecture

The system follows Mindbots' cell-tissue-organ architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway                               │
│                    (External Access Point)                       │
└────────────┬────────────┬────────────┬────────────┬────────────┘
             │            │            │            │
     ┌───────▼──────┐ ┌──▼───────┐ ┌─▼──────┐ ┌──▼──────┐
     │ Bank Adapter │ │ AI Agents│ │  Odoo  │ │ Storage │
     │   Service    │ │ (3 types)│ │Modules │ │ (MinIO) │
     └──────────────┘ └──────────┘ └────────┘ └─────────┘
             │            │            │            │
     ┌───────▼────────────▼────────────▼────────────▼────────┐
     │              PostgreSQL + Redis                        │
     └────────────────────────────────────────────────────────┘
```

## 📂 Project Structure

```
mindbots-pfm/
├── agents/                    # AI Agents
│   ├── transaction-classification/
│   ├── receipt-matching/
│   └── financial-analysis/
├── services/                  # Microservices
│   ├── bank-adapter/         # Banking integrations
│   └── api-gateway/          # Central API gateway
├── odoo/                     # Odoo ERP modules
│   ├── addons/              # Custom modules
│   └── config/              # Configuration
├── shared/                   # Shared components
│   └── pfm_shared/          # Common models & utils
├── infrastructure/           # Deployment configs
├── docs/                    # Documentation
└── docker-compose.yml       # Local development
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Poetry 1.7.0+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis

### Development Setup

1. **Clone the repository with submodules:**
```bash
git clone --recursive https://github.com/mindbots-inc/mindbots-pfm.git
cd mindbots-pfm
```

2. **Copy environment configuration:**
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

3. **Start the development environment:**
```bash
docker compose up -d
```

4. **Verify services are running:**
```bash
docker compose ps
```

Services will be available at:
- API Gateway: http://localhost:8000
- Bank Adapter: http://localhost:8001
- Odoo: http://localhost:8069
- MinIO Console: http://localhost:9001

## 🧩 Components

### Services

#### Bank Adapter Service
- Integrates with banking providers (Plaid, Yodlee)
- Syncs transactions and balances
- Manages bank connections
- [Documentation](services/bank-adapter/README.md)

#### API Gateway
- Central entry point for all services
- JWT authentication
- Request routing and rate limiting
- [Documentation](services/api-gateway/README.md)

### AI Agents

#### Transaction Classification
- Automatically categorizes transactions
- Multi-model support (GPT-4, Claude)
- Learns from user feedback
- [Documentation](agents/transaction-classification/README.md)

#### Receipt Matching
- Matches receipts to transactions
- OCR integration
- Fuzzy matching algorithms
- [Documentation](agents/receipt-matching/README.md)

#### Financial Analysis
- Generates spending insights
- Cash flow predictions
- Anomaly detection
- [Documentation](agents/financial-analysis/README.md)

### Odoo Modules

Custom ERP modules for:
- Account management
- Transaction tracking
- Financial reporting
- Budget management
- [Documentation](odoo/README.md)

## 🧪 Testing

### Run All Tests
```bash
# Unit tests for a specific service
cd services/bank-adapter
poetry run pytest

# Integration tests
docker compose up -d
poetry run pytest tests/integration/

# Coverage report
poetry run pytest --cov --cov-report=html
```

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 🔧 Development

### Adding a New Service

1. Create service directory: `services/new-service/`
2. Initialize Poetry: `poetry init`
3. Create module.yml configuration
4. Implement service logic
5. Add to docker-compose.yml
6. Update CI/CD workflows

### Working with AI Agents

Agents use LangChain/LangGraph framework:
```python
from transaction_classification import TransactionClassifier

classifier = TransactionClassifier()
result = await classifier.classify_transaction(transaction_data)
```

### Database Migrations

Using Alembic for database migrations:
```bash
# Create migration
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations
poetry run alembic upgrade head
```

## 📚 Documentation

- [Architecture Overview](docs/architecture/README.md)
- [API Documentation](docs/api/README.md)
- [Development Guide](docs/development/README.md)
- [Deployment Guide](docs/deployment/README.md)

## 🔒 Security

- JWT-based authentication
- Environment-based configuration
- Encrypted API communications
- Regular security audits

## 🤝 Contributing

1. Create feature branch from epic branch
2. Follow coding standards (enforced by pre-commit)
3. Write tests (minimum 80% coverage)
4. Update documentation
5. Submit PR with clear description

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📈 Monitoring

- Prometheus metrics at `/metrics`
- Health checks at `/health`
- OpenTelemetry tracing
- Centralized logging

## 🚢 Deployment

### Docker
```bash
docker build -t mindbots-pfm .
docker run -p 8000:8000 mindbots-pfm
```

### Kubernetes
```bash
kubectl apply -f infrastructure/k8s/
```

## 📄 License

Proprietary - Mindbots Inc. All rights reserved.

---

**Version:** 0.1.0  
**Status:** Development  
**Epic:** [Intelligent Personal Finance Management Service](https://github.com/mindbots-inc/mindbots-pfm/issues/1)
