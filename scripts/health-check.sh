#!/usr/bin/env bash
# byte-by-byte: daily health check
# Verifies for TODAY (or, on Sat/Sun, just deepdive/week-review):
#   1. Expected archive files exist and aren't placeholders
#   2. Email was sent today (email-send-log.json)
#   3. byte-by-byte git tree is clean and pushed
#   4. Parent workspace submodule pointer matches byte-by-byte HEAD
# Alerts via Telegram on ANY failure. Exits non-zero if anything is wrong.
# Designed to run AFTER the morning send cycle (e.g. 10 AM PT).

set -uo pipefail  # NOTE: no -e — we want to collect all failures

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$REPO_DIR/config.env"

TODAY=$(TZ="${TIMEZONE:-UTC}" date +%Y-%m-%d)
DOW=$(TZ="${TIMEZONE:-UTC}" date +%u)  # 1=Mon, 7=Sun
ISSUES=()

log() { echo "[health-check] $*"; }

# ── 1. Archive files for today ───────────────────────────────────────
ARCHIVE_DIR="$REPO_DIR/archive"
if [ "$DOW" = "6" ]; then
  # Saturday: deepdive
  F="$ARCHIVE_DIR/${TODAY}-deepdive.md"
  if [ ! -f "$F" ]; then
    ISSUES+=("Saturday deepdive missing: ${TODAY}-deepdive.md")
  elif [ "$(wc -c < "$F")" -lt 1000 ]; then
    ISSUES+=("Saturday deepdive too small: $(wc -c < "$F") bytes")
  fi
elif [ "$DOW" = "7" ]; then
  # Sunday: week-review
  F="$ARCHIVE_DIR/${TODAY}-week-review.md"
  if [ ! -f "$F" ]; then
    ISSUES+=("Sunday week-review missing: ${TODAY}-week-review.md")
  elif [ "$(wc -c < "$F")" -lt 500 ]; then
    ISSUES+=("Sunday week-review too small")
  fi
else
  # Weekday: review day (day%5==0) OR normal 5 sections
  CURRENT_DAY=$(python3 -c "import json;print(json.load(open('$REPO_DIR/state.json'))['currentDay'])" 2>/dev/null || echo 0)
  IS_REVIEW=0
  [ "$CURRENT_DAY" -gt 0 ] && (( CURRENT_DAY % 5 == 0 )) && IS_REVIEW=1

  if [ "$IS_REVIEW" = "1" ] && [ -f "$ARCHIVE_DIR/${TODAY}-review.md" ]; then
    if [ "$(wc -c < "$ARCHIVE_DIR/${TODAY}-review.md")" -lt 500 ]; then
      ISSUES+=("Review file too small")
    fi
  else
    MISSING=""
    for s in system-design algorithms soft-skills python-craft ai; do
      F="$ARCHIVE_DIR/${TODAY}-${s}.md"
      if [ ! -f "$F" ]; then
        MISSING="$MISSING $s"
      elif [ "$(wc -c < "$F")" -lt 500 ]; then
        MISSING="$MISSING ${s}(too-small)"
      fi
    done
    if [ -n "$MISSING" ]; then
      ISSUES+=("Missing sections for $TODAY:$MISSING")
    fi
  fi
fi

# ── 2. Email sent today? ─────────────────────────────────────────────
SEND_LOG="$REPO_DIR/email-send-log.json"
if [ -f "$SEND_LOG" ]; then
  SENT=$(python3 -c "
import json
d = json.load(open('$SEND_LOG'))
e = d.get('$TODAY')
if not e:
    print('no')
elif e.get('sections', 0) == 0:
    print('zero')
else:
    print(f\"ok:{e.get('sections',0)}:{e.get('recipients',0)}\")
" 2>/dev/null || echo "error")
  case "$SENT" in
    no)    ISSUES+=("No email sent today");;
    zero)  ISSUES+=("Email log says 0 sections sent");;
    error) ISSUES+=("Could not read email-send-log.json");;
    ok:*)  : ;;  # ok
  esac
else
  ISSUES+=("email-send-log.json missing")
fi

# ── 3. Git tree clean and pushed? ────────────────────────────────────
cd "$REPO_DIR"
DIRTY=$(git status --porcelain | head -5)
if [ -n "$DIRTY" ]; then
  ISSUES+=("byte-by-byte has uncommitted changes: $(echo "$DIRTY" | tr '\n' '|' | head -c 200)")
fi
git fetch origin --quiet 2>/dev/null || true
AHEAD=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
BEHIND=$(git log HEAD..origin/main --oneline 2>/dev/null | wc -l | tr -d ' ')
if [ "$AHEAD" != "0" ]; then
  ISSUES+=("byte-by-byte is $AHEAD commits ahead of origin (not pushed)")
fi
if [ "$BEHIND" != "0" ]; then
  ISSUES+=("byte-by-byte is $BEHIND commits behind origin (needs pull)")
fi

# ── 4. Workspace submodule pointer up to date? ───────────────────────
WORKSPACE_DIR="$(dirname "$REPO_DIR")"
if [ -d "$WORKSPACE_DIR/.git" ]; then
  cd "$WORKSPACE_DIR"
  BBB_TRACKED=$(git ls-tree HEAD byte-by-byte 2>/dev/null | awk '{print $3}')
  BBB_HEAD=$(cd "$REPO_DIR" && git rev-parse HEAD)
  if [ -n "$BBB_TRACKED" ] && [ "$BBB_TRACKED" != "$BBB_HEAD" ]; then
    ISSUES+=("Workspace repo points at byte-by-byte ${BBB_TRACKED:0:8}, but HEAD is ${BBB_HEAD:0:8}")
  fi
fi

# ── Report ───────────────────────────────────────────────────────────
if [ ${#ISSUES[@]} -eq 0 ]; then
  log "✅ All checks passed for $TODAY"
  exit 0
fi

MSG="⚠️ byte-by-byte health-check FAILED ($TODAY):"$'\n'
for i in "${ISSUES[@]}"; do
  MSG+="• $i"$'\n'
done

log "$MSG"

# Alert via the real transport (openclaw + TELEGRAM_TARGET). The old gate on
# TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID was dead code — those vars don't exist.
python3 "$REPO_DIR/scripts/send-telegram.py" "$MSG" 2>/dev/null || \
  log "Telegram alert failed (non-critical)"

exit 1
