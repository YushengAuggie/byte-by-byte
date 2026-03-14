#!/usr/bin/env python3
"""byte-by-byte: Send daily digest email as formatted HTML. No external dependencies."""

import smtplib
import socket
import sys
import os
import re
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

CSS = """
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.7; color: #1a1a1a; max-width: 680px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
  .container { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 28px 32px; text-align: center; }
  .header h1 { margin: 0; font-size: 24px; letter-spacing: -0.5px; }
  .header .tagline { opacity: 0.85; font-size: 14px; margin-top: 6px; }
  .header .day { font-size: 16px; opacity: 0.9; margin-top: 4px; }
  .section { padding: 24px 32px; border-bottom: 1px solid #eee; }
  .section:last-child { border-bottom: none; }
  h2 { font-size: 18px; margin-top: 0; color: #333; padding-bottom: 8px; border-bottom: 2px solid #667eea; display: inline-block; }
  h3 { font-size: 15px; color: #555; margin-top: 20px; }
  pre { background: #1e1e2e; color: #cdd6f4; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 13px; line-height: 1.5; white-space: pre-wrap; word-wrap: break-word; }
  code { font-family: 'SF Mono', 'Fira Code', Consolas, monospace; font-size: 13px; }
  p code { background: #f0f0f5; padding: 2px 6px; border-radius: 4px; color: #e53e3e; }
  blockquote { border-left: 3px solid #667eea; margin: 12px 0; padding: 8px 16px; background: #f8f7ff; border-radius: 0 6px 6px 0; color: #555; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0; }
  th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; font-size: 14px; }
  th { background: #f8f7ff; font-weight: 600; }
  hr { border: none; height: 1px; background: #eee; margin: 20px 0; }
  ul, ol { padding-left: 24px; }
  li { margin: 4px 0; }
  .toc { background: #f8f7ff; padding: 16px 24px; text-align: center; }
  .toc a { color: #667eea; text-decoration: none; font-weight: 500; margin: 0 10px; font-size: 14px; }
  .footer { text-align: center; padding: 20px 32px; color: #999; font-size: 13px; }
  .footer a { color: #667eea; text-decoration: none; }
</style>
"""

SECTION_META = [
    ('system-design', '🏗️', 'System Design', '系统设计'),
    ('algorithms',    '💻', 'Algorithms',    '算法'),
    ('soft-skills',   '🗣️', 'Soft Skills',   '软技能'),
    ('frontend',      '🎨', 'Frontend',      '前端'),
    ('ai',            '🤖', 'AI',            'AI'),
]

def load_config():
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

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def md_to_html(md_text):
    """Simple markdown to HTML — no external deps. Handles the patterns we use."""
    lines = md_text.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    in_table = False
    i = 0

    while i < len(lines):
        line = lines[i]

        # Fenced code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                lang = line.strip()[3:].strip()
                html_lines.append(f'<pre><code>')
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            html_lines.append(escape_html(line))
            i += 1
            continue

        # Close list if we're not in one
        if in_list and not line.strip().startswith(('- ', '* ', '• ')) and not re.match(r'^\d+\.', line.strip()):
            if line.strip():
                html_lines.append('</ul>')
                in_list = False

        # Close table
        if in_table and not line.strip().startswith('|'):
            html_lines.append('</table>')
            in_table = False

        stripped = line.strip()

        # Empty line
        if not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            i += 1
            continue

        # Headers
        if stripped.startswith('# '):
            html_lines.append(f'<h2>{inline_format(stripped[2:])}</h2>')
        elif stripped.startswith('## '):
            html_lines.append(f'<h2>{inline_format(stripped[3:])}</h2>')
        elif stripped.startswith('### '):
            html_lines.append(f'<h3>{inline_format(stripped[4:])}</h3>')

        # Horizontal rule
        elif stripped in ('---', '***', '___'):
            html_lines.append('<hr>')

        # Table
        elif stripped.startswith('|'):
            if not in_table:
                html_lines.append('<table>')
                in_table = True
            # Skip separator rows
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                i += 1
                continue
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            tag = 'th' if not any('<td>' in l for l in html_lines[-5:] if '<t' in l) and in_table and html_lines[-1] == '<table>' else 'td'
            row = ''.join(f'<{tag}>{inline_format(c)}</{tag}>' for c in cells)
            html_lines.append(f'<tr>{row}</tr>')

        # Blockquote
        elif stripped.startswith('>'):
            text = stripped[1:].strip()
            html_lines.append(f'<blockquote>{inline_format(text)}</blockquote>')

        # Unordered list
        elif stripped.startswith(('- ', '* ', '• ')):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            text = stripped[2:].strip()
            html_lines.append(f'<li>{inline_format(text)}</li>')

        # Ordered list
        elif re.match(r'^\d+\.\s', stripped):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            text = re.sub(r'^\d+\.\s', '', stripped)
            html_lines.append(f'<li>{inline_format(text)}</li>')

        # Regular paragraph
        else:
            html_lines.append(f'<p>{inline_format(stripped)}</p>')

        i += 1

    if in_code_block:
        html_lines.append('</code></pre>')
    if in_list:
        html_lines.append('</ul>')
    if in_table:
        html_lines.append('</table>')

    return '\n'.join(html_lines)

def inline_format(text):
    """Handle bold, italic, inline code, links."""
    # Inline code first (protect from other formatting)
    parts = re.split(r'(`[^`]+`)', text)
    result = []
    for part in parts:
        if part.startswith('`') and part.endswith('`'):
            result.append(f'<code>{escape_html(part[1:-1])}</code>')
        else:
            # Bold
            part = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', part)
            # Italic
            part = re.sub(r'\*(.+?)\*', r'<em>\1</em>', part)
            # Links
            part = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color:#667eea">\1</a>', part)
            result.append(part)
    return ''.join(result)

