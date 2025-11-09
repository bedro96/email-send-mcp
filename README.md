# Email Send/Receive MCP Server

A Model Context Protocol (MCP) server for sending and receiving emails via SMTP, POP3, and IMAP. Built with FastMCP 2.0 and optimized for deployment on Azure Container Apps.

## Features

- **Email Sending (SMTP)**
  - Send emails with validated recipient addresses
  - Support for CC and BCC
  - HTML and plain text email bodies
  - File attachments support
  - Configurable sender information

- **Email Receiving (IMAP/POP3)**
  - Retrieve emails from IMAP servers
  - Support for POP3 protocol
  - Filter by mailbox/folder
  - Unread emails filtering
  - Attachment information extraction

- **Email Validation**
  - RFC-compliant email address validation
  - Automatic email normalization
  - Batch validation for multiple recipients

## Installation

### Using uv (recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/bedro96/email-send-mcp.git
cd email-send-mcp

# Install dependencies
uv pip install -e .

# For development with testing tools
uv pip install -e ".[dev]"
```

### Using pip

```bash
pip install -e .
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your email server credentials:

```env
# SMTP Configuration (for sending emails)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@example.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true

# IMAP Configuration (for receiving emails)
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=your-email@example.com
IMAP_PASSWORD=your-app-password
IMAP_USE_SSL=true

# POP3 Configuration (alternative for receiving emails)
POP3_SERVER=pop.gmail.com
POP3_PORT=995
POP3_USERNAME=your-email@example.com
POP3_PASSWORD=your-app-password
POP3_USE_SSL=true

# Email Settings
DEFAULT_FROM_EMAIL=your-email@example.com
DEFAULT_FROM_NAME=MCP Email Server
MAX_ATTACHMENT_SIZE_MB=25
```

### Gmail Setup

For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the App Password in the configuration

## Usage

### Running the MCP Server

```bash
python main.py
```

The server will start and expose the following MCP tools:

### Available Tools

#### `send_email`
Send an email via SMTP.

**Parameters:**
- `recipient` (required): Email address of the recipient
- `subject` (required): Email subject/title
- `body` (required): Email body content
- `attachments` (optional): List of file paths to attach
- `cc` (optional): List of CC recipients
- `bcc` (optional): List of BCC recipients
- `is_html` (optional): Whether the body is HTML (default: False)

**Example:**
```python
send_email(
    recipient="user@example.com",
    subject="Hello from MCP",
    body="This is a test email",
    attachments=["/path/to/file.pdf"],
    cc=["cc@example.com"],
    is_html=False
)
```

#### `receive_emails_imap`
Receive emails using IMAP protocol.

**Parameters:**
- `mailbox` (optional): Mailbox to read from (default: "INBOX")
- `limit` (optional): Maximum number of emails to retrieve (default: 10)
- `unread_only` (optional): Only retrieve unread emails (default: False)

**Example:**
```python
receive_emails_imap(
    mailbox="INBOX",
    limit=5,
    unread_only=True
)
```

#### `receive_emails_pop3`
Receive emails using POP3 protocol.

**Parameters:**
- `limit` (optional): Maximum number of emails to retrieve (default: 10)

**Example:**
```python
receive_emails_pop3(limit=10)
```

## Docker Deployment

### Build the Docker image

```bash
docker build -t email-send-mcp .
```

### Run the container

```bash
docker run -d \
  --name email-mcp \
  -e SMTP_SERVER=smtp.gmail.com \
  -e SMTP_PORT=587 \
  -e SMTP_USERNAME=your-email@gmail.com \
  -e SMTP_PASSWORD=your-app-password \
  -e IMAP_SERVER=imap.gmail.com \
  -e IMAP_PORT=993 \
  -e IMAP_USERNAME=your-email@gmail.com \
  -e IMAP_PASSWORD=your-app-password \
  email-send-mcp
```

Or use a `.env` file:

```bash
docker run -d --name email-mcp --env-file .env email-send-mcp
```

## Azure Container Apps Deployment

1. Create an Azure Container Registry (ACR)
2. Push the Docker image to ACR
3. Create a Container App with environment variables
4. Configure scaling and networking as needed

Example Azure CLI commands:

```bash
# Build and push to ACR
az acr build --registry <your-acr-name> --image email-send-mcp:latest .

# Create Container App
az containerapp create \
  --name email-send-mcp \
  --resource-group <your-rg> \
  --environment <your-env> \
  --image <your-acr-name>.azurecr.io/email-send-mcp:latest \
  --env-vars \
    SMTP_SERVER=smtp.gmail.com \
    SMTP_PORT=587 \
    SMTP_USERNAME=secretref:smtp-username \
    SMTP_PASSWORD=secretref:smtp-password
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Formatting

```bash
black src/ tests/ main.py
isort src/ tests/ main.py
```

### Type Checking

```bash
mypy src/
```

## Architecture

```
email-send-mcp/
├── main.py                 # Entry point
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── server.py          # FastMCP server setup
│   ├── services/
│   │   ├── email_sender.py    # SMTP service
│   │   └── email_receiver.py  # IMAP/POP3 service
│   └── utils/
│       └── validators.py      # Email validation
├── tests/                 # Test files
├── Dockerfile            # Container configuration
├── pyproject.toml        # Project dependencies
└── .env.example          # Example configuration
```

## Technology Stack

- **FastMCP 2.0**: MCP server framework
- **aiosmtplib**: Async SMTP client
- **aioimaplib**: Async IMAP client
- **email-validator**: RFC-compliant email validation
- **Pydantic**: Settings management and validation
- **uv**: Fast Python package manager

## Security Considerations

- Never commit `.env` files with real credentials
- Use App Passwords for Gmail and other providers
- Store secrets securely in production (Azure Key Vault, etc.)
- Validate all email addresses before sending
- Implement rate limiting for production use
- Use TLS/SSL for all email connections

## Troubleshooting

### Gmail "Less secure app" error
- Enable 2FA and use App Passwords instead of your regular password

### Connection timeout
- Check firewall settings
- Verify server addresses and ports
- Ensure TLS/SSL settings match your provider

### Authentication failed
- Verify credentials in `.env`
- Check if App Password is used (for Gmail)
- Ensure IMAP/POP3 access is enabled in email settings

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Support

For issues and questions, please open a GitHub issue.
