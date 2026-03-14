#!/usr/bin/env bash
# byte-by-byte daily content generator
# Reads config.env, picks today's topics, updates state atomically.
# On review days (day % 5 == 0), writes /tmp/bbb-review.txt instead.
# Usage: ./scripts/generate.sh

set -euo pipefail

# ── Load config ──────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$REPO_DIR/config.env"

STATE_FILE="$BBB_REPO_DIR/state.json"
CONTENT_DIR="$BBB_REPO_DIR/content"
ARCHIVE_DIR="$BBB_REPO_DIR/archive"
DIFFICULTY_MAP="$CONTENT_DIR/difficulty-map.json"
TODAY=$(date +%Y-%m-%d)

mkdir -p "$ARCHIVE_DIR"

# ── Helpers ──────────────────────────────────────────────────────────
get_index() {
  python3 -c "import json; print(json.load(open('$STATE_FILE'))['$1'])"
}

get_state_field() {
  python3 -c "import json; d = json.load(open('$STATE_FILE')); print(d.get('$1', 'null'))"
}

update_state() {
  python3 -c "
import json
with open('$STATE_FILE', 'r') as f:
    state = json.load(f)
state['$1'] = $2
state['lastSentDate'] = '$TODAY'
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
"
}

update_state_str() {
  python3 -c "
import json
with open('$STATE_FILE', 'r') as f:
    state = json.load(f)
state['$1'] = '$2'
state['lastSentDate'] = '$TODAY'
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
"
}

get_topic() {
  python3 -c "
import json
with open('$1') as f:
    items = json.load(f)
idx = min(int('$2'), len(items) - 1)
print(json.dumps(items[idx]))
"
}

extract() {
  echo "$1" | python3 -c "import json,sys; print(json.load(sys.stdin)['$2'])"
}

get_difficulty_phase() {
  local day=$1
  python3 -c "
import json
day = $day
with open('$DIFFICULTY_MAP') as f:
    dm = json.load(f)
for phase in dm['phases']:
    lo, hi = phase['dayRange']
    if lo <= day <= hi:
        print(phase['name'])
        exit()
print('Expert')
"
}

