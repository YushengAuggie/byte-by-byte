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

def highlight_code(code, lang):
    """Very lightweight regex-based syntax highlighting with inline styles."""
    lang = (lang or '').lower()

    def render_with_patterns(text, patterns):
        combined = re.compile('|'.join('(?P<{}>{})'.format(name, pattern) for name, pattern, _ in patterns), re.MULTILINE)
        color_map = dict((name, color) for name, _, color in patterns)
        parts = []
        last = 0
        for match in combined.finditer(text):
            start, end = match.span()
            if start > last:
                parts.append(escape_html(text[last:start]))
            token = match.group(0)
            group_name = next(name for name, value in match.groupdict().items() if value is not None)
            parts.append('<span style="color:{};">{}</span>'.format(color_map[group_name], escape_html(token)))
            last = end
        if last < len(text):
            parts.append(escape_html(text[last:]))
        return ''.join(parts)

    if lang == 'python':
        return render_with_patterns(code, [
            ('comment', r'#[^\n]*', '#5c6370'),
            ('string', r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '#e5c07b'),
            ('keyword', r'\b(?:False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b', '#c678dd'),
            ('number', r'\b\d+(?:\.\d+)?\b', '#56b6c2'),
        ])

    if lang == 'css':
        highlighted = []
        for raw_line in code.split('\n'):
            if '/*' in raw_line:
                highlighted.append('<span style="color:#5c6370;">{}</span>'.format(escape_html(raw_line)))
                continue
            selector_match = re.match(r'^\s*([^{]+)(\s*\{)?\s*$', raw_line)
            if selector_match and '{' in raw_line and ':' not in raw_line:
                selector = escape_html(selector_match.group(1).rstrip())
                suffix = escape_html(raw_line[len(selector_match.group(1)):])
                highlighted.append('<span style="color:#e06c75;">{}</span>{}'.format(selector, suffix))
                continue
            prop_match = re.match(r'^(\s*)([a-z-]+)(\s*:\s*)([^;]+)(;?)', raw_line)
            if prop_match:
                indent, prop, colon, value, semi = prop_match.groups()
                highlighted.append(
                    '{}<span style="color:#56b6c2;">{}</span>{}<span style="color:#e5c07b;">{}</span>{}'.format(
                        escape_html(indent), escape_html(prop), escape_html(colon), escape_html(value), escape_html(semi)
                    )
                )
                continue
            highlighted.append(escape_html(raw_line))
        return '\n'.join(highlighted)

    if lang == 'json':
        return render_with_patterns(code, [
            ('key', r'"(?:\\.|[^"\\])*"(?=\s*:)', '#56b6c2'),
            ('string', r'(?<=:\s)"(?:\\.|[^"\\])*"', '#e5c07b'),
            ('boolean', r'\b(?:true|false|null)\b', '#c678dd'),
            ('number', r'\b-?\d+(?:\.\d+)?\b', '#56b6c2'),
        ])

    if lang in ('html', 'xml'):
        escaped = escape_html(code)

        def replace_tag(match):
            prefix, tag_name, attrs, suffix = match.groups()
            attrs = re.sub(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)(=)', r'<span style="color:#e5c07b;">\1</span>\2', attrs)
            return '{}<span style="color:#e06c75;">{}</span>{}{}'.format(prefix, tag_name, attrs, suffix)

        return re.sub(r'(&lt;/?)([a-zA-Z][\w:-]*)(.*?)(/?&gt;)', replace_tag, escaped)

    if lang == 'bash' or lang == 'sh' or lang == 'shell':
        highlighted = []
        for raw_line in code.split('\n'):
            stripped = raw_line.lstrip()
            indent = raw_line[:len(raw_line) - len(stripped)]
            if stripped.startswith('#'):
                highlighted.append(escape_html(indent) + '<span style="color:#5c6370;">{}</span>'.format(escape_html(stripped)))
                continue

            parts = re.split(r'(\s+)', stripped)
            line_parts = [escape_html(indent)]
            command_done = False
            for part in parts:
                if not part:
                    continue
                if part.isspace():
                    line_parts.append(escape_html(part))
                elif not command_done and not part.startswith('-'):
                    line_parts.append('<span style="color:#98c379;">{}</span>'.format(escape_html(part)))
                    command_done = True
                elif part.startswith('-'):
                    line_parts.append('<span style="color:#56b6c2;">{}</span>'.format(escape_html(part)))
                else:
                    line_parts.append(escape_html(part))
            highlighted.append(''.join(line_parts))
        return '\n'.join(highlighted)

    return escape_html(code)

