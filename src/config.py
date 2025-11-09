"""
Configuration management for the Email MCP server.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")
    
    # SMTP Configuration
    SMTP_SERVER: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USERNAME: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    SMTP_USE_TLS: bool = Field(default=True)
    
    # IMAP Configuration
    IMAP_SERVER: str = Field(default="imap.gmail.com")
    IMAP_PORT: int = Field(default=993)
    IMAP_USERNAME: str = Field(default="")
    IMAP_PASSWORD: str = Field(default="")
    IMAP_USE_SSL: bool = Field(default=True)
    
    # POP3 Configuration
    POP3_SERVER: str = Field(default="pop.gmail.com")
    POP3_PORT: int = Field(default=995)
    POP3_USERNAME: str = Field(default="")
    POP3_PASSWORD: str = Field(default="")
    POP3_USE_SSL: bool = Field(default=True)
    
    # Email Settings
    DEFAULT_FROM_EMAIL: str = Field(default="")
    DEFAULT_FROM_NAME: str = Field(default="MCP Email Server")
    MAX_ATTACHMENT_SIZE_MB: int = Field(default=25)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @field_validator("SMTP_PORT", "IMAP_PORT", "POP3_PORT")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Validate port numbers are in valid range."""
        if not (1 <= v <= 65535):
            raise ValueError(f"Port must be between 1 and 65535, got {v}")
        return v


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings (singleton pattern)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
