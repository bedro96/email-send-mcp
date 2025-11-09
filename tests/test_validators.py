"""
Tests for email validation utilities.
"""

import pytest
from src.utils.validators import (
    validate_email_address,
    validate_email_addresses,
    format_email_address
)


class TestEmailValidation:
    """Test email validation functions."""
    
    def test_validate_valid_email(self):
        """Test validation of a valid email address."""
        is_valid, result = validate_email_address("user@example.com")
        assert is_valid is True
        assert "@" in result
    
    def test_validate_invalid_email_no_at(self):
        """Test validation of email without @ symbol."""
        is_valid, result = validate_email_address("userexample.com")
        assert is_valid is False
        assert "must have an @" in result.lower() or "@ sign" in result.lower()
    
    def test_validate_invalid_email_no_domain(self):
        """Test validation of email without domain."""
        is_valid, result = validate_email_address("user@")
        assert is_valid is False
    
    def test_validate_email_with_dots(self):
        """Test validation of email with dots."""
        is_valid, result = validate_email_address("first.last@example.com")
        assert is_valid is True
    
    def test_validate_email_with_plus(self):
        """Test validation of email with plus sign."""
        is_valid, result = validate_email_address("user+tag@example.com")
        assert is_valid is True
    
    def test_validate_multiple_emails(self):
        """Test validation of multiple email addresses."""
        emails = [
            "valid1@example.com",
            "invalid-email",
            "valid2@example.com",
            "another@invalid"
        ]
        
        valid, invalid = validate_email_addresses(emails)
        
        assert len(valid) >= 2  # At least 2 valid emails
        assert len(invalid) >= 1  # At least 1 invalid email
    
    def test_format_email_without_name(self):
        """Test formatting email address without name."""
        result = format_email_address("user@example.com")
        assert result == "user@example.com"
    
    def test_format_email_with_name(self):
        """Test formatting email address with name."""
        result = format_email_address("user@example.com", "John Doe")
        assert "John Doe" in result
        assert "user@example.com" in result
        assert "<" in result and ">" in result
