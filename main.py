import os
import sys
import dotenv
import logging
from src.server import create_server
from src.config import get_settings
# Load environment variables from .env file
dotenv.load_dotenv()
# Create the server instance at the global scope
server = create_server()

def set_values_from_env(settings):
    """Set configuration values from environment variables."""
    env_vars = {
        "SMTP_SERVER": os.getenv("SMTP_SERVER"),
        "SMTP_PORT": os.getenv("SMTP_PORT"),
        "SMTP_USERNAME": os.getenv("SMTP_USERNAME"),
        "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD"),
        "IMAP_SERVER": os.getenv("IMAP_SERVER"),
        "IMAP_PORT": os.getenv("IMAP_PORT"),
        "IMAP_USERNAME": os.getenv("IMAP_USERNAME"),
        "IMAP_PASSWORD": os.getenv("IMAP_PASSWORD"),
        "POP3_SERVER": os.getenv("POP3_SERVER"),
        "POP3_PORT": os.getenv("POP3_PORT"),
        "POP3_USERNAME": os.getenv("POP3_USERNAME"),
        "POP3_PASSWORD": os.getenv("POP3_PASSWORD"),
        "DEFAULT_FROM_EMAIL": os.getenv("DEFAULT_FROM_EMAIL"),
    }

    for key, value in env_vars.items():
        if value is not None:
            field_type = type(getattr(settings, key))
            try:
                if field_type is bool:
                    casted_value = value.lower() in ("true", "1", "yes")
                else:
                    casted_value = field_type(value)
                setattr(settings, key, casted_value)
            except ValueError as e:
                print(f"Invalid value for {key}: {value}. Error: {str(e)}", file=sys.stderr)
    

def main():
    """Main entry point for the MCP server."""
    try:
        settings = get_settings()
        
        # Verify SMTP credentials are configured
        if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
            print("Warning: SMTP credentials not configured. Email sending may not work.", file=sys.stderr)
        
        # Run the FastMCP server (handles asyncio internally)
        server.run(transport="http", host="0.0.0.0", port=8888, path="/mcp")
            
    except Exception as e:
        print(f"Failed to start server: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
