# Email Send/Receive MCP Server

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.0-green.svg)](https://github.com/jlowin/fastmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server for sending and receiving emails via SMTP, POP3, and IMAP. Built with FastMCP 2.0, this server enables AI assistants like Claude to interact with email services, making it easy to automate email workflows, check inboxes, and send messages programmatically.

## 🎯 What is MCP?

The Model Context Protocol (MCP) is an open standard that enables AI applications to securely connect to external data sources and tools. This server implements MCP to give AI assistants the ability to:

- **Send emails** with attachments, CC/BCC support
- **Receive and read emails** from IMAP/POP3 servers
- **Search and filter** email messages
- **Work with multiple email providers** (Gmail, Outlook, Yahoo, etc.)

Perfect for integration with AI assistants like [Claude Desktop](https://claude.ai/download), this server acts as a bridge between conversational AI and your email infrastructure.

## ✨ Features

### 📤 Email Sending (SMTP)
- ✅ Send emails with validated recipient addresses
- ✅ Support for CC (Carbon Copy) and BCC (Blind Carbon Copy)
- ✅ HTML and plain text email bodies
- ✅ File attachments support with size validation
- ✅ Configurable sender information (name and email)
- ✅ Batch email validation for multiple recipients
- ✅ Smart TLS/SSL connection handling

### 📥 Email Receiving (IMAP/POP3)
- ✅ Retrieve emails from IMAP servers with full folder support
- ✅ POP3 protocol support for simple email retrieval
- ✅ Filter by mailbox/folder (INBOX, Sent, Drafts, etc.)
- ✅ Unread emails filtering
- ✅ Attachment information extraction
- ✅ Email metadata parsing (sender, subject, date, etc.)
- ✅ Body preview with length limiting

### 🔒 Email Validation & Security
- ✅ RFC-compliant email address validation
- ✅ Automatic email normalization
- ✅ Batch validation for multiple recipients
- ✅ App Password support for major providers
- ✅ TLS/SSL encryption for all connections
- ✅ Secure credential management via environment variables

### 🛡️ API Key Authentication
- ✅ `x-api-key` header-based authentication via ASGI middleware
- ✅ Case-insensitive header key matching (`X-Api-Key`, `x-api-key`, etc.)
- ✅ Production mode enforces authentication; Development mode bypasses it
- ✅ `/api/health` endpoint is always public (no auth required)
- ✅ Configurable via `MODE` and `X-API-KEY` environment variables

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Authentication](#-authentication)
- [MCP Tools (Functions)](#-mcp-tools-functions)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)
- [Smoke Test Results](#-smoke-test-results)
- [Integration with MCP Clients](#-integration-with-mcp-clients)
- [Docker Deployment](#-docker-deployment)
- [Architecture](#-architecture)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## 🚀 Quick Start

Get started in 5 minutes! Follow these steps:

```bash
# 1. Clone and install
git clone https://github.com/bedro96/email-send-mcp.git
cd email-send-mcp
pip install -e .

# 2. Configure email credentials
cp .env.example .env
# Edit .env with your email provider settings

# 3. Run the server
python main.py
```

For detailed quick start instructions, see [QUICKSTART.md](QUICKSTART.md).

## 📦 Installation

### Prerequisites

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **Email account** with SMTP/IMAP access (Gmail, Outlook, Yahoo, etc.)
- **App Password** for your email provider (for Gmail, Outlook, Yahoo)

### Method 1: Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package manager that simplifies dependency management.

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

### Method 2: Using pip

```bash
# Clone the repository
git clone https://github.com/bedro96/email-send-mcp.git
cd email-send-mcp

# Install dependencies
pip install -e .

# For development (optional)
pip install -e ".[dev]"
```

### Verify Installation

```bash
# Check if dependencies are installed
python -c "import fastmcp; print('FastMCP version:', fastmcp.__version__)"
```

## ⚙️ Configuration

### Step 1: Create Environment File

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

# Server Configuration
LOG_LEVEL=INFO
DEBUG=false

# Mode: Development (auth bypassed) or Production (auth enforced)
MODE=Production

# API Key for x-api-key header authentication
X-API-KEY=your-strong-api-key-here
```

### Step 2: Email Provider Setup

#### Gmail Setup (Most Common)

For Gmail, you'll need to:

1. **Enable 2-Factor Authentication**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable 2-Step Verification

2. **Generate an App Password**
   - Visit [App Passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" and your device
   - Copy the generated 16-character password
   - Use this password in your `.env` file

3. **Enable IMAP Access** (for receiving emails)
   - Open Gmail → Settings → See all settings
   - Go to "Forwarding and POP/IMAP" tab
   - Enable IMAP
   - Save Changes

**Gmail Configuration:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # 16-character app password
SMTP_USE_TLS=true

IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=your-email@gmail.com
IMAP_PASSWORD=xxxx xxxx xxxx xxxx  # Same app password
IMAP_USE_SSL=true

DEFAULT_FROM_EMAIL=your-email@gmail.com
```

#### Other Email Providers

For configuration details for Outlook, Yahoo, ProtonMail, iCloud, and custom SMTP servers, see [EMAIL_PROVIDERS.md](EMAIL_PROVIDERS.md).

### Configuration Parameters Explained

| Parameter | Description | Default | Required |
|-----------|-------------|---------|----------|
| `SMTP_SERVER` | SMTP server hostname | smtp.gmail.com | Yes (for sending) |
| `SMTP_PORT` | SMTP server port (587 for TLS, 465 for SSL) | 587 | Yes (for sending) |
| `SMTP_USERNAME` | SMTP authentication username (usually email) | - | Yes (for sending) |
| `SMTP_PASSWORD` | SMTP authentication password (use app password) | - | Yes (for sending) |
| `SMTP_USE_TLS` | Use STARTTLS for SMTP (recommended for port 587) | true | No |
| `IMAP_SERVER` | IMAP server hostname | imap.gmail.com | Yes (for receiving) |
| `IMAP_PORT` | IMAP server port (993 for SSL) | 993 | Yes (for receiving) |
| `IMAP_USERNAME` | IMAP authentication username | - | Yes (for receiving) |
| `IMAP_PASSWORD` | IMAP authentication password | - | Yes (for receiving) |
| `IMAP_USE_SSL` | Use SSL for IMAP | true | No |
| `POP3_SERVER` | POP3 server hostname | pop.gmail.com | No |
| `POP3_PORT` | POP3 server port (995 for SSL) | 995 | No |
| `POP3_USERNAME` | POP3 authentication username | - | No |
| `POP3_PASSWORD` | POP3 authentication password | - | No |
| `POP3_USE_SSL` | Use SSL for POP3 | true | No |
| `DEFAULT_FROM_EMAIL` | Default sender email address | - | Yes |
| `DEFAULT_FROM_NAME` | Default sender display name | MCP Email Server | No |
| `MAX_ATTACHMENT_SIZE_MB` | Maximum attachment size in MB | 25 | No |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO | No |
| `DEBUG` | Enable debug mode | false | No |

### Security Best Practices

⚠️ **Important Security Notes:**

1. **Never commit `.env` files** with real credentials to version control
2. **Always use App Passwords** instead of your main account password
3. **Enable 2-Factor Authentication** on your email account
4. **Use TLS/SSL** for all email connections
5. **Store secrets securely** in production (Azure Key Vault, AWS Secrets Manager, etc.)
6. **Rotate passwords regularly** and revoke unused app passwords
7. **Limit permissions** to only what's necessary

## 🛡️ Authentication

The server uses `x-api-key` header-based authentication controlled by the `MODE` environment variable.

### How It Works

| `MODE` value | Behaviour |
|---|---|
| `Production` | Every request to `/mcp` must include a valid `x-api-key` header |
| `Development` (default) | Authentication is **bypassed** — all requests are allowed |

The `/api/health` endpoint is **always public** regardless of mode.

### Header Rules

- **Key matching is case-insensitive**: `x-api-key`, `X-Api-Key`, `X-API-KEY` are all accepted.
- **Value matching is exact**: the provided value must match `X-API-KEY` in `.env` exactly (case-sensitive).

### Configuration

```env
# .env
MODE=Production          # or Development
X-API-KEY=your-strong-secret-key
```

### Testing Authentication

```bash
# Without key (Production mode) → 401
curl https://<host>/mcp

# With correct key → 200 / normal MCP response
curl -H "x-api-key: your-strong-secret-key" https://<host>/mcp

# Health check — always works without a key
curl https://<host>/api/health
```

## 🛠️ MCP Tools (Functions)

This server exposes **3 powerful MCP tools** that AI assistants can use to interact with email services. Each tool is thoroughly documented below.

### 1. `send_email` - Send Emails via SMTP

Send emails with full support for attachments, CC/BCC, and HTML formatting.

**Function Signature:**
```python
async def send_email(
    recipient: str,              # Required: Primary recipient email
    subject: str,                # Required: Email subject/title
    body: str,                   # Required: Email body content
    attachments: List[str] = None,  # Optional: File paths to attach
    cc: List[str] = None,        # Optional: CC recipients
    bcc: List[str] = None,       # Optional: BCC recipients
    is_html: bool = False        # Optional: HTML formatting flag
) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `recipient` | `str` | ✅ Yes | Primary recipient email address (validated against RFC standards) |
| `subject` | `str` | ✅ Yes | Email subject line |
| `body` | `str` | ✅ Yes | Email body content (plain text or HTML) |
| `attachments` | `List[str]` | ❌ No | List of absolute file paths to attach (validates size and existence) |
| `cc` | `List[str]` | ❌ No | List of carbon copy recipient email addresses |
| `bcc` | `List[str]` | ❌ No | List of blind carbon copy recipient email addresses |
| `is_html` | `bool` | ❌ No | Set to `true` for HTML-formatted emails (default: `false` for plain text) |

**Returns:**
- Success: Formatted confirmation message with delivery details
- Error: Error message explaining what went wrong

**Example Usage in Claude:**
```
Please send an email to john@example.com with the subject "Project Update" 
and body "The quarterly report is attached." Attach the file /path/to/report.pdf
```

**Example Response:**
```
✅ Email sent successfully!
Recipient: john@example.com
Subject: Project Update
CC: None
BCC: None
Attachments: 1
```

**Features:**
- ✅ Automatic email address validation and normalization
- ✅ File attachment with size validation (default max: 25MB)
- ✅ Support for multiple CC and BCC recipients
- ✅ HTML email support with proper MIME encoding
- ✅ Smart SMTP connection handling (TLS/SSL)
- ✅ Detailed error messages for troubleshooting

---

### 2. `receive_emails_imap` - Retrieve Emails via IMAP

Retrieve and read emails from IMAP servers with advanced filtering options.

**Function Signature:**
```python
async def receive_emails_imap(
    mailbox: str = "INBOX",      # Mailbox/folder to read from
    limit: int = 10,             # Maximum emails to retrieve
    unread_only: bool = False    # Filter for unread only
) -> str
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `mailbox` | `str` | ❌ No | `"INBOX"` | Mailbox/folder name (INBOX, Sent, Drafts, etc.) |
| `limit` | `int` | ❌ No | `10` | Maximum number of emails to retrieve (1-100) |
| `unread_only` | `bool` | ❌ No | `false` | Only retrieve unread messages |

**Returns:**
- Formatted list of emails with metadata and body previews
- Each email includes: ID, From, To, Subject, Date, Body Preview, Attachments

**Example Usage in Claude:**
```
Please check my inbox and show me the last 5 unread emails
```

**Example Response:**
```
📬 Retrieved 5 email(s):

--- Email 1 ---
ID: 12345
From: alice@company.com
To: you@example.com
Subject: Meeting Tomorrow
Date: Mon, 10 Nov 2025 10:30:00 +0000
Attachments: 1
  - agenda.pdf (application/pdf)
Body Preview: Hi, just a reminder about our meeting tomorrow at 2 PM. 
I've attached the agenda for your review...
Body Length: 450 characters

--- Email 2 ---
[...]
```

**Features:**
- ✅ Support for all IMAP folders (INBOX, Sent, Drafts, custom folders)
- ✅ Unread-only filtering
- ✅ Attachment detection and metadata extraction
- ✅ Email body preview (first 200 characters)
- ✅ Full metadata parsing (sender, recipient, date, subject)
- ✅ Handles multiple encodings and international characters
- ✅ Secure SSL/TLS connection

**Supported Mailbox Names:**
- `INBOX` - Primary inbox
- `Sent` - Sent emails
- `Drafts` - Draft messages
- `Trash` - Deleted items
- `Spam` or `Junk` - Spam folder
- Custom folders created by the user

---

### 3. `receive_emails_pop3` - Retrieve Emails via POP3

Retrieve emails using the simpler POP3 protocol (note: POP3 is less feature-rich than IMAP).

**Function Signature:**
```python
def receive_emails_pop3(
    limit: int = 10              # Maximum emails to retrieve
) -> str
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | `int` | ❌ No | `10` | Maximum number of emails to retrieve |

**Returns:**
- Formatted list of emails (similar to IMAP output)

**Example Usage in Claude:**
```
Fetch my last 10 emails using POP3
```

**Features:**
- ✅ Simple email retrieval
- ✅ Attachment detection
- ✅ Email metadata parsing
- ✅ SSL/TLS support

**Note:** POP3 has limitations compared to IMAP:
- ❌ No folder support (only retrieves from main inbox)
- ❌ No unread filtering
- ❌ Less efficient for large mailboxes
- ✅ Use IMAP when possible for better features

---

### Tool Comparison

| Feature | `send_email` | `receive_emails_imap` | `receive_emails_pop3` |
|---------|--------------|------------------------|------------------------|
| **Primary Function** | Send emails | Receive emails | Receive emails |
| **Protocol** | SMTP | IMAP | POP3 |
| **Attachments Support** | ✅ Send | ✅ Detect | ✅ Detect |
| **HTML Support** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Folder Support** | N/A | ✅ Yes | ❌ No |
| **Unread Filtering** | N/A | ✅ Yes | ❌ No |
| **CC/BCC Support** | ✅ Yes | N/A | N/A |
| **Use Case** | Sending automated emails | Full email management | Simple email retrieval |

## 💡 Usage Examples

### Running the MCP Server

Start the server in HTTP mode (for MCP client connections):

```bash
python main.py
```

The server will:
1. Load configuration from `.env` file
2. Initialize SMTP, IMAP, and POP3 services
3. Start listening on `http://0.0.0.0:8888/mcp`
4. Expose MCP tools for AI assistants to use
5. Log all activities to console and log files

**Server Output:**
```
2025-11-10 15:57:03 - email-send-mcp - INFO - Starting Email Send/Receive MCP Server...
2025-11-10 15:57:03 - email-send-mcp - INFO - Configuration values set from environment variables.
2025-11-10 15:57:03 - email-send-mcp - INFO - EmailSender service initialized.
2025-11-10 15:57:03 - email-send-mcp - INFO - EmailReceiver service initialized.
2025-11-10 15:57:03 - email-send-mcp - INFO - Server running on http://0.0.0.0:8888/mcp
```

### Example 1: Send a Simple Text Email

**Natural Language Request (via Claude):**
```
Please send an email to colleague@company.com with the subject "Team Meeting" 
and tell them the meeting is scheduled for tomorrow at 2 PM.
```

**What Happens:**
- Claude uses the `send_email` tool
- Email address is validated
- Email is sent via configured SMTP server
- Confirmation is returned

**MCP Tool Call (Behind the Scenes):**
```python
send_email(
    recipient="colleague@company.com",
    subject="Team Meeting",
    body="The meeting is scheduled for tomorrow at 2 PM."
)
```

**Response:**
```
✅ Email sent successfully!
Recipient: colleague@company.com
Subject: Team Meeting
CC: None
BCC: None
Attachments: 0
```

---

### Example 2: Send HTML Email with Attachments

**Natural Language Request:**
```
Send an email to team@company.com with subject "Quarterly Report" 
and include the report.pdf file. Use HTML formatting with a professional header.
```

**MCP Tool Call:**
```python
send_email(
    recipient="team@company.com",
    subject="Quarterly Report",
    body="""
    <html>
        <body>
            <h1>Quarterly Report - Q4 2025</h1>
            <p>Dear Team,</p>
            <p>Please find attached the quarterly report for your review.</p>
            <p>Best regards,<br>Management</p>
        </body>
    </html>
    """,
    attachments=["/path/to/report.pdf"],
    is_html=True
)
```

---

### Example 3: Send Email with CC and BCC

**Natural Language Request:**
```
Email the project update to john@company.com, CC alice@company.com 
and bob@company.com, and BCC the manager@company.com
```

**MCP Tool Call:**
```python
send_email(
    recipient="john@company.com",
    subject="Project Update",
    body="The project is on track and will be completed by the deadline.",
    cc=["alice@company.com", "bob@company.com"],
    bcc=["manager@company.com"]
)
```

---

### Example 4: Check Unread Emails

**Natural Language Request:**
```
Show me my unread emails from the last week
```

**MCP Tool Call:**
```python
receive_emails_imap(
    mailbox="INBOX",
    limit=20,
    unread_only=True
)
```

**Response:**
```
📬 Retrieved 3 email(s):

--- Email 1 ---
ID: 12345
From: client@example.com
To: you@company.com
Subject: Question about Invoice
Date: Mon, 09 Nov 2025 14:30:00 +0000
Body Preview: Hi, I have a question about invoice #12345. Could you please clarify the charges for...
Body Length: 320 characters

[More emails...]
```

---

### Example 5: Check Specific Email Folder

**Natural Language Request:**
```
Check my Sent folder and show me the last 5 emails I sent
```

**MCP Tool Call:**
```python
receive_emails_imap(
    mailbox="Sent",
    limit=5,
    unread_only=False
)
```

---

### Example 6: Retrieve Emails with Attachments

**Natural Language Request:**
```
Show me emails with attachments from my inbox
```

**MCP Tool Call:**
```python
receive_emails_imap(
    mailbox="INBOX",
    limit=10,
    unread_only=False
)
```

**Response (showing attachment info):**
```
📬 Retrieved 2 email(s):

--- Email 1 ---
ID: 98765
From: partner@company.com
To: you@example.com
Subject: Contract Documents
Date: Tue, 08 Nov 2025 16:45:00 +0000
Attachments: 2
  - contract.pdf (application/pdf)
  - terms.docx (application/vnd.openxmlformats-officedocument.wordprocessingml.document)
Body Preview: Please review the attached contract documents...
```

---

### Example 7: Using POP3 for Simple Retrieval

**Natural Language Request:**
```
Get my last 5 emails using POP3
```

**MCP Tool Call:**
```python
receive_emails_pop3(limit=5)
```

---

### Programmatic Usage (Python)

If you want to use the email services directly in Python (without MCP):

```python
import asyncio
from src.services.email_sender import EmailSender
from src.services.email_receiver import EmailReceiver

async def main():
    # Send an email
    sender = EmailSender()
    result = await sender.send_email(
        recipient="user@example.com",
        subject="Test Email",
        body="This is a test message"
    )
    print(result)
    
    # Receive emails
    receiver = EmailReceiver()
    result = await receiver.receive_emails_imap(
        mailbox="INBOX",
        limit=5,
        unread_only=True
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

For more examples, see [examples.py](examples.py) in the repository.

## 🧪 Testing

This project includes comprehensive test coverage for validators, configuration, and core functionality.

### Running Tests

#### Run All Tests

```bash
# Basic test run
pytest tests/ -v

# Run with detailed output
pytest tests/ -vv

# Run tests with coverage report
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run tests in parallel (faster)
pytest tests/ -n auto
```

#### Run Specific Test Files

```bash
# Test email validators only
pytest tests/test_validators.py -v

# Test configuration management
pytest tests/test_config.py -v

# Test specific function
pytest tests/test_validators.py::TestEmailValidation::test_validate_valid_email -v
```

### Test Coverage

The project includes tests for:

✅ **Email Validation** (`tests/test_validators.py`)
- Valid email address validation
- Invalid email detection (missing @, invalid domain, etc.)
- Email normalization
- Batch email validation
- Email formatting with names

✅ **Configuration Management** (`tests/test_config.py`)
- Settings loading from environment
- Default value validation
- Port number validation
- Field type validation

✅ **SMTP Testing** (`test_smtp.py`, `test_smtp_variations.py`)
- SMTP connection testing
- Email sending variations
- Different provider configurations

✅ **Integration Tests** (`test_kakao_specific.py`)
- Provider-specific testing
- Real-world scenarios

### Example Test Output

```bash
$ pytest tests/ -v

============================= test session starts ==============================
tests/test_validators.py::TestEmailValidation::test_validate_valid_email PASSED
tests/test_validators.py::TestEmailValidation::test_validate_invalid_email_no_at PASSED
tests/test_validators.py::TestEmailValidation::test_validate_email_with_dots PASSED
tests/test_validators.py::TestEmailValidation::test_validate_email_with_plus PASSED
tests/test_validators.py::TestEmailValidation::test_validate_multiple_emails PASSED
tests/test_validators.py::TestEmailValidation::test_format_email_with_name PASSED
tests/test_config.py::TestSettings::test_default_values PASSED
tests/test_config.py::TestSettings::test_port_validation PASSED
============================== 8 passed in 0.45s ===============================
```

### Writing New Tests

When adding new features, include tests following this pattern:

```python
# tests/test_my_feature.py
import pytest
from src.services.my_service import MyService

class TestMyFeature:
    """Test suite for my new feature."""
    
    def test_basic_functionality(self):
        """Test basic feature operation."""
        service = MyService()
        result = service.do_something()
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_async_functionality(self):
        """Test async feature operation."""
        service = MyService()
        result = await service.do_something_async()
        assert result["status"] == "success"
```

### Integration Testing

For testing with real email servers:

1. **Create a test email account** (don't use your primary account)
2. **Set up test credentials** in `.env.test`:
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=test-account@gmail.com
   SMTP_PASSWORD=test-app-password
   ```
3. **Run integration tests** (not included in default test suite):
   ```bash
   pytest tests/integration/ -v --env-file=.env.test
   ```

### Manual Testing

You can test the MCP server manually:

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Test with curl** (health check):
   ```bash
   curl http://localhost:8888/api/health
   # Expected: {"status":"ok"}
   ```

3. **Test email sending** (using examples.py):
   ```bash
   python examples.py
   ```

### Testing Checklist

Before submitting code:

- [ ] All existing tests pass (`pytest tests/ -v`)
- [ ] New tests added for new features
- [ ] Code coverage maintained or improved
- [ ] Tests follow naming conventions (`test_*.py`, `Test*` classes)
- [ ] Async tests use `@pytest.mark.asyncio` decorator
- [ ] Integration tests are marked separately

### Continuous Integration

This project is ready for CI/CD integration. Example GitHub Actions workflow:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      - name: Run tests
        run: |
          pytest tests/ -v --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 🔬 Smoke Test Results

Live smoke test performed against the production Azure Container Apps deployment:

**Production URL:** `https://email-send-mcp.victoriousdune-f6c83ffa.koreacentral.azurecontainerapps.io`

### How to Run the Tests

**Test A — Unauthenticated request (expect 401 after deployment):**
```bash
curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
  https://email-send-mcp.victoriousdune-f6c83ffa.koreacentral.azurecontainerapps.io/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
# Expected: HTTP 401
```

**Test B — Wrong API key (expect 401):**
```bash
curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
  https://email-send-mcp.victoriousdune-f6c83ffa.koreacentral.azurecontainerapps.io/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "x-api-key: wrongkey" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
# Expected: HTTP 401
```

**Test C — Authenticated send_email (expect 200 + delivery):**
```bash
curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
  https://email-send-mcp.victoriousdune-f6c83ffa.koreacentral.azurecontainerapps.io/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "x-api-key: $X_API_KEY" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "send_email",
      "arguments": {
        "recipient": "kunhoko@kakao.com",
        "subject": "Smoke testing",
        "body": "Do you see this message! It is test message from Github Copilot"
      }
    }
  }'
# Expected: HTTP 200, email delivered
```

**Test D — Health check (always public, expect 200):**
```bash
curl -s -w "\nHTTP_STATUS:%{http_code}" \
  https://email-send-mcp.victoriousdune-f6c83ffa.koreacentral.azurecontainerapps.io/api/health
# Expected: HTTP 200 {"status":"ok"}
```

**Test E — Case-insensitive header key (expect 200):**
```bash
curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
  https://email-send-mcp.victoriousdune-f6c83ffa.koreacentral.azurecontainerapps.io/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "X-Api-Key: $X_API_KEY" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
# Expected: HTTP 200 (mixed-case key accepted)
```

### Results (commit [2fbb904](https://github.com/bedro96/email-send-mcp/commit/2fbb904))

| Test | Expected | HTTP | Status | Notes |
|---|---|---|---|---|
| D — `GET /api/health` (no key) | `200 {"status":"ok"}` | 200 | ✅ Pass | Always public |
| C — Authenticated `send_email` | 200 + email delivered | 200 | ✅ Pass | Email confirmed delivered to `kunhoko@kakao.com` |
| A — No `x-api-key` header | 401 | — | ⏳ Pending | Awaiting new image deployment |
| B — Wrong `x-api-key` value | 401 | — | ⏳ Pending | Awaiting new image deployment |
| E — Mixed-case `X-Api-Key` header | 200 | — | ⏳ Pending | Awaiting new image deployment |

> **Note:** Tests A, B, and E require the new Docker image (containing the auth middleware) to be deployed.
> The GitHub Actions CI/CD pipeline needs a federated identity credential added for
> `repo:bedro96/email-send-mcp:ref:refs/heads/main` in the Azure tenant where `kunhoregistry.azurecr.io`
> and `azureaiagent-rg` reside. Once deployed, all three tests are expected to pass.

### Confirmed email delivery

Email successfully delivered to `kunhoko@kakao.com`:
- **Subject:** Smoke testing
- **Body:** Do you see this message! It is test message from Github Copilot
- **Sent via:** SMTP (Kakao Mail)

## 🔌 Integration with MCP Clients

This server is compatible with any MCP client. Below are detailed instructions for popular clients.

### Claude Desktop Integration

[Claude Desktop](https://claude.ai/download) is Anthropic's official desktop app that supports MCP servers.

#### Setup Instructions

1. **Locate Claude Desktop Configuration File**

   The configuration file location varies by operating system:
   
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

2. **Add Email MCP Server to Configuration**

   **Option A: Using Environment Variables** (Recommended)
   
   ```json
   {
     "mcpServers": {
       "email": {
         "command": "python",
         "args": ["/absolute/path/to/email-send-mcp/main.py"],
         "env": {
           "SMTP_SERVER": "smtp.gmail.com",
           "SMTP_PORT": "587",
           "SMTP_USERNAME": "your-email@gmail.com",
           "SMTP_PASSWORD": "your-app-password",
           "IMAP_SERVER": "imap.gmail.com",
           "IMAP_PORT": "993",
           "IMAP_USERNAME": "your-email@gmail.com",
           "IMAP_PASSWORD": "your-app-password",
           "DEFAULT_FROM_EMAIL": "your-email@gmail.com"
         }
       }
     }
   }
   ```

   **Option B: Using .env File** (Simpler)
   
   ```json
   {
     "mcpServers": {
       "email": {
         "command": "python",
         "args": ["/absolute/path/to/email-send-mcp/main.py"],
         "cwd": "/absolute/path/to/email-send-mcp"
       }
     }
   }
   ```
   
   > This option assumes you have a `.env` file in the project directory.

3. **Restart Claude Desktop**

   After updating the configuration, fully quit and restart Claude Desktop.

4. **Verify Integration**

   In Claude Desktop, you should see email tools available. Try asking:
   ```
   Can you help me send an email?
   ```
   
   Claude should recognize it has access to the `send_email` tool.

#### Using Email Tools in Claude Desktop

Once configured, you can use natural language to interact with emails:

**Sending Emails:**
- "Send an email to john@example.com with subject 'Meeting' and tell him about tomorrow's meeting"
- "Email the team about the project update"
- "Send an email with the quarterly report attached"

**Receiving Emails:**
- "Check my inbox for unread emails"
- "Show me the last 10 emails I received"
- "What emails with attachments do I have?"
- "Check my Sent folder"

### Other MCP Clients

This server works with any MCP-compatible client:

#### Custom MCP Client

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["/path/to/email-send-mcp/main.py"],
        env={
            "SMTP_SERVER": "smtp.gmail.com",
            # ... other env vars
        }
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", tools)
            
            # Call send_email tool
            result = await session.call_tool(
                "send_email",
                arguments={
                    "recipient": "user@example.com",
                    "subject": "Test",
                    "body": "Hello from MCP client!"
                }
            )
            print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### HTTP MCP Client

The server also supports HTTP transport for web-based integrations:

```javascript
// JavaScript/Node.js example
const response = await fetch('http://localhost:8888/mcp', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    jsonrpc: '2.0',
    method: 'tools/call',
    params: {
      name: 'send_email',
      arguments: {
        recipient: 'user@example.com',
        subject: 'Test Email',
        body: 'Hello from HTTP client!'
      }
    },
    id: 1
  })
});

const result = await response.json();
console.log(result);
```

### Environment Variable Reference for MCP Clients

When configuring MCP clients, these environment variables are required:

**Minimum Required Variables:**
```json
{
  "SMTP_SERVER": "smtp.gmail.com",
  "SMTP_PORT": "587",
  "SMTP_USERNAME": "your-email@gmail.com",
  "SMTP_PASSWORD": "your-app-password",
  "DEFAULT_FROM_EMAIL": "your-email@gmail.com"
}
```

**For Email Receiving (Optional):**
```json
{
  "IMAP_SERVER": "imap.gmail.com",
  "IMAP_PORT": "993",
  "IMAP_USERNAME": "your-email@gmail.com",
  "IMAP_PASSWORD": "your-app-password"
}
```

### Troubleshooting MCP Integration

**Issue: Tools not appearing in Claude Desktop**
- Solution: Verify the config file path is correct
- Solution: Check that the Python path is absolute
- Solution: Restart Claude Desktop after configuration changes

**Issue: "Module not found" errors**
- Solution: Ensure dependencies are installed (`pip install -e .`)
- Solution: Use the full Python path (e.g., `/usr/local/bin/python3`)

**Issue: Authentication errors**
- Solution: Verify environment variables are set correctly
- Solution: Check that app passwords are used (not regular passwords)
- Solution: Verify SMTP/IMAP credentials are correct

**Issue: Server not starting**
- Solution: Check logs in the `logs/` directory
- Solution: Verify `.env` file exists and is readable
- Solution: Test server manually: `python main.py`

## 🐳 Docker Deployment

Docker provides a containerized way to run the Email MCP Server, ensuring consistency across different environments.

### Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (optional, for multi-container setups)

### Quick Start with Docker

#### Step 1: Build the Docker Image

```bash
docker build -t email-send-mcp .
```

This creates a Docker image with all dependencies installed.

#### Step 2: Run the Container

**Option A: Using Environment Variables**

```bash
docker run -d \
  --name email-mcp \
  -p 8888:8888 \
  -e SMTP_SERVER=smtp.gmail.com \
  -e SMTP_PORT=587 \
  -e SMTP_USERNAME=your-email@gmail.com \
  -e SMTP_PASSWORD=your-app-password \
  -e IMAP_SERVER=imap.gmail.com \
  -e IMAP_PORT=993 \
  -e IMAP_USERNAME=your-email@gmail.com \
  -e IMAP_PASSWORD=your-app-password \
  -e DEFAULT_FROM_EMAIL=your-email@gmail.com \
  email-send-mcp
```

**Option B: Using .env File (Recommended)**

```bash
docker run -d \
  --name email-mcp \
  -p 8888:8888 \
  --env-file .env \
  email-send-mcp
```

#### Step 3: Verify Container is Running

```bash
# Check container status
docker ps

# View logs
docker logs email-mcp

# Follow logs in real-time
docker logs -f email-mcp

# Test health endpoint
curl http://localhost:8888/api/health
```

### Docker Compose Setup

For easier management, use Docker Compose:

**`docker-compose.yml`:**
```yaml
version: '3.8'

services:
  email-mcp:
    build: .
    container_name: email-send-mcp
    ports:
      - "8888:8888"
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8888/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Start with Docker Compose:**
```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

### Docker Management Commands

```bash
# Stop the container
docker stop email-mcp

# Start the container
docker start email-mcp

# Restart the container
docker restart email-mcp

# Remove the container
docker rm email-mcp

# Remove the image
docker rmi email-send-mcp

# View container logs
docker logs email-mcp --tail 100

# Execute commands inside container
docker exec -it email-mcp /bin/bash

# Inspect container
docker inspect email-mcp
```

### Production Docker Best Practices

1. **Use Multi-Stage Builds** (already in Dockerfile)
2. **Run as Non-Root User** (already configured)
3. **Use Health Checks** (see Docker Compose example)
4. **Mount Logs as Volumes** for persistence
5. **Use Secrets Management** for production credentials
6. **Set Resource Limits:**

```bash
docker run -d \
  --name email-mcp \
  --memory="512m" \
  --cpus="0.5" \
  --env-file .env \
  email-send-mcp
```

## ☁️ Azure Container Apps Deployment

Deploy the Email MCP Server to Azure Container Apps for scalable, serverless hosting.

### Prerequisites

- Azure account with active subscription
- Azure CLI installed ([Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
- Docker installed

### Deployment Steps

#### Step 1: Login to Azure

```bash
az login
az account set --subscription <your-subscription-id>
```

#### Step 2: Create Resource Group

```bash
az group create \
  --name email-mcp-rg \
  --location eastus
```

#### Step 3: Create Azure Container Registry (ACR)

```bash
# Create ACR
az acr create \
  --resource-group email-mcp-rg \
  --name emailmcpacr \
  --sku Basic

# Login to ACR
az acr login --name emailmcpacr
```

#### Step 4: Build and Push Image to ACR

```bash
# Build and push in one command
az acr build \
  --registry emailmcpacr \
  --image email-send-mcp:latest \
  .

# Or build locally and push
docker build -t emailmcpacr.azurecr.io/email-send-mcp:latest .
docker push emailmcpacr.azurecr.io/email-send-mcp:latest
```

#### Step 5: Create Container Apps Environment

```bash
# Create environment
az containerapp env create \
  --name email-mcp-env \
  --resource-group email-mcp-rg \
  --location eastus
```

#### Step 6: Deploy Container App

```bash
az containerapp create \
  --name email-send-mcp \
  --resource-group email-mcp-rg \
  --environment email-mcp-env \
  --image emailmcpacr.azurecr.io/email-send-mcp:latest \
  --target-port 8888 \
  --ingress external \
  --registry-server emailmcpacr.azurecr.io \
  --cpu 0.5 \
  --memory 1Gi \
  --min-replicas 1 \
  --max-replicas 3 \
  --secrets \
    smtp-password=<your-app-password> \
    imap-password=<your-app-password> \
  --env-vars \
    SMTP_SERVER=smtp.gmail.com \
    SMTP_PORT=587 \
    SMTP_USERNAME=secretref:smtp-password \
    SMTP_PASSWORD=secretref:smtp-password \
    IMAP_SERVER=imap.gmail.com \
    IMAP_PORT=993 \
    IMAP_USERNAME=secretref:imap-password \
    IMAP_PASSWORD=secretref:imap-password \
    DEFAULT_FROM_EMAIL=your-email@gmail.com
```

#### Step 7: Get Application URL

```bash
az containerapp show \
  --name email-send-mcp \
  --resource-group email-mcp-rg \
  --query properties.configuration.ingress.fqdn
```

### Azure Container Apps Features

✅ **Auto-scaling:** Automatically scales based on HTTP traffic
✅ **Zero Downtime:** Seamless deployments with rolling updates
✅ **Built-in Load Balancing:** Distributes traffic across replicas
✅ **HTTPS by Default:** Automatic SSL/TLS certificates
✅ **Secrets Management:** Secure credential storage
✅ **Monitoring:** Integrated with Azure Monitor and Application Insights

### Update Deployment

```bash
# Update with new image
az containerapp update \
  --name email-send-mcp \
  --resource-group email-mcp-rg \
  --image emailmcpacr.azurecr.io/email-send-mcp:v2

# Update environment variables
az containerapp update \
  --name email-send-mcp \
  --resource-group email-mcp-rg \
  --set-env-vars LOG_LEVEL=DEBUG
```

### Monitoring and Logs

```bash
# View logs
az containerapp logs show \
  --name email-send-mcp \
  --resource-group email-mcp-rg \
  --follow

# View metrics
az monitor metrics list \
  --resource /subscriptions/<subscription-id>/resourceGroups/email-mcp-rg/providers/Microsoft.App/containerApps/email-send-mcp \
  --metric-names HttpRequestsCount
```

### Cost Optimization

- Use consumption plan (pay only for what you use)
- Set appropriate min/max replicas
- Configure scale rules based on metrics
- Use reserved capacity for predictable workloads

### Security Best Practices

1. **Use Azure Key Vault** for secrets
2. **Enable Managed Identity** for ACR authentication
3. **Use Private Endpoints** for internal-only access
4. **Configure CORS** policies
5. **Enable Azure AD authentication** for API access
6. **Use VNet integration** for enhanced security

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     MCP Client Layer                         │
│  (Claude Desktop, Custom Clients, Web Applications)         │
└────────────────────────┬────────────────────────────────────┘
                         │ MCP Protocol (HTTP/Stdio)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  FastMCP Server (main.py)                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              MCP Tools Router                       │   │
│  │  • send_email                                       │   │
│  │  • receive_emails_imap                              │   │
│  │  • receive_emails_pop3                              │   │
│  └─────────────────┬───────────────────────────────────┘   │
└────────────────────┼───────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐      ┌────────▼────────┐
│  EmailSender   │      │ EmailReceiver   │
│   (SMTP)       │      │  (IMAP/POP3)    │
└───────┬────────┘      └────────┬────────┘
        │                        │
        │ ┌──────────────────────┴────┐
        │ │   Validators & Utils      │
        │ │  • Email validation       │
        │ │  • Normalization          │
        │ │  • Formatting             │
        │ └──────────────────────────┬┘
        │                            │
        └────────────────┬───────────┘
                         │
        ┌────────────────▼───────────────┐
        │      Email Service Providers    │
        │  • Gmail (SMTP/IMAP)           │
        │  • Outlook (SMTP/IMAP)         │
        │  • Yahoo (SMTP/IMAP)           │
        │  • Custom SMTP/IMAP Servers    │
        └────────────────────────────────┘
```

### Project Structure

```
email-send-mcp/
├── main.py                      # Entry point - initializes and runs FastMCP server
├── src/
│   ├── __init__.py             # Package initialization
│   ├── config.py               # Configuration management with Pydantic Settings
│   ├── server.py               # FastMCP server setup and MCP tools definition
│   ├── services/
│   │   ├── __init__.py
│   │   ├── email_sender.py     # SMTP email sending service
│   │   └── email_receiver.py   # IMAP/POP3 email receiving service
│   └── utils/
│       ├── __init__.py
│       └── validators.py        # Email validation and formatting utilities
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_config.py          # Configuration tests
│   ├── test_validators.py      # Email validation tests
│   └── ...
├── logs/                        # Application logs (auto-created)
├── Dockerfile                   # Container configuration
├── docker-compose.yml          # Docker Compose setup (optional)
├── pyproject.toml              # Project dependencies and metadata
├── .env.example                # Example environment configuration
├── .env                        # Actual environment configuration (not in git)
├── README.md                   # This file
├── QUICKSTART.md              # Quick start guide
├── EMAIL_PROVIDERS.md         # Provider-specific configurations
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT License
└── examples.py                # Usage examples

```

### Component Details

#### 1. **main.py** - Application Entry Point
- Loads environment variables from `.env`
- Configures logging (console + file)
- Initializes FastMCP server
- Sets up SMTP, IMAP, POP3 services
- Starts HTTP server on port 8888

#### 2. **src/config.py** - Configuration Management
- Uses Pydantic Settings for type-safe configuration
- Loads settings from environment variables
- Validates port numbers and required fields
- Provides singleton pattern for settings access
- Supports multiple email providers

#### 3. **src/server.py** - MCP Server
- Defines MCP tools using `@mcp.tool()` decorator
- Integrates EmailSender and EmailReceiver services
- Handles tool parameter validation
- Formats responses for AI assistants
- Provides health check endpoint

#### 4. **src/services/email_sender.py** - SMTP Service
- Async SMTP client using `aiosmtplib`
- Supports TLS (port 587) and SSL (port 465)
- Validates all email addresses before sending
- Handles file attachments with size limits
- Supports CC, BCC, and HTML emails
- Smart MIME message construction

#### 5. **src/services/email_receiver.py** - IMAP/POP3 Service
- Async IMAP client using `aioimaplib`
- Sync POP3 client using `poplib`
- Folder/mailbox support (IMAP)
- Unread filtering (IMAP)
- Email parsing with proper encoding handling
- Attachment metadata extraction

#### 6. **src/utils/validators.py** - Email Utilities
- RFC-compliant email validation using `email-validator`
- Email normalization and formatting
- Batch email validation
- Display name formatting

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **MCP Framework** | FastMCP 2.0 | Model Context Protocol server implementation |
| **SMTP Client** | aiosmtplib | Async SMTP email sending |
| **IMAP Client** | aioimaplib | Async IMAP email receiving |
| **POP3 Client** | poplib (stdlib) | Sync POP3 email receiving |
| **Email Validation** | email-validator | RFC-compliant email address validation |
| **Settings Management** | Pydantic Settings | Type-safe configuration |
| **Environment Vars** | python-dotenv | .env file support |
| **HTTP Server** | FastAPI (via FastMCP) | HTTP transport for MCP |
| **Package Manager** | uv | Fast Python package management |
| **Testing** | pytest, pytest-asyncio | Test framework |
| **Code Quality** | black, isort, mypy, ruff | Code formatting and linting |

### Data Flow

#### Sending an Email

```
1. MCP Client → send_email tool call
2. FastMCP Server → validates parameters
3. EmailSender → validates recipient addresses
4. EmailSender → constructs MIME message
5. EmailSender → connects to SMTP server (TLS/SSL)
6. EmailSender → authenticates with credentials
7. EmailSender → sends email
8. EmailSender → returns success/error status
9. FastMCP Server → formats response
10. Response → returns to MCP Client
```

#### Receiving Emails

```
1. MCP Client → receive_emails_imap tool call
2. FastMCP Server → validates parameters
3. EmailReceiver → connects to IMAP server (SSL)
4. EmailReceiver → authenticates with credentials
5. EmailReceiver → selects mailbox/folder
6. EmailReceiver → searches for emails (filtered)
7. EmailReceiver → fetches email messages
8. EmailReceiver → parses email content
9. EmailReceiver → extracts metadata and attachments
10. EmailReceiver → returns formatted email list
11. FastMCP Server → formats response
12. Response → returns to MCP Client
```

### Logging and Monitoring

- **Log Location:** `logs/email-send-mcp_YYYYMMDD.log`
- **Log Rotation:** Daily (midnight)
- **Log Format:** `YYYY-MM-DD HH:MM:SS - logger_name - LEVEL - message`
- **Log Levels:** DEBUG, INFO, WARNING, ERROR
- **Console Output:** Enabled for development
- **Structured Logging:** JSON-compatible format for cloud environments

### Security Architecture

1. **Credential Storage:** Environment variables (never hardcoded)
2. **TLS/SSL:** Enforced for all email connections
3. **Input Validation:** All emails validated before processing
4. **Attachment Validation:** File size and existence checks
5. **Error Handling:** Sensitive data not exposed in errors
6. **Logging:** Passwords and secrets never logged

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue: "Authentication failed" or "Invalid credentials"

**Symptoms:**
- Error message: "535 Authentication failed" or similar
- Cannot connect to SMTP/IMAP server

**Solutions:**
1. **Use App Password instead of regular password**
   - For Gmail: [Create App Password](https://myaccount.google.com/apppasswords)
   - For Yahoo: Account Security → Generate app password
   - For Outlook: May need app-specific password or OAuth

2. **Verify credentials in `.env` file**
   ```bash
   # Check your .env file
   cat .env | grep -E "USERNAME|PASSWORD"
   ```

3. **Ensure 2FA is enabled** (required for app passwords)

4. **Check IMAP/SMTP access is enabled**
   - Gmail: Settings → See all settings → Forwarding and POP/IMAP → Enable IMAP
   - Outlook: Settings → Sync email → POP and IMAP

---

#### Issue: "Connection timeout" or "Connection refused"

**Symptoms:**
- Server doesn't respond
- Timeout errors after 60+ seconds

**Solutions:**
1. **Check firewall settings**
   ```bash
   # Test SMTP connectivity
   telnet smtp.gmail.com 587
   
   # Test IMAP connectivity
   telnet imap.gmail.com 993
   ```

2. **Verify server addresses and ports**
   - SMTP: Usually port 587 (TLS) or 465 (SSL)
   - IMAP: Usually port 993 (SSL)
   - POP3: Usually port 995 (SSL)

3. **Check if your ISP blocks SMTP/IMAP ports**
   - Some ISPs block port 25, 587
   - Try using VPN or alternative network

4. **Verify TLS/SSL settings match your provider**
   ```env
   # For port 587, use:
   SMTP_USE_TLS=true
   
   # For port 465, use:
   SMTP_USE_TLS=true  # aiosmtplib handles this automatically
   ```

---

#### Issue: Gmail "Less secure app access" error

**Symptoms:**
- "Please log in via your web browser" error
- Account access blocked

**Solutions:**
1. **Enable 2-Factor Authentication**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Turn on 2-Step Verification

2. **Generate and use App Password**
   - Visit [App Passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" and your device
   - Copy the 16-character password
   - Use in `.env` file (remove spaces)

3. **Never use "Less secure app access"** (deprecated and insecure)

---

#### Issue: "Module not found" errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'fastmcp'
ModuleNotFoundError: No module named 'dotenv'
```

**Solutions:**
```bash
# Reinstall dependencies
pip install -e .

# Or with uv
uv pip install -e .

# For development dependencies
pip install -e ".[dev]"

# Verify installation
python -c "import fastmcp; print('FastMCP OK')"
python -c "import dotenv; print('dotenv OK')"
```

---

#### Issue: "Permission denied" or "File not found" (attachments)

**Symptoms:**
- "Attachment file not found: /path/to/file.pdf"
- Permission errors when reading attachment files

**Solutions:**
1. **Use absolute paths for attachments**
   ```python
   # ✅ Good
   attachments=["/home/user/documents/report.pdf"]
   
   # ❌ Bad
   attachments=["report.pdf"]
   ```

2. **Verify file exists and is readable**
   ```bash
   ls -la /path/to/file.pdf
   # Should show readable permissions
   ```

3. **Check file size**
   ```bash
   # Default max is 25MB
   du -h /path/to/file.pdf
   ```

---

#### Issue: "Tools not appearing in Claude Desktop"

**Symptoms:**
- MCP server configured but tools don't show up
- Claude doesn't recognize email commands

**Solutions:**
1. **Verify config file path is correct**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Use absolute paths in configuration**
   ```json
   {
     "mcpServers": {
       "email": {
         "command": "python",
         "args": ["/absolute/path/to/email-send-mcp/main.py"]
       }
     }
   }
   ```

3. **Restart Claude Desktop completely**
   - Quit application (not just close window)
   - Restart from Applications/Start Menu

4. **Check server logs**
   ```bash
   # View logs to see if server started
   tail -f logs/email-send-mcp_*.log
   ```

---

#### Issue: Email sends but recipient doesn't receive it

**Symptoms:**
- "Email sent successfully" message
- But recipient never receives the email

**Solutions:**
1. **Check recipient's spam/junk folder**

2. **Verify sender email is correct**
   ```env
   DEFAULT_FROM_EMAIL=your-actual-email@gmail.com
   ```

3. **Check email provider's sent folder**

4. **Verify recipient email address is valid**
   ```python
   # Test email validation
   from src.utils.validators import validate_email_address
   is_valid, result = validate_email_address("recipient@example.com")
   print(f"Valid: {is_valid}, Result: {result}")
   ```

5. **Check for bounce-back emails** in your inbox

---

#### Issue: "Maximum attachment size exceeded"

**Symptoms:**
- Error about attachment size limit

**Solutions:**
1. **Check file size**
   ```bash
   du -h attachment.pdf
   ```

2. **Increase limit in `.env`**
   ```env
   MAX_ATTACHMENT_SIZE_MB=50  # Default is 25
   ```

3. **Compress large files** before attaching

4. **Use cloud storage links** for very large files

---

#### Issue: Cannot receive emails / Empty inbox

**Symptoms:**
- "No emails found" message
- IMAP returns empty results

**Solutions:**
1. **Verify IMAP credentials are correct**
   ```env
   IMAP_USERNAME=your-email@gmail.com
   IMAP_PASSWORD=your-app-password
   ```

2. **Check mailbox name is correct**
   ```python
   # Common mailbox names
   receive_emails_imap(mailbox="INBOX")      # ✅
   receive_emails_imap(mailbox="Sent")       # ✅
   receive_emails_imap(mailbox="inbox")      # ❌ Case-sensitive
   ```

3. **Verify emails exist in that folder**
   - Check via web interface
   - Try different folder: "Sent", "Drafts", etc.

4. **Increase limit parameter**
   ```python
   receive_emails_imap(limit=50)  # Default is 10
   ```

---

### Debugging Tips

#### Enable Debug Logging

Add to `.env`:
```env
LOG_LEVEL=DEBUG
DEBUG=true
```

Restart server and check logs:
```bash
tail -f logs/email-send-mcp_$(date +%Y%m%d).log
```

#### Test SMTP Connection Manually

```python
import asyncio
from src.services.email_sender import EmailSender

async def test():
    sender = EmailSender()
    result = await sender.send_email(
        recipient="test@example.com",
        subject="Test",
        body="Testing SMTP connection"
    )
    print(result)

asyncio.run(test())
```

#### Test IMAP Connection Manually

```python
import asyncio
from src.services.email_receiver import EmailReceiver

async def test():
    receiver = EmailReceiver()
    result = await receiver.receive_emails_imap(limit=1)
    print(result)

asyncio.run(test())
```

#### Check Environment Variables

```bash
# Verify .env is being loaded
python -c "from src.config import get_settings; s = get_settings(); print(f'SMTP: {s.SMTP_SERVER}:{s.SMTP_PORT}')"
```

---

### Getting Help

If you're still experiencing issues:

1. **Check existing issues:** [GitHub Issues](https://github.com/bedro96/email-send-mcp/issues)
2. **Search discussions:** [GitHub Discussions](https://github.com/bedro96/email-send-mcp/discussions)
3. **Open a new issue:**
   - Include error messages
   - Include relevant logs (remove sensitive data)
   - Include your configuration (without passwords)
   - Include steps to reproduce

## 👥 Contributing

We welcome contributions! Here's how you can help:

### Quick Start for Contributors

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/email-send-mcp.git
   cd email-send-mcp
   ```

2. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes and add tests**

5. **Run tests and linting**
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Format code
   black src/ tests/ main.py
   isort src/ tests/ main.py
   
   # Type checking
   mypy src/
   
   # Linting
   ruff check src/ tests/
   ```

6. **Commit and push**
   ```bash
   git commit -m "Add feature: description"
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**

### Contribution Guidelines

- **Code Style:** Follow PEP 8, use Black formatter
- **Tests:** Add tests for new features
- **Documentation:** Update README and docstrings
- **Commits:** Write clear commit messages
- **Issues:** Link PRs to related issues

For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📚 Additional Resources

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[EMAIL_PROVIDERS.md](EMAIL_PROVIDERS.md)** - Provider-specific configurations
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[examples.py](examples.py)** - Code examples
- **[FastMCP Documentation](https://github.com/jlowin/fastmcp)** - MCP framework docs
- **[Model Context Protocol](https://modelcontextprotocol.io/)** - MCP specification

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastMCP** - Excellent MCP framework by [@jlowin](https://github.com/jlowin)
- **Anthropic** - Model Context Protocol specification
- **Contributors** - Thank you to all contributors!

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/bedro96/email-send-mcp/issues)
- **Discussions:** [GitHub Discussions](https://github.com/bedro96/email-send-mcp/discussions)
- **Email:** For private inquiries only

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ for the MCP community

</div>
