# Quick Start Guide

Get started with the Email Send/Receive MCP Server in 5 minutes!

## 1. Install Dependencies

```bash
# Clone the repository
git clone https://github.com/bedro96/email-send-mcp.git
cd email-send-mcp

# Install using pip
pip install -e .
```

## 2. Configure Email Settings

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your email credentials
nano .env  # or use your preferred editor
```

**For Gmail:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password  # Get from: https://myaccount.google.com/apppasswords
SMTP_USE_TLS=true

IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=your-email@gmail.com
IMAP_PASSWORD=your-app-password
IMAP_USE_SSL=true

DEFAULT_FROM_EMAIL=your-email@gmail.com
```

See [EMAIL_PROVIDERS.md](EMAIL_PROVIDERS.md) for other providers.

## 3. Run the MCP Server

```bash
python main.py
```

The server will start and expose three MCP tools that can be used by MCP clients like Claude Desktop.

## 4. Use with Claude Desktop

Add to your Claude Desktop MCP configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "email": {
      "command": "python",
      "args": ["/path/to/email-send-mcp/main.py"],
      "env": {
        "SMTP_SERVER": "smtp.gmail.com",
        "SMTP_PORT": "587",
        "SMTP_USERNAME": "your-email@gmail.com",
        "SMTP_PASSWORD": "your-app-password",
        "IMAP_SERVER": "imap.gmail.com",
        "IMAP_PORT": "993",
        "IMAP_USERNAME": "your-email@gmail.com",
        "IMAP_PASSWORD": "your-app-password"
      }
    }
  }
}
```

Or reference your `.env` file (recommended):

```json
{
  "mcpServers": {
    "email": {
      "command": "python",
      "args": ["/path/to/email-send-mcp/main.py"],
      "cwd": "/path/to/email-send-mcp"
    }
  }
}
```

## 5. Test the Tools

In Claude Desktop, you can now use:

### Send an email:
```
Please send an email to test@example.com with the subject "Test Email" and body "This is a test message"
```

### Receive emails:
```
Please check my inbox and show me the last 5 unread emails
```

## Docker Quick Start

```bash
# Build the image
docker build -t email-send-mcp .

# Run with environment file
docker run --env-file .env email-send-mcp

# Or run with environment variables
docker run \
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

## Available Tools

### 1. `send_email`
Send an email with optional attachments, CC, and BCC.

**Example:**
- "Send an email to john@example.com with subject 'Meeting' and body 'See you at 3pm'"
- "Send an HTML email to team@company.com about the project update"
- "Email the report to boss@company.com with the file /path/to/report.pdf attached"

### 2. `receive_emails_imap`
Retrieve emails from your inbox via IMAP.

**Example:**
- "Show me my last 10 emails"
- "Get unread emails from my inbox"
- "Check my Sent folder for recent emails"

### 3. `receive_emails_pop3`
Retrieve emails via POP3 (simpler but less flexible than IMAP).

**Example:**
- "Fetch my last 5 emails using POP3"

## Troubleshooting

### "Authentication failed"
- Make sure you're using an **App Password**, not your regular password
- For Gmail: https://myaccount.google.com/apppasswords
- For Yahoo: Account Security → Generate app password

### "Connection refused" or "Timeout"
- Check your firewall settings
- Verify the server address and port
- Ensure your email provider allows IMAP/SMTP access

### "Module not found"
```bash
# Reinstall dependencies
pip install -e .
```

### Gmail not receiving emails
- Enable IMAP: Gmail Settings → See all settings → Forwarding and POP/IMAP → Enable IMAP

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [EMAIL_PROVIDERS.md](EMAIL_PROVIDERS.md) for provider-specific settings
- See [examples.py](examples.py) for code examples
- Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Support

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/bedro96/email-send-mcp/issues)
- 💬 [Discussions](https://github.com/bedro96/email-send-mcp/discussions)

Happy emailing! 📧
