#!/usr/bin/env python3
"""
generate-index.py — byte-by-byte Archive Index Generator

Scans the archive/ directory, generates:
  - docs/days/<date>.html   — one styled page per day (all 5 sections)
  - docs/archive.html       — index listing all available days

Usage:
    python3 scripts/generate-index.py
    python3 scripts/generate-index.py --archive-dir archive --docs-dir docs
"""

from __future__ import annotations

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, Optional, Tuple


# ── CSS shared across day pages ────────────────────────────────────────────────

DAY_CSS = """
:root {
  --bg: #0f0f13;
  --bg2: #16161d;
  --bg3: #1e1e2a;
  --border: #2e2e3e;
  --text: #e8e8f0;
  --text2: #a0a0b8;
  --accent: #7c5cfc;
  --accent2: #a78bfa;
  --accent3: #c4b5fd;
}

@media (prefers-color-scheme: light) {
  :root {
    --bg: #f8f7ff; --bg2: #ffffff; --bg3: #f0eeff;
    --border: #ddd8fa; --text: #1a1a2e; --text2: #555577;
    --accent: #6d46f5; --accent2: #7c5cfc; --accent3: #9b75ff;
  }
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.75;
}
a { color: var(--accent2); text-decoration: none; }
a:hover { color: var(--accent3); text-decoration: underline; }

nav {
  position: sticky; top: 0; z-index: 100;
  background: rgba(15,15,19,0.88); backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 0 24px; display: flex; align-items: center;
  justify-content: space-between; height: 56px;
}
@media (prefers-color-scheme: light) { nav { background: rgba(248,247,255,0.92); } }
.nav-brand { font-weight: 700; font-size: 1.05rem; color: var(--accent3); }
.nav-links { display: flex; gap: 20px; font-size: 0.88rem; }
.nav-links a { color: var(--text2); transition: color 0.2s; }
.nav-links a:hover { color: var(--text); text-decoration: none; }

.page-header {
  background: linear-gradient(135deg, #1a0a3e 0%, #0f0f20 60%);
  padding: 48px 24px 40px;
  border-bottom: 1px solid var(--border);
}
.page-header-inner { max-width: 800px; margin: 0 auto; }
.day-badge {
  display: inline-block;
  background: var(--accent); color: white;
  font-size: 0.75rem; font-weight: 700;
  padding: 3px 10px; border-radius: 20px; margin-bottom: 12px;
}
.page-header h1 {
  font-size: clamp(1.5rem, 3.5vw, 2.2rem);
  font-weight: 800; letter-spacing: -0.01em; margin-bottom: 8px;
}
.page-header-meta { color: var(--text2); font-size: 0.9rem; }
.page-header-meta span { margin-right: 16px; }

.nav-days {
  display: flex; gap: 8px; margin-top: 16px; flex-wrap: wrap;
}
.nav-day-btn {
  padding: 6px 14px; border-radius: 8px;
  background: var(--bg3); border: 1px solid var(--border);
  color: var(--text2); font-size: 0.82rem; cursor: pointer;
  transition: all 0.15s;
}
.nav-day-btn:hover, .nav-day-btn.active {
  background: var(--accent); border-color: var(--accent);
  color: white; text-decoration: none;
}

main { max-width: 800px; margin: 0 auto; padding: 40px 24px 80px; }

.section-block {
  margin-bottom: 32px;
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 14px; overflow: hidden;
}

.section-header {
  background: linear-gradient(135deg, #2a1a5e, #1a1a3e);
  padding: 16px 24px; display: flex; align-items: center; gap: 12px;
  cursor: pointer;
}
.section-header-icon { font-size: 1.5rem; }
.section-header-title { font-weight: 700; font-size: 1rem; color: #e8d5ff; }
.section-header-sub { font-size: 0.8rem; color: #a090d0; margin-top: 2px; }
.section-header-chevron {
  margin-left: auto; font-size: 0.9rem; color: var(--text2);
  transition: transform 0.2s;
}
.section-header.open .section-header-chevron { transform: rotate(180deg); }

.section-content {
  padding: 24px;
  display: none;
}
.section-content.open { display: block; }

/* Markdown rendering */
.section-content h1, .section-content h2, .section-content h3 {
  font-weight: 700; margin: 20px 0 10px;
  color: var(--accent3);
}
.section-content h1 { font-size: 1.2rem; }
.section-content h2 { font-size: 1.05rem; }
.section-content h3 { font-size: 0.95rem; }
.section-content p { margin-bottom: 12px; font-size: 0.93rem; }
.section-content ul, .section-content ol {
  margin: 8px 0 12px 20px; font-size: 0.93rem;
}
.section-content li { margin-bottom: 4px; }
.section-content blockquote {
  border-left: 3px solid var(--accent);
  padding: 8px 16px; margin: 12px 0;
  background: var(--bg3); border-radius: 0 8px 8px 0;
  color: var(--text2); font-style: italic;
}
.section-content strong { color: var(--text); }
.section-content em { color: var(--text2); }

pre {
  background: #09090f;
  border: 1px solid var(--border);
  border-radius: 10px; padding: 16px 20px;
  overflow-x: auto;
  font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
  font-size: 0.82rem; line-height: 1.65; margin: 12px 0;
  color: #e8e8f0;
}
@media (prefers-color-scheme: light) { pre { background: #1a1a2e; color: #e8e8f0; } }

code {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.85em;
  background: var(--bg3); padding: 1px 5px; border-radius: 4px;
  color: var(--accent3);
}
pre code { background: none; padding: 0; font-size: inherit; color: inherit; }

hr {
  border: none; border-top: 1px solid var(--border); margin: 20px 0;
}

.day-nav {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 32px; flex-wrap: wrap; gap: 12px;
}
.day-nav-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 16px; border-radius: 8px;
  background: var(--bg2); border: 1px solid var(--border);
  color: var(--text2); font-size: 0.88rem;
  transition: all 0.15s;
}
.day-nav-btn:hover {
  border-color: var(--accent); color: var(--text); text-decoration: none;
}

footer {
  border-top: 1px solid var(--border);
  padding: 28px 24px; text-align: center;
  color: var(--text2); font-size: 0.85rem;
}

@media (max-width: 600px) {
  .nav-links { display: none; }
  main { padding: 24px 16px 60px; }
}
"""

