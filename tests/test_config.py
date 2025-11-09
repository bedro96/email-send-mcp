"""
Tests for configuration management.
"""

import pytest
from src.config import Settings, get_settings


class TestConfiguration:
    """Test configuration management."""
    
    def test_default_settings(self):
        """Test default settings values."""
        settings = Settings()
        
        assert settings.VERSION == "1.0.0"
        assert settings.DEBUG is False
        assert settings.LOG_LEVEL == "INFO"
        assert settings.SMTP_PORT == 587
        assert settings.IMAP_PORT == 993
        assert settings.POP3_PORT == 995
    
    def test_smtp_tls_default(self):
        """Test SMTP TLS is enabled by default."""
        settings = Settings()
        assert settings.SMTP_USE_TLS is True
    
    def test_imap_ssl_default(self):
        """Test IMAP SSL is enabled by default."""
        settings = Settings()
        assert settings.IMAP_USE_SSL is True
    
    def test_max_attachment_size(self):
        """Test max attachment size default."""
        settings = Settings()
        assert settings.MAX_ATTACHMENT_SIZE_MB == 25
    
    def test_port_validation(self):
        """Test port number validation."""
        # Valid port
        settings = Settings(SMTP_PORT=587)
        assert settings.SMTP_PORT == 587
        
        # Invalid port should raise error
        with pytest.raises(Exception):
            Settings(SMTP_PORT=99999)
    
    def test_get_settings_singleton(self):
        """Test that get_settings returns the same instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2
