#!/usr/bin/env bash
# byte-by-byte content exhaustion checker
# Reads state.json and content/*.json to calculate remaining days per section.
# Outputs a WARNING if any section has ≤5 days remaining.
# Usage: ./scripts/check-exhaustion.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$REPO_DIR/config.env"

STATE_FILE="$BBB_REPO_DIR/state.json"
CONTENT_DIR="$BBB_REPO_DIR/content"
WARN_THRESHOLD=10
CRITICAL_THRESHOLD=5

echo "=== byte-by-byte content exhaustion check ==="
echo ""

export BBB_REPO_DIR WARN_THRESHOLD CRITICAL_THRESHOLD

python3 - << 'EOF'
import json
import os
import sys

state_file = os.environ.get('BBB_REPO_DIR', '') + '/state.json'
content_dir = os.environ.get('BBB_REPO_DIR', '') + '/content'
warn_threshold = int(os.environ.get('WARN_THRESHOLD', '10'))
critical_threshold = int(os.environ.get('CRITICAL_THRESHOLD', '5'))

# Read state
with open(state_file) as f:
    state = json.load(f)

# Define sections: (label, state_key, content_file)
sections = [
    ("system_design", "systemDesignIndex", "system-design.json"),
    ("algorithms",    "leetcodeIndex",     "neetcode-150.json"),
    ("behavioral",    "behavioralIndex",   "behavioral.json"),
    ("frontend",      "frontendIndex",     "frontend.json"),
    ("ai_concepts",   "aiTopicIndex",      "ai-topics.json"),
]

warnings = []
criticals = []
all_ok = True

for label, state_key, content_file in sections:
    content_path = os.path.join(content_dir, content_file)
    try:
        with open(content_path) as f:
            items = json.load(f)
        total = len(items)
        used = state.get(state_key, 0)
        remaining = total - used

        if remaining <= critical_threshold:
            icon = "🚨"
            criticals.append((label, remaining, used, total))
            all_ok = False
        elif remaining <= warn_threshold:
            icon = "⚠️"
            warnings.append((label, remaining, used, total))
            all_ok = False
        else:
            icon = "✅"

        print(f"  {icon} {label}: {remaining} days remaining ({used}/{total} used)")

    except FileNotFoundError:
        print(f"  ❓ {label}: content file not found ({content_file})")
        all_ok = False

print("")

if criticals:
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🚨 CRITICAL — content nearly exhausted:")
    print("")
    for label, remaining, used, total in criticals:
        print(f"  🚨 {label}: only {remaining} day(s) remaining ({used}/{total} used)")
    print("")
    print("  → ACTION REQUIRED: Add more topics to the corresponding content/*.json files")
    print("  → Open content/*.json and append additional entries to avoid gaps")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if warnings:
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("WARNINGS — content running low:")
    print("")
    for label, remaining, used, total in warnings:
        print(f"  ⚠️  {label}: {remaining} days remaining ({used}/{total} used)")
    print("")
    print("  → Action: Add more topics to the corresponding content/*.json file")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if not all_ok:
    sys.exit(1)
else:
    print("✅ All sections have adequate content. No action needed.")
    sys.exit(0)
EOF
EOF_STATUS=$?

echo ""
echo "=== Check complete ==="
exit $EOF_STATUS
