#!/usr/bin/env python3
"""Test different SMTP configurations for Kakao Mail."""

import asyncio
import aiosmtplib
import os
from dotenv import load_dotenv

load_dotenv()

async def test_configuration(server, port, username, password, use_tls=True, start_tls=False):
    """Test a specific SMTP configuration."""
    print(f"\nTesting: {server}:{port}")
    print(f"Username: {username}")
    print(f"SSL/TLS: use_tls={use_tls}, start_tls={start_tls}")
    print("-" * 40)
    
    try:
        if port == 465 and use_tls:
            # Direct SSL connection
            smtp = aiosmtplib.SMTP(hostname=server, port=port, use_tls=True)
            await smtp.connect()
            print("✓ Connected (SSL)")
            await smtp.login(username, password)
            print("✓ ✓ ✓ AUTHENTICATION SUCCESSFUL! ✓ ✓ ✓")
            await smtp.quit()
            return True
            
        elif start_tls:
            # STARTTLS connection
            smtp = aiosmtplib.SMTP(hostname=server, port=port)
            await smtp.connect()
            print("✓ Connected")
            await smtp.starttls()
            print("✓ STARTTLS")
            await smtp.login(username, password)
            print("✓ ✓ ✓ AUTHENTICATION SUCCESSFUL! ✓ ✓ ✓")
            await smtp.quit()
            return True
            
        else:
            # Plain connection
            smtp = aiosmtplib.SMTP(hostname=server, port=port)
            await smtp.connect()
            print("✓ Connected")
            await smtp.login(username, password)
            print("✓ ✓ ✓ AUTHENTICATION SUCCESSFUL! ✓ ✓ ✓")
            await smtp.quit()
            return True
            
    except aiosmtplib.SMTPAuthenticationError as e:
        print(f"❌ Auth failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return False

async def main():
    """Test various configurations."""
    password = os.getenv("SMTP_PASSWORD", "")
    email = os.getenv("DEFAULT_FROM_EMAIL", "kunhoko@kakao.com")
    username_part = email.split("@")[0]
    
    print("=" * 50)
    print("KAKAO MAIL SMTP CONFIGURATION TEST")
    print("=" * 50)
    
    configurations = [
        # Standard Kakao configurations
        ("smtp.kakao.com", 465, username_part, password, True, False),
        ("smtp.kakao.com", 465, email, password, True, False),
        ("smtp.kakao.com", 587, username_part, password, False, True),
        ("smtp.kakao.com", 587, email, password, False, True),
        
        # Alternative Kakao configurations
        ("smtp.daum.net", 465, username_part, password, True, False),
        ("smtp.daum.net", 465, email, password, True, False),
        ("smtp.daum.net", 587, username_part, password, False, True),
        ("smtp.daum.net", 587, email, password, False, True),
    ]
    
    for config in configurations:
        result = await test_configuration(*config)
        if result:
            server, port, username, _, use_tls, start_tls = config
            print("\n" + "=" * 50)
            print("SUCCESS! Use this configuration:")
            print("=" * 50)
            print(f"SMTP_SERVER={server}")
            print(f"SMTP_PORT={port}")
            print(f"SMTP_USERNAME={username}")
            if port == 465:
                print("SMTP_USE_TLS=true")
            else:
                print("SMTP_USE_TLS=true (for STARTTLS)")
            return
    
    print("\n" + "=" * 50)
    print("All configurations failed.")
    print("=" * 50)
    print("\nPlease check:")
    print("1. SMTP access is enabled in Kakao Mail settings")
    print("2. The app password is valid and for mail/SMTP access")
    print("3. Your account type supports SMTP (some free accounts may not)")
    print("4. Try generating a new app password from Kakao account settings")

if __name__ == "__main__":
    asyncio.run(main())