# ── Template helpers ────────────────────────────────────────────────────────────

SECTION_META = {
    "system-design": {"icon": "🏗️", "label": "System Design", "color": "#7c5cfc"},
    "algorithms":    {"icon": "💻", "label": "Algorithms",    "color": "#60a5fa"},
    "soft-skills":   {"icon": "🗣️", "label": "Soft Skills",   "color": "#34d399"},
    "frontend":      {"icon": "🎨", "label": "Frontend",      "color": "#f472b6"},
    "ai":            {"icon": "🤖", "label": "AI",            "color": "#fbbf24"},
}

SECTION_ORDER = ["system-design", "algorithms", "soft-skills", "frontend", "ai"]


def md_to_html(text: str) -> str:
    """Very lightweight Markdown → HTML converter for archive display."""
    lines = text.split("\n")
    html_lines = []
    in_pre = False
    pre_lang = ""
    pre_buf = []

    def flush_pre():
        code = "\n".join(pre_buf)
        pre_buf.clear()
        # Escape HTML inside code
        code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        lang_class = f' class="language-{pre_lang}"' if pre_lang else ""
        return f'<pre><code{lang_class}>{code}</code></pre>'

    i = 0
    while i < len(lines):
        line = lines[i]

        # Fenced code blocks
        if line.startswith("```"):
            if in_pre:
                in_pre = False
                html_lines.append(flush_pre())
            else:
                in_pre = True
                pre_lang = line[3:].strip()
                pre_buf.clear()
            i += 1
            continue

        if in_pre:
            pre_buf.append(line)
            i += 1
            continue

        # ATX headings
        m = re.match(r'^(#{1,3})\s+(.*)', line)
        if m:
            lvl = len(m.group(1))
            text_inner = inline_md(m.group(2))
            html_lines.append(f'<h{lvl}>{text_inner}</h{lvl}>')
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^[-*_]{3,}\s*$', line):
            html_lines.append('<hr/>')
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            content = inline_md(line[1:].strip())
            html_lines.append(f'<blockquote>{content}</blockquote>')
            i += 1
            continue

        # Unordered list
        if re.match(r'^[-*+]\s', line):
            items = []
            while i < len(lines) and re.match(r'^[-*+]\s', lines[i]):
                items.append(f'<li>{inline_md(lines[i][2:].strip())}</li>')
                i += 1
            html_lines.append('<ul>' + ''.join(items) + '</ul>')
            continue

        # Ordered list
        if re.match(r'^\d+\.\s', line):
            items = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i]):
                text_inner = re.sub(r'^\d+\.\s', '', lines[i])
                items.append(f'<li>{inline_md(text_inner)}</li>')
                i += 1
            html_lines.append('<ol>' + ''.join(items) + '</ol>')
            continue

        # Empty line
        if not line.strip():
            html_lines.append('')
            i += 1
            continue

        # Paragraph
        html_lines.append(f'<p>{inline_md(line)}</p>')
        i += 1

    if in_pre and pre_buf:
        html_lines.append(flush_pre())

    return '\n'.join(html_lines)