def get_day_number(config):
    try:
        repo_dir = config['BBB_REPO_DIR']
        with open(os.path.join(repo_dir, 'state.json')) as f:
            state = json.load(f)
        indices = [state.get('systemDesignIndex', 0), state.get('algorithmIndex', 0),
                   state.get('behavioralIndex', 0), state.get('frontendIndex', 0)]
        return max(indices) if any(indices) else 1
    except:
        return None

def load_subscribers(repo_dir, config):
    """Load subscribers from Google Sheet CSV (auto) + local subscribers.txt (manual fallback)."""
    subscribers = []

    # Source 1: Google Sheet CSV (automated via form)
    csv_url = config.get('SUBSCRIBERS_CSV_URL', '')
    if csv_url:
        try:
            import urllib.request
            import csv
            import io
            req = urllib.request.Request(csv_url, headers={'User-Agent': 'byte-by-byte/1.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                text = resp.read().decode('utf-8')
            reader = csv.reader(io.StringIO(text))
            header = next(reader, None)  # skip header row
            # Find the email column (look for column containing "email")
            email_col = 0
            if header:
                for i, col in enumerate(header):
                    if 'email' in col.lower():
                        email_col = i
                        break
            for row in reader:
                if len(row) > email_col:
                    email = row[email_col].strip()
                    if email and '@' in email:
                        subscribers.append(email)
            print('  📋 Loaded {} subscribers from Google Sheet'.format(len(subscribers)))
        except Exception as e:
            print('  ⚠️  Could not fetch subscriber sheet: {}'.format(e))

    # Source 2: Local subscribers.txt (manual additions)
    sub_file = os.path.join(repo_dir, 'subscribers.txt')
    if os.path.exists(sub_file):
        with open(sub_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '@' in line:
                    if line.lower() not in [s.lower() for s in subscribers]:
                        subscribers.append(line)

    return subscribers

def main():
    config = load_config()
    repo_dir = config['BBB_REPO_DIR']
    email_target = config['EMAIL_TARGET']
    today = date.today().isoformat()
    archive_dir = os.path.join(repo_dir, 'archive')
    smtp_user = config.get('SMTP_USER', email_target)
    smtp_pass = config.get('SMTP_APP_PASSWORD', '')

    # Build recipient list: owner + subscribers
    recipients = [email_target]
    subscribers = load_subscribers(repo_dir, config)
    for sub in subscribers:
        if sub.lower() not in [r.lower() for r in recipients]:
            recipients.append(sub)

    if not smtp_pass:
        print('SMTP_APP_PASSWORD not set in config.env')
        sys.exit(1)

    # Load sections
    sections_html = []
    plain_parts = []
    found = 0
    for filename, icon, name_en, name_cn in SECTION_META:
        path = os.path.join(archive_dir, '{}-{}.md'.format(today, filename))
        if os.path.exists(path):
            with open(path) as f:
                content = f.read()
            html = md_to_html(content)
            sections_html.append((icon, name_en, name_cn, filename, html))
            plain_parts.append(content)
            found += 1

    if found == 0:
        print('No archive files found for {}. Skipping email.'.format(today))
        sys.exit(0)

    day_num = get_day_number(config)
    day_label = ' Day {}'.format(day_num) if day_num else ''

    # TOC
    toc_links = ' &nbsp;|&nbsp; '.join(
        '<a href="#{}">{} {}</a>'.format(fid, icon, en)
        for icon, en, cn, fid, _ in sections_html
    )

    # Section blocks
    section_blocks = ''
    for icon, en, cn, fid, html in sections_html:
        section_blocks += '''
        <div class="section" id="{}">
            {}
        </div>
        '''.format(fid, html)

    full_html = '''<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{css}</head>
<body>
<div class="container">
    <div class="header">
        <h1>🧠 byte-by-byte{day_label}</h1>
        <div class="day">{today}</div>
        <div class="tagline">A little bit every day. A lot over time. / 每天一点，积少成多</div>
    </div>
    <div class="toc">{toc}</div>
    {sections}
    <div class="footer">
        <p>🧠 <a href="https://github.com/YushengAuggie/byte-by-byte">byte-by-byte</a> — open source daily learning</p>
    </div>
</div>
</body>
</html>'''.format(css=CSS, day_label=day_label, today=today, toc=toc_links, sections=section_blocks)

    # Build plain text fallback
    plain_text = 'byte-by-byte{} - {}\n\n'.format(day_label, today)
    plain_text += '\n\n---\n\n'.join(plain_parts)
    plain_text += '\n\n---\nA little bit every day. A lot over time.'
    plain_text += '\n\nUnsubscribe: reply with "unsubscribe"'

    # Add unsubscribe note to HTML footer
    full_html = full_html.replace(
        'open source daily learning</p>',
        'open source daily learning<br><small>Reply "unsubscribe" to stop receiving emails</small></p>'
    )

    # Send to all recipients
    socket.setdefaulttimeout(20)
    print('Sending HTML digest to {} recipients...'.format(len(recipients)))

    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(smtp_user, smtp_pass)

        for recipient in recipients:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = '🧠 byte-by-byte{} ({})'.format(day_label, today)
            msg['From'] = smtp_user
            msg['To'] = recipient
            msg.attach(MIMEText(plain_text, 'plain', 'utf-8'))
            msg.attach(MIMEText(full_html, 'html', 'utf-8'))
            s.send_message(msg)
            print('  ✉️  {}'.format(recipient))

    print('Email sent to {} recipients'.format(len(recipients)))

if __name__ == '__main__':
    main()
