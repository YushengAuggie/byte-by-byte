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

.section-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 14px 0;
  border: 1px solid var(--border);
  overflow: hidden;
  border-radius: 12px;
}
.section-content th, .section-content td {
  border: 1px solid var(--border);
  padding: 10px 12px;
  text-align: left;
  font-size: 0.9rem;
}
.section-content th {
  background: #667eea;
  color: white;
  font-weight: 700;
}
.section-content tbody tr:nth-child(even) {
  background: rgba(124, 92, 252, 0.08);
}

.code-block {
  position: relative;
  margin: 14px 0;
}

.copy-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.08);
  color: #d6d6ee;
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 0.72rem;
  cursor: pointer;
}
.copy-btn:hover {
  background: rgba(255,255,255,0.14);
}

.code-block pre {
  background: #09090f;
  border: 1px solid var(--border);
  border-radius: 10px; padding: 16px 20px;
  overflow-x: auto;
  font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
  font-size: 0.82rem; line-height: 1.65; margin: 12px 0;
  color: #e8e8f0;
}
@media (prefers-color-scheme: light) { .code-block pre { background: #1a1a2e; color: #e8e8f0; } }

code {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.85em;
  background: var(--bg3); padding: 1px 5px; border-radius: 4px;
  color: var(--accent3);
}
.code-block pre code { background: none; padding: 0; font-size: inherit; color: inherit; }

.diagram-block {
  background: #1a1a2e;
  border-left: 4px solid var(--accent);
  padding: 16px;
  border-radius: 8px;
  font-family: 'SF Mono', 'Fira Code', monospace;
  white-space: pre;
  overflow-x: auto;
  color: #e8e8f0;
  line-height: 1.4;
  margin: 12px 0;
}

.live-demo {
  margin: 12px 0 20px;
  padding: 16px;
  background: #f8f7ff;
  border: 1px solid #ddd8fa;
  border-radius: 12px;
  color: #1a1a2e;
}
.live-demo-label {
  color: #555;
  font-size: 12px;
  margin: 0 0 8px;
}
.live-demo-canvas {
  overflow-x: auto;
}

.trace-card {
  margin: 18px 0 8px;
  padding: 18px;
  border: 1px solid var(--border);
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(124,92,252,0.14), rgba(96,165,250,0.08));
}
.trace-card h3 {
  margin: 0 0 12px;
}
.trace-steps {
  display: grid;
  gap: 10px;
}
.trace-step {
  display: grid;
  grid-template-columns: 92px 1fr;
  gap: 12px;
  align-items: start;
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(10, 10, 18, 0.34);
  border: 1px solid rgba(255,255,255,0.06);
}
.trace-step-label {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--accent3);
}
.trace-step-body {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.8rem;
  color: #dfe5ff;
}

.flow-chart {
  display: grid;
  gap: 14px;
  margin: 16px 0;
}
.flow-node {
  position: relative;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 14px;
  align-items: center;
  padding: 16px 18px;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.08);
  background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
  box-shadow: 0 18px 36px rgba(0,0,0,0.16);
}
.flow-node-browser { background: linear-gradient(135deg, rgba(59,130,246,0.24), rgba(37,99,235,0.08)); }
.flow-node-cache { background: linear-gradient(135deg, rgba(34,197,94,0.24), rgba(22,163,74,0.08)); }
.flow-node-resolver { background: linear-gradient(135deg, rgba(249,115,22,0.24), rgba(234,88,12,0.08)); }
.flow-node-root { background: linear-gradient(135deg, rgba(239,68,68,0.22), rgba(185,28,28,0.08)); }
.flow-node-tld { background: linear-gradient(135deg, rgba(168,85,247,0.24), rgba(126,34,206,0.08)); }
.flow-node-authoritative { background: linear-gradient(135deg, rgba(20,184,166,0.24), rgba(13,148,136,0.08)); }
.flow-node-return { background: linear-gradient(135deg, rgba(124,92,252,0.24), rgba(96,165,250,0.08)); }
.flow-badge {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: #fff;
  background: rgba(10,10,18,0.48);
  border: 1px solid rgba(255,255,255,0.2);
}
.flow-copy {
  min-width: 0;
}
.flow-title {
  font-weight: 700;
  font-size: 1rem;
  color: #f5f3ff;
}
.flow-subtitle {
  color: rgba(232,232,240,0.78);
  font-size: 0.9rem;
  margin-top: 4px;
}
.flow-arrow {
  width: 2px;
  height: 28px;
  margin: -4px auto -2px;
  background: linear-gradient(180deg, rgba(124,92,252,0.2), rgba(124,92,252,0.9));
  position: relative;
}
.flow-arrow::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: -6px;
  transform: translateX(-50%);
  border-left: 7px solid transparent;
  border-right: 7px solid transparent;
  border-top: 10px solid var(--accent3);
}

