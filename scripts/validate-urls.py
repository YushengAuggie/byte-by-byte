#!/usr/bin/env python3
"""byte-by-byte: Validate URLs found in archive/*.md files.

Extracts all http/https URLs from archive markdown files,
performs HEAD requests with a 5s timeout, and reports broken links.

Exit code: 0 if all OK, 1 if broken links found.
"""

import os
import re
import sys
import urllib.request
import urllib.error
import ssl
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
ARCHIVE_DIR = REPO_DIR / "archive"
TIMEOUT = 5

URL_RE = re.compile(r'https?://[^\s\)\]\'"<>]+')

def extract_urls(text: str) -> list:
    urls = URL_RE.findall(text)
    # Clean trailing punctuation that's likely not part of the URL
    cleaned = []
    for url in urls:
        url = url.rstrip('.,;:!?)]}')
        if url:
            cleaned.append(url)
    return cleaned

def check_url(url: str) -> tuple:
    """Returns (ok: bool, status: str)"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(
            url,
            method='HEAD',
            headers={'User-Agent': 'byte-by-byte-url-checker/1.0'}
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            code = resp.getcode()
            if 400 <= code < 600:
                return False, f"HTTP {code}"
            return True, f"HTTP {code}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        reason = str(e.reason)
        if 'timed out' in reason.lower() or isinstance(e.reason, OSError):
            return False, f"TIMEOUT/ERROR: {reason}"
        return False, f"URL_ERROR: {reason}"
    except Exception as e:
        return False, f"ERROR: {e}"

def main():
    if not ARCHIVE_DIR.exists():
        print(f"ERROR: archive/ directory not found at {ARCHIVE_DIR}")
        sys.exit(1)

    md_files = sorted(ARCHIVE_DIR.glob("*.md"))
    if not md_files:
        print("No archive files found.")
        sys.exit(0)

    # Collect all URLs across all files
    all_urls = {}  # url -> [filenames]
    for f in md_files:
        text = f.read_text(encoding='utf-8')
        for url in extract_urls(text):
            all_urls.setdefault(url, []).append(f.name)

    if not all_urls:
        print("No URLs found in archive files.")
        sys.exit(0)

    print(f"🔗 Checking {len(all_urls)} unique URLs from {len(md_files)} archive files...")
    print()

    broken = []
    ok_count = 0

    for url, files in sorted(all_urls.items()):
        ok, status = check_url(url)
        if ok:
            ok_count += 1
            print(f"  ✅ {status:8s}  {url}")
        else:
            broken.append((url, status, files))
            print(f"  ❌ {status:8s}  {url}")
            print(f"             Found in: {', '.join(files)}")

    print()
    print(f"Results: {ok_count} OK, {len(broken)} broken")

    if broken:
        print()
        print("━━━━ BROKEN LINKS ━━━━")
        for url, status, files in broken:
            print(f"  {status}: {url}")
            print(f"    → Found in: {', '.join(files)}")
        sys.exit(1)
    else:
        print("✅ All URLs are reachable.")
        sys.exit(0)

if __name__ == '__main__':
    main()
