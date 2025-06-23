"""Transaction models for classification."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class TransactionInput(BaseModel):
    """Input model for transaction classification."""
    
    id: Optional[str] = Field(None, description="Transaction ID")
    description: str = Field(..., description="Transaction description/merchant name")
    amount: Decimal = Field(..., description="Transaction amount")
    date: datetime = Field(..., description="Transaction date")
    account_id: Optional[str] = Field(None, description="Account ID")
    currency: str = Field(default="USD", description="Currency code")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional transaction metadata"
    )
    
    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        """Validate and normalize currency code."""
        return v.upper()
    
    class Config:
        """Model configuration."""
        json_encoders = {
            Decimal: str,
            datetime: lambda v: v.isoformat(),
        }


class ClassificationResult(BaseModel):
    """Result of transaction classification."""
    
    transaction_id: Optional[str] = Field(None, description="Original transaction ID")
    category: str = Field(..., description="Predicted category")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    merchant_name: Optional[str] = Field(
        None,
        description="Normalized merchant name"
    )
    subcategory: Optional[str] = Field(None, description="Subcategory if applicable")
    tags: List[str] = Field(
        default_factory=list,
        description="Additional tags or labels"
    )
    reasoning: Optional[str] = Field(
        None,
        description="LLM reasoning for classification"
    )
    model_used: str = Field(..., description="Model used for classification")
    classified_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Classification timestamp"
    )
    
    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Round confidence to 3 decimal places."""
        return round(v, 3)


class BatchClassificationRequest(BaseModel):
    """Request for batch transaction classification."""
    
    transactions: List[TransactionInput] = Field(
        ...,
        description="List of transactions to classify"
    )
    force_model: Optional[str] = Field(
        None,
        description="Force specific model for this batch"
    )
    include_reasoning: bool = Field(
        default=False,
        description="Include LLM reasoning in results"
    )


class BatchClassificationResponse(BaseModel):
    """Response for batch transaction classification."""
    
    results: List[ClassificationResult] = Field(
        ...,
        description="Classification results"
    )
    total_processed: int = Field(..., description="Total transactions processed")
    failed_count: int = Field(default=0, description="Number of failed classifications")
    processing_time_ms: int = Field(..., description="Total processing time in ms")
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_processed == 0:
            return 0.0
        return (self.total_processed - self.failed_count) / self.total_processed


class CategoryInfo(BaseModel):
    """Information about a transaction category."""
    
    name: str = Field(..., description="Category name")
    description: str = Field(..., description="Category description")
    parent_category: Optional[str] = Field(None, description="Parent category if nested")
    keywords: List[str] = Field(
        default_factory=list,
        description="Keywords associated with category"
    )
    examples: List[str] = Field(
        default_factory=list,
        description="Example merchants for this category"
    )