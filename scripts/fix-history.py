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

# A "full day" is the three shared sections plus a 4th that changed when the
# curriculum migrated frontend → python-craft (around day 46). Accept either.
CORE_SECTIONS = {"system-design", "algorithms", "soft-skills", "ai"}
VARIABLE_SECTIONS = {"frontend", "python-craft"}
NORMAL_SECTIONS = CORE_SECTIONS | VARIABLE_SECTIONS


def is_complete_day(secs: set) -> bool:
    """A complete day = all core sections + exactly one of the variable ones."""
    return CORE_SECTIONS.issubset(secs) and bool(VARIABLE_SECTIONS & secs)


# Maps archive slug → state.json key for extracting titles
SECTION_TITLE_KEYS = {
    "system-design": "system_design",
    "algorithms": "algorithms",
    "soft-skills": "soft_skills",
    "frontend": "frontend",
    "python-craft": "python_craft",
    "ai": "ai",
}


def scan_archive(archive_dir: Path) -> dict:
    """
    Returns dict: date_str → dict of {section_slug: content_text}
    Only includes dates with all 5 normal sections present.
    """
    pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$")
    days = {}
    for f in sorted(archive_dir.glob("*.md")):
        m = pattern.match(f.name)
        if not m:
            continue
        date_str, section = m.group(1), m.group(2)
        if section not in NORMAL_SECTIONS:
            continue
        days.setdefault(date_str, {})[section] = f.read_text(encoding="utf-8")

    # Only return days that have a complete section set (either schema)
    return {d: secs for d, secs in days.items() if is_complete_day(set(secs.keys()))}


def extract_title(content: str) -> str:
    """Pull the first H1/H2 heading from markdown content as a title."""
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("# ") or line.startswith("## "):
            title = re.sub(r"^#{1,3}\s+", "", line)
            # Strip emoji prefixes and day labels like "🏗️ Day 7 /"
            title = re.sub(
                r"^[\U00010000-\U0010ffff\u2600-\u26FF\u2700-\u27BF\s]+",
                "",
                title,
                flags=re.UNICODE,
            )
            title = re.sub(r"^Day\s+\d+\s*[/·\-]?\s*", "", title, flags=re.IGNORECASE)
            title = title.strip()
            if title:
                return title[:120]
    return "Unknown"


def extract_behavioral_question(content: str) -> str:
    """Extract behavioral question from soft-skills content."""
    # Look for a line starting with "Tell me", "Describe", "How", etc.
    question_patterns = [
        r"^(Tell me about .+)",
        r"^(Describe a .+)",
        r"^(How do you .+)",
        r"^(How would you .+)",
        r"^(What .+\?)",
        r"^(When .+\?)",
    ]
    for line in content.splitlines():
        line = line.strip().lstrip("#").lstrip("*").strip()
        for pat in question_patterns:
            m = re.match(pat, line, re.IGNORECASE)
            if m:
                return m.group(1)[:200]
    return extract_title(content)


def build_history_entry(day_num: int, date_str: str, sections: dict) -> dict:
    """Build a history entry dict for a given day (either curriculum schema)."""
    entry_sections = {
        "system_design": {"title": extract_title(sections.get("system-design", ""))},
        "algorithms": {"title": extract_title(sections.get("algorithms", ""))},
        "soft_skills": {
            "question": extract_behavioral_question(sections.get("soft-skills", ""))
        },
        "ai": {"title": extract_title(sections.get("ai", ""))},
    }
    # Whichever 4th section this day used (frontend pre-migration, python-craft after).
    if "python-craft" in sections:
        entry_sections["python_craft"] = {
            "title": extract_title(sections["python-craft"])
        }
    if "frontend" in sections:
        entry_sections["frontend"] = {"title": extract_title(sections["frontend"])}

    return {
        "day": day_num,
        "date": date_str,
        "difficultyPhase": "Foundation",
        "sections": entry_sections,
    }


def main():
    dry_run = "--dry-run" in sys.argv

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

    # Day numbers must stay consistent with the date ordering: a missing date
    # gets a number *between* its chronological neighbours, never a fresh number
    # appended after the latest day (the old bug numbered April dates as Day 81+).
    # (day, date) pairs sorted by date, used to interpolate.
    known = sorted(((e["day"], e["date"]) for e in history), key=lambda p: p[1])

    def interpolate_day(date_str: str, used: set) -> int | None:
        prev_day = max((d for d, dt in known if dt < date_str), default=0)
        next_day = min((d for d, dt in known if dt > date_str), default=None)
        candidate = prev_day + 1
        # walk forward past review-day slots and any already-taken numbers
        while candidate % 5 == 0 or candidate in history_days or candidate in used:
            candidate += 1
        if next_day is not None and candidate >= next_day:
            return None  # no free slot between neighbours — don't corrupt ordering
        return candidate

    added = []
    used_days: set = set()
    for date_str in sorted_dates:
        if date_str in history_dates:
            continue  # Already in history

        day_num = interpolate_day(date_str, used_days)
        if day_num is None:
            print(
                f"  ⏭️  Skipping {date_str} — no free day slot between neighbours "
                f"(ambiguous; fix manually)"
            )
            continue

        used_days.add(day_num)
        entry = build_history_entry(day_num, date_str, complete_days[date_str])
        added.append(entry)
        print(f"  ➕ Will add Day {day_num} ({date_str})")

    if not added:
        print("✅ No gaps found. History is up to date.")
        return

    print()
    if dry_run:
        print(
            f"DRY RUN: Would add {len(added)} history entries. Use without --dry-run to apply."
        )
        return

    # Merge new entries into history, sorted by day number
    all_entries = history + added
    all_entries.sort(key=lambda e: (e["day"], e["date"]))

    state["history"] = all_entries

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"✅ Added {len(added)} history entries to state.json")
    print(f"   Total history entries: {len(all_entries)}")


if __name__ == "__main__":
    main()
