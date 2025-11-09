"""
FastMCP Server implementation for Email Send/Receive.
"""

from typing import List, Optional
from fastmcp import FastMCP

from .services.email_sender import EmailSender
from .services.email_receiver import EmailReceiver
from .config import get_settings


def create_server() -> FastMCP:
    """Create and configure the FastMCP server."""
    
    # Initialize server
    mcp = FastMCP("Email Send/Receive MCP")
    
    # Initialize service classes
    email_sender = EmailSender()
    email_receiver = EmailReceiver()
    
    # === EMAIL SENDING TOOLS ===
    
    @mcp.tool()
    async def send_email(
        recipient: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        is_html: bool = False
    ) -> str:
        """Send an email via SMTP.
        
        Args:
            recipient: Email address of the recipient (will be validated)
            subject: Email subject/title
            body: Email body content
            attachments: Optional list of file paths to attach
            cc: Optional list of CC recipients
            bcc: Optional list of BCC recipients
            is_html: Whether the body is HTML (default: False for plain text)
        
        Returns:
            JSON string with status and details of the sent email
        """
        result = await email_sender.send_email(
            recipient=recipient,
            subject=subject,
            body=body,
            attachments=attachments,
            cc=cc,
            bcc=bcc,
            is_html=is_html
        )
        
        if result["status"] == "success":
            details = result.get("details", {})
            return (
                f"✅ Email sent successfully!\n"
                f"Recipient: {details.get('recipient', recipient)}\n"
                f"Subject: {details.get('subject', subject)}\n"
                f"CC: {', '.join(details.get('cc', [])) if details.get('cc') else 'None'}\n"
                f"BCC: {', '.join(details.get('bcc', [])) if details.get('bcc') else 'None'}\n"
                f"Attachments: {details.get('attachments', 0)}"
            )
        else:
            return f"❌ Error: {result['message']}"
    
    # === EMAIL RECEIVING TOOLS ===
    
    @mcp.tool()
    async def receive_emails_imap(
        mailbox: str = "INBOX",
        limit: int = 10,
        unread_only: bool = False
    ) -> str:
        """Receive emails using IMAP protocol.
        
        Args:
            mailbox: Mailbox to read from (default: INBOX)
            limit: Maximum number of emails to retrieve (default: 10)
            unread_only: Only retrieve unread emails (default: False)
        
        Returns:
            JSON string with received emails
        """
        result = await email_receiver.receive_emails_imap(
            mailbox=mailbox,
            limit=limit,
            unread_only=unread_only
        )
        
        if result["status"] == "success":
            emails = result.get("emails", [])
            if not emails:
                return "📭 No emails found."
            
            output = f"📬 Retrieved {len(emails)} email(s):\n\n"
            for idx, email_data in enumerate(emails, 1):
                output += f"--- Email {idx} ---\n"
                output += f"ID: {email_data.get('id', 'N/A')}\n"
                output += f"From: {email_data.get('from', 'N/A')}\n"
                output += f"To: {email_data.get('to', 'N/A')}\n"
                output += f"Subject: {email_data.get('subject', 'N/A')}\n"
                output += f"Date: {email_data.get('date', 'N/A')}\n"
                
                if email_data.get('has_attachments'):
                    output += f"Attachments: {len(email_data.get('attachments', []))}\n"
                    for att in email_data.get('attachments', []):
                        output += f"  - {att.get('filename', 'N/A')} ({att.get('content_type', 'N/A')})\n"
                
                body = email_data.get('body', '')
                body_preview = body[:200] + "..." if len(body) > 200 else body
                output += f"Body Preview: {body_preview}\n"
                output += f"Body Length: {email_data.get('body_length', 0)} characters\n\n"
            
            return output
        else:
            return f"❌ Error: {result['message']}"
    
    @mcp.tool()
    def receive_emails_pop3(
        limit: int = 10
    ) -> str:
        """Receive emails using POP3 protocol.
        
        Args:
            limit: Maximum number of emails to retrieve (default: 10)
        
        Returns:
            JSON string with received emails
        """
        result = email_receiver.receive_emails_pop3(limit=limit)
        
        if result["status"] == "success":
            emails = result.get("emails", [])
            if not emails:
                return "📭 No emails found."
            
            output = f"📬 Retrieved {len(emails)} email(s):\n\n"
            for idx, email_data in enumerate(emails, 1):
                output += f"--- Email {idx} ---\n"
                output += f"ID: {email_data.get('id', 'N/A')}\n"
                output += f"From: {email_data.get('from', 'N/A')}\n"
                output += f"To: {email_data.get('to', 'N/A')}\n"
                output += f"Subject: {email_data.get('subject', 'N/A')}\n"
                output += f"Date: {email_data.get('date', 'N/A')}\n"
                
                if email_data.get('has_attachments'):
                    output += f"Attachments: {len(email_data.get('attachments', []))}\n"
                    for att in email_data.get('attachments', []):
                        output += f"  - {att.get('filename', 'N/A')} ({att.get('content_type', 'N/A')})\n"
                
                body = email_data.get('body', '')
                body_preview = body[:200] + "..." if len(body) > 200 else body
                output += f"Body Preview: {body_preview}\n"
                output += f"Body Length: {email_data.get('body_length', 0)} characters\n\n"
            
            return output
        else:
            return f"❌ Error: {result['message']}"
    
    return mcp
