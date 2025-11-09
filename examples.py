"""
Example usage of the Email Send/Receive MCP Server
"""

import asyncio
from src.server import create_server
from src.services.email_sender import EmailSender
from src.services.email_receiver import EmailReceiver


async def send_simple_email_example():
    """Example: Send a simple text email."""
    sender = EmailSender()
    
    result = await sender.send_email(
        recipient="recipient@example.com",
        subject="Hello from MCP",
        body="This is a test email sent via the Email MCP Server."
    )
    
    print(f"Send result: {result}")


async def send_email_with_attachments_example():
    """Example: Send an email with attachments."""
    sender = EmailSender()
    
    result = await sender.send_email(
        recipient="recipient@example.com",
        subject="Email with Attachment",
        body="Please find the attached document.",
        attachments=["/path/to/document.pdf"],
        cc=["cc1@example.com", "cc2@example.com"]
    )
    
    print(f"Send result: {result}")


async def send_html_email_example():
    """Example: Send an HTML email."""
    sender = EmailSender()
    
    html_body = """
    <html>
        <body>
            <h1>Welcome!</h1>
            <p>This is an <strong>HTML</strong> email.</p>
            <ul>
                <li>Feature 1</li>
                <li>Feature 2</li>
            </ul>
        </body>
    </html>
    """
    
    result = await sender.send_email(
        recipient="recipient@example.com",
        subject="HTML Email Example",
        body=html_body,
        is_html=True
    )
    
    print(f"Send result: {result}")


async def receive_emails_imap_example():
    """Example: Receive emails via IMAP."""
    receiver = EmailReceiver()
    
    # Get last 5 unread emails
    result = await receiver.receive_emails_imap(
        mailbox="INBOX",
        limit=5,
        unread_only=True
    )
    
    if result["status"] == "success":
        print(f"Retrieved {result['count']} emails:")
        for email in result["emails"]:
            print(f"\nSubject: {email['subject']}")
            print(f"From: {email['from']}")
            print(f"Date: {email['date']}")
            print(f"Body preview: {email['body'][:100]}...")
    else:
        print(f"Error: {result['message']}")


def receive_emails_pop3_example():
    """Example: Receive emails via POP3."""
    receiver = EmailReceiver()
    
    # Get last 10 emails
    result = receiver.receive_emails_pop3(limit=10)
    
    if result["status"] == "success":
        print(f"Retrieved {result['count']} emails:")
        for email in result["emails"]:
            print(f"\nSubject: {email['subject']}")
            print(f"From: {email['from']}")
            if email['has_attachments']:
                print(f"Attachments: {len(email['attachments'])}")
    else:
        print(f"Error: {result['message']}")


async def using_mcp_server_example():
    """Example: Using the MCP server directly."""
    # Create the server
    mcp = create_server()
    
    # The server exposes tools that can be called by MCP clients
    # When running mcp.run(), it will handle tool invocations
    # from connected clients (like Claude Desktop)
    
    print("MCP Server created with the following tools:")
    print("- send_email")
    print("- receive_emails_imap")
    print("- receive_emails_pop3")
    print("\nRun main.py to start the server")


async def main():
    """Run examples."""
    print("=== Email MCP Server Examples ===\n")
    
    # Uncomment the examples you want to run
    
    # await send_simple_email_example()
    # await send_email_with_attachments_example()
    # await send_html_email_example()
    # await receive_emails_imap_example()
    # receive_emails_pop3_example()
    await using_mcp_server_example()


if __name__ == "__main__":
    asyncio.run(main())
