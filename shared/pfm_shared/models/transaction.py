"""Shared transaction models for PFM system."""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TransactionType(str, Enum):
    """Transaction type enumeration."""
    
    DEBIT = "debit"
    CREDIT = "credit"
    TRANSFER = "transfer"


class TransactionStatus(str, Enum):
    """Transaction status enumeration."""
    
    PENDING = "pending"
    POSTED = "posted"
    CANCELLED = "cancelled"
    FAILED = "failed"


class TransactionCategory(str, Enum):
    """Common transaction categories."""
    
    GROCERIES = "groceries"
    RESTAURANTS = "restaurants"
    TRANSPORTATION = "transportation"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    HEALTHCARE = "healthcare"
    SHOPPING = "shopping"
    INCOME = "income"
    TRANSFER = "transfer"
    OTHER = "other"


class Transaction(BaseModel):
    """Transaction data model."""
    
    id: str = Field(..., description="Unique transaction identifier")
    account_id: str = Field(..., description="Associated account ID")
    amount: Decimal = Field(..., description="Transaction amount")
    currency: str = Field(default="USD", description="Currency code")
    transaction_type: TransactionType = Field(..., description="Type of transaction")
    status: TransactionStatus = Field(
        default=TransactionStatus.PENDING,
        description="Transaction status"
    )
    
    # Transaction details
    description: str = Field(..., description="Transaction description")
    merchant_name: Optional[str] = Field(None, description="Merchant name")
    category: Optional[TransactionCategory] = Field(
        None,
        description="Transaction category"
    )
    
    # Dates
    transaction_date: datetime = Field(..., description="Transaction date")
    posted_date: Optional[datetime] = Field(None, description="Posted date")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record update timestamp"
    )
    
    # Metadata
    external_id: Optional[str] = Field(
        None,
        description="External system ID (bank/provider)"
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Additional metadata"
    )
    
    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Validate transaction amount."""
        if v == 0:
            raise ValueError("Transaction amount cannot be zero")
        return v
    
    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        """Validate currency code."""
        return v.upper()
    
    class Config:
        """Model configuration."""
        
        json_encoders = {
            Decimal: str,
            datetime: lambda v: v.isoformat(),
        }