"""
Email sending service using SMTP.
"""

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
import os
from pathlib import Path

from ..config import get_settings
from ..utils.validators import validate_email_address, format_email_address


class EmailSender:
    """Service for sending emails via SMTP."""
    
    def __init__(self):
        """Initialize the email sender with configuration."""
        self.settings = get_settings()
    
    async def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        is_html: bool = False,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email via SMTP.
        
        Args:
            recipient: Email address of the recipient
            subject: Email subject
            body: Email body content
            attachments: Optional list of file paths to attach
            cc: Optional list of CC recipients
            bcc: Optional list of BCC recipients
            is_html: Whether the body is HTML (default: False for plain text)
            from_email: Optional sender email (uses default if not provided)
            from_name: Optional sender name (uses default if not provided)
            
        Returns:
            Dictionary with status and message
        """
        # Validate recipient email
        is_valid, result = validate_email_address(recipient)
        if not is_valid:
            return {
                "status": "error",
                "message": f"Invalid recipient email: {result}"
            }
        recipient = result
        
        # Validate CC emails if provided
        if cc:
            valid_cc = []
            for email in cc:
                is_valid, result = validate_email_address(email)
                if not is_valid:
                    return {
                        "status": "error",
                        "message": f"Invalid CC email: {result}"
                    }
                valid_cc.append(result)
            cc = valid_cc
        
        # Validate BCC emails if provided
        if bcc:
            valid_bcc = []
            for email in bcc:
                is_valid, result = validate_email_address(email)
                if not is_valid:
                    return {
                        "status": "error",
                        "message": f"Invalid BCC email: {result}"
                    }
                valid_bcc.append(result)
            bcc = valid_bcc
        
        # Set from email and name
        sender_email = from_email or self.settings.DEFAULT_FROM_EMAIL
        sender_name = from_name or self.settings.DEFAULT_FROM_NAME
        
        if not sender_email:
            return {
                "status": "error",
                "message": "No sender email configured"
            }
        
        # Validate sender email
        is_valid, result = validate_email_address(sender_email)
        if not is_valid:
            return {
                "status": "error",
                "message": f"Invalid sender email: {result}"
            }
        sender_email = result
        
        # Create message
        message = MIMEMultipart()
        message["From"] = format_email_address(sender_email, sender_name)
        message["To"] = recipient
        message["Subject"] = subject
        
        if cc:
            message["Cc"] = ", ".join(cc)
        
        # Add body
        body_type = "html" if is_html else "plain"
        message.attach(MIMEText(body, body_type))
        
        # Add attachments if provided
        if attachments:
            for file_path in attachments:
                try:
                    attachment_result = await self._add_attachment(message, file_path)
                    if attachment_result["status"] == "error":
                        return attachment_result
                except Exception as e:
                    return {
                        "status": "error",
                        "message": f"Error adding attachment {file_path}: {str(e)}"
                    }
        
        # Send email
        try:
            recipients = [recipient]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            await self._send_smtp_message(message, sender_email, recipients)
            
            return {
                "status": "success",
                "message": f"Email sent successfully to {recipient}",
                "details": {
                    "recipient": recipient,
                    "subject": subject,
                    "cc": cc,
                    "bcc": bcc,
                    "attachments": len(attachments) if attachments else 0
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to send email: {str(e)}"
            }
    
    async def _add_attachment(self, message: MIMEMultipart, file_path: str) -> Dict[str, str]:
        """
        Add an attachment to the email message.
        
        Args:
            message: The MIME message to add attachment to
            file_path: Path to the file to attach
            
        Returns:
            Dictionary with status
        """
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            return {
                "status": "error",
                "message": f"Attachment file not found: {file_path}"
            }
        
        # Check file size
        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb > self.settings.MAX_ATTACHMENT_SIZE_MB:
            return {
                "status": "error",
                "message": f"Attachment {path.name} exceeds maximum size of {self.settings.MAX_ATTACHMENT_SIZE_MB}MB"
            }
        
        # Read and attach file
        with open(path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {path.name}"
        )
        
        message.attach(part)
        return {"status": "success"}
    
    async def _send_smtp_message(
        self,
        message: MIMEMultipart,
        sender: str,
        recipients: List[str]
    ) -> None:
        """
        Send the SMTP message.
        
        Args:
            message: The MIME message to send
            sender: Sender email address
            recipients: List of recipient email addresses
        """
        # Port 465 requires SSL, port 587 requires STARTTLS
        if self.settings.SMTP_PORT == 465:
            # Direct SSL connection for port 465
            async with aiosmtplib.SMTP(
                hostname=self.settings.SMTP_SERVER,
                port=self.settings.SMTP_PORT,
                username=self.settings.SMTP_USERNAME,
                password=self.settings.SMTP_PASSWORD,
                use_tls=True
            ) as smtp:
                await smtp.send_message(message, sender=sender, recipients=recipients)
        else:
            # STARTTLS for port 587
            async with aiosmtplib.SMTP(
                hostname=self.settings.SMTP_SERVER,
                port=self.settings.SMTP_PORT,
                username=self.settings.SMTP_USERNAME,
                password=self.settings.SMTP_PASSWORD,
                start_tls=True if self.settings.SMTP_USE_TLS else False
            ) as smtp:
                await smtp.send_message(message, sender=sender, recipients=recipients)
