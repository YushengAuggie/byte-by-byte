#!/usr/bin/env bash
# byte-by-byte: commit and push today's archive + state
# Usage: ./scripts/commit.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$REPO_DIR/config.env"

cd "$BBB_REPO_DIR"
TODAY=$(date +%Y-%m-%d)
STATE=$(python3 -c "import json; s=json.load(open('state.json')); print(s['currentDay'],s.get('lastSentDate','?'),s.get('leetcodeIndex',0),s.get('systemDesignIndex',0),s.get('frontendIndex',0),s.get('behavioralIndex',0),s.get('aiTopicIndex',0))")
CURRENT_DAY=$(echo "$STATE" | cut -d' ' -f1)
LAST_DATE=$(echo "$STATE" | cut -d' ' -f2)
ALGO_IDX=$(echo "$STATE" | cut -d' ' -f3)
SD_IDX=$(echo "$STATE" | cut -d' ' -f4)
FE_IDX=$(echo "$STATE" | cut -d' ' -f5)
SOFT_IDX=$(echo "$STATE" | cut -d' ' -f6)
AI_IDX=$(echo "$STATE" | cut -d' ' -f7)

# Update README progress table
python3 - <<PYEOF
import re, pathlib

readme = pathlib.Path("README.md").read_text()
table = """| Field | Value |
|-------|-------|
| **Current Day** | Day ${CURRENT_DAY} |
| **Last Sent** | ${LAST_DATE} |
| **Algorithms** | ${ALGO_IDX} / 150 (NeetCode 150) |
| **System Design** | ${SD_IDX} / 40 |
| **Frontend** | ${FE_IDX} / 50 |
| **Soft Skills** | ${SOFT_IDX} / 40 |
| **AI Topics** | ${AI_IDX} / 30 |"""
readme = re.sub(
    r'(<!-- AUTO-UPDATED.*?-->\n\n)\|.*?\n\n',
    r'\1' + table + '\n\n',
    readme, flags=re.DOTALL
)
pathlib.Path("README.md").write_text(readme)
print("✓ Updated README progress table")
PYEOF

# Regenerate archive index
if python3 scripts/generate-index.py 2>/dev/null; then
  echo "✓ Regenerated docs/archive index"
fi

git add -A

if git diff --cached --quiet; then
  echo "Nothing to commit."
  exit 0
fi

git commit -m "Day $CURRENT_DAY ($TODAY): daily content generated"

if ! git push 2>&1; then
  echo "Push failed, trying pull --rebase..."
  git pull --rebase
  git push
fi

echo "✓ Committed and pushed Day $CURRENT_DAY"
