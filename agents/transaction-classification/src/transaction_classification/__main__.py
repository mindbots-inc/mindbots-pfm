"""Main entry point for Transaction Classification Agent."""

import asyncio
import sys
from datetime import datetime
from decimal import Decimal

from structlog import get_logger

from transaction_classification import TransactionClassifier
from transaction_classification.config import settings
from transaction_classification.models.transaction import TransactionInput

logger = get_logger()


async def main():
    """Run example classification."""
    logger.info(
        "Starting Transaction Classification Agent",
        version="0.1.0",
        model=settings.classification_model,
    )
    
    # Initialize classifier
    classifier = TransactionClassifier()
    
    # Example transaction
    transaction = TransactionInput(
        id="example_001",
        description="WHOLE FOODS MARKET #365 NEW YORK NY",
        amount=Decimal("-85.42"),
        date=datetime.now(),
        currency="USD",
    )
    
    try:
        # Classify transaction
        logger.info("Classifying transaction", transaction_id=transaction.id)
        result = await classifier.classify_transaction(
            transaction,
            include_reasoning=True
        )
        
        # Display result
        logger.info(
            "Classification complete",
            category=result.category,
            confidence=result.confidence,
            merchant=result.merchant_name,
            reasoning=result.reasoning,
        )
        
        # Get available categories
        categories = await classifier.get_categories()
        logger.info("Available categories", categories=categories)
        
    except Exception as e:
        logger.error("Classification failed", error=str(e), exc_info=True)
        sys.exit(1)
    
    logger.info("Agent execution complete")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())