.sequence-diagram {
  margin: 16px 0;
  padding: 18px;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.08);
  background: linear-gradient(135deg, rgba(124,92,252,0.14), rgba(17,24,39,0.82));
}
.sequence-grid {
  display: grid;
  grid-template-columns: minmax(88px, 1fr) 64px minmax(88px, 1fr);
  gap: 14px 10px;
  align-items: center;
}
.seq-party {
  font-weight: 800;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  color: #f5f3ff;
}
.seq-party.server { text-align: right; }
.seq-line {
  grid-column: 2;
  justify-self: center;
  width: 2px;
  height: 100%;
  min-height: 36px;
  background: linear-gradient(180deg, rgba(196,181,253,0.18), rgba(196,181,253,0.82));
}
.seq-event {
  display: contents;
}
.seq-label {
  font-size: 0.82rem;
  color: var(--text2);
}
.seq-label.right {
  text-align: right;
}
.seq-arrow {
  position: relative;
  height: 3px;
  border-radius: 999px;
  background: var(--accent2);
}
.seq-arrow.syn { background: linear-gradient(90deg, #60a5fa, #38bdf8); }
.seq-arrow.syn-ack { background: linear-gradient(90deg, #f472b6, #fb7185); }
.seq-arrow.ack { background: linear-gradient(90deg, #34d399, #22c55e); }
.seq-arrow.right::after,
.seq-arrow.left::before {
  content: "";
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  border-top: 7px solid transparent;
  border-bottom: 7px solid transparent;
}
.seq-arrow.right::after {
  right: -1px;
  border-left: 12px solid currentColor;
}
.seq-arrow.left::before {
  left: -1px;
  border-right: 12px solid currentColor;
}
.seq-arrow.syn { color: #38bdf8; }
.seq-arrow.syn-ack { color: #fb7185; }
.seq-arrow.ack { color: #22c55e; }
.seq-est {
  margin-top: 18px;
  padding: 10px 14px;
  border-radius: 999px;
  text-align: center;
  font-weight: 700;
  background: linear-gradient(90deg, rgba(34,197,94,0.18), rgba(16,185,129,0.34));
  border: 1px solid rgba(34,197,94,0.35);
  color: #d1fae5;
}

.playground {
  margin: 18px 0;
  padding: 18px;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.08);
  background: linear-gradient(135deg, rgba(15,23,42,0.96), rgba(55,48,163,0.2));
}
.playground h3,
.attention-card h3 {
  margin: 0 0 10px;
}
.playground-controls {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}
.playground-controls label {
  display: grid;
  gap: 6px;
  font-size: 0.82rem;
  color: var(--text2);
}
.playground-controls select {
  width: 100%;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(15,15,19,0.95);
  color: var(--text);
}
.playground-stage {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 16px;
}
.playground-canvas,
.playground-compare {
  background: rgba(9,9,15,0.68);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  padding: 16px;
}
.playground-label {
  display: block;
  margin-bottom: 10px;
  color: var(--text2);
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.playground-demo {
  min-height: 200px;
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  background:
    linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px) 0 0 / 24px 24px,
    linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px) 0 0 / 24px 24px,
    rgba(255,255,255,0.02);
}
.playground-box,
.compare-box {
  border-radius: 12px;
  min-width: 56px;
  min-height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  font-weight: 800;
  color: #fff;
}
.playground-box.a,
.compare-box.a { background: linear-gradient(135deg, #60a5fa, #2563eb); }
.playground-box.b,
.compare-box.b { background: linear-gradient(135deg, #f472b6, #db2777); }
.playground-box.c,
.compare-box.c { background: linear-gradient(135deg, #34d399, #059669); }
.playground-demo.column .playground-box {
  width: 100%;
}
.playground-compare-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.compare-scenario {
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.02);
  padding: 12px;
}
.compare-row {
  display: flex;
  gap: 10px;
}
.compare-scenario p {
  margin: 0 0 8px;
  font-size: 0.8rem;
  color: var(--text2);
}
.compare-box {
  justify-content: flex-start;
  align-items: flex-start;
  text-align: left;
  font-size: 0.78rem;
  line-height: 1.35;
}

.attention-card {
  margin: 18px 0;
  padding: 18px;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.08);
  background: linear-gradient(135deg, rgba(88,28,135,0.28), rgba(17,24,39,0.88));
}
.heatmap-wrap {
  overflow-x: auto;
}
.heatmap {
  border-collapse: separate;
  border-spacing: 6px;
  width: max-content;
  min-width: 100%;
}
.heatmap th,
.heatmap td {
  border: none;
  padding: 0;
}
.heatmap-axis {
  font-size: 0.74rem;
  color: var(--text2);
  padding: 6px 8px;
  text-align: center;
}
.heatmap-axis.row-label {
  text-align: right;
  padding-right: 10px;
}
.heatmap-cell {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.08);
  transition: transform 0.15s, box-shadow 0.15s;
}
.heatmap-cell:hover {
  transform: scale(1.06);
  box-shadow: 0 0 0 2px rgba(255,255,255,0.08);
}

.trace-card {
  margin: 18px 0 8px;
  padding: 18px;
  border: 1px solid var(--border);
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(124,92,252,0.14), rgba(96,165,250,0.08));
}
.trace-visual {
  display: grid;
  gap: 14px;
}
.trace-step {
  grid-template-columns: auto 1fr;
  gap: 14px;
  padding: 14px;
  border-radius: 14px;
  background: rgba(10, 10, 18, 0.42);
  border: 1px solid rgba(255,255,255,0.06);
}
.trace-step-index {
  width: 36px;
  height: 36px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: #fff;
  background: linear-gradient(135deg, var(--accent), #4f46e5);
  box-shadow: 0 10px 24px rgba(124,92,252,0.35);
}
.trace-step-copy {
  display: grid;
  gap: 10px;
}
.trace-step-header {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.trace-step-label {
  font-size: 0.84rem;
}
.trace-step-note {
  font-size: 0.84rem;
  color: var(--text2);
}
.hash-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(84px, 1fr));
  gap: 10px;
}
.hash-box {
  padding: 12px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.03);
  display: grid;
  gap: 4px;
  min-height: 76px;
}
.hash-box.active {
  border-color: rgba(124,92,252,0.9);
  box-shadow: 0 0 0 1px rgba(124,92,252,0.45), 0 0 18px rgba(124,92,252,0.28);
}
.hash-box.done {
  border-color: rgba(34,197,94,0.45);
  background: rgba(34,197,94,0.08);
}
.hash-key {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.78rem;
  color: var(--text2);
}
.hash-value {
  font-size: 1.2rem;
  font-weight: 800;
}
.hash-status {
  font-size: 0.78rem;
  color: var(--text2);
}

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
  .trace-step {
    grid-template-columns: 1fr;
  }
  .flow-node {
    grid-template-columns: 1fr;
  }
  .flow-badge {
    width: 34px;
    height: 34px;
  }
  .sequence-grid {
    grid-template-columns: minmax(64px, 1fr) 32px minmax(64px, 1fr);
    gap: 12px 8px;
  }
  .playground-controls,
  .playground-stage,
  .playground-compare-grid {
    grid-template-columns: 1fr;
  }
  .playground-demo {
    min-height: 160px;
  }
  .copy-btn {
    top: 8px;
    right: 8px;
  }
  .code-block pre {
    padding-top: 46px;
  }
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


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def highlight_code(code: str, lang: str) -> str:
    lang = (lang or "").lower()

    def render_with_patterns(text: str, patterns: list[tuple[str, str, str]]) -> str:
        combined = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern, _ in patterns), re.MULTILINE)
        color_map = {name: color for name, _, color in patterns}
        parts = []
        last = 0
        for match in combined.finditer(text):
            start, end = match.span()
            if start > last:
                parts.append(escape_html(text[last:start]))
            group_name = next(name for name, value in match.groupdict().items() if value is not None)
            parts.append(f'<span style="color:{color_map[group_name]};">{escape_html(match.group(0))}</span>')
            last = end
        if last < len(text):
            parts.append(escape_html(text[last:]))
        return ''.join(parts)

    if lang == "python":
        return render_with_patterns(code, [
            ("comment", r"#[^\n]*", "#5c6370"),
            ("string", r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', "#e5c07b"),
            ("keyword", r"\b(?:False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b", "#c678dd"),
            ("number", r"\b\d+(?:\.\d+)?\b", "#56b6c2"),
        ])
    if lang == "css":
        highlighted = []
        for line in code.splitlines():
            escaped = escape_html(line)
            if "/*" in line:
                highlighted.append(f'<span style="color:#5c6370;">{escaped}</span>')
                continue
            selector_match = re.match(r"^\s*([^{]+)(\s*\{)?\s*$", line)
            if selector_match and "{" in line and ":" not in line:
                selector = escape_html(selector_match.group(1).rstrip())
                suffix = escape_html(line[len(selector_match.group(1)):])
                highlighted.append(f'<span style="color:#e06c75;">{selector}</span>{suffix}')
                continue
            prop_match = re.match(r"^(\s*)([a-z-]+)(\s*:\s*)([^;]+)(;?)", line)
            if prop_match:
                indent, prop, colon, value, semi = prop_match.groups()
                highlighted.append(
                    f'{escape_html(indent)}<span style="color:#56b6c2;">{escape_html(prop)}</span>'
                    f'{escape_html(colon)}<span style="color:#e5c07b;">{escape_html(value)}</span>{escape_html(semi)}'
                )
                continue
            highlighted.append(escaped)
        return "\n".join(highlighted)
    if lang == "json":
        return render_with_patterns(code, [
            ("key", r'"(?:\\.|[^"\\])*"(?=\s*:)', "#56b6c2"),
            ("string", r'(?<=:\s)"(?:\\.|[^"\\])*"', "#e5c07b"),
            ("boolean", r"\b(?:true|false|null)\b", "#c678dd"),
            ("number", r"\b-?\d+(?:\.\d+)?\b", "#56b6c2"),
        ])
    if lang in {"html", "xml"}:
        escaped = escape_html(code)

        def replace_tag(match):
            prefix, tag_name, attrs, suffix = match.groups()
            attrs = re.sub(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)(=)', r'<span style="color:#e5c07b;">\1</span>\2', attrs)
            return f'{prefix}<span style="color:#e06c75;">{tag_name}</span>{attrs}{suffix}'

        return re.sub(r"(&lt;/?)([a-zA-Z][\w:-]*)(.*?)(/?&gt;)", replace_tag, escaped)
    if lang in {"bash", "sh", "shell"}:
        highlighted = []
        for raw_line in code.splitlines():
            stripped = raw_line.lstrip()
            indent = raw_line[:len(raw_line) - len(stripped)]
            if stripped.startswith("#"):
                highlighted.append(escape_html(indent) + f'<span style="color:#5c6370;">{escape_html(stripped)}</span>')
                continue
            parts = re.split(r"(\s+)", stripped)
            line_parts = [escape_html(indent)]
            command_done = False
            for part in parts:
                if not part:
                    continue
                if part.isspace():
                    line_parts.append(escape_html(part))
                elif not command_done and not part.startswith("-"):
                    line_parts.append(f'<span style="color:#98c379;">{escape_html(part)}</span>')
                    command_done = True
                elif part.startswith("-"):
                    line_parts.append(f'<span style="color:#56b6c2;">{escape_html(part)}</span>')
                else:
                    line_parts.append(escape_html(part))
            highlighted.append("".join(line_parts))
        return "\n".join(highlighted)
    return escape_html(code)


def is_diagram_line(line: str) -> bool:
    stripped = line.rstrip()
    if not stripped:
        return False
    if re.search(r"[┌┐└┘│─┬├┤▼→←═╔╗╚╝║]", stripped):
        arrow_like = len(re.findall(r"[▼→←═│─┌┐└┘┬├┤╔╗╚╝║]", stripped))
        if arrow_like >= 2 or re.search(r"[┌┐└┘│─┬├┤╔╗╚╝║]", stripped):
            return True
    if stripped.count("|") >= 2 and re.search(r"[A-Za-z0-9]", stripped):
        return True
    if len(re.findall(r"(?:->|=>|<-|→|←)", stripped)) >= 2 and re.search(r"[A-Za-z0-9]", stripped):
        return True
    return False


def looks_like_diagram_block(code: str) -> bool:
    lines = [line for line in code.splitlines() if line.strip()]
    if not lines:
        return False
    diagram_count = sum(1 for line in lines if is_diagram_line(line))
    return diagram_count >= 2 or any(re.search(r"[┌┐└┘│─┬├┤▼→←═╔╗╚╝║]", line) for line in lines)


def render_live_demo(code: str, lang: str, section_key: str) -> str:
    if section_key != "frontend" or (lang or "").lower() != "css":
        return ""
    if "justify-content: space-between" not in code or "width: 300px" not in code:
        return ""
    return """
<div class="live-demo">
  <p class="live-demo-label">▶ Live result / 实际效果:</p>
  <div class="live-demo-canvas">
    <div style="display:flex; justify-content:space-between; width:300px; padding:12px; background:#ffffff; border:1px dashed #c9c2f6; border-radius:10px; margin:0 auto;">
      <div style="width:80px; height:80px; background:#e06c75; color:#fff; display:flex; align-items:center; justify-content:center; border-radius:10px; font-weight:700;">A</div>
      <div style="width:80px; height:80px; background:#56b6c2; color:#fff; display:flex; align-items:center; justify-content:center; border-radius:10px; font-weight:700;">B</div>
      <div style="width:80px; height:80px; background:#98c379; color:#fff; display:flex; align-items:center; justify-content:center; border-radius:10px; font-weight:700;">C</div>
    </div>
  </div>
</div>
""".strip()


def render_code_block(code: str, lang: str, section_key: str) -> str:
    if not (lang or "").strip() and looks_like_diagram_block(code):
        return f'<div class="diagram-block">{escape_html(code)}</div>'
    lang_attr = escape_html(lang or "text")
    highlighted = highlight_code(code, lang)
    demo = render_live_demo(code, lang, section_key)
    escaped_raw = escape_html(code)
    attr_value = escaped_raw.replace('"', "&quot;").replace("\n", "&#10;")
    return f"""
<div class="code-block">
  <button class="copy-btn" type="button" data-copy="{attr_value}">Copy</button>
  <pre><code class="language-{lang_attr}">{highlighted}</code></pre>
</div>
{demo}
""".strip()


def render_dns_flowchart() -> str:
    steps = [
        ("1", "flow-node-browser", "你的浏览器 / Browser", "User enters a URL and starts lookup."),
        ("2", "flow-node-cache", "本地缓存 + hosts / Local Cache + hosts", "Check browser cache, OS cache, and hosts file first."),
        ("3", "flow-node-resolver", "递归解析器 / Recursive Resolver", "Usually ISP DNS or a public resolver like 8.8.8.8."),
        ("4", "flow-node-root", "根域名服务器 / Root Nameserver", "Points the resolver toward the right TLD."),
        ("5", "flow-node-tld", "TLD 服务器 / TLD Nameserver", "For `.com`, `.org`, and other top-level domains."),
        ("6", "flow-node-authoritative", "权威 DNS / Authoritative Nameserver", "Returns the final IP for `myblog.com`."),
    ]
    parts = ['<div class="flow-chart" role="img" aria-label="DNS resolution flow from browser to authoritative nameserver">']
    for index, color_class, title, subtitle in steps:
        parts.append(
            f'''
  <div class="flow-node {color_class}">
    <span class="flow-badge" aria-hidden="true">{index}</span>
    <div class="flow-copy">
      <div class="flow-title">{title}</div>
      <div class="flow-subtitle">{subtitle}</div>
    </div>
  </div>'''.rstrip()
        )
        if index != "6":
            parts.append('  <div class="flow-arrow" aria-hidden="true"></div>')
    parts.append(
        '''
  <div class="flow-node flow-node-return">
    <span class="flow-badge" aria-hidden="true">✓</span>
    <div class="flow-copy">
      <div class="flow-title">IP 返回浏览器 / IP Returned to Browser</div>
      <div class="flow-subtitle">The browser can now open a connection to the server.</div>
    </div>
  </div>
</div>'''.strip()
    )
    return "\n".join(parts)


def render_tcp_handshake() -> str:
    return """
<div class="sequence-diagram" role="img" aria-label="TCP three-way handshake sequence diagram between client and server">
  <div class="sequence-grid">
    <div class="seq-party">Client</div>
    <div></div>
    <div class="seq-party server">Server</div>

    <div class="seq-label">Ready to connect</div>
    <div class="seq-line" aria-hidden="true"></div>
    <div class="seq-label right">Listening</div>

    <div class="seq-event">
      <div class="seq-label">SYN</div>
      <div class="seq-arrow syn right" aria-hidden="true"></div>
      <div class="seq-label right">“I want to connect”</div>
    </div>

    <div class="seq-event">
      <div class="seq-label">Waiting for reply</div>
      <div class="seq-arrow syn-ack left" aria-hidden="true"></div>
      <div class="seq-label right">SYN-ACK</div>
    </div>

    <div class="seq-event">
      <div class="seq-label">ACK</div>
      <div class="seq-arrow ack right" aria-hidden="true"></div>
      <div class="seq-label right">Connection confirmed</div>
    </div>
  </div>
  <div class="seq-est">Connection Established / 连接建立</div>
</div>
""".strip()


def enhance_diagrams(html: str, section_key: str) -> str:
    if section_key != "system-design":
        return html

    def replace(match: re.Match[str]) -> str:
        raw = match.group(1)
        text = re.sub(r"<[^>]+>", "", raw)
        text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        lowered = text.lower()
        if any(keyword in lowered for keyword in ["root nameserver", "recursive resolver", "authoritative nameserver", "tld nameserver"]):
            return render_dns_flowchart()
        if "syn" in lowered and "ack" in lowered and "client" in lowered and "server" in lowered:
            return render_tcp_handshake()
        return match.group(0)

    return re.sub(r'<div class="diagram-block">(.*?)</div>', replace, html, flags=re.DOTALL)


def render_flexbox_playground() -> str:
    return """
<div class="playground" data-flexbox-playground>
  <h3>Interactive Flexbox Playground</h3>
  <p>Change the flex container controls and compare <code>flex: 1</code> with <code>flex: 1 1 auto</code>.</p>
  <div class="playground-controls">
    <label>
      <span>justify-content</span>
      <select data-control="justify-content" aria-label="justify-content">
        <option value="flex-start">flex-start</option>
        <option value="center">center</option>
        <option value="space-between" selected>space-between</option>
        <option value="space-around">space-around</option>
        <option value="space-evenly">space-evenly</option>
      </select>
    </label>
    <label>
      <span>align-items</span>
      <select data-control="align-items" aria-label="align-items">
        <option value="stretch">stretch</option>
        <option value="flex-start">flex-start</option>
        <option value="center" selected>center</option>
        <option value="flex-end">flex-end</option>
      </select>
    </label>
    <label>
      <span>flex-direction</span>
      <select data-control="flex-direction" aria-label="flex-direction">
        <option value="row" selected>row</option>
        <option value="column">column</option>
      </select>
    </label>
  </div>
  <div class="playground-stage">
    <div class="playground-canvas">
      <span class="playground-label">Live Container</span>
      <div class="playground-demo" data-playground-demo>
        <div class="playground-box a">A</div>
        <div class="playground-box b">B</div>
        <div class="playground-box c">C</div>
      </div>
    </div>
    <div class="playground-compare">
      <span class="playground-label">Shorthand Comparison</span>
      <div class="playground-compare-grid">
        <div class="compare-scenario">
          <p><code>flex: 1</code> starts from zero width.</p>
          <div class="compare-row">
            <div class="compare-box a" style="flex:1;">A short</div>
            <div class="compare-box b" style="flex:1;">B has much longer text content</div>
          </div>
        </div>
        <div class="compare-scenario">
          <p><code>flex: 1 1 auto</code> respects content size first.</p>
          <div class="compare-row">
            <div class="compare-box a" style="flex:1 1 auto;">A short</div>
            <div class="compare-box b" style="flex:1 1 auto;">B has much longer text content</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
""".strip()


def render_attention_heatmap() -> str:
    words = ["The", "animal", "didnt", "cross", "the", "street", "because", "it", "was", "too", "tired"]
    attention = {
        "The": 0.02,
        "animal": 0.86,
        "didnt": 0.03,
        "cross": 0.04,
        "the": 0.02,
        "street": 0.08,
        "because": 0.05,
        "it": 0.03,
        "was": 0.07,
        "too": 0.1,
        "tired": 0.3,
    }
    header = "".join(f'<th class="heatmap-axis">{escape_html(word)}</th>' for word in words)
    cells = []
    for word in words:
        value = attention[word]
        alpha = max(0.04, min(1.0, value))
        bg = f"rgba(167, 139, 250, {alpha:.2f})"
        cells.append(
            f'<td><div class="heatmap-cell" title="{word}: {value:.2f}" aria-label="{word} attention weight {value:.2f}" style="background:{bg};"></div></td>'
        )
    row = "".join(cells)
    return f"""
<div class="attention-card">
  <h3>Attention Heatmap</h3>
  <p>When the model processes <code>it</code>, it attends most strongly to <code>animal</code>.</p>
  <div class="heatmap-wrap">
    <table class="heatmap">
      <thead>
        <tr>
          <th></th>
          {header}
        </tr>
      </thead>
      <tbody>
        <tr>
          <th class="heatmap-axis row-label">it →</th>
          {row}
        </tr>
      </tbody>
    </table>
  </div>
</div>
""".strip()


def render_algorithm_trace(section_key: str, text: str) -> str:
    if section_key != "algorithms" or 's = "anagram"' not in text:
        return ""

    steps = [
        ("1", "Start", "Empty counter before scanning any characters.", {}, None, False),
        ("2", "Scan s", 'Read `anagram` and count each character.', {"a": 3, "n": 1, "g": 1, "r": 1, "m": 1}, "a", False),
        ("3", "State", "Hash map now stores the required counts.", {"a": 3, "n": 1, "g": 1, "r": 1, "m": 1}, None, False),
        ("4", "Scan t", 'Read `nagaram` and subtract each character back down.', {"a": 0, "n": 0, "g": 0, "r": 0, "m": 0}, "m", True),
        ("5", "Finish", "All counts return to zero, so the strings are anagrams.", {"a": 0, "n": 0, "g": 0, "r": 0, "m": 0}, None, True),
    ]

    step_html = []
    for index, label, note, state, active_key, done in steps:
        boxes = []
        for key, value in state.items():
            classes = ["hash-box"]
            if active_key == key:
                classes.append("active")
            if done and value == 0:
                classes.append("done")
            status = "active key" if active_key == key else ("balanced ✓" if done and value == 0 else "count")
            boxes.append(
                f'''
        <div class="{" ".join(classes)}">
          <div class="hash-key">key['{key}']</div>
          <div class="hash-value">{value}</div>
          <div class="hash-status">{status}</div>
        </div>'''.rstrip()
            )
        if not boxes:
            boxes.append(
                """
        <div class="hash-box">
          <div class="hash-key">count</div>
          <div class="hash-value">{}</div>
          <div class="hash-status">empty map</div>
        </div>
""".rstrip()
            )
        step_html.append(
            f'''
    <div class="trace-step">
      <div class="trace-step-index" aria-hidden="true">{index}</div>
      <div class="trace-step-copy">
        <div class="trace-step-header">
          <div class="trace-step-label">{label}</div>
          <div class="trace-step-note">{note}</div>
        </div>
        <div class="hash-grid">
{"".join(boxes)}
        </div>
      </div>
    </div>'''.rstrip()
        )

    return """
<div class="trace-card">
  <h3>Visual Step Trace</h3>
  <div class="trace-visual">
    STEP_HTML
  </div>
</div>
""".replace("STEP_HTML", "\n".join(step_html)).strip()


def md_to_html(text: str, section_key: str = "") -> str:
    """Very lightweight Markdown → HTML converter for archive display."""
    lines = text.split("\n")
    html_lines = []
    in_pre = False
    pre_lang = ""
    pre_buf = []
    in_table = False
    table_rows = []

    def flush_pre():
        code = "\n".join(pre_buf)
        pre_buf.clear()
        return render_code_block(code, pre_lang, section_key)

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return ""
        header = table_rows[0]
        body = table_rows[1:]
        header_html = "".join(f"<th>{inline_md(cell)}</th>" for cell in header)
        body_html = "".join(
            "<tr>{}</tr>".format("".join(f"<td>{inline_md(cell)}</td>" for cell in row))
            for row in body
        )
        table_rows = []
        return f"<table><thead><tr>{header_html}</tr></thead><tbody>{body_html}</tbody></table>"

    i = 0
    while i < len(lines):
        line = lines[i]

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

        if in_table and not line.strip().startswith("|"):
            html_lines.append(flush_table())
            in_table = False

        m = re.match(r"^(#{1,3})\s+(.*)", line)
        if m:
            lvl = len(m.group(1))
            text_inner = inline_md(m.group(2))
            html_lines.append(f"<h{lvl}>{text_inner}</h{lvl}>")
            i += 1
            continue

        if re.match(r"^[-*_]{3,}\s*$", line):
            html_lines.append("<hr/>")
            i += 1
            continue

        if line.startswith(">"):
            content = inline_md(line[1:].strip())
            html_lines.append(f"<blockquote>{content}</blockquote>")
            i += 1
            continue

        if line.strip().startswith("|"):
            in_table = True
            if not re.match(r"^\|[\s\-:|]+\|$", line.strip()):
                table_rows.append([cell.strip() for cell in line.strip().split("|")[1:-1]])
            i += 1
            continue

        if re.match(r"^[-*+]\s", line):
            items = []
            while i < len(lines) and re.match(r"^[-*+]\s", lines[i]):
                items.append(f"<li>{inline_md(lines[i][2:].strip())}</li>")
                i += 1
            html_lines.append("<ul>" + "".join(items) + "</ul>")
            continue

        if re.match(r"^\d+\.\s", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i]):
                text_inner = re.sub(r"^\d+\.\s", "", lines[i])
                items.append(f"<li>{inline_md(text_inner)}</li>")
                i += 1
            html_lines.append("<ol>" + "".join(items) + "</ol>")
            continue

        if is_diagram_line(line):
            diagram_lines = [line.rstrip()]
            i += 1
            while i < len(lines) and is_diagram_line(lines[i]):
                diagram_lines.append(lines[i].rstrip())
                i += 1
            html_lines.append(f'<div class="diagram-block">{escape_html(chr(10).join(diagram_lines))}</div>')
            continue

        if not line.strip():
            html_lines.append("")
            i += 1
            continue

        html_lines.append(f"<p>{inline_md(line)}</p>")
        i += 1

    if in_pre and pre_buf:
        html_lines.append(flush_pre())
    if in_table:
        html_lines.append(flush_table())
    if section_key == "frontend" and "flexbox" in text.lower():
        html_lines.append(render_flexbox_playground())
    if section_key == "ai" and any(keyword in text.lower() for keyword in ["attention", "transformer"]):
        html_lines.append(render_attention_heatmap())
    trace = render_algorithm_trace(section_key, text)
    if trace:
        html_lines.append(trace)
    return enhance_diagrams("\n".join(html_lines), section_key)


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
        content_html = md_to_html(sections[key], key)
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

document.querySelectorAll('.copy-btn').forEach((button) => {{
  button.addEventListener('click', async () => {{
    const text = button.getAttribute('data-copy').replace(/&#10;/g, '\\n');
    try {{
      await navigator.clipboard.writeText(text);
      const original = button.textContent;
      button.textContent = 'Copied';
      setTimeout(() => {{ button.textContent = original; }}, 1200);
    }} catch (err) {{
      button.textContent = 'Failed';
      setTimeout(() => {{ button.textContent = 'Copy'; }}, 1200);
    }}
  }});
}});

document.querySelectorAll('[data-flexbox-playground]').forEach((playground) => {{
  const demo = playground.querySelector('[data-playground-demo]');
  const controls = playground.querySelectorAll('[data-control]');
  const applyState = () => {{
    const direction = playground.querySelector('[data-control="flex-direction"]').value;
    demo.style.justifyContent = playground.querySelector('[data-control="justify-content"]').value;
    demo.style.alignItems = playground.querySelector('[data-control="align-items"]').value;
    demo.style.flexDirection = direction;
    demo.classList.toggle('column', direction === 'column');
  }};
  controls.forEach((control) => control.addEventListener('change', applyState));
  applyState();
}});
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