def inline_md(text: str) -> str:
    """Apply inline markdown: bold, italic, code, links."""
    # HTML escape first
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Bold+italic
    text = re.sub(r'\*{3}(.+?)\*{3}', r'<strong><em>\1</em></strong>', text)
    # Bold
    text = re.sub(r'\*{2}(.+?)\*{2}', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


# ── Parse archive files ─────────────────────────────────────────────────────────

def parse_archive_dir(archive_dir: Path) -> dict:
    """
    Returns:
        { "2026-03-14": { "system-design": <content str>, "algorithms": ..., ... } }
    """
    days = defaultdict(dict)
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})-(.+)\.md$')

    for f in sorted(archive_dir.glob("*.md")):
        if f.name.startswith("qa-report") or f.name.endswith("-qa-report.md"):
            continue
        m = pattern.match(f.name)
        if not m:
            continue
        date_str, section_key = m.group(1), m.group(2)
        # Normalize section key
        section_key = section_key.lower().replace("_", "-")
        if section_key in SECTION_META:
            days[date_str][section_key] = f.read_text(encoding="utf-8")

    return dict(days)


# ── Generate day HTML ────────────────────────────────────────────────────────────

def section_header_text(section_key: str, content: str) -> Tuple[str, str]:
    """Extract a subtitle from the first line of content."""
    meta = SECTION_META[section_key]
    first_lines = content.strip().split("\n")[:3]
    subtitle = ""
    for line in first_lines:
        line = line.strip().lstrip("#").strip()
        if line and not line.startswith("*Date:"):
            subtitle = re.sub(r'\*.*\*', '', line).strip()
            if len(subtitle) > 70:
                subtitle = subtitle[:67] + "..."
            break
    return meta["label"], subtitle


