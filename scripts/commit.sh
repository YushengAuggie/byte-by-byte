#!/usr/bin/env bash
# byte-by-byte: commit and push today's archive + state
# Usage: ./scripts/commit.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$REPO_DIR/config.env"

cd "$BBB_REPO_DIR"
TODAY=$(date +%Y-%m-%d)
CURRENT_DAY=$(python3 -c "import json; print(json.load(open('state.json'))['currentDay'])")

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
