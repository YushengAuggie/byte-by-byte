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

# Pick the generation prompt for a given weekday. Weekdays (Mon–Fri) use the
# 5-section weekday prompt (which also handles review days); Sat/Sun use the
# deep-dive / week-in-review prompts. The legacy combined daily prompt and the
# legacy QA prompt are DEPRECATED and intentionally NOT wired here.
GEN_PROMPT_FILE="$REPO_DIR/cron/weekday-prompt.md"
SAT_PROMPT_FILE="$REPO_DIR/cron/saturday-prompt.md"
SUN_PROMPT_FILE="$REPO_DIR/cron/sunday-prompt.md"
REVIEW_SEND_FILE="$REPO_DIR/cron/review-and-send-prompt.md"

# Job 1: Weekday generation (Mon–Fri) — generate content, do NOT send
WEEKDAY_PROMPT=$(resolve_prompt "$GEN_PROMPT_FILE")
"$OPENCLAW_BIN" cron add \
  --name "byte-by-byte generate (weekday)" \
  --cron "$(echo "$CRON_SCHEDULE" | awk '{print $1, $2, $3, $4, "1-5"}')" \
  --tz "$TIMEZONE" \
  --exact \
  --session isolated \
  --message "$WEEKDAY_PROMPT" \
  --announce \
  --channel telegram \
  --to "$TELEGRAM_TARGET" \
  --model "$MODEL" 2>&1 | head -3
echo "✓ Created: byte-by-byte generate (weekday)"

# Job 2: Saturday deep dive
SAT_PROMPT=$(resolve_prompt "$SAT_PROMPT_FILE")
"$OPENCLAW_BIN" cron add \
  --name "byte-by-byte generate (saturday)" \
  --cron "$(echo "$CRON_SCHEDULE" | awk '{print $1, $2, $3, $4, "6"}')" \
  --tz "$TIMEZONE" --exact --session isolated \
  --message "$SAT_PROMPT" --announce --channel telegram \
  --to "$TELEGRAM_TARGET" --model "$MODEL" 2>&1 | head -3
echo "✓ Created: byte-by-byte generate (saturday)"

# Job 3: Sunday week-in-review
SUN_PROMPT=$(resolve_prompt "$SUN_PROMPT_FILE")
"$OPENCLAW_BIN" cron add \
  --name "byte-by-byte generate (sunday)" \
  --cron "$(echo "$CRON_SCHEDULE" | awk '{print $1, $2, $3, $4, "0"}')" \
  --tz "$TIMEZONE" --exact --session isolated \
  --message "$SUN_PROMPT" --announce --channel telegram \
  --to "$TELEGRAM_TARGET" --model "$MODEL" 2>&1 | head -3
echo "✓ Created: byte-by-byte generate (sunday)"

# Job 4: Review + send (all days), a few minutes after generation
REVIEW_PROMPT=$(resolve_prompt "$REVIEW_SEND_FILE")
"$OPENCLAW_BIN" cron add \
  --name "byte-by-byte review-and-send" \
  --cron "$QA_SCHEDULE" \
  --tz "$TIMEZONE" \
  --exact \
  --session isolated \
  --message "$REVIEW_PROMPT" \
  --announce \
  --channel telegram \
  --to "$TELEGRAM_TARGET" \
  --model "$MODEL" 2>&1 | head -3
echo "✓ Created: byte-by-byte review-and-send ($QA_SCHEDULE $TIMEZONE)"

# Install pre-commit hook
echo ""
echo "Installing pre-commit hook..."
cp "$REPO_DIR/hooks/pre-commit" "$REPO_DIR/.git/hooks/pre-commit"
chmod +x "$REPO_DIR/.git/hooks/pre-commit"
echo "✓ Pre-commit hook installed (runs test.sh before every commit)"

echo ""
echo "=== Setup complete ==="
"$OPENCLAW_BIN" cron list 2>&1
echo ""
echo "First run: tomorrow at $(echo $CRON_SCHEDULE | awk '{print $2":"$1}') $TIMEZONE"
echo "To test now: $OPENCLAW_BIN cron run <job-id>"
