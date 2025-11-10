"""
Email receiving service using IMAP and POP3.
"""

import aioimaplib
import asyncio
import email
import email.message
from email.header import decode_header
from typing import List, Dict, Any, Optional
import poplib
from datetime import datetime

from ..config import get_settings


class EmailReceiver:
    """Service for receiving emails via IMAP or POP3."""
    
    def __init__(self):
        """Initialize the email receiver with configuration."""
        self.settings = get_settings()
    
    async def receive_emails_imap(
        self,
        mailbox: str = "INBOX",
        limit: int = 10,
        unread_only: bool = False
    ) -> Dict[str, Any]:
        """
        Receive emails using IMAP.
        
        Args:
            mailbox: Mailbox to read from (default: INBOX)
            limit: Maximum number of emails to retrieve
            unread_only: Only retrieve unread emails
            
        Returns:
            Dictionary with status and email list
        """
        try:
            # Connect to IMAP server
            imap = aioimaplib.IMAP4_SSL(
                host=self.settings.IMAP_SERVER,
                port=self.settings.IMAP_PORT
            )
            
            await imap.wait_hello_from_server()
            
            # Login
            await imap.login(
                self.settings.IMAP_USERNAME,
                self.settings.IMAP_PASSWORD
            )
            
            # Select mailbox
            await imap.select(mailbox)
            
            # Search for emails
            search_criteria = "UNSEEN" if unread_only else "ALL"
            response = await imap.search(search_criteria)
            
            if response[0] != "OK":
                return {
                    "status": "error",
                    "message": "Failed to search emails"
                }
            
            email_ids = response[1][0].split()
            
            # Limit the number of emails
            email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            
            emails = []
            for email_id in email_ids:
                # Convert bytes to string for aioimaplib
                email_id_str = email_id.decode() if isinstance(email_id, bytes) else str(email_id)
                email_data = await self._fetch_email_imap(imap, email_id_str)
                if email_data:
                    emails.append(email_data)
            
            # Logout
            await imap.logout()
            
            return {
                "status": "success",
                "count": len(emails),
                "emails": emails
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to receive emails via IMAP: {str(e)}"
            }
    
    async def _fetch_email_imap(
        self,
        imap: aioimaplib.IMAP4_SSL,
        email_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch a single email via IMAP.
        
        Args:
            imap: IMAP connection
            email_id: Email ID to fetch
            
        Returns:
            Dictionary with email data or None
        """
        try:
            # Use RFC822 to fetch the complete message
            response = await imap.fetch(email_id, "RFC822")
            
            if response[0] != "OK":
                return None
            
            # Extract email body from response
            # Based on our testing, the message is in response[1][1]
            if len(response[1]) >= 2:
                email_body = response[1][1]
            elif len(response[1]) >= 1:
                email_body = response[1][0]
            else:
                return None
            
            # Convert to bytes if needed
            if isinstance(email_body, str):
                email_body = email_body.encode()
            
            # Parse the email message
            email_message = email.message_from_bytes(email_body)
            
            return self._parse_email(email_message, email_id)
            
        except Exception as e:
            return None
    
    def receive_emails_pop3(
        self,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Receive emails using POP3 (synchronous operation).
        
        Args:
            limit: Maximum number of emails to retrieve
            
        Returns:
            Dictionary with status and email list
        """
        try:
            # Connect to POP3 server
            if self.settings.POP3_USE_SSL:
                pop = poplib.POP3_SSL(
                    self.settings.POP3_SERVER,
                    self.settings.POP3_PORT
                )
            else:
                pop = poplib.POP3(
                    self.settings.POP3_SERVER,
                    self.settings.POP3_PORT
                )
            
            # Login
            pop.user(self.settings.POP3_USERNAME)
            pop.pass_(self.settings.POP3_PASSWORD)
            
            # Get message count
            num_messages = len(pop.list()[1])
            
            # Limit the number of emails
            start_index = max(1, num_messages - limit + 1)
            
            emails = []
            for i in range(start_index, num_messages + 1):
                try:
                    response, lines, octets = pop.retr(i)
                    email_content = b"\r\n".join(lines)
                    email_message = email.message_from_bytes(email_content)
                    
                    email_data = self._parse_email(email_message, str(i))
                    if email_data:
                        emails.append(email_data)
                except Exception as e:
                    continue
            
            # Quit
            pop.quit()
            
            return {
                "status": "success",
                "count": len(emails),
                "emails": emails
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to receive emails via POP3: {str(e)}"
            }
    
    def _parse_email(
        self,
        email_message: email.message.Message,
        email_id: str
    ) -> Dict[str, Any]:
        """
        Parse an email message.
        
        Args:
            email_message: Email message object
            email_id: Email ID
            
        Returns:
            Dictionary with parsed email data
        """
        # Decode subject
        subject = ""
        if email_message["Subject"]:
            subject_parts = decode_header(email_message["Subject"])
            subject = ""
            for content, encoding in subject_parts:
                if isinstance(content, bytes):
                    subject += content.decode(encoding or "utf-8", errors="ignore")
                else:
                    subject += content
        
        # Get sender
        from_header = email_message.get("From", "")
        
        # Get recipient
        to_header = email_message.get("To", "")
        
        # Get date
        date_header = email_message.get("Date", "")
        
        # Get body
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
                    except:
                        pass
        else:
            try:
                body = email_message.get_payload(decode=True).decode(errors="ignore")
            except:
                body = str(email_message.get_payload())
        
        # Get attachments info
        attachments = []
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_disposition() == "attachment":
                    filename = part.get_filename()
                    if filename:
                        attachments.append({
                            "filename": filename,
                            "content_type": part.get_content_type()
                        })
        
        return {
            "id": email_id,
            "subject": subject,
            "from": from_header,
            "to": to_header,
            "date": date_header,
            "body": body[:1000] if len(body) > 1000 else body,  # Limit body length
            "body_length": len(body),
            "attachments": attachments,
            "has_attachments": len(attachments) > 0
        }
