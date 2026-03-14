#!/usr/bin/env python3
"""byte-by-byte: Verify the NeetCode 150 problem list for slug validity and duplicates.

Usage:
    python3 verify-neetcode.py [path/to/neetcode-150.json]

This is a local-only check — no network calls are made.
Exit codes:
    0 — no issues found
    1 — issues found (see report)
"""

import sys
import os
import json
import re
from collections import defaultdict
from typing import Optional, Tuple, List

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
REPO_DIR      = os.path.join(SCRIPT_DIR, '..')
DEFAULT_INPUT = os.path.join(REPO_DIR, 'content', 'neetcode-150.json')

LEETCODE_BASE = 'https://leetcode.com/problems/'
# A valid LeetCode slug: lowercase letters, digits, and hyphens, 2–80 chars
SLUG_RE = re.compile(r'^[a-z0-9][a-z0-9\-]{1,78}[a-z0-9]$')
# LeetCode problem URL pattern
URL_RE  = re.compile(r'^https://leetcode\.com/problems/([a-z0-9\-]+)/?$')

def check_slug(slug):
    # type: (str) -> Optional[str]
    """Return an error string if slug is invalid, else None."""
    if not slug:
        return 'empty slug'
    if not SLUG_RE.match(slug):
        return 'invalid slug format: {!r}'.format(slug)
    return None

def extract_slug_from_url(url):
    # type: (str) -> Tuple[str, Optional[str]]
    """Return (slug, error). error is None on success."""
    if not url:
        return '', 'missing url'
    m = URL_RE.match(url.rstrip('/') + '/')
    if not m:
        return '', 'URL does not match expected pattern: {!r}'.format(url)
    return m.group(1), None

def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT

    if not os.path.exists(input_path):
        print(f'ERROR: File not found: {input_path}')
        sys.exit(1)

    with open(input_path) as f:
        problems = json.load(f)

    print(f'byte-by-byte — NeetCode 150 Verification Report')
    print(f'File: {input_path}')
    print('=' * 60)

    issues = []
    seen_ids           = defaultdict(list)   # id → [titles]
    seen_slugs         = defaultdict(list)   # slug → [titles]
    seen_leetcode_nums = defaultdict(list)   # leetcode_num → [titles]
    seen_titles        = defaultdict(list)   # title → [ids]

    for i, prob in enumerate(problems):
        loc = f'[index {i}]'
        pid     = prob.get('id')
        title   = prob.get('title', '')
        num     = prob.get('leetcode_num')
        pattern = prob.get('pattern', '')
        diff    = prob.get('difficulty', '')
        url     = prob.get('url', '')

        # Track for duplicate detection
        if pid is not None:
            seen_ids[pid].append(title or loc)
        if title:
            seen_titles[title].append(str(pid))
        if num is not None:
            seen_leetcode_nums[num].append(title or loc)

        # ── URL / slug validation ──────────────────────────────────────────
        slug, url_err = extract_slug_from_url(url)
        if url_err:
            issues.append(f'  #{pid} {title!r}: {url_err}')
        else:
            slug_err = check_slug(slug)
            if slug_err:
                issues.append(f'  #{pid} {title!r}: {slug_err}')
            else:
                seen_slugs[slug].append(title or loc)

        # ── Required field checks ──────────────────────────────────────────
        for field in ('id', 'title', 'leetcode_num', 'pattern', 'difficulty', 'url'):
            if field not in prob or prob[field] is None or prob[field] == '':
                issues.append(f'  {loc}: missing required field: {field!r}')

        # ── Difficulty check ───────────────────────────────────────────────
        if diff and diff not in ('Easy', 'Medium', 'Hard'):
            issues.append(f'  #{pid} {title!r}: unexpected difficulty {diff!r}')

    # ── Duplicate checks ───────────────────────────────────────────────────────
    for pid, titles in seen_ids.items():
        if len(titles) > 1:
            issues.append(f'  Duplicate id={pid}: {titles}')

    for title, ids in seen_titles.items():
        if len(ids) > 1:
            issues.append(f'  Duplicate title {title!r}: ids={ids}')

    for num, titles in seen_leetcode_nums.items():
        if len(titles) > 1:
            issues.append(f'  Duplicate leetcode_num={num}: {titles}')

    for slug, titles in seen_slugs.items():
        if len(titles) > 1:
            issues.append(f'  Duplicate slug {slug!r}: {titles}')

    # ── Report ─────────────────────────────────────────────────────────────────
    total = len(problems)
    print(f'\nTotal problems : {total}')
    print(f'Expected       : 150')
    if total != 150:
        issues.append(f'  Problem count is {total}, expected 150')

    print(f'Issues found   : {len(issues)}')
    print()

    if issues:
        print('─── Issues ───────────────────────────────────────────────────')
        for issue in issues:
            print(issue)
        print()
        print('Result: ❌ FAIL')
        sys.exit(1)
    else:
        print('Result: ✅ PASS — all slugs valid, no duplicates')
        sys.exit(0)


if __name__ == '__main__':
    main()