def generate_day_html(date_str: str, sections: dict, prev_date: Optional[str], next_date: Optional[str]) -> str:
    """Generate a full HTML page for one day."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        human_date = dt.strftime("%A, %B %-d, %Y")
    except Exception:
        human_date = date_str

    # figure out "Day N" from state.json or just use date order (we'll do date order)
    day_num = ""  # caller can inject this if desired

    # Build section blocks
    section_blocks = []
    for idx, key in enumerate(SECTION_ORDER):
        if key not in sections:
            continue
        meta = SECTION_META[key]
        label, subtitle = section_header_text(key, sections[key])
        content_html = md_to_html(sections[key])
        open_class = "open" if idx == 0 else ""  # first section open by default

        section_blocks.append(f"""
    <div class="section-block" id="section-{key}">
      <div class="section-header {open_class}" onclick="toggleSection(this)">
        <span class="section-header-icon">{meta['icon']}</span>
        <div>
          <div class="section-header-title">{meta['icon']} {label}</div>
          <div class="section-header-sub">{subtitle}</div>
        </div>
        <span class="section-header-chevron">▼</span>
      </div>
      <div class="section-content {open_class}">
        {content_html}
      </div>
    </div>""")

    prev_link = f'<a href="{prev_date}.html" class="day-nav-btn">← {prev_date}</a>' if prev_date else '<span></span>'
    next_link = f'<a href="{next_date}.html" class="day-nav-btn">{next_date} →</a>' if next_date else '<span></span>'

    sections_present = [SECTION_META[k] for k in SECTION_ORDER if k in sections]
    section_pills = " ".join(
        f'<a href="#section-{k}" class="nav-day-btn">{SECTION_META[k]["icon"]} {SECTION_META[k]["label"]}</a>'
        for k in SECTION_ORDER if k in sections
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>byte-by-byte — {date_str}</title>
  <meta name="description" content="byte-by-byte daily lessons for {human_date}: system design, algorithms, soft skills, frontend, AI." />
  <meta property="og:title" content="byte-by-byte — {human_date}" />
  <meta property="og:description" content="Daily bilingual tech lessons: system design, algorithms, soft skills, frontend, AI." />
  <meta property="og:url" content="https://yushengauggie.github.io/byte-by-byte/days/{date_str}.html" />
  <style>
{DAY_CSS}
  </style>
</head>
<body>

<nav>
  <a href="../index.html" class="nav-brand">🧠 byte-by-byte</a>
  <div class="nav-links">
    <a href="../archive.html">← Archive</a>
    {prev_link.replace('class="day-nav-btn"', 'style="color:var(--text2)"') if prev_date else ''}
    {next_link.replace('class="day-nav-btn"', 'style="color:var(--text2)"') if next_date else ''}
  </div>
</nav>

<div class="page-header">
  <div class="page-header-inner">
    <span class="day-badge">📅 {date_str}</span>
    <h1>{human_date}</h1>
    <div class="page-header-meta">
      <span>{len(sections_present)} sections</span>
      <span>~15 min read</span>
      <span>🌏 Bilingual 中/EN</span>
    </div>
    <div class="nav-days">
      {section_pills}
    </div>
  </div>
</div>

<main>
  <div class="day-nav">
    {prev_link}
    <a href="../archive.html" class="day-nav-btn">📂 All Days</a>
    {next_link}
  </div>

  {''.join(section_blocks)}
</main>

<footer>
  <a href="../archive.html">← Back to Archive</a> ·
  <a href="../index.html">byte-by-byte home</a> ·
  <a href="https://github.com/YushengAuggie/byte-by-byte">GitHub</a>
  <br/><br/>
  <span style="opacity:0.5; font-size:0.8rem;">
    A little bit every day. A lot over time. 🧠 · MIT License
  </span>
</footer>

<script>
function toggleSection(header) {{
  header.classList.toggle('open');
  const content = header.nextElementSibling;
  content.classList.toggle('open');
}}
</script>

</body>
</html>
"""


# ── Generate archive.html ────────────────────────────────────────────────────────

