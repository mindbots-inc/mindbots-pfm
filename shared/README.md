# PFM Shared Components

Shared models, utilities, and constants for the Personal Finance Management system.

## Overview

This package provides common components used across all PFM services and agents:
- Pydantic models for data validation
- Shared utilities and helpers
- Common constants and enumerations
- Type definitions

## Structure

- `pfm_shared/models/` - Shared data models
- `pfm_shared/utils/` - Common utility functions
- `pfm_shared/constants/` - Shared constants

## Installation

Add to your service's pyproject.toml:
```toml
[tool.poetry.dependencies]
pfm-shared = {path = "../shared", develop = true}
```

Then install:
```bash
poetry install
```

## Usage

```python
from pfm_shared.models.transaction import Transaction, TransactionType
from pfm_shared.utils.date import parse_date
from pfm_shared.constants import SUPPORTED_CURRENCIES

# Create a transaction
transaction = Transaction(
    id="tx_123",
    account_id="acc_456",
    amount=Decimal("-25.50"),
    transaction_type=TransactionType.DEBIT,
    description="Coffee Shop"
)
```

## Development

### Adding New Models

1. Create model file in `pfm_shared/models/`
2. Use Pydantic for validation
3. Add to `__init__.py` exports
4. Document model fields

### Testing

```bash
poetry run pytest
```

## License

Proprietary - Mindbots Inc. All rights reserved.