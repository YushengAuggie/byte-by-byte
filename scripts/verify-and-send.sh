#!/usr/bin/env bash
# byte-by-byte: Verify archive files, advance state, send email, generate web pages, commit.
# Used by backup cron (8:10 AM) to catch missed deliveries.
# Also usable manually: bash scripts/verify-and-send.sh
# Exit codes: 0 = success, 1 = content missing (needs agent intervention)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$REPO_DIR/config.env"

TODAY=$(TZ="${TIMEZONE:-UTC}" date +%Y-%m-%d)
SEND_LOG="$BBB_REPO_DIR/email-send-log.json"

echo "=== byte-by-byte verify-and-send ==="
echo "Date: $TODAY"

# NOTE: no coarse "already sent today" short-circuit here. send-email.py now
# does per-recipient dedup (and skips a fully-delivered / legacy day on its own),
# so we always let it run — that way a PARTIAL send (some recipients failed) is
# correctly retried for just the missing addresses instead of being skipped.

# ── Step 2: Verify archive files exist ───────────────────────────────
ARCHIVE_DIR="$BBB_REPO_DIR/archive"
NORMAL_COUNT=0
for section in system-design algorithms soft-skills python-craft ai; do
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
  echo "Manual intervention needed."
  exit 1
fi

if [ "$NORMAL_COUNT" -gt 0 ] && [ "$NORMAL_COUNT" -lt 5 ]; then
  echo "⚠️ WARNING: Only $NORMAL_COUNT/5 sections found. Sending what we have."
fi

# ── Step 3: Advance state (if not already) ───────────────────────────
echo "Checking state..."
bash "$BBB_REPO_DIR/scripts/advance-state.sh" || {
  echo "⚠️ advance-state.sh failed — state may already be current or files missing"
}

# ── Step 4: Send email ───────────────────────────────────────────────
echo "Sending email..."
python3 "$BBB_REPO_DIR/scripts/send-email.py"

# ── Step 5: Generate web pages and commit ────────────────────────────
echo "Generating web pages..."
python3 "$BBB_REPO_DIR/scripts/generate-index.py"

echo "Committing..."
bash "$BBB_REPO_DIR/scripts/commit.sh" || true

echo "=== verify-and-send complete ==="
