"""Transaction Classification Agent for Mindbots PFM.

This agent uses LLMs to automatically categorize financial transactions,
identify merchants, and learn from user feedback.
"""

__version__ = "0.1.0"
__author__ = "Mindbots Inc"

from transaction_classification.agents.classifier import TransactionClassifier
from transaction_classification.models.transaction import (
    ClassificationResult,
    TransactionInput,
)

__all__ = [
    "TransactionClassifier",
    "ClassificationResult",
    "TransactionInput",
]