get_history_topics() {
  # Get topic titles from history for review day
  python3 -c "
import json
with open('$STATE_FILE') as f:
    state = json.load(f)
history = state.get('history', [])
# Last 4 entries (days before this review day)
recent = history[-4:] if len(history) >= 4 else history
for entry in recent:
    day = entry.get('day', '?')
    print(f\"Day {day}:\")
    for section, info in entry.get('sections', {}).items():
        title = info.get('title', info.get('question', 'Unknown'))
        print(f\"  [{section}] {title}\")
"
}

append_history() {
  # Append today's topics to history array in state.json
  python3 -c "
import json
with open('$STATE_FILE', 'r') as f:
    state = json.load(f)
if 'history' not in state:
    state['history'] = []
state['history'].append($1)
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
"
}

# ── Main ─────────────────────────────────────────────────────────────
echo "=== byte-by-byte generator ==="
echo "Date: $TODAY"
echo "Repo: $BBB_REPO_DIR"
echo ""

# Get current day (pre-increment)
CURRENT_DAY=$(get_index "currentDay")
NEXT_DAY=$((CURRENT_DAY + 1))

# ── Difficulty Phase ─────────────────────────────────────────────────
DIFFICULTY_PHASE=$(get_difficulty_phase "$NEXT_DAY")
echo "Day: $NEXT_DAY | Difficulty Phase: $DIFFICULTY_PHASE"
echo ""

# ── Review Day Detection ──────────────────────────────────────────────
IS_REVIEW_DAY=0
if (( NEXT_DAY % 5 == 0 )); then
  IS_REVIEW_DAY=1
fi

if (( IS_REVIEW_DAY == 1 )); then
  echo "🔄 Day $NEXT_DAY is a REVIEW DAY (day % 5 == 0)"
  echo ""

  # Gather history for the past 4 days
  HISTORY_TOPICS=$(get_history_topics)

  cat > /tmp/bbb-review.txt << EOF
REVIEW_DAY: $NEXT_DAY
DATE: $TODAY
DIFFICULTY_PHASE: $DIFFICULTY_PHASE
LOOKBACK_DAYS: 4
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-review.md

PAST_TOPICS:
$HISTORY_TOPICS

INSTRUCTIONS:
Generate a review quiz with 3 mini-quizzes drawn from the past 4 days of content above.
Format each as:
  Q[n]: [Section] Short question referencing the topic
  A[n]: Concise answer with the key insight

Review day format (see cron/daily-prompt.md for full instructions).
EOF

  echo "✓ Review file written to /tmp/bbb-review.txt"
  echo ""

  # Update state: increment day, mark as review
  update_state "currentDay" "$NEXT_DAY"
  update_state_str "lastReviewDay" "$NEXT_DAY"
  update_state_str "lastSentDate" "$TODAY"

  # Also initialize review tracking if not present
  python3 -c "
import json
with open('$STATE_FILE', 'r') as f:
    state = json.load(f)
if 'reviewDaysCompleted' not in state:
    state['reviewDaysCompleted'] = []
if $NEXT_DAY not in state['reviewDaysCompleted']:
    state['reviewDaysCompleted'].append($NEXT_DAY)
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
"
  echo "✓ State updated with review tracking"
  echo ""
  echo "=== Review day setup complete ==="
  echo "→ Read /tmp/bbb-review.txt and cron/daily-prompt.md for review generation instructions"
  exit 0
fi

# ── Normal Day: Generate 5 Sections ──────────────────────────────────
echo "📚 Day $NEXT_DAY — Normal content day (Phase: $DIFFICULTY_PHASE)"
echo ""

# Section 1: System Design
SD_INDEX=$(get_index "systemDesignIndex")
SD_TOPIC=$(get_topic "$CONTENT_DIR/system-design.json" "$SD_INDEX")
SD_DAY=$((SD_INDEX + 1))
cat > /tmp/bbb-section-1.txt << EOF
SECTION: System Design
DAY: $SD_DAY
TOPIC: $(extract "$SD_TOPIC" "title")
CATEGORY: $(extract "$SD_TOPIC" "category")
DIFFICULTY: $(extract "$SD_TOPIC" "difficulty")
DIFFICULTY_PHASE: $DIFFICULTY_PHASE
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-system-design.md
EOF
update_state "systemDesignIndex" "$((SD_INDEX + 1))"
echo "✓ Section 1: System Design Day $SD_DAY — $(extract "$SD_TOPIC" "title")"

# Section 2: Algorithms
LC_INDEX=$(get_index "leetcodeIndex")
LC_TOPIC=$(get_topic "$CONTENT_DIR/neetcode-150.json" "$LC_INDEX")
LC_DAY=$((LC_INDEX + 1))
cat > /tmp/bbb-section-2.txt << EOF
SECTION: Algorithms
DAY: $LC_DAY
TITLE: $(extract "$LC_TOPIC" "title")
LEETCODE_NUM: $(extract "$LC_TOPIC" "leetcode_num")
PATTERN: $(extract "$LC_TOPIC" "pattern")
DIFFICULTY: $(extract "$LC_TOPIC" "difficulty")
DIFFICULTY_PHASE: $DIFFICULTY_PHASE
URL: $(extract "$LC_TOPIC" "url")
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-algorithms.md
EOF
update_state "leetcodeIndex" "$((LC_INDEX + 1))"
echo "✓ Section 2: Algorithms Day $LC_DAY — #$(extract "$LC_TOPIC" "leetcode_num") $(extract "$LC_TOPIC" "title")"

# Section 3: Soft Skills
BH_INDEX=$(get_index "behavioralIndex")
BH_TOPIC=$(get_topic "$CONTENT_DIR/behavioral.json" "$BH_INDEX")
BH_DAY=$((BH_INDEX + 1))
cat > /tmp/bbb-section-3.txt << EOF
SECTION: Soft Skills
DAY: $BH_DAY
QUESTION: $(extract "$BH_TOPIC" "question")
CATEGORY: $(extract "$BH_TOPIC" "category")
LEVEL: $(extract "$BH_TOPIC" "level")
DIFFICULTY_PHASE: $DIFFICULTY_PHASE
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-soft-skills.md
EOF
update_state "behavioralIndex" "$((BH_INDEX + 1))"
echo "✓ Section 3: Soft Skills Day $BH_DAY — $(extract "$BH_TOPIC" "category")"

# Section 4: Frontend
FE_INDEX=$(get_index "frontendIndex")
FE_TOPIC=$(get_topic "$CONTENT_DIR/frontend.json" "$FE_INDEX")
FE_DAY=$((FE_INDEX + 1))
cat > /tmp/bbb-section-4.txt << EOF
SECTION: Frontend
DAY: $FE_DAY
TITLE: $(extract "$FE_TOPIC" "title")
CATEGORY: $(extract "$FE_TOPIC" "category")
WEEK: $(extract "$FE_TOPIC" "week")
DIFFICULTY_PHASE: $DIFFICULTY_PHASE
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-frontend.md
EOF
update_state "frontendIndex" "$((FE_INDEX + 1))"
echo "✓ Section 4: Frontend Day $FE_DAY — $(extract "$FE_TOPIC" "title")"

# Section 5: AI
AI_INDEX=$(get_index "aiTopicIndex")
AI_DAY=$NEXT_DAY

if (( AI_DAY % 2 == 1 )); then
  cat > /tmp/bbb-section-5.txt << EOF
SECTION: AI
DAY: $AI_DAY
MODE: NEWS
DIFFICULTY_PHASE: $DIFFICULTY_PHASE
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-ai.md
EOF
  echo "✓ Section 5: AI Day $AI_DAY — NEWS"
  AI_TITLE="AI News Roundup"
else
  AI_TOPIC=$(get_topic "$CONTENT_DIR/ai-topics.json" "$AI_INDEX")
  AI_TITLE=$(extract "$AI_TOPIC" "title")
  cat > /tmp/bbb-section-5.txt << EOF
SECTION: AI
DAY: $AI_DAY
MODE: CONCEPT
TITLE: $AI_TITLE
CATEGORY: $(extract "$AI_TOPIC" "category")
DIFFICULTY_PHASE: $DIFFICULTY_PHASE
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-ai.md
EOF
  update_state "aiTopicIndex" "$((AI_INDEX + 1))"
  echo "✓ Section 5: AI Day $AI_DAY — CONCEPT: $AI_TITLE"
fi

# ── Update state with today's topics in history ───────────────────────
SD_TITLE=$(extract "$SD_TOPIC" "title")
LC_TITLE=$(extract "$LC_TOPIC" "title")
BH_Q=$(extract "$BH_TOPIC" "question")
FE_TITLE=$(extract "$FE_TOPIC" "title")

append_history "{
  \"day\": $NEXT_DAY,
  \"date\": \"$TODAY\",
  \"difficultyPhase\": \"$DIFFICULTY_PHASE\",
  \"sections\": {
    \"system_design\": {\"title\": $(echo "$SD_TITLE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')},
    \"algorithms\": {\"title\": $(echo "$LC_TITLE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')},
    \"soft_skills\": {\"question\": $(echo "$BH_Q" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')},
    \"frontend\": {\"title\": $(echo "$FE_TITLE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')},
    \"ai\": {\"title\": $(echo "$AI_TITLE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')}
  }
}"

update_state "currentDay" "$NEXT_DAY"

# Clean up any leftover review file from a previous review day
rm -f /tmp/bbb-review.txt

echo ""
echo "=== All 5 sections prepared (Phase: $DIFFICULTY_PHASE) ==="
echo "State: $(cat "$STATE_FILE")"
