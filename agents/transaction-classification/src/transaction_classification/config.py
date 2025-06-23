"""Configuration settings for Transaction Classification Agent."""

from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings for the Transaction Classification Agent."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="TRANSACTION_CLASSIFIER_",
    )
    
    # Agent settings
    agent_name: str = Field(default="TransactionClassifier")
    agent_version: str = Field(default="0.1.0")
    
    # LLM settings
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    classification_model: str = Field(
        default="gpt-4",
        description="Default model for classification (gpt-4, claude-3)"
    )
    
    # Classification settings
    confidence_threshold: float = Field(
        default=0.85,
        description="Minimum confidence for auto-classification"
    )
    available_categories: List[str] = Field(
        default=[
            "groceries",
            "restaurants",
            "transportation",
            "utilities",
            "entertainment",
            "healthcare",
            "shopping",
            "income",
            "transfer",
            "other"
        ]
    )
    
    # Cache settings
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    cache_ttl: int = Field(
        default=3600,
        description="Cache TTL in seconds"
    )
    
    # Memory Cell integration
    memory_cell_url: Optional[str] = Field(
        default=None,
        description="Memory Cell service URL for storing patterns"
    )
    
    # Performance settings
    batch_size: int = Field(
        default=100,
        description="Maximum batch size for classification"
    )
    max_concurrent_requests: int = Field(
        default=10,
        description="Maximum concurrent LLM requests"
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