#!/usr/bin/env bash
# byte-by-byte: commit and push today's archive + state
# Called after all 5 sections have been generated and archived.
# Usage: ./scripts/commit.sh

set -euo pipefail

REPO_DIR="/Users/davidding/.openclaw/workspace/byte-by-byte"
TODAY=$(date +%Y-%m-%d)

cd "$REPO_DIR"

# Get current day from state for commit message
CURRENT_DAY=$(python3 -c "import json; print(json.load(open('state.json'))['currentDay'])")

# Stage all changes
git add -A

# Check if there's anything to commit
if git diff --cached --quiet; then
  echo "Nothing to commit."
  exit 0
fi

# Commit with descriptive message
git commit -m "Day $CURRENT_DAY ($TODAY): daily content generated

Sections delivered:
- System Design
- Algorithms (NeetCode 150)
- Soft Skills
- Frontend
- AI"

# Push with retry
if ! git push 2>&1; then
  echo "Push failed, trying pull --rebase first..."
  git pull --rebase
  git push
fi

echo "✓ Committed and pushed Day $CURRENT_DAY"
