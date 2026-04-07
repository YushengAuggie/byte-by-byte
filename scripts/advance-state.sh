#!/usr/bin/env bash
# byte-by-byte: Verify archive files exist, THEN advance state.json.
# This is Phase 2 — only runs after the agent has written all archive files.
# Exits with code 1 if any required files are missing.
# Usage: ./scripts/advance-state.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$REPO_DIR/config.env"

STATE_FILE="$BBB_REPO_DIR/state.json"
CONTENT_DIR="$BBB_REPO_DIR/content"
ARCHIVE_DIR="$BBB_REPO_DIR/archive"
TODAY=$(date +%Y-%m-%d)

echo "=== byte-by-byte: advance state ==="
echo "Date: $TODAY"

# ── Read planned day info ────────────────────────────────────────────
if [ ! -f /tmp/bbb-day-info.json ]; then
  echo "❌ /tmp/bbb-day-info.json not found. Run generate.sh first."
  exit 1
fi

NEXT_DAY=$(python3 -c "import json; print(json.load(open('/tmp/bbb-day-info.json'))['nextDay'])")
DIFFICULTY_PHASE=$(python3 -c "import json; print(json.load(open('/tmp/bbb-day-info.json'))['difficultyPhase'])")

echo "Planned: Day $NEXT_DAY ($DIFFICULTY_PHASE)"

# ── Check if already advanced ────────────────────────────────────────
CURRENT_DAY=$(python3 -c "import json; print(json.load(open('$STATE_FILE'))['currentDay'])")
if [ "$CURRENT_DAY" -ge "$NEXT_DAY" ]; then
  echo "✅ State already at Day $CURRENT_DAY (>= $NEXT_DAY). Nothing to advance."
  exit 0
fi

# ── Detect review vs normal day ──────────────────────────────────────
IS_REVIEW=0
if (( NEXT_DAY % 5 == 0 )); then
  IS_REVIEW=1
fi

# ── Verify archive files ────────────────────────────────────────────
MISSING=0
if [ "$IS_REVIEW" -eq 1 ]; then
  echo "Review day — checking review archive..."
  REVIEW_FILE="$ARCHIVE_DIR/${TODAY}-review.md"
  if [ ! -f "$REVIEW_FILE" ]; then
    echo "❌ MISSING: $REVIEW_FILE"
    MISSING=1
  else
    SIZE=$(wc -c < "$REVIEW_FILE")
    if [ "$SIZE" -lt 100 ]; then
      echo "❌ TOO SMALL: $REVIEW_FILE ($SIZE bytes)"
      MISSING=1
    else
      echo "✅ review: $SIZE bytes"
    fi
  fi
else
  echo "Normal day — checking 5 section archives..."
  for section in system-design algorithms soft-skills frontend ai; do
    FILE="$ARCHIVE_DIR/${TODAY}-${section}.md"
    if [ ! -f "$FILE" ]; then
      echo "❌ MISSING: $FILE"
      MISSING=1
    else
      SIZE=$(wc -c < "$FILE")
      # Check for placeholder markers (deep dive day stubs, etc.)
      if grep -qi "placeholder\|deep dive day\|content is not generated\|deepdive\.md\|week-review\.md" "$FILE" 2>/dev/null; then
        echo "⚠️ PLACEHOLDER: $FILE ($SIZE bytes) — stub file, skipping"
        MISSING=1
      elif [ "$SIZE" -lt 500 ]; then
        echo "❌ TOO SMALL: $FILE ($SIZE bytes) — likely a placeholder stub"
        MISSING=1
      else
        echo "✅ ${section}: $SIZE bytes"
      fi
    fi
  done
fi

if [ "$MISSING" -eq 1 ]; then
  echo ""
  echo "❌ ABORTING: Archive files missing or too small."
  echo "State will NOT be advanced. Fix the missing files and re-run."
  exit 1
fi

# ── All files verified — advance state ───────────────────────────────
echo ""
echo "All archive files verified. Advancing state..."

python3 << PYEOF
import json, os

state_file = "$STATE_FILE"
content_dir = "$CONTENT_DIR"
next_day = $NEXT_DAY
today = "$TODAY"
difficulty_phase = "$DIFFICULTY_PHASE"
is_review = $IS_REVIEW

with open(state_file) as f:
    state = json.load(f)

if is_review:
    # Review day: advance currentDay + mark review + add history entry
    state['currentDay'] = next_day
    state['lastSentDate'] = today
    state['lastReviewDay'] = str(next_day)
    if 'reviewDaysCompleted' not in state:
        state['reviewDaysCompleted'] = []
    if next_day not in state['reviewDaysCompleted']:
        state['reviewDaysCompleted'].append(next_day)
    # Also add a history entry for review days (was previously missing)
    if 'history' not in state:
        state['history'] = []
    state['history'].append({
        'day': next_day,
        'date': today,
        'difficultyPhase': difficulty_phase,
        'sections': {'review': {'title': f'Review Day {next_day}'}}
    })
    print(f"✅ State advanced to Day {next_day} (review day)")
else:
    # Normal day: advance all indices + add history entry
    # Read section info to get topic titles
    sections_data = {}
    section_files = {
        1: ('system_design', 'systemDesignIndex', 'TOPIC'),
        2: ('algorithms', 'leetcodeIndex', 'TITLE'),
        3: ('soft_skills', 'behavioralIndex', 'QUESTION'),
        4: ('frontend', 'frontendIndex', 'TITLE'),
        5: ('ai', 'aiTopicIndex', None),
    }

    for n, (key, index_key, title_field) in section_files.items():
        section_path = f"/tmp/bbb-section-{n}.txt"
        if os.path.exists(section_path):
            info = {}
            with open(section_path) as f:
                for line in f:
                    if ':' in line:
                        k, v = line.split(':', 1)
                        info[k.strip()] = v.strip()

            # Advance index (except AI NEWS mode which doesn't advance)
            if index_key and index_key in state:
                if key == 'ai' and info.get('MODE') == 'NEWS':
                    pass  # NEWS doesn't consume an ai topic
                else:
                    old_val = state[index_key]
                    state[index_key] = old_val + 1

            # Record title for history
            if title_field and title_field in info:
                title_key = 'question' if title_field == 'QUESTION' else 'title'
                sections_data[key] = {title_key: info[title_field]}
            elif key == 'ai':
                mode = info.get('MODE', 'NEWS')
                if mode == 'NEWS':
                    sections_data[key] = {'title': 'AI News Roundup'}
                else:
                    sections_data[key] = {'title': info.get('TITLE', 'AI Concept')}

    # Add history entry
    if 'history' not in state:
        state['history'] = []
    state['history'].append({
        'day': next_day,
        'date': today,
        'difficultyPhase': difficulty_phase,
        'sections': sections_data
    })

    state['currentDay'] = next_day
    state['lastSentDate'] = today
    print(f"✅ State advanced to Day {next_day}")
    print(f"   Indices: SD={state['systemDesignIndex']} LC={state['leetcodeIndex']} BH={state['behavioralIndex']} FE={state['frontendIndex']} AI={state['aiTopicIndex']}")

with open(state_file, 'w') as f:
    json.dump(state, f, indent=2)

print(f"   History: {[h['day'] for h in state.get('history',[])]}")
PYEOF

echo ""
echo "=== State advanced successfully ==="
