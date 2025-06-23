"""Configuration settings for Bank Adapter Service."""

from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application settings
    APP_NAME: str = "Bank Adapter Service"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = Field(default=False)
    
    # API settings
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS settings
    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:8000",
            "https://app.mindbots.com",
        ]
    )
    
    # Database settings
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/bank_adapter"
    )
    
    # Redis settings
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # Plaid settings
    PLAID_CLIENT_ID: str = Field(default="")
    PLAID_SECRET: str = Field(default="")
    PLAID_ENV: str = Field(default="sandbox")
    PLAID_PRODUCTS: List[str] = Field(
        default=["transactions", "accounts", "balance", "identity"]
    )
    PLAID_COUNTRY_CODES: List[str] = Field(default=["US", "CA", "GB"])
    
    # Yodlee settings
    YODLEE_CLIENT_ID: str = Field(default="")
    YODLEE_CLIENT_SECRET: str = Field(default="")
    YODLEE_API_URL: str = Field(default="https://sandbox.api.yodlee.com/ysl")
    
    # Security settings
    SECRET_KEY: str = Field(default="change-me-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    @field_validator("PLAID_ENV")
    @classmethod
    def validate_plaid_env(cls, v: str) -> str:
        """Validate Plaid environment."""
        allowed = ["sandbox", "development", "production"]
        if v not in allowed:
            raise ValueError(f"PLAID_ENV must be one of {allowed}")
        return v
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()


# Create settings instance
settings = Settings()