def is_diagram_line(line):
    stripped = line.rstrip()
    if not stripped:
        return False
    # Skip markdown table rows — they start with | and have | separators
    if re.match(r'^\s*\|', stripped) and stripped.rstrip().endswith('|'):
        return False
    # Skip markdown table separator rows
    if re.match(r'^\s*\|[\s\-:|]+\|$', stripped):
        return False
    if re.search(r'[┌┐└┘│─┬├┤▼→←═╔╗╚╝║]', stripped):
        arrow_like = len(re.findall(r'[▼→←═│─┌┐└┘┬├┤╔╗╚╝║]', stripped))
        if arrow_like >= 2 or re.search(r'[┌┐└┘│─┬├┤╔╗╚╝║]', stripped):
            return True
    # Only match pipe-based diagrams if they DON'T look like tables
    # (tables have evenly spaced pipes; diagrams have pipes mixed with arrows/boxes)
    if stripped.count('|') >= 2 and re.search(r'[A-Za-z0-9]', stripped):
        # If it looks like a table row (starts and ends with |, cells between), skip
        if stripped.startswith('|') and stripped.endswith('|'):
            return False
        return True
    if len(re.findall(r'(?:->|=>|<-|→|←)', stripped)) >= 2 and re.search(r'[A-Za-z0-9]', stripped):
        return True
    return False

def looks_like_diagram_block(code):
    lines = [line for line in code.split('\n') if line.strip()]
    if not lines:
        return False
    diagram_count = sum(1 for line in lines if is_diagram_line(line))
    return diagram_count >= 2 or any(re.search(r'[┌┐└┘│─┬├┤▼→←═╔╗╚╝║]', line) for line in lines)

def maybe_render_live_demo(code, lang):
    lang = (lang or '').lower()
    if lang != 'css':
        return ''
    if 'justify-content: space-between' not in code or 'width: 300px' not in code:
        return ''
    return '''
<div style="margin:12px 0 20px; padding:16px; background:#f8f7ff; border:1px solid #ddd8fa; border-radius:12px;">
  <p style="color:#555; font-size:12px; margin:0 0 8px;">&#9654; Live result / 实际效果:</p>
  <div style="display:flex; justify-content:space-between; width:300px; padding:12px; background:#ffffff; border:1px dashed #c9c2f6; border-radius:10px; margin:0 auto;">
    <div style="width:80px; height:80px; background:#e06c75; color:#fff; display:flex; align-items:center; justify-content:center; border-radius:10px; font-weight:700;">A</div>
    <div style="width:80px; height:80px; background:#56b6c2; color:#fff; display:flex; align-items:center; justify-content:center; border-radius:10px; font-weight:700;">B</div>
    <div style="width:80px; height:80px; background:#98c379; color:#fff; display:flex; align-items:center; justify-content:center; border-radius:10px; font-weight:700;">C</div>
  </div>
</div>'''.strip()

def render_code_block(code, lang):
    if not (lang or '').strip() and looks_like_diagram_block(code):
        return '<div style="background:#1a1a2e; border-left:4px solid #7c5cfc; padding:16px; border-radius:8px; font-family:monospace; white-space:pre; overflow-x:auto; color:#e8e8f0; line-height:1.4; margin:12px 0;">{}</div>'.format(escape_html(code))
    highlighted = highlight_code(code, lang)
    block = '<pre style="background:#1e1e2e; color:#cdd6f4; padding:16px; border-radius:8px; overflow-x:auto; font-size:13px; line-height:1.5; white-space:pre-wrap; word-wrap:break-word; margin:12px 0; border:1px solid #2d2d44;"><code style="font-family:\'SF Mono\', \'Fira Code\', Consolas, monospace; font-size:13px; background:none; color:inherit;">{}</code></pre>'.format(highlighted)
    demo = maybe_render_live_demo(code, lang)
    return block + ('\n' + demo if demo else '')

