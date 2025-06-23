"""Receipt Matching Agent for Mindbots PFM.

This agent uses AI to match receipts to transactions through OCR,
intelligent matching algorithms, and confidence scoring.
"""

__version__ = "0.1.0"
__author__ = "Mindbots Inc"

from receipt_matching.agents.matcher import ReceiptMatcher
from receipt_matching.models.receipt import (
    MatchResult,
    ReceiptData,
    MatchingRequest,
)

__all__ = [
    "ReceiptMatcher",
    "MatchResult",
    "ReceiptData",
    "MatchingRequest",
]