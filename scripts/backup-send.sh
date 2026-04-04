#!/usr/bin/env bash
# backup-send.sh — Fallback delivery if review-and-send cron failed.
# Runs at 8:30 AM. If email already sent today, exits silently.
# If content exists but wasn't sent, sends it and alerts via Telegram.
# NO LLM dependency — pure bash + Python scripts.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load config
source "$REPO_DIR/config.env"
export BBB_REPO_DIR GMAIL_USER GMAIL_APP_PASSWORD SUBSCRIBERS_CSV_URL \
       EMAIL_TARGET SMTP_USER SMTP_APP_PASSWORD \
       TELEGRAM_BOT_TOKEN TELEGRAM_CHAT_ID 2>/dev/null || true

TODAY=$(date +%Y-%m-%d)
LOG_FILE="$REPO_DIR/email-send-log.json"

log() { echo "[backup-send] $*"; }

# ── 1. Check if already sent today ──────────────────────────────────
if [ -f "$LOG_FILE" ]; then
  ALREADY_SENT=$(python3 -c "
import json, sys
data = json.load(open('$LOG_FILE'))
print('yes' if '$TODAY' in data else 'no')
" 2>/dev/null || echo "no")

  if [ "$ALREADY_SENT" = "yes" ]; then
    log "Email already sent for $TODAY. Nothing to do."
    exit 0
  fi
fi

log "No email found for $TODAY — checking for archive content..."

# ── 2. Check what content exists for today ──────────────────────────
ARCHIVE_DIR="$REPO_DIR/archive"
CONTENT_TYPE=""
CONTENT_FILES=()

# Saturday deepdive?
if [ -f "$ARCHIVE_DIR/${TODAY}-deepdive.md" ] && \
   [ "$(wc -c < "$ARCHIVE_DIR/${TODAY}-deepdive.md")" -gt 1000 ]; then
  CONTENT_TYPE="deepdive"
  CONTENT_FILES=("${TODAY}-deepdive.md")

# Sunday week-review?
elif [ -f "$ARCHIVE_DIR/${TODAY}-week-review.md" ] && \
     [ "$(wc -c < "$ARCHIVE_DIR/${TODAY}-week-review.md")" -gt 500 ]; then
  CONTENT_TYPE="week-review"
  CONTENT_FILES=("${TODAY}-week-review.md")

# Review day?
elif [ -f "$ARCHIVE_DIR/${TODAY}-review.md" ] && \
     [ "$(wc -c < "$ARCHIVE_DIR/${TODAY}-review.md")" -gt 500 ]; then
  CONTENT_TYPE="review"
  CONTENT_FILES=("${TODAY}-review.md")

# Normal weekday — need all 5 sections
else
  MISSING=""
  for s in system-design algorithms soft-skills frontend ai; do
    FILE="$ARCHIVE_DIR/${TODAY}-${s}.md"
    if [ ! -f "$FILE" ]; then
      MISSING="$MISSING $s(missing)"
    elif [ "$(wc -c < "$FILE")" -lt 500 ]; then
      SIZE=$(wc -c < "$FILE")
      MISSING="$MISSING $s(${SIZE}B<500)"
    else
      CONTENT_FILES+=("${TODAY}-${s}.md")
    fi
  done

  if [ -z "$MISSING" ]; then
    CONTENT_TYPE="normal"
  else
    log "Incomplete content for $TODAY:$MISSING — cannot send."
    # Notify via Telegram if available
    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
      MSG="⚠️ byte-by-byte backup-send: No content for $TODAY.$MISSING. Review-and-send may have timed out AND content was never generated."
      python3 "$REPO_DIR/scripts/send-telegram.py" "$MSG" 2>/dev/null || true
    fi
    exit 1
  fi
fi

log "Found $CONTENT_TYPE content for $TODAY (${#CONTENT_FILES[@]} file(s)). Sending..."

# ── 3. Send email ────────────────────────────────────────────────────
if python3 "$REPO_DIR/scripts/send-email.py"; then
  log "Email sent successfully."
else
  log "ERROR: send-email.py failed."
  exit 1
fi

# ── 4. Alert via Telegram ────────────────────────────────────────────
ALERT="⚠️ byte-by-byte backup-send triggered for $TODAY ($CONTENT_TYPE). The review-and-send cron failed or timed out — backup sent email directly without QA review."
python3 "$REPO_DIR/scripts/send-telegram.py" "$ALERT" 2>/dev/null || \
  log "Telegram alert failed (non-critical)"

log "Done."
