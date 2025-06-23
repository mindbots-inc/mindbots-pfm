"""Pytest configuration for transaction classification tests."""

import asyncio
from datetime import datetime
from decimal import Decimal
from typing import List

import pytest
import pytest_asyncio

from transaction_classification.models.transaction import TransactionInput


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_transaction() -> TransactionInput:
    """Create a sample transaction for testing."""
    return TransactionInput(
        id="tx_123",
        description="STARBUCKS STORE #1234 NEW YORK NY",
        amount=Decimal("-5.75"),
        date=datetime(2025, 6, 23, 10, 30, 0),
        account_id="acc_456",
        currency="USD",
    )


@pytest.fixture
def sample_transactions() -> List[TransactionInput]:
    """Create a list of sample transactions for batch testing."""
    return [
        TransactionInput(
            id="tx_1",
            description="WHOLE FOODS MARKET #365",
            amount=Decimal("-125.43"),
            date=datetime(2025, 6, 23, 9, 0, 0),
        ),
        TransactionInput(
            id="tx_2",
            description="UBER *TRIP HELP.UBER.COM",
            amount=Decimal("-18.50"),
            date=datetime(2025, 6, 23, 14, 30, 0),
        ),
        TransactionInput(
            id="tx_3",
            description="NETFLIX.COM",
            amount=Decimal("-15.99"),
            date=datetime(2025, 6, 23, 0, 0, 0),
        ),
        TransactionInput(
            id="tx_4",
            description="SHELL OIL 57444533",
            amount=Decimal("-65.00"),
            date=datetime(2025, 6, 22, 16, 45, 0),
        ),
        TransactionInput(
            id="tx_5",
            description="PAYROLL DEPOSIT ACME CORP",
            amount=Decimal("2500.00"),
            date=datetime(2025, 6, 21, 8, 0, 0),
        ),
    ]


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response for testing."""
    return {
        "category": "restaurants",
        "confidence": 0.95,
        "merchant_name": "Starbucks",
        "subcategory": "coffee_shops",
        "tags": ["coffee", "beverages", "quick_service"],
        "reasoning": "Transaction at Starbucks coffee shop",
    }


@pytest.fixture
def mock_cache_manager(mocker):
    """Create a mock cache manager."""
    cache = mocker.Mock()
    cache.get = mocker.AsyncMock(return_value=None)
    cache.set = mocker.AsyncMock(return_value=True)
    cache.delete = mocker.AsyncMock(return_value=True)
    cache.get_transaction_key = mocker.Mock(return_value="tx_class:test_key")
    return cache