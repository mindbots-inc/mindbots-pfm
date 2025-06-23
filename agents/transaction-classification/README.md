# Transaction Classification Agent

AI-powered agent for automatic transaction categorization in the Personal Finance Management system.

## Overview

The Transaction Classification Agent uses advanced language models to:
- Automatically categorize financial transactions
- Identify and normalize merchant names
- Learn from user feedback
- Provide confidence scores for classifications

## Features

- **Multi-Model Support**: OpenAI GPT-4, Anthropic Claude
- **Zero-Shot Classification**: Works without training data
- **Few-Shot Learning**: Improves with examples
- **Batch Processing**: Efficient handling of multiple transactions
- **Context Awareness**: Considers user history and patterns

## Architecture

- LangChain/LangGraph for agent framework
- Multiple LLM providers for flexibility
- Redis for caching and performance
- Memory Cell integration for learning

## Development Setup

### Prerequisites

- Python 3.12+
- Poetry 1.7.0+
- Redis
- API keys for LLM providers

### Installation

1. Install dependencies:
```bash
poetry install
```

2. Configure environment:
```bash
cp .env.example .env
# Add your API keys and configuration
```

3. Run the agent:
```bash
poetry run python -m transaction_classification
```

## Usage Example

```python
from transaction_classification import TransactionClassifier

classifier = TransactionClassifier()

# Single transaction
result = await classifier.classify_transaction({
    "description": "STARBUCKS STORE #1234",
    "amount": -5.75,
    "date": "2025-06-23"
})
print(f"Category: {result.category}, Confidence: {result.confidence}")

# Batch processing
results = await classifier.classify_batch(transactions)
```

## Testing

```bash
# Run all tests
poetry run pytest

# With coverage
poetry run pytest --cov=transaction_classification
```

## Configuration

Key environment variables:
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `CLASSIFICATION_MODEL`: Default model (gpt-4, claude-3)
- `CONFIDENCE_THRESHOLD`: Min confidence for auto-classification

## License

Proprietary - Mindbots Inc. All rights reserved.