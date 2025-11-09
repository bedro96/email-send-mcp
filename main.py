#!/usr/bin/env python3
"""
Email Send/Receive MCP Server
Entry point for the MCP server application.
"""

import sys
from src.server import create_server
from src.config import get_settings

# Create the server instance at the global scope
server = create_server()


def main():
    """Main entry point for the MCP server."""
    try:
        settings = get_settings()
        
        # Verify SMTP credentials are configured
        if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
            print("Warning: SMTP credentials not configured. Email sending may not work.", file=sys.stderr)
        
        # Run the FastMCP server (handles asyncio internally)
        server.run()
            
    except Exception as e:
        print(f"Failed to start server: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
