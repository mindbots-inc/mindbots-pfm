"""Configuration settings for Financial Analysis Agent."""

from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings for the Financial Analysis Agent."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="FINANCIAL_ANALYZER_",
    )
    
    # Agent settings
    agent_name: str = Field(default="FinancialAnalyzer")
    agent_version: str = Field(default="0.1.0")
    
    # LLM settings
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    analysis_model: str = Field(
        default="gpt-4",
        description="Default model for financial analysis"
    )
    
    # Analysis settings
    analysis_period_days: int = Field(
        default=90,
        description="Default analysis period in days"
    )
    anomaly_threshold: float = Field(
        default=2.5,
        description="Standard deviations for anomaly detection"
    )
    prediction_horizon_days: int = Field(
        default=30,
        description="Default prediction horizon in days"
    )
    min_transactions_for_analysis: int = Field(
        default=10,
        description="Minimum transactions needed for analysis"
    )
    
    # Report settings
    report_frequency: str = Field(
        default="weekly",
        description="Default report generation frequency"
    )
    report_formats: List[str] = Field(
        default=["json", "markdown", "pdf"],
        description="Supported report formats"
    )
    include_visualizations: bool = Field(
        default=True,
        description="Include charts in reports"
    )
    
    # Cache settings
    redis_url: str = Field(
        default="redis://localhost:6379/2",
        env="REDIS_URL"
    )
    cache_ttl: int = Field(
        default=7200,  # 2 hours
        description="Cache TTL in seconds"
    )
    
    # Integration settings
    bank_adapter_url: Optional[str] = Field(
        default="http://localhost:8001",
        description="Bank adapter service URL"
    )
    memory_cell_url: Optional[str] = Field(
        default=None,
        description="Memory Cell service URL"
    )
    
    # Performance settings
    max_concurrent_analyses: int = Field(
        default=5,
        description="Maximum concurrent analysis operations"
    )
    batch_size: int = Field(
        default=1000,
        description="Batch size for transaction processing"
    )
    
    # Machine Learning settings
    ml_confidence_threshold: float = Field(
        default=0.8,
        description="Minimum confidence for ML predictions"
    )
    enable_trend_analysis: bool = Field(
        default=True,
        description="Enable trend analysis features"
    )
    enable_anomaly_detection: bool = Field(
        default=True,
        description="Enable anomaly detection"
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