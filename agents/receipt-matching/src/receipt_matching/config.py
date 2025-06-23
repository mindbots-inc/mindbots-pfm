"""Configuration settings for Receipt Matching Agent."""

from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings for the Receipt Matching Agent."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="RECEIPT_MATCHER_",
    )
    
    # Agent settings
    agent_name: str = Field(default="ReceiptMatcher")
    agent_version: str = Field(default="0.1.0")
    
    # LLM settings
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    ocr_model: str = Field(
        default="gpt-4-vision",
        description="Model for OCR and receipt processing"
    )
    matching_model: str = Field(
        default="gpt-4",
        description="Model for transaction matching"
    )
    
    # Matching settings
    matching_threshold: float = Field(
        default=0.75,
        description="Minimum confidence for auto-matching"
    )
    fuzzy_match_ratio: float = Field(
        default=0.8,
        description="Fuzzy string matching threshold"
    )
    amount_tolerance: float = Field(
        default=0.02,
        description="Tolerance for amount matching (2%)"
    )
    date_tolerance_days: int = Field(
        default=3,
        description="Days tolerance for date matching"
    )
    
    # OCR settings
    ocr_service_url: Optional[str] = Field(
        default=None,
        description="External OCR service URL"
    )
    supported_formats: List[str] = Field(
        default=["pdf", "png", "jpg", "jpeg", "tiff"],
        description="Supported receipt file formats"
    )
    
    # Cache settings
    redis_url: str = Field(
        default="redis://localhost:6379/1",
        env="REDIS_URL"
    )
    cache_ttl: int = Field(
        default=86400,  # 24 hours
        description="Cache TTL in seconds"
    )
    
    # Performance settings
    max_concurrent_ocr: int = Field(
        default=5,
        description="Maximum concurrent OCR operations"
    )
    max_receipt_size_mb: int = Field(
        default=10,
        description="Maximum receipt file size in MB"
    )
    
    # Logging settings
    log_level: str = Field(default="INFO")
    
    @property
    def has_openai(self) -> bool:
        """Check if OpenAI is configured."""
        return bool(self.openai_api_key)
    
    @property
    def has_anthropic(self) -> bool:
        """Check if Anthropic is configured."""
        return bool(self.anthropic_api_key)


# Create global settings instance
settings = Settings()