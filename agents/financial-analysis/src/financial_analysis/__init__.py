"""Financial Analysis Agent for Mindbots PFM.

This agent generates financial insights, recommendations, and predictive
analytics using advanced AI models and time-series analysis.
"""

__version__ = "0.1.0"
__author__ = "Mindbots Inc"

from financial_analysis.agents.analyzer import FinancialAnalyzer
from financial_analysis.models.analysis import (
    AnalysisResult,
    SpendingPattern,
    CashFlowPrediction,
    FinancialInsight,
)

__all__ = [
    "FinancialAnalyzer",
    "AnalysisResult",
    "SpendingPattern",
    "CashFlowPrediction",
    "FinancialInsight",
]