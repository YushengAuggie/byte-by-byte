#!/usr/bin/env bash
# byte-by-byte: Verify today's content exists, send email, generate web pages, commit.
# Used by backup cron to catch missed deliveries.
# Exit codes: 0 = success, 1 = content missing (needs agent intervention)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$REPO_DIR/config.env"

STATE_FILE="$BBB_REPO_DIR/state.json"
ARCHIVE_DIR="$BBB_REPO_DIR/archive"
TODAY=$(date +%Y-%m-%d)
SEND_LOG="$BBB_REPO_DIR/email-send-log.json"

echo "=== byte-by-byte verify-and-send ==="
echo "Date: $TODAY"

# ── Step 1: Check if email already sent today ────────────────────────
if [ -f "$SEND_LOG" ]; then
  ALREADY_SENT=$(python3 -c "
import json
from datetime import date
today = date.today().isoformat()
with open('$SEND_LOG') as f:
    log = json.load(f)
print('yes' if today in log else 'no')
" 2>/dev/null || echo "no")
  if [ "$ALREADY_SENT" = "yes" ]; then
    echo "✅ Email already sent today. Ensuring web pages are current..."
    python3 "$BBB_REPO_DIR/scripts/generate-index.py"
    bash "$BBB_REPO_DIR/scripts/commit.sh" || true
    echo "Done."
    exit 0
  fi
fi

echo "📧 Email not sent yet today."

# ── Step 2: Check if archive files exist ─────────────────────────────
NORMAL_COUNT=0
for section in system-design algorithms soft-skills frontend ai; do
  if [ -f "$ARCHIVE_DIR/${TODAY}-${section}.md" ]; then
    NORMAL_COUNT=$((NORMAL_COUNT + 1))
  fi
done

REVIEW_EXISTS=0
if [ -f "$ARCHIVE_DIR/${TODAY}-review.md" ]; then
  REVIEW_EXISTS=1
fi

echo "Normal sections: $NORMAL_COUNT/5, Review file: $REVIEW_EXISTS"

if [ "$NORMAL_COUNT" -eq 0 ] && [ "$REVIEW_EXISTS" -eq 0 ]; then
  echo "❌ ERROR: No archive files for $TODAY!"
  echo "The 8AM daily cron failed to generate content."
  echo "Manual intervention needed: run the daily cron or generate content manually."
  exit 1
fi

if [ "$NORMAL_COUNT" -gt 0 ] && [ "$NORMAL_COUNT" -lt 5 ]; then
  echo "⚠️ WARNING: Only $NORMAL_COUNT/5 sections found. Sending what we have."
fi

# ── Step 3: Send email ───────────────────────────────────────────────
echo "Sending email..."
python3 "$BBB_REPO_DIR/scripts/send-email.py"

# ── Step 4: Generate web pages and commit ────────────────────────────
echo "Generating web pages..."
python3 "$BBB_REPO_DIR/scripts/generate-index.py"

echo "Committing..."
bash "$BBB_REPO_DIR/scripts/commit.sh" || true

echo "=== verify-and-send complete ==="
