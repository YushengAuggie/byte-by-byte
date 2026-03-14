#!/usr/bin/env bash
# byte-by-byte: setup script for new machines
# Creates OpenClaw cron jobs from the repo config.
# Usage: ./scripts/setup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check config.env exists
if [ ! -f "$REPO_DIR/config.env" ]; then
  echo "❌ config.env not found!"
  echo "   cp config.env.example config.env"
  echo "   Then edit config.env with your settings."
  exit 1
fi

source "$REPO_DIR/config.env"

echo "=== byte-by-byte setup ==="
echo "Repo: $BBB_REPO_DIR"
echo "OpenClaw: $OPENCLAW_BIN"
echo "Telegram: $TELEGRAM_TARGET"
echo "Email: $EMAIL_TARGET"
echo "Schedule: $CRON_SCHEDULE ($TIMEZONE)"
echo "QA Schedule: $QA_SCHEDULE ($TIMEZONE)"
echo "Model: $MODEL"
echo ""

# Verify openclaw exists
if [ ! -f "$OPENCLAW_BIN" ]; then
  echo "❌ OpenClaw not found at $OPENCLAW_BIN"
  echo "   Update OPENCLAW_BIN in config.env"
  exit 1
fi

# Verify repo dir matches
if [ "$BBB_REPO_DIR" != "$REPO_DIR" ]; then
  echo "⚠️  BBB_REPO_DIR in config.env ($BBB_REPO_DIR)"
  echo "    doesn't match actual repo location ($REPO_DIR)"
  echo "    Update BBB_REPO_DIR in config.env"
  exit 1
fi

# Check if cron jobs already exist
EXISTING=$("$OPENCLAW_BIN" cron list 2>&1 | grep -c "byte-by-byte" || true)
if [ "$EXISTING" -gt 0 ]; then
  echo "⚠️  Found $EXISTING existing byte-by-byte cron job(s)."
  read -p "Remove and recreate? (y/N) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    "$OPENCLAW_BIN" cron list 2>&1 | grep "byte-by-byte" | awk '{print $1}' | while read -r id; do
      "$OPENCLAW_BIN" cron remove "$id" 2>&1
      echo "  Removed $id"
    done
  else
    echo "Keeping existing jobs. Exiting."
    exit 0
  fi
fi

# Resolve prompt templates — replace {{placeholders}} with config values
resolve_prompt() {
  local template_file="$1"
  sed \
    -e "s|{{BBB_REPO_DIR}}|$BBB_REPO_DIR|g" \
    -e "s|{{TELEGRAM_TARGET}}|$TELEGRAM_TARGET|g" \
    -e "s|{{EMAIL_TARGET}}|$EMAIL_TARGET|g" \
    -e "s|{{MODEL}}|$MODEL|g" \
    "$template_file"
}

echo "Creating cron jobs..."

# Job 1: Main daily generation
DAILY_PROMPT=$(resolve_prompt "$REPO_DIR/cron/daily-prompt.md")
"$OPENCLAW_BIN" cron add \
  --name "byte-by-byte daily" \
  --cron "$CRON_SCHEDULE" \
  --tz "$TIMEZONE" \
  --exact \
  --session isolated \
  --message "$DAILY_PROMPT" \
  --announce \
  --channel telegram \
  --to "$TELEGRAM_TARGET" \
  --model "$MODEL" 2>&1 | head -3

echo "✓ Created: byte-by-byte daily ($CRON_SCHEDULE $TIMEZONE)"

# Job 2: QA reviewer
QA_PROMPT=$(resolve_prompt "$REPO_DIR/cron/qa-prompt.md")
"$OPENCLAW_BIN" cron add \
  --name "byte-by-byte QA" \
  --cron "$QA_SCHEDULE" \
  --tz "$TIMEZONE" \
  --exact \
  --session isolated \
  --message "$QA_PROMPT" \
  --announce \
  --channel telegram \
  --to "$TELEGRAM_TARGET" \
  --model "$MODEL" 2>&1 | head -3

echo "✓ Created: byte-by-byte QA ($QA_SCHEDULE $TIMEZONE)"

echo ""
echo "=== Setup complete ==="
"$OPENCLAW_BIN" cron list 2>&1
echo ""
echo "First run: tomorrow at $(echo $CRON_SCHEDULE | awk '{print $2":"$1}') $TIMEZONE"
echo "To test now: $OPENCLAW_BIN cron run <job-id>"
