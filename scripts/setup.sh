#!/usr/bin/env bash
# byte-by-byte: setup script for new machines
# Creates OpenClaw cron jobs from the repo config.
# Usage: ./scripts/setup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$REPO_DIR/config.env"

echo "=== byte-by-byte setup ==="
echo "Repo: $BBB_REPO_DIR"
echo "OpenClaw: $OPENCLAW_BIN"
echo "Telegram target: $TELEGRAM_TARGET"
echo "Schedule: $CRON_SCHEDULE ($TIMEZONE)"
echo ""

# Verify openclaw exists
if [ ! -f "$OPENCLAW_BIN" ]; then
  echo "❌ OpenClaw not found at $OPENCLAW_BIN"
  echo "   Update OPENCLAW_BIN in config.env"
  exit 1
fi

# Check if cron jobs already exist
EXISTING=$("$OPENCLAW_BIN" cron list 2>&1 | grep -c "byte-by-byte" || true)
if [ "$EXISTING" -gt 0 ]; then
  echo "⚠️  Found $EXISTING existing byte-by-byte cron job(s)."
  read -p "Remove and recreate? (y/N) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Remove existing byte-by-byte jobs
    "$OPENCLAW_BIN" cron list 2>&1 | grep "byte-by-byte" | awk '{print $1}' | while read -r id; do
      "$OPENCLAW_BIN" cron remove "$id" 2>&1
      echo "  Removed $id"
    done
  else
    echo "Keeping existing jobs. Exiting."
    exit 0
  fi
fi

# Read cron job definitions from repo
echo "Creating cron jobs..."

# Job 1: Main daily generation
"$OPENCLAW_BIN" cron add \
  --name "byte-by-byte daily" \
  --cron "$CRON_SCHEDULE" \
  --tz "$TIMEZONE" \
  --exact \
  --session isolated \
  --message "$(cat "$REPO_DIR/cron/daily-prompt.md")" \
  --announce \
  --channel telegram \
  --to "$TELEGRAM_TARGET" \
  --model "$MODEL" 2>&1

echo "✓ Created: byte-by-byte daily ($CRON_SCHEDULE $TIMEZONE)"

# Job 2: QA reviewer
"$OPENCLAW_BIN" cron add \
  --name "byte-by-byte QA" \
  --cron "$QA_SCHEDULE" \
  --tz "$TIMEZONE" \
  --exact \
  --session isolated \
  --message "$(cat "$REPO_DIR/cron/qa-prompt.md")" \
  --announce \
  --channel telegram \
  --to "$TELEGRAM_TARGET" \
  --model "$MODEL" 2>&1

echo "✓ Created: byte-by-byte QA ($QA_SCHEDULE $TIMEZONE)"

echo ""
echo "=== Setup complete ==="
"$OPENCLAW_BIN" cron list 2>&1