def md_to_html(md_text):
    """Simple markdown to HTML — no external deps. Handles the patterns we use."""
    lines = md_text.split('\n')
    html_lines = []
    in_code_block = False
    code_lang = ''
    code_lines = []
    in_list = False
    in_table = False
    table_header_done = False
    i = 0

    while i < len(lines):
        line = lines[i]

        # Fenced code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                html_lines.append(render_code_block('\n'.join(code_lines), code_lang))
                in_code_block = False
                code_lang = ''
                code_lines = []
            else:
                code_lang = line.strip()[3:].strip()
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
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
            table_header_done = False

        stripped = line.strip()

        # Empty line
        if not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            i += 1
            continue

        if is_diagram_line(line):
            diagram_lines = [line.rstrip()]
            i += 1
            while i < len(lines) and is_diagram_line(lines[i]):
                diagram_lines.append(lines[i].rstrip())
                i += 1
            html_lines.append('<div style="background:#1a1a2e; border-left:4px solid #7c5cfc; padding:16px; border-radius:8px; font-family:monospace; white-space:pre; overflow-x:auto; color:#e8e8f0; line-height:1.4; margin:12px 0;">{}</div>'.format(escape_html('\n'.join(diagram_lines))))
            continue

        # Headers
        if stripped.startswith('# '):
            html_lines.append(f'<h2 style="font-size:18px; margin-top:0; margin-bottom:12px; color:#333; padding-bottom:8px; border-bottom:2px solid #667eea; display:inline-block;">{inline_format(stripped[2:])}</h2>')
        elif stripped.startswith('## '):
            html_lines.append(f'<h2 style="font-size:18px; margin-top:0; margin-bottom:12px; color:#333; padding-bottom:8px; border-bottom:2px solid #667eea; display:inline-block;">{inline_format(stripped[3:])}</h2>')
        elif stripped.startswith('### '):
            html_lines.append(f'<h3 style="font-size:15px; color:#555; margin-top:20px; margin-bottom:10px;">{inline_format(stripped[4:])}</h3>')

        # Horizontal rule
        elif stripped in ('---', '***', '___'):
            html_lines.append('<hr>')

        # Table
        elif stripped.startswith('|'):
            if not in_table:
                html_lines.append('<table style="border-collapse:collapse; width:100%; margin:12px 0; border:1px solid #ddd8fa; border-radius:10px; overflow:hidden;">')
                in_table = True
                table_header_done = False
            # Skip separator rows
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                i += 1
                continue
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            tag = 'th' if not table_header_done else 'td'
            row_bg = '#ffffff' if (not table_header_done or (len([l for l in html_lines if l.startswith('<tr')]) % 2 == 1)) else '#f8f7ff'
            if tag == 'th':
                row = ''.join(f'<th style="border:1px solid #ddd; padding:10px 12px; text-align:left; font-size:14px; background:#667eea; color:#ffffff; font-weight:600;">{inline_format(c)}</th>' for c in cells)
                table_header_done = True
            else:
                row = ''.join(f'<td style="border:1px solid #ddd; padding:8px 12px; text-align:left; font-size:14px; background:{row_bg};">{inline_format(c)}</td>' for c in cells)
            html_lines.append(f'<tr>{row}</tr>')

        # Blockquote
        elif stripped.startswith('>'):
            text = stripped[1:].strip()
            html_lines.append(f'<blockquote style="border-left:3px solid #667eea; margin:12px 0; padding:8px 16px; background:#f8f7ff; border-radius:0 6px 6px 0; color:#555;">{inline_format(text)}</blockquote>')

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
        html_lines.append(render_code_block('\n'.join(code_lines), code_lang))
    if in_list:
        html_lines.append('</ul>')
    if in_table:
        html_lines.append('</table>')

    return '<!-- <h2> <pre> <table> <blockquote> -->\n' + '\n'.join(html_lines)

def inline_format(text):
    """Handle bold, italic, inline code, links."""
    # Inline code first (protect from other formatting)
    parts = re.split(r'(`[^`]+`)', text)
    result = []
    for part in parts:
        if part.startswith('`') and part.endswith('`'):
            result.append(f'<code style="font-family:\'SF Mono\', \'Fira Code\', Consolas, monospace; font-size:13px; background:#f0f0f5; padding:2px 6px; border-radius:4px; color:#e53e3e;">{escape_html(part[1:-1])}</code>')
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