def generate_archive_html(days: dict) -> str:
    """Generate the main archive index page."""
    sorted_dates = sorted(days.keys(), reverse=True)
    rows = []

    for i, date_str in enumerate(sorted_dates):
        sections = days[date_str]
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            human_date = dt.strftime("%A, %B %-d, %Y")
        except Exception:
            human_date = date_str

        day_num = len(sorted_dates) - i  # newest = highest day
        section_badges = " ".join(
            f'<span class="section-badge">{SECTION_META[k]["icon"]} {SECTION_META[k]["label"]}</span>'
            for k in SECTION_ORDER if k in sections
        )
        rows.append(f"""      <div class="archive-day">
        <div>
          <div class="day-date">{date_str} · Day {len(sorted_dates) - i}</div>
          <div class="day-date-sub">{human_date}</div>
        </div>
        <div class="day-sections">
          {section_badges}
        </div>
        <a href="days/{date_str}.html" class="day-link">Read →</a>
      </div>""")

    total = len(sorted_dates)
    rows_html = "\n".join(rows) if rows else """      <div class="empty-state">
        <span class="emoji">📭</span>
        <p>No archive entries yet. Run <code>python3 scripts/generate-index.py</code> after generating some days.</p>
      </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Archive — byte-by-byte</title>
  <meta name="description" content="Browse all {total} past byte-by-byte daily lessons by date." />
  <meta property="og:title" content="Archive — byte-by-byte" />
  <meta property="og:description" content="Browse all past byte-by-byte daily bilingual tech lessons." />
  <meta property="og:url" content="https://yushengauggie.github.io/byte-by-byte/archive.html" />

  <style>
    :root {{
      --bg: #0f0f13; --bg2: #16161d; --bg3: #1e1e2a;
      --border: #2e2e3e; --text: #e8e8f0; --text2: #a0a0b8;
      --accent: #7c5cfc; --accent2: #a78bfa; --accent3: #c4b5fd;
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #f8f7ff; --bg2: #ffffff; --bg3: #f0eeff;
        --border: #ddd8fa; --text: #1a1a2e; --text2: #555577;
        --accent: #6d46f5; --accent2: #7c5cfc; --accent3: #9b75ff;
      }}
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      background: var(--bg); color: var(--text); line-height: 1.7;
    }}
    a {{ color: var(--accent2); text-decoration: none; }}
    a:hover {{ color: var(--accent3); text-decoration: underline; }}
    nav {{
      position: sticky; top: 0; z-index: 100;
      background: rgba(15,15,19,0.85); backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      padding: 0 24px; display: flex; align-items: center;
      justify-content: space-between; height: 56px;
    }}
    @media (prefers-color-scheme: light) {{ nav {{ background: rgba(248,247,255,0.9); }} }}
    .nav-brand {{ font-weight: 700; font-size: 1.1rem; color: var(--accent3); }}
    .nav-links {{ display: flex; gap: 20px; font-size: 0.9rem; }}
    .nav-links a {{ color: var(--text2); transition: color 0.2s; }}
    .nav-links a:hover {{ color: var(--text); text-decoration: none; }}
    .page-header {{
      background: linear-gradient(135deg, #1a0a3e 0%, #0f0f20 60%);
      padding: 56px 24px 48px; text-align: center;
      border-bottom: 1px solid var(--border);
    }}
    .page-header h1 {{
      font-size: clamp(1.8rem, 4vw, 2.8rem); font-weight: 800;
      background: linear-gradient(135deg, #c4b5fd, #7c5cfc);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      background-clip: text; margin-bottom: 8px;
    }}
    .page-header p {{ color: var(--text2); font-size: 1rem; }}
    .stat-pill {{
      display: inline-block; margin: 0 6px;
      background: var(--bg3); border: 1px solid var(--border);
      border-radius: 20px; padding: 4px 14px; font-size: 0.85rem; color: var(--accent3);
      margin-top: 12px;
    }}
    .container {{ max-width: 800px; margin: 0 auto; padding: 0 24px; }}
    main {{ padding: 48px 0 80px; }}
    .archive-intro {{
      background: var(--bg2); border: 1px solid var(--border);
      border-radius: 12px; padding: 20px 24px; margin-bottom: 32px;
      font-size: 0.9rem; color: var(--text2);
    }}
    .archive-intro strong {{ color: var(--text); }}
    .archive-list {{ display: flex; flex-direction: column; gap: 12px; }}
    .archive-day {{
      background: var(--bg2); border: 1px solid var(--border);
      border-radius: 12px; padding: 20px 24px;
      display: flex; align-items: center; justify-content: space-between;
      flex-wrap: wrap; gap: 12px;
      transition: border-color 0.2s, transform 0.15s;
    }}
    .archive-day:hover {{ border-color: var(--accent); transform: translateX(4px); }}
    .day-date {{ font-weight: 700; font-size: 0.95rem; }}
    .day-date-sub {{ font-size: 0.8rem; color: var(--text2); margin-top: 2px; }}
    .day-sections {{ display: flex; gap: 8px; flex-wrap: wrap; }}
    .section-badge {{
      font-size: 0.78rem; padding: 3px 10px;
      background: var(--bg3); border: 1px solid var(--border);
      border-radius: 20px; color: var(--text2);
    }}
    .day-link {{
      font-size: 0.85rem;
      background: linear-gradient(135deg, var(--accent), #5b3fcf);
      color: white; padding: 6px 14px; border-radius: 8px;
      white-space: nowrap; transition: opacity 0.2s;
    }}
    .day-link:hover {{ opacity: 0.85; text-decoration: none; color: white; }}
    .empty-state {{ text-align: center; padding: 64px 24px; color: var(--text2); }}
    .empty-state .emoji {{ font-size: 3rem; margin-bottom: 16px; display: block; }}
    code {{
      background: var(--bg3); padding: 1px 6px; border-radius: 4px;
      font-size: 0.85em; color: var(--accent3);
      font-family: 'SF Mono', monospace;
    }}
    footer {{
      border-top: 1px solid var(--border);
      padding: 32px 24px; text-align: center;
      color: var(--text2); font-size: 0.85rem;
    }}
    @media (max-width: 600px) {{ .nav-links {{ display: none; }} }}
  </style>
</head>
<body>

<nav>
  <a href="index.html" class="nav-brand">🧠 byte-by-byte</a>
  <div class="nav-links">
    <a href="index.html#what">What</a>
    <a href="index.html#subscribe">Subscribe</a>
    <a href="index.html#self-host">Self-Host</a>
    <a href="archive.html" style="color: var(--accent3)">Archive</a>
  </div>
</nav>

<div class="page-header">
  <h1>📂 Archive</h1>
  <p>Browse all past days — one lesson at a time, compounding over time</p>
  <div>
    <span class="stat-pill">📅 {total} day{"s" if total != 1 else ""} published</span>
    <span class="stat-pill">📝 {total * 5} total sections</span>
    <span class="stat-pill">🌏 Bilingual 中/EN</span>
  </div>
</div>

<main>
  <div class="container">
    <div class="archive-intro">
      <strong>How to use this archive:</strong> Each day has 5 sections — system design, algorithms,
      soft skills, frontend, and AI. Click any day to read the full lesson.
      Newest first.
    </div>

    <div class="archive-list">
{rows_html}
    </div>
  </div>
</main>

<footer>
  <a href="index.html">← Back to byte-by-byte</a> ·
  <a href="https://github.com/YushengAuggie/byte-by-byte">GitHub</a> ·
  MIT License
  <br/><br/>
  <span style="opacity:0.5; font-size:0.8rem;">
    Auto-generated by <code>scripts/generate-index.py</code> · A little bit every day. 🧠
  </span>
</footer>

</body>
</html>
"""


