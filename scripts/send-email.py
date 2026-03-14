#!/usr/bin/env python3
"""byte-by-byte: Send daily digest email combining all 5 sections."""

import smtplib
import socket
import sys
import os
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

def load_config():
    """Load config from config.env"""
    config = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'config.env')
    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                config[key.strip()] = val.strip().strip('"')
    return config

def main():
    config = load_config()
    repo_dir = config['BBB_REPO_DIR']
    email_target = config['EMAIL_TARGET']
    today = date.today().isoformat()
    archive_dir = os.path.join(repo_dir, 'archive')

    # Gmail SMTP credentials from config
    smtp_user = config.get('SMTP_USER', email_target)
    smtp_pass = config.get('SMTP_APP_PASSWORD', '')

    if not smtp_pass:
        print('❌ SMTP_APP_PASSWORD not set in config.env')
        sys.exit(1)

    # Find today's archive files
    sections = [
        ('system-design', '🏗️ System Design'),
        ('algorithms', '💻 Algorithms'),
        ('soft-skills', '🗣️ Soft Skills'),
        ('frontend', '🎨 Frontend'),
        ('ai', '🤖 AI'),
    ]

    body_parts = []
    found = 0
    for filename, header in sections:
        path = os.path.join(archive_dir, f'{today}-{filename}.md')
        if os.path.exists(path):
            with open(path) as f:
                content = f.read()
            body_parts.append(content)
            found += 1
        else:
            body_parts.append(f'*{header}: No content generated today*\n')

    if found == 0:
        print(f'No archive files found for {today}. Skipping email.')
        sys.exit(0)

    # Build email
    full_body = '\n\n---\n\n'.join(body_parts)
    full_body = f'# 🧠 byte-by-byte — Daily Digest ({today})\n\n' + full_body
    full_body += '\n\n---\n*A little bit every day. A lot over time.*'

    msg = MIMEText(full_body, 'plain', 'utf-8')
    msg['Subject'] = f'🧠 byte-by-byte Day {today}'
    msg['From'] = smtp_user
    msg['To'] = email_target

    # Send
    socket.setdefaulttimeout(20)
    print(f'Sending digest to {email_target}...')
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(smtp_user, smtp_pass)
        s.send_message(msg)

    print(f'✅ Email sent to {email_target}')

if __name__ == '__main__':
    main()
