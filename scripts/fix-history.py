#!/usr/bin/env python3
"""byte-by-byte: Fix gaps in state.json history.

Scans archive/ directory for dates with 5 section files.
For each such date that is NOT in state.json history (and not a review day),
adds a synthetic history entry.

Review days (day % 5 == 0) are excluded from history per spec.
Idempotent: safe to run multiple times.

Usage:
    python3 scripts/fix-history.py [--dry-run]
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
ARCHIVE_DIR = REPO_DIR / "archive"
STATE_FILE = REPO_DIR / "state.json"

# Section slugs that count toward a "full day"
NORMAL_SECTIONS = {"system-design", "algorithms", "soft-skills", "frontend", "ai"}

# Maps archive slug → state.json key for extracting titles
SECTION_TITLE_KEYS = {
    "system-design": "system_design",
    "algorithms": "algorithms",
    "soft-skills": "soft_skills",
    "frontend": "frontend",
    "ai": "ai",
}


def scan_archive(archive_dir: Path) -> dict:
    """
    Returns dict: date_str → dict of {section_slug: content_text}
    Only includes dates with all 5 normal sections present.
    """
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})-(.+)\.md$')
    days = {}
    for f in sorted(archive_dir.glob("*.md")):
        m = pattern.match(f.name)
        if not m:
            continue
        date_str, section = m.group(1), m.group(2)
        if section not in NORMAL_SECTIONS:
            continue
        days.setdefault(date_str, {})[section] = f.read_text(encoding='utf-8')

    # Only return days with all 5 sections
    return {d: secs for d, secs in days.items() if set(secs.keys()) == NORMAL_SECTIONS}


def extract_title(content: str) -> str:
    """Pull the first H1/H2 heading from markdown content as a title."""
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('# ') or line.startswith('## '):
            title = re.sub(r'^#{1,3}\s+', '', line)
            # Strip emoji prefixes and day labels like "🏗️ Day 7 /"
            title = re.sub(r'^[\U00010000-\U0010ffff\u2600-\u26FF\u2700-\u27BF\s]+', '', title, flags=re.UNICODE)
            title = re.sub(r'^Day\s+\d+\s*[/·\-]?\s*', '', title, flags=re.IGNORECASE)
            title = title.strip()
            if title:
                return title[:120]
    return "Unknown"


def extract_behavioral_question(content: str) -> str:
    """Extract behavioral question from soft-skills content."""
    # Look for a line starting with "Tell me", "Describe", "How", etc.
    question_patterns = [
        r'^(Tell me about .+)',
        r'^(Describe a .+)',
        r'^(How do you .+)',
        r'^(How would you .+)',
        r'^(What .+\?)',
        r'^(When .+\?)',
    ]
    for line in content.splitlines():
        line = line.strip().lstrip('#').lstrip('*').strip()
        for pat in question_patterns:
            m = re.match(pat, line, re.IGNORECASE)
            if m:
                return m.group(1)[:200]
    return extract_title(content)


def build_history_entry(day_num: int, date_str: str, sections: dict) -> dict:
    """Build a history entry dict for a given day."""
    sd_title = extract_title(sections.get("system-design", ""))
    algo_title = extract_title(sections.get("algorithms", ""))
    soft_q = extract_behavioral_question(sections.get("soft-skills", ""))
    fe_title = extract_title(sections.get("frontend", ""))
    ai_title = extract_title(sections.get("ai", ""))

    return {
        "day": day_num,
        "date": date_str,
        "difficultyPhase": "Foundation",
        "sections": {
            "system_design": {"title": sd_title},
            "algorithms": {"title": algo_title},
            "soft_skills": {"question": soft_q},
            "frontend": {"title": fe_title},
            "ai": {"title": ai_title},
        }
    }


def main():
    dry_run = '--dry-run' in sys.argv

    if not ARCHIVE_DIR.exists():
        print(f"ERROR: archive/ not found at {ARCHIVE_DIR}")
        sys.exit(1)

    if not STATE_FILE.exists():
        print(f"ERROR: state.json not found at {STATE_FILE}")
        sys.exit(1)

    with open(STATE_FILE) as f:
        state = json.load(f)

    history = state.get("history", [])

    # Build set of dates already in history
    history_dates = {entry["date"] for entry in history}
    # Build set of day numbers already in history
    history_days = {entry["day"] for entry in history}

    # Scan archive for complete days
    complete_days = scan_archive(ARCHIVE_DIR)
    sorted_dates = sorted(complete_days.keys())

    print(f"📂 Found {len(complete_days)} complete archive days (5 sections each)")
    print(f"📋 History has {len(history)} entries")
    print()

    # Determine what day numbers to assign to archive dates
    # Use existing history to map dates → day numbers where possible,
    # then assign sequential numbers for new ones.
    date_to_day = {entry["date"]: entry["day"] for entry in history}

    # Figure out the next available day number for gap-filling
    # We assign day numbers in chronological order, skipping review days (day % 5 == 0)
    max_existing_day = max((e["day"] for e in history), default=0)

    added = []
    for date_str in sorted_dates:
        if date_str in history_dates:
            continue  # Already in history

        # Determine the day number for this date
        if date_str in date_to_day:
            day_num = date_to_day[date_str]
        else:
            # Assign next sequential day number, skipping review day slots
            max_existing_day += 1
            # Skip review days (day % 5 == 0)
            while max_existing_day % 5 == 0:
                max_existing_day += 1
            day_num = max_existing_day

        # Double-check: if this day_num is a review day, skip
        if day_num % 5 == 0:
            print(f"  ⏭️  Skipping {date_str} — Day {day_num} is a review day (day % 5 == 0)")
            continue

        entry = build_history_entry(day_num, date_str, complete_days[date_str])
        added.append(entry)
        print(f"  ➕ Will add Day {day_num} ({date_str})")

    if not added:
        print("✅ No gaps found. History is up to date.")
        return

    print()
    if dry_run:
        print(f"DRY RUN: Would add {len(added)} history entries. Use without --dry-run to apply.")
        return

    # Merge new entries into history, sorted by day number
    all_entries = history + added
    all_entries.sort(key=lambda e: (e["day"], e["date"]))

    state["history"] = all_entries

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print(f"✅ Added {len(added)} history entries to state.json")
    print(f"   Total history entries: {len(all_entries)}")


if __name__ == '__main__':
    main()