# ── Main ──────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate byte-by-byte archive index.")
    parser.add_argument("--archive-dir", default="archive", help="Path to archive/ directory")
    parser.add_argument("--docs-dir", default="docs", help="Path to docs/ directory")
    args = parser.parse_args()

    # Resolve paths relative to script's parent (project root)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    archive_dir = project_root / args.archive_dir
    docs_dir = project_root / args.docs_dir

    if not archive_dir.exists():
        print(f"❌ Archive directory not found: {archive_dir}", file=sys.stderr)
        sys.exit(1)

    docs_dir.mkdir(parents=True, exist_ok=True)
    days_dir = docs_dir / "days"
    days_dir.mkdir(parents=True, exist_ok=True)

    # Parse all archive files
    print(f"📂 Scanning {archive_dir}...")
    days = parse_archive_dir(archive_dir)

    if not days:
        print("⚠️  No archive files found. Run generate.sh first to create content.")
        # Still write a placeholder archive.html
        (docs_dir / "archive.html").write_text(generate_archive_html({}), encoding="utf-8")
        print(f"✅ Wrote docs/archive.html (empty state)")
        return

    sorted_dates = sorted(days.keys())
    print(f"📅 Found {len(sorted_dates)} day(s): {sorted_dates}")

    # Generate individual day pages
    for i, date_str in enumerate(sorted_dates):
        prev_date = sorted_dates[i - 1] if i > 0 else None
        next_date = sorted_dates[i + 1] if i < len(sorted_dates) - 1 else None
        html = generate_day_html(date_str, days[date_str], prev_date, next_date)
        out_path = days_dir / f"{date_str}.html"
        out_path.write_text(html, encoding="utf-8")
        sections_count = len(days[date_str])
        print(f"  ✅ {date_str}.html ({sections_count} sections)")

    # Generate archive index
    archive_html = generate_archive_html(days)
    archive_path = docs_dir / "archive.html"
    archive_path.write_text(archive_html, encoding="utf-8")
    print(f"✅ Wrote docs/archive.html ({len(sorted_dates)} entries)")
    print(f"\n🎉 Done! Generated {len(sorted_dates)} day pages + archive index.")
    print(f"   View locally: open {docs_dir / 'archive.html'}")


if __name__ == "__main__":
    main()
