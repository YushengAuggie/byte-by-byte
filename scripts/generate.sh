#!/usr/bin/env bash
# byte-by-byte daily content generator
# Reads config.env, picks today's topics, updates state atomically.
# Usage: ./scripts/generate.sh

set -euo pipefail

# ── Load config ──────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$REPO_DIR/config.env"

STATE_FILE="$BBB_REPO_DIR/state.json"
CONTENT_DIR="$BBB_REPO_DIR/content"
ARCHIVE_DIR="$BBB_REPO_DIR/archive"
TODAY=$(date +%Y-%m-%d)

mkdir -p "$ARCHIVE_DIR"

# ── Helpers ──────────────────────────────────────────────────────────
get_index() {
  python3 -c "import json; print(json.load(open('$STATE_FILE'))['$1'])"
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

# ── Main ─────────────────────────────────────────────────────────────
echo "=== byte-by-byte generator ==="
echo "Date: $TODAY"
echo "Repo: $BBB_REPO_DIR"
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
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-frontend.md
EOF
update_state "frontendIndex" "$((FE_INDEX + 1))"
echo "✓ Section 4: Frontend Day $FE_DAY — $(extract "$FE_TOPIC" "title")"

# Section 5: AI
AI_INDEX=$(get_index "aiTopicIndex")
CURRENT_DAY=$(get_index "currentDay")
AI_DAY=$((CURRENT_DAY + 1))

if (( AI_DAY % 2 == 1 )); then
  cat > /tmp/bbb-section-5.txt << EOF
SECTION: AI
DAY: $AI_DAY
MODE: NEWS
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-ai.md
EOF
  echo "✓ Section 5: AI Day $AI_DAY — NEWS"
else
  AI_TOPIC=$(get_topic "$CONTENT_DIR/ai-topics.json" "$AI_INDEX")
  cat > /tmp/bbb-section-5.txt << EOF
SECTION: AI
DAY: $AI_DAY
MODE: CONCEPT
TITLE: $(extract "$AI_TOPIC" "title")
CATEGORY: $(extract "$AI_TOPIC" "category")
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-ai.md
EOF
  update_state "aiTopicIndex" "$((AI_INDEX + 1))"
  echo "✓ Section 5: AI Day $AI_DAY — CONCEPT: $(extract "$AI_TOPIC" "title")"
fi

update_state "currentDay" "$AI_DAY"

echo ""
echo "=== All 5 sections prepared ==="
echo "State: $(cat "$STATE_FILE")"
