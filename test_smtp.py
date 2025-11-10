#!/usr/bin/env python3
"""Test SMTP connection to diagnose authentication issues."""

import asyncio
import aiosmtplib
import os
from dotenv import load_dotenv

load_dotenv()

async def test_smtp_connection():
    """Test SMTP connection with detailed error reporting."""
    
    server = os.getenv("SMTP_SERVER", "smtp.kakao.com")
    port = int(os.getenv("SMTP_PORT", "465"))
    username = os.getenv("SMTP_USERNAME", "")
    password = os.getenv("SMTP_PASSWORD", "")
    
    print(f"Testing SMTP connection...")
    print(f"Server: {server}")
    print(f"Port: {port}")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)} ({len(password)} chars)")
    print("-" * 50)
    
    try:
        # Test with port 465 (SSL)
        if port == 465:
            print("Attempting SSL connection (port 465)...")
            smtp = aiosmtplib.SMTP(hostname=server, port=port, use_tls=True)
            await smtp.connect()
            print("✓ Connected successfully")
            
            print(f"Attempting login with username: {username}")
            await smtp.login(username, password)
            print("✓ Authentication successful!")
            
            await smtp.quit()
            print("✓ Connection closed")
            
        # Test with port 587 (STARTTLS)
        elif port == 587:
            print("Attempting STARTTLS connection (port 587)...")
            smtp = aiosmtplib.SMTP(hostname=server, port=port)
            await smtp.connect()
            print("✓ Connected successfully")
            
            await smtp.starttls()
            print("✓ STARTTLS successful")
            
            print(f"Attempting login with username: {username}")
            await smtp.login(username, password)
            print("✓ Authentication successful!")
            
            await smtp.quit()
            print("✓ Connection closed")
            
        print("\n" + "=" * 50)
        print("SUCCESS: SMTP configuration is working!")
        print("=" * 50)
        
    except aiosmtplib.SMTPAuthenticationError as e:
        print(f"\n❌ Authentication Error: {e}")
        print("\nPossible solutions:")
        print("1. Check if you need an app-specific password for Kakao Mail")
        print("2. Verify SMTP access is enabled in your Kakao account settings")
        print("3. Try using just the username part (without @kakao.com)")
        print("4. Try using the full email address (with @kakao.com)")
        print("5. Check if 2FA is enabled and requires app password")
        
    except aiosmtplib.SMTPConnectError as e:
        print(f"\n❌ Connection Error: {e}")
        print("\nPossible solutions:")
        print("1. Verify the SMTP server address is correct")
        print("2. Check if port is correct (465 for SSL, 587 for STARTTLS)")
        print("3. Check firewall settings")
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_smtp_connection())
