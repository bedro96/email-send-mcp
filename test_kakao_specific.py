#!/usr/bin/env python3
"""Test Kakao Mail with specific SSL configurations."""

import asyncio
import aiosmtplib
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

async def test_kakao_smtp():
    """Test Kakao SMTP with various SSL contexts."""
    
    server = "smtp.kakao.com"
    port = 465
    username = "kunhoko"
    password = os.getenv("SMTP_PASSWORD", "")
    
    print("=" * 60)
    print("KAKAO MAIL SMTP TEST - Various SSL Configurations")
    print("=" * 60)
    print(f"Server: {server}:{port}")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)} ({len(password)} chars)")
    print()
    
    # Test 1: Default SSL context with use_tls=True
    print("Test 1: Default SSL with use_tls=True")
    print("-" * 60)
    try:
        smtp = aiosmtplib.SMTP(
            hostname=server,
            port=port,
            use_tls=True,
            timeout=10
        )
        await smtp.connect()
        print("✓ Connected")
        await smtp.login(username, password)
        print("✓ ✓ ✓ AUTHENTICATION SUCCESSFUL! ✓ ✓ ✓")
        await smtp.quit()
        print("\n>>> SUCCESS WITH DEFAULT SSL CONTEXT <<<\n")
        return
    except Exception as e:
        print(f"❌ Failed: {e}\n")
    
    # Test 2: Custom SSL context - less strict
    print("Test 2: Custom SSL context (less strict verification)")
    print("-" * 60)
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        smtp = aiosmtplib.SMTP(
            hostname=server,
            port=port,
            use_tls=True,
            tls_context=ssl_context,
            timeout=10
        )
        await smtp.connect()
        print("✓ Connected")
        await smtp.login(username, password)
        print("✓ ✓ ✓ AUTHENTICATION SUCCESSFUL! ✓ ✓ ✓")
        await smtp.quit()
        print("\n>>> SUCCESS WITH CUSTOM SSL CONTEXT <<<\n")
        return
    except Exception as e:
        print(f"❌ Failed: {e}\n")
    
    # Test 3: With validate_certs=False
    print("Test 3: Disable certificate validation")
    print("-" * 60)
    try:
        smtp = aiosmtplib.SMTP(
            hostname=server,
            port=port,
            use_tls=True,
            validate_certs=False,
            timeout=10
        )
        await smtp.connect()
        print("✓ Connected")
        await smtp.login(username, password)
        print("✓ ✓ ✓ AUTHENTICATION SUCCESSFUL! ✓ ✓ ✓")
        await smtp.quit()
        print("\n>>> SUCCESS WITH DISABLED CERT VALIDATION <<<\n")
        return
    except Exception as e:
        print(f"❌ Failed: {e}\n")
    
    # Test 4: Try with full email as username
    print("Test 4: Using full email address as username")
    print("-" * 60)
    try:
        smtp = aiosmtplib.SMTP(
            hostname=server,
            port=port,
            use_tls=True,
            validate_certs=False,
            timeout=10
        )
        await smtp.connect()
        print("✓ Connected")
        await smtp.login("kunhoko@kakao.com", password)
        print("✓ ✓ ✓ AUTHENTICATION SUCCESSFUL! ✓ ✓ ✓")
        await smtp.quit()
        print("\n>>> SUCCESS WITH FULL EMAIL ADDRESS <<<\n")
        return
    except Exception as e:
        print(f"❌ Failed: {e}\n")
    
    print("=" * 60)
    print("All SSL configurations failed")
    print("=" * 60)
    print("\nPossible issues:")
    print("1. SMTP access may not be enabled in Kakao Mail settings")
    print("2. Check if you need to enable 'External Mail Client' access")
    print("3. The app password might need to be regenerated from:")
    print("   Kakao Mail → Settings → Security → App Passwords")
    print("4. Your account might need additional verification")

if __name__ == "__main__":
    asyncio.run(test_kakao_smtp())
