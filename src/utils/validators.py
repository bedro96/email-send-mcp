"""
Utility functions for email operations.
"""

from email_validator import validate_email, EmailNotValidError
from typing import List, Tuple


def validate_email_address(email: str) -> Tuple[bool, str]:
    """
    Validate if an email address is in a valid format.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, normalized_email_or_error_message)
    """
    try:
        # Validate and normalize the email
        validation = validate_email(email, check_deliverability=False)
        return True, validation.normalized
    except EmailNotValidError as e:
        return False, str(e)


def validate_email_addresses(emails: List[str]) -> Tuple[List[str], List[str]]:
    """
    Validate multiple email addresses.
    
    Args:
        emails: List of email addresses to validate
        
    Returns:
        Tuple of (valid_emails, invalid_emails_with_errors)
    """
    valid_emails = []
    invalid_emails = []
    
    for email in emails:
        is_valid, result = validate_email_address(email)
        if is_valid:
            valid_emails.append(result)
        else:
            invalid_emails.append(f"{email}: {result}")
    
    return valid_emails, invalid_emails


def format_email_address(email: str, name: str = "") -> str:
    """
    Format an email address with optional name.
    
    Args:
        email: Email address
        name: Optional display name
        
    Returns:
        Formatted email address string
    """
    if name:
        return f'"{name}" <{email}>'
    return email
