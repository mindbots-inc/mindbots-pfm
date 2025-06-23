# Contributing to Mindbots PFM

Thank you for your interest in contributing to the Mindbots Personal Finance Management system!

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## 🤝 Code of Conduct

We are committed to fostering a welcoming and inclusive environment. All contributors are expected to:
- Be respectful and professional
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what is best for the project and community

## 🚀 Getting Started

### Prerequisites

1. Fork the repository
2. Clone your fork with submodules:
   ```bash
   git clone --recursive https://github.com/YOUR_USERNAME/mindbots-pfm.git
   cd mindbots-pfm
   ```

3. Set up development environment:
   ```bash
   cp .env.example .env
   # Configure your environment variables
   
   # Install pre-commit hooks
   pre-commit install
   
   # Start development services
   docker compose up -d
   ```

### Development Workflow

1. Create a feature branch from the appropriate epic branch:
   ```bash
   git checkout feature/1-intelligent-personal-finance-management
   git pull origin feature/1-intelligent-personal-finance-management
   git checkout -b feature/ISSUE_NUMBER-brief-description
   ```

2. Make your changes following our coding standards

3. Test thoroughly:
   ```bash
   # Run pre-commit checks
   pre-commit run --all-files
   
   # Run tests
   poetry run pytest
   ```

4. Commit with meaningful messages:
   ```bash
   git add .
   git commit -m "feat(component): Add feature description
   
   - Detailed change 1
   - Detailed change 2
   
   Closes #ISSUE_NUMBER"
   ```

## 💻 Coding Standards

### Python Code Style

- **Formatter**: Black (line length: 88)
- **Linter**: Ruff
- **Type Checker**: MyPy
- **Python Version**: 3.12+

### Code Organization

```python
"""Module docstring explaining purpose."""

# Standard library imports
import os
from typing import Optional

# Third-party imports
from pydantic import BaseModel

# Local imports
from pfm_shared.models import Transaction

# Constants
DEFAULT_TIMEOUT = 30

# Your code here...
```

### Best Practices

1. **Type Hints**: Always use type hints
   ```python
   def process_transaction(transaction: Transaction) -> Optional[str]:
       """Process a transaction and return category."""
       pass
   ```

2. **Async/Await**: Use async for I/O operations
   ```python
   async def fetch_transactions(account_id: str) -> List[Transaction]:
       """Fetch transactions from bank API."""
       async with httpx.AsyncClient() as client:
           response = await client.get(f"/accounts/{account_id}/transactions")
           return response.json()
   ```

3. **Error Handling**: Use specific exceptions
   ```python
   class TransactionNotFoundError(Exception):
       """Raised when transaction is not found."""
       pass
   ```

4. **Logging**: Use structured logging
   ```python
   import structlog
   
   logger = structlog.get_logger()
   logger.info("Processing transaction", transaction_id=tx_id, amount=amount)
   ```

## 🧪 Testing Requirements

### Test Coverage

- Minimum coverage: 80%
- Critical paths: 95%+
- New features must include tests

### Test Structure

```python
# tests/unit/test_transaction_classifier.py
import pytest
from transaction_classification import TransactionClassifier

class TestTransactionClassifier:
    """Test transaction classification functionality."""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return TransactionClassifier()
    
    async def test_classify_transaction(self, classifier):
        """Test basic transaction classification."""
        result = await classifier.classify_transaction({
            "description": "STARBUCKS",
            "amount": -5.75
        })
        assert result.category == "restaurants"
        assert result.confidence > 0.8
```

### Test Types

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test service interactions
3. **End-to-End Tests**: Test complete workflows

## 📚 Documentation

### Code Documentation

- All public functions/classes need docstrings
- Use Google-style docstrings:
  ```python
  def calculate_budget(transactions: List[Transaction], 
                      categories: List[str]) -> Budget:
      """Calculate budget based on transactions.
      
      Args:
          transactions: List of transactions to analyze
          categories: Categories to include in budget
          
      Returns:
          Budget object with calculated values
          
      Raises:
          ValueError: If no transactions provided
      """
  ```

### API Documentation

- Document all endpoints in OpenAPI format
- Include request/response examples
- Document error responses

### README Updates

- Update relevant README files
- Add new dependencies to documentation
- Update architecture diagrams if needed

## 🔄 Pull Request Process

### Before Submitting

1. ✅ All tests pass
2. ✅ Pre-commit hooks pass
3. ✅ Documentation updated
4. ✅ No merge conflicts
5. ✅ Issue referenced in PR

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated

Closes #ISSUE_NUMBER
```

### Review Process

1. Automated checks must pass
2. At least one approval required
3. Maintainer performs final review
4. Squash and merge to epic branch

## 🐛 Reporting Issues

### Bug Reports

Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error messages/logs

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative approaches
- Impact on existing features

## 🎯 Areas for Contribution

Current areas where we welcome contributions:

1. **Additional Banking Providers**: Integrate new banks
2. **AI Agent Improvements**: Enhance classification accuracy
3. **Performance Optimization**: Improve response times
4. **Documentation**: Improve guides and examples
5. **Testing**: Increase test coverage
6. **UI/UX**: Improve user interfaces

## 💬 Getting Help

- Check existing issues and PRs
- Read the documentation
- Ask in discussions
- Contact maintainers

---

Thank you for contributing to Mindbots PFM! Your efforts help make personal finance management accessible and intelligent for everyone.