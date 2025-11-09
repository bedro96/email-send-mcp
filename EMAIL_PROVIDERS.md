# Email Provider Configuration Guide

This guide provides configuration settings for popular email providers.

## Gmail

### Prerequisites
1. Enable 2-factor authentication
2. Generate an App Password: https://myaccount.google.com/apppasswords

### Configuration
```env
# SMTP (Sending)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true

# IMAP (Receiving)
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=your-email@gmail.com
IMAP_PASSWORD=your-app-password
IMAP_USE_SSL=true

# POP3 (Alternative Receiving)
POP3_SERVER=pop.gmail.com
POP3_PORT=995
POP3_USERNAME=your-email@gmail.com
POP3_PASSWORD=your-app-password
POP3_USE_SSL=true
```

### Additional Steps
- Enable IMAP in Gmail settings: Settings → See all settings → Forwarding and POP/IMAP → Enable IMAP

## Outlook / Office 365

### Prerequisites
- Use your Microsoft account credentials or App Password

### Configuration
```env
# SMTP (Sending)
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
SMTP_USE_TLS=true

# IMAP (Receiving)
IMAP_SERVER=outlook.office365.com
IMAP_PORT=993
IMAP_USERNAME=your-email@outlook.com
IMAP_PASSWORD=your-password
IMAP_USE_SSL=true

# POP3 (Alternative Receiving)
POP3_SERVER=outlook.office365.com
POP3_PORT=995
POP3_USERNAME=your-email@outlook.com
POP3_PASSWORD=your-password
POP3_USE_SSL=true
```

## Yahoo Mail

### Prerequisites
- Generate an App Password: Account Security → Generate app password

### Configuration
```env
# SMTP (Sending)
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true

# IMAP (Receiving)
IMAP_SERVER=imap.mail.yahoo.com
IMAP_PORT=993
IMAP_USERNAME=your-email@yahoo.com
IMAP_PASSWORD=your-app-password
IMAP_USE_SSL=true

# POP3 (Alternative Receiving)
POP3_SERVER=pop.mail.yahoo.com
POP3_PORT=995
POP3_USERNAME=your-email@yahoo.com
POP3_PASSWORD=your-app-password
POP3_USE_SSL=true
```

## ProtonMail

### Prerequisites
- ProtonMail Bridge required for SMTP/IMAP access
- Download and install: https://proton.me/mail/bridge

### Configuration
```env
# SMTP (Sending) - via ProtonMail Bridge
SMTP_SERVER=127.0.0.1
SMTP_PORT=1025
SMTP_USERNAME=your-email@protonmail.com
SMTP_PASSWORD=bridge-password
SMTP_USE_TLS=false

# IMAP (Receiving) - via ProtonMail Bridge
IMAP_SERVER=127.0.0.1
IMAP_PORT=1143
IMAP_USERNAME=your-email@protonmail.com
IMAP_PASSWORD=bridge-password
IMAP_USE_SSL=false
```

## iCloud Mail

### Prerequisites
- Generate an App-Specific Password: appleid.apple.com → Security → App-Specific Passwords

### Configuration
```env
# SMTP (Sending)
SMTP_SERVER=smtp.mail.me.com
SMTP_PORT=587
SMTP_USERNAME=your-email@icloud.com
SMTP_PASSWORD=your-app-specific-password
SMTP_USE_TLS=true

# IMAP (Receiving)
IMAP_SERVER=imap.mail.me.com
IMAP_PORT=993
IMAP_USERNAME=your-email@icloud.com
IMAP_PASSWORD=your-app-specific-password
IMAP_USE_SSL=true
```

## Zoho Mail

### Configuration
```env
# SMTP (Sending)
SMTP_SERVER=smtp.zoho.com
SMTP_PORT=587
SMTP_USERNAME=your-email@zoho.com
SMTP_PASSWORD=your-password
SMTP_USE_TLS=true

# IMAP (Receiving)
IMAP_SERVER=imap.zoho.com
IMAP_PORT=993
IMAP_USERNAME=your-email@zoho.com
IMAP_PASSWORD=your-password
IMAP_USE_SSL=true

# POP3 (Alternative Receiving)
POP3_SERVER=pop.zoho.com
POP3_PORT=995
POP3_USERNAME=your-email@zoho.com
POP3_PASSWORD=your-password
POP3_USE_SSL=true
```

## Custom SMTP/IMAP Server

For custom email servers, contact your email administrator for the following information:

```env
# SMTP (Sending)
SMTP_SERVER=smtp.yourdomain.com
SMTP_PORT=587  # or 465 for SSL, 25 for non-TLS
SMTP_USERNAME=your-email@yourdomain.com
SMTP_PASSWORD=your-password
SMTP_USE_TLS=true  # or false for SSL-only connections

# IMAP (Receiving)
IMAP_SERVER=imap.yourdomain.com
IMAP_PORT=993  # or 143 for non-SSL
IMAP_USERNAME=your-email@yourdomain.com
IMAP_PASSWORD=your-password
IMAP_USE_SSL=true

# POP3 (Alternative Receiving)
POP3_SERVER=pop.yourdomain.com
POP3_PORT=995  # or 110 for non-SSL
POP3_USERNAME=your-email@yourdomain.com
POP3_PASSWORD=your-password
POP3_USE_SSL=true
```

## Common Port Numbers

### SMTP Ports
- **25**: Standard SMTP (usually blocked by ISPs)
- **587**: SMTP with STARTTLS (recommended)
- **465**: SMTP over SSL (legacy but still used)
- **2525**: Alternative SMTP port (some providers)

### IMAP Ports
- **143**: IMAP without SSL
- **993**: IMAP over SSL (recommended)

### POP3 Ports
- **110**: POP3 without SSL
- **995**: POP3 over SSL (recommended)

## Security Best Practices

1. **Always use SSL/TLS** when available
2. **Use App Passwords** instead of main account passwords
3. **Enable 2-Factor Authentication** on your email account
4. **Store credentials securely** in `.env` files (never commit to git)
5. **Rotate passwords regularly**
6. **Limit application permissions** to only what's needed
7. **Monitor account activity** for unauthorized access

## Troubleshooting

### "Authentication failed"
- Verify credentials are correct
- Check if you're using an App Password (required for Gmail, Yahoo, etc.)
- Ensure IMAP/SMTP access is enabled in your email settings

### "Connection timeout"
- Verify server addresses and ports
- Check firewall settings
- Ensure SSL/TLS settings match your provider

### "Too many login attempts"
- Your account may be temporarily locked
- Wait 15-30 minutes before trying again
- Contact your email provider's support

### "Less secure app access"
- This is outdated terminology
- Use App Passwords or OAuth2 instead
- Never reduce account security to make it work
