#!/usr/bin/env python3
"""byte-by-byte: Generate RSS 2.0 feed from archive files.

Reads all .md files in archive/ directory.
Groups by date, combining all sections from the same day into one RSS item.
Outputs docs/feed.xml.

Usage:
    python3 generate-rss.py
"""

import os
import sys
import re
import html
from datetime import datetime, timezone
from collections import defaultdict
from email.utils import format_datetime

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
REPO_DIR    = os.path.join(SCRIPT_DIR, '..')
ARCHIVE_DIR = os.path.join(REPO_DIR, 'archive')
DOCS_DIR    = os.path.join(REPO_DIR, 'docs')
OUTPUT_XML  = os.path.join(DOCS_DIR, 'feed.xml')

CHANNEL_TITLE       = 'byte-by-byte — Daily Tech Learning'
CHANNEL_LINK        = 'https://github.com/YushengAuggie/byte-by-byte'
CHANNEL_DESCRIPTION = ('Daily bilingual (Chinese/English) tech learning: '
                       'system design, algorithms, soft skills, frontend, and AI.')
CHANNEL_LANG        = 'en-us'

# Section display order and labels
SECTION_ORDER = ['system-design', 'algorithms', 'soft-skills', 'frontend', 'ai']
SECTION_LABELS = {
    'system-design': '🏗️ System Design',
    'algorithms':    '💻 Algorithms',
    'soft-skills':   '🗣️ Soft Skills',
    'frontend':      '🎨 Frontend',
    'ai':            '🤖 AI',
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def parse_filename(name: str):
    """
    Parse archive filename: YYYY-MM-DD-section-slug.md
    Returns (date_str, section_slug) or (None, None).
    """
    m = re.match(r'^(\d{4}-\d{2}-\d{2})-(.+)\.md$', name)
    if not m:
        return None, None
    return m.group(1), m.group(2)

def date_to_rfc822(date_str: str) -> str:
    """Convert YYYY-MM-DD to RFC 822 datetime string (noon UTC)."""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d').replace(
            hour=12, minute=0, second=0, tzinfo=timezone.utc
        )
        return format_datetime(dt)
    except ValueError:
        return format_datetime(datetime.now(timezone.utc))

def md_to_escaped_html(md_text: str) -> str:
    """
    Convert minimal markdown to safe HTML suitable for RSS CDATA.
    Handles: code blocks, inline code, bold, headers, paragraphs.
    Full HTML escape for security.
    """
    lines   = md_text.split('\n')
    output  = []
    in_code = False

    for line in lines:
        if line.strip().startswith('```'):
            if in_code:
                output.append('</code></pre>')
                in_code = False
            else:
                output.append('<pre><code>')
                in_code = True
            continue

        if in_code:
            output.append(html.escape(line))
            continue

        stripped = line.strip()

        if not stripped:
            output.append('')
            continue

        if stripped.startswith('# '):
            output.append(f'<h2>{html.escape(stripped[2:])}</h2>')
        elif stripped.startswith('## '):
            output.append(f'<h2>{html.escape(stripped[3:])}</h2>')
        elif stripped.startswith('### '):
            output.append(f'<h3>{html.escape(stripped[4:])}</h3>')
        elif stripped.startswith('---'):
            output.append('<hr/>')
        else:
            # Inline formatting
            text = html.escape(stripped)
            text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            output.append(f'<p>{text}</p>')

    if in_code:
        output.append('</code></pre>')

    return '\n'.join(output)

def xml_escape(text: str) -> str:
    """Escape text for plain XML elements (not CDATA)."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;'))

def build_item(date_str: str, sections: dict) -> str:
    """Build one <item> for a given date with all its sections."""
    pub_date = date_to_rfc822(date_str)
    title    = xml_escape(f'byte-by-byte — {date_str}')
    link     = xml_escape(f'{CHANNEL_LINK}/tree/main/archive')
    guid     = xml_escape(f'{CHANNEL_LINK}/archive/{date_str}')

    # Build description from sections in canonical order
    parts = []
    for slug in SECTION_ORDER:
        if slug in sections:
            label   = SECTION_LABELS.get(slug, slug)
            content = md_to_escaped_html(sections[slug])
            parts.append(f'<h1>{html.escape(label)}</h1>\n{content}')

    # Include any sections not in canonical order
    for slug, content in sections.items():
        if slug not in SECTION_ORDER:
            label = slug.replace('-', ' ').title()
            parts.append(f'<h1>{html.escape(label)}</h1>\n{md_to_escaped_html(content)}')

    description_content = '\n<hr/>\n'.join(parts)

    return f'''    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="false">{guid}</guid>
      <pubDate>{pub_date}</pubDate>
      <description><![CDATA[{description_content}]]></description>
    </item>'''

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    if not os.path.isdir(ARCHIVE_DIR):
        print(f'ERROR: archive/ directory not found at {ARCHIVE_DIR}')
        sys.exit(1)

    os.makedirs(DOCS_DIR, exist_ok=True)

    # Group files by date
    days: dict[str, dict[str, str]] = defaultdict(dict)

    md_files = sorted(
        f for f in os.listdir(ARCHIVE_DIR) if f.endswith('.md')
    )

    for fname in md_files:
        date_str, section = parse_filename(fname)
        if not date_str:
            print(f'  SKIP (unrecognised filename): {fname}')
            continue

        # Skip QA/meta files
        if section in ('qa-report',):
            continue

        fpath = os.path.join(ARCHIVE_DIR, fname)
        with open(fpath, encoding='utf-8') as f:
            days[date_str][section] = f.read()

    if not days:
        print('No archive files found. docs/feed.xml not written.')
        sys.exit(0)

    # Build items newest-first
    sorted_dates = sorted(days.keys(), reverse=True)
    items = [build_item(d, days[d]) for d in sorted_dates]

    now_rfc822 = format_datetime(datetime.now(timezone.utc))

    rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{xml_escape(CHANNEL_TITLE)}</title>
    <link>{xml_escape(CHANNEL_LINK)}</link>
    <description>{xml_escape(CHANNEL_DESCRIPTION)}</description>
    <language>{CHANNEL_LANG}</language>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
    <atom:link href="{xml_escape(CHANNEL_LINK)}/raw/main/docs/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
'''

    with open(OUTPUT_XML, 'w', encoding='utf-8') as f:
        f.write(rss)

    print(f'✅ RSS feed written to {OUTPUT_XML}')
    print(f'   Days included : {len(sorted_dates)}')
    print(f'   Date range    : {sorted_dates[-1]} → {sorted_dates[0]}')


if __name__ == '__main__':
    main()
