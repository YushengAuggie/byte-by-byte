#!/usr/bin/env bash
# byte-by-byte daily content generator
# Called by a single OpenClaw cron job. Orchestrates all 5 sections sequentially.
# Usage: ./scripts/generate.sh

set -euo pipefail

REPO_DIR="/Users/davidding/.openclaw/workspace/byte-by-byte"
STATE_FILE="$REPO_DIR/state.json"
CONTENT_DIR="$REPO_DIR/content"
ARCHIVE_DIR="$REPO_DIR/archive"
SCRIPTS_DIR="$REPO_DIR/scripts"
TODAY=$(date +%Y-%m-%d)

# Ensure archive dir exists
mkdir -p "$ARCHIVE_DIR"

# ── Read current state ──────────────────────────────────────────────
read_state() {
  cat "$STATE_FILE"
}

get_index() {
  local field="$1"
  python3 -c "import json; print(json.load(open('$STATE_FILE'))['$field'])"
}

# ── Atomic state update ─────────────────────────────────────────────
# Updates one field at a time with proper JSON handling
update_state() {
  local field="$1"
  local value="$2"
  python3 -c "
import json
with open('$STATE_FILE', 'r') as f:
    state = json.load(f)
state['$field'] = $value
state['lastSentDate'] = '$TODAY'
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
"
}

# ── Get topic from content JSON ──────────────────────────────────────
get_topic() {
  local file="$1"
  local index="$2"
  python3 -c "
import json
with open('$file') as f:
    items = json.load(f)
idx = min(int('$index'), len(items) - 1)
print(json.dumps(items[idx]))
"
}

# ── Output files for OpenClaw to send ────────────────────────────────
# Each section writes to a numbered output file
# The cron job prompt reads these and sends them as messages

echo "=== byte-by-byte generator ==="
echo "Date: $TODAY"
echo "State: $(read_state)"
echo ""

# ── Section 1: System Design ────────────────────────────────────────
SD_INDEX=$(get_index "systemDesignIndex")
SD_TOPIC=$(get_topic "$CONTENT_DIR/system-design.json" "$SD_INDEX")
SD_TITLE=$(echo "$SD_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['title'])")
SD_CATEGORY=$(echo "$SD_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['category'])")
SD_DIFFICULTY=$(echo "$SD_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['difficulty'])")
SD_DAY=$((SD_INDEX + 1))

cat > /tmp/bbb-section-1.txt << PROMPT_END
SECTION: System Design
DAY: $SD_DAY
TOPIC: $SD_TITLE
CATEGORY: $SD_CATEGORY
DIFFICULTY: $SD_DIFFICULTY
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-system-design.md
PROMPT_END

update_state "systemDesignIndex" "$((SD_INDEX + 1))"
echo "✓ Section 1 prepared: System Design Day $SD_DAY — $SD_TITLE"

# ── Section 2: Algorithms (LeetCode) ────────────────────────────────
LC_INDEX=$(get_index "leetcodeIndex")
LC_TOPIC=$(get_topic "$CONTENT_DIR/neetcode-150.json" "$LC_INDEX")
LC_TITLE=$(echo "$LC_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['title'])")
LC_NUM=$(echo "$LC_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['leetcode_num'])")
LC_PATTERN=$(echo "$LC_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['pattern'])")
LC_DIFF=$(echo "$LC_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['difficulty'])")
LC_URL=$(echo "$LC_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['url'])")
LC_DAY=$((LC_INDEX + 1))

cat > /tmp/bbb-section-2.txt << PROMPT_END
SECTION: Algorithms
DAY: $LC_DAY
TITLE: $LC_TITLE
LEETCODE_NUM: $LC_NUM
PATTERN: $LC_PATTERN
DIFFICULTY: $LC_DIFF
URL: $LC_URL
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-algorithms.md
PROMPT_END

update_state "leetcodeIndex" "$((LC_INDEX + 1))"
echo "✓ Section 2 prepared: Algorithms Day $LC_DAY — #$LC_NUM $LC_TITLE ($LC_PATTERN)"

# ── Section 3: Soft Skills ──────────────────────────────────────────
BH_INDEX=$(get_index "behavioralIndex")
BH_TOPIC=$(get_topic "$CONTENT_DIR/behavioral.json" "$BH_INDEX")
BH_QUESTION=$(echo "$BH_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['question'])")
BH_CATEGORY=$(echo "$BH_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['category'])")
BH_LEVEL=$(echo "$BH_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['level'])")
BH_DAY=$((BH_INDEX + 1))

cat > /tmp/bbb-section-3.txt << PROMPT_END
SECTION: Soft Skills
DAY: $BH_DAY
QUESTION: $BH_QUESTION
CATEGORY: $BH_CATEGORY
LEVEL: $BH_LEVEL
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-soft-skills.md
PROMPT_END

update_state "behavioralIndex" "$((BH_INDEX + 1))"
echo "✓ Section 3 prepared: Soft Skills Day $BH_DAY — $BH_CATEGORY"

# ── Section 4: Frontend ─────────────────────────────────────────────
FE_INDEX=$(get_index "frontendIndex")
FE_TOPIC=$(get_topic "$CONTENT_DIR/frontend.json" "$FE_INDEX")
FE_TITLE=$(echo "$FE_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['title'])")
FE_CATEGORY=$(echo "$FE_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['category'])")
FE_WEEK=$(echo "$FE_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['week'])")
FE_DAY=$((FE_INDEX + 1))

cat > /tmp/bbb-section-4.txt << PROMPT_END
SECTION: Frontend
DAY: $FE_DAY
TITLE: $FE_TITLE
CATEGORY: $FE_CATEGORY
WEEK: $FE_WEEK
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-frontend.md
PROMPT_END

update_state "frontendIndex" "$((FE_INDEX + 1))"
echo "✓ Section 4 prepared: Frontend Day $FE_DAY — $FE_TITLE"

# ── Section 5: AI ───────────────────────────────────────────────────
AI_INDEX=$(get_index "aiTopicIndex")
CURRENT_DAY=$(get_index "currentDay")
AI_DAY=$((CURRENT_DAY + 1))

# Odd days = NEWS, Even days = CONCEPT
if (( AI_DAY % 2 == 1 )); then
  AI_MODE="NEWS"
  AI_TITLE="今日AI动态 / AI News Today"
  cat > /tmp/bbb-section-5.txt << PROMPT_END
SECTION: AI
DAY: $AI_DAY
MODE: NEWS
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-ai.md
PROMPT_END
else
  AI_MODE="CONCEPT"
  AI_TOPIC=$(get_topic "$CONTENT_DIR/ai-topics.json" "$AI_INDEX")
  AI_TITLE=$(echo "$AI_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['title'])")
  AI_CAT=$(echo "$AI_TOPIC" | python3 -c "import json,sys; print(json.load(sys.stdin)['category'])")
  cat > /tmp/bbb-section-5.txt << PROMPT_END
SECTION: AI
DAY: $AI_DAY
MODE: CONCEPT
TITLE: $AI_TITLE
CATEGORY: $AI_CAT
ARCHIVE_PATH: $ARCHIVE_DIR/${TODAY}-ai.md
PROMPT_END
  update_state "aiTopicIndex" "$((AI_INDEX + 1))"
fi

update_state "currentDay" "$AI_DAY"
echo "✓ Section 5 prepared: AI Day $AI_DAY — $AI_MODE"

# ── Summary ──────────────────────────────────────────────────────────
echo ""
echo "=== All 5 sections prepared ==="
echo "State updated: $(read_state)"
echo ""
echo "Section files written to /tmp/bbb-section-{1..5}.txt"
echo "Cron job should now generate content for each section and send via Telegram."
