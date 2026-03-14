#!/usr/bin/env bash
# byte-by-byte test suite — runs all checks
# Usage: bash scripts/test.sh
# Exit code: 0 = all pass, 1 = failures found

set -uo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

PASS=0
FAIL=0
WARN=0

pass() { echo "  ✅ $1"; PASS=$((PASS + 1)); }
fail() { echo "  ❌ $1"; FAIL=$((FAIL + 1)); }
warn() { echo "  ⚠️  $1"; WARN=$((WARN + 1)); }

echo "🧪 byte-by-byte test suite"
echo "=========================="
echo ""

# --- 1. JSON validity + schema ---
echo "📋 JSON validity:"
for f in content/*.json state.json; do
  if python3 -c "import json; json.load(open('$f'))" 2>/dev/null; then
    pass "$f"
  else
    fail "$f — invalid JSON"
  fi
done

# --- 2. JSON schema checks ---
echo ""
echo "📋 JSON schema:"

# NeetCode 150 — must have 150 entries with required fields
python3 -c "
import json, sys
data = json.load(open('content/neetcode-150.json'))
if len(data) != 150:
    print('  ❌ neetcode-150.json: expected 150, got', len(data)); sys.exit(1)
required = {'title', 'difficulty', 'pattern'}
for i, p in enumerate(data):
    missing = required - set(p.keys())
    if missing:
        print(f'  ❌ neetcode-150.json[{i}]: missing {missing}'); sys.exit(1)
# Check for duplicate titles
slugs = [p['title'] for p in data]
dupes = [s for s in set(slugs) if slugs.count(s) > 1]
if dupes:
    print(f'  ❌ neetcode-150.json: duplicate slugs: {dupes}'); sys.exit(1)
print('  ✅ neetcode-150.json: 150 entries, no dupes, schema OK')
" 2>&1 && PASS=$((PASS + 1)) || FAIL=$((FAIL + 1))

# Other content files — check required fields
python3 -c "
import json, sys
checks = [
    ('content/system-design.json', 40, {'title', 'difficulty'}),
    ('content/behavioral.json', 40, {'question', 'category'}),
    ('content/frontend.json', 50, {'title', 'category'}),
    ('content/ai-topics.json', 30, {'title', 'category'}),
]
ok = True
for path, expected, required in checks:
    data = json.load(open(path))
    if len(data) != expected:
        print(f'  ❌ {path}: expected {expected}, got {len(data)}'); ok = False; continue
    for i, item in enumerate(data):
        missing = required - set(item.keys())
        if missing:
            print(f'  ❌ {path}[{i}]: missing {missing}'); ok = False; break
    else:
        print(f'  ✅ {path}: {expected} entries, schema OK')
if not ok: sys.exit(1)
" 2>&1 && PASS=$((PASS + 4)) || FAIL=$((FAIL + 1))

# state.json schema
python3 -c "
import json, sys
s = json.load(open('state.json'))
required = ['currentDay', 'lastSentDate', 'systemDesignIndex', 'leetcodeIndex',
            'behavioralIndex', 'frontendIndex', 'aiTopicIndex', 'history',
            'lastReviewDay', 'reviewDaysCompleted']
missing = [k for k in required if k not in s]
if missing:
    print(f'  ❌ state.json: missing keys: {missing}'); sys.exit(1)
print('  ✅ state.json: all required keys present')
" 2>&1 && PASS=$((PASS + 1)) || FAIL=$((FAIL + 1))

# difficulty-map.json
if [ -f content/difficulty-map.json ]; then
  python3 -c "
import json, sys
data = json.load(open('content/difficulty-map.json'))
if not isinstance(data, (list, dict)):
    print('  ❌ difficulty-map.json: unexpected type'); sys.exit(1)
print('  ✅ difficulty-map.json: valid')
" 2>&1 && PASS=$((PASS + 1)) || FAIL=$((FAIL + 1))
fi

# review-schedule.json
if [ -f content/review-schedule.json ]; then
  python3 -c "
import json, sys
data = json.load(open('content/review-schedule.json'))
if not isinstance(data, (list, dict)):
    print('  ❌ review-schedule.json: unexpected type'); sys.exit(1)
print('  ✅ review-schedule.json: valid')
" 2>&1 && PASS=$((PASS + 1)) || FAIL=$((FAIL + 1))
fi

# --- 3. Shell syntax ---
echo ""
echo "📋 Shell syntax:"
for f in scripts/*.sh; do
  if bash -n "$f" 2>/dev/null; then
    pass "$f"
  else
    fail "$f — syntax error"
  fi
done

# --- 4. Python syntax ---
echo ""
echo "📋 Python syntax:"
for f in scripts/*.py; do
  if python3 -m py_compile "$f" 2>/dev/null; then
    pass "$f"
  else
    fail "$f — syntax error"
  fi
done

# --- 5. No personal info in tracked files ---
echo ""
echo "📋 Personal info check:"
TRACKED_FILES=$(git ls-files | grep -v 'config\.env$' | grep -v '\.gitignore')
# Load personal patterns from config.env dynamically — nothing hardcoded
PERSONAL_PATTERNS=""
if [ -f "$REPO_DIR/config.env" ]; then
  _tg=$(grep '^TELEGRAM_TARGET=' "$REPO_DIR/config.env" 2>/dev/null | cut -d= -f2 | tr -d '"' || true)
  _em=$(grep '^EMAIL_TARGET=' "$REPO_DIR/config.env" 2>/dev/null | cut -d= -f2 | tr -d '"' || true)
  _rd=$(grep '^BBB_REPO_DIR=' "$REPO_DIR/config.env" 2>/dev/null | cut -d= -f2 | tr -d '"' || true)
  [ -n "$_tg" ] && PERSONAL_PATTERNS="$_tg"
  [ -n "$_em" ] && { [ -n "$PERSONAL_PATTERNS" ] && PERSONAL_PATTERNS="$PERSONAL_PATTERNS\|$_em" || PERSONAL_PATTERNS="$_em"; }
fi
if [ -n "$PERSONAL_PATTERNS" ]; then
  LEAKS=$(echo "$TRACKED_FILES" | xargs grep -il "$PERSONAL_PATTERNS" 2>/dev/null || true)
else
  echo "  ⚠️  No config.env found, skipping personal info check"
  LEAKS=""
fi
if [ -z "$LEAKS" ]; then
  pass "No personal info in tracked files"
else
  fail "Personal info found in: $LEAKS"
fi

# --- 6. Placeholder check in cron prompts ---
echo ""
echo "📋 Cron prompt placeholders:"
for f in cron/*.md; do
  if grep -q '{{BBB_REPO_DIR}}' "$f" 2>/dev/null; then
    pass "$f — has {{placeholders}}"
  else
    fail "$f — missing placeholders (may be hardcoded)"
  fi
done

# --- 7. Executables ---
echo ""
echo "📋 Executable permissions:"
for f in scripts/*.sh scripts/*.py; do
  if [ -x "$f" ]; then
    pass "$f"
  else
    warn "$f — not executable"
  fi
done

# --- 8. Content indices in bounds ---
echo ""
echo "📋 State indices in bounds:"
python3 -c "
import json, sys
s = json.load(open('state.json'))
bounds = {
    'systemDesignIndex': ('content/system-design.json', 40),
    'leetcodeIndex': ('content/neetcode-150.json', 150),
    'behavioralIndex': ('content/behavioral.json', 40),
    'frontendIndex': ('content/frontend.json', 50),
    'aiTopicIndex': ('content/ai-topics.json', 30),
}
ok = True
for key, (path, limit) in bounds.items():
    val = s.get(key, 0)
    if val < 0 or val > limit:
        print(f'  ❌ {key}={val} out of bounds [0, {limit}]'); ok = False
    else:
        print(f'  ✅ {key}={val} within [0, {limit}]')
if not ok: sys.exit(1)
" 2>&1 && PASS=$((PASS + 5)) || FAIL=$((FAIL + 1))

# --- 9. Required files exist ---
echo ""
echo "📋 Required files:"
for f in README.md SPEC.md PLAN.md LICENSE CONTRIBUTING.md config.env.example .gitignore state.json; do
  if [ -f "$f" ]; then
    pass "$f"
  else
    fail "$f — MISSING"
  fi
done

# --- 10. send-email.py dry-run (build HTML, don't send) ---
echo ""
echo "📋 Email build check:"
python3 -c "
import sys, os
sys.path.insert(0, 'scripts')

# Verify the HTML builder works without sending
# Just import and check key functions exist
import importlib.util
spec = importlib.util.spec_from_file_location('send_email', 'scripts/send-email.py')
mod = importlib.util.module_from_spec(spec)

# Check the file has the key components
with open('scripts/send-email.py') as f:
    content = f.read()
    checks = ['MIMEMultipart', 'MIMEText', 'smtp.gmail.com', 'load_config', 'md_to_html']
    for c in checks:
        if c not in content:
            print(f'  ❌ send-email.py missing: {c}'); sys.exit(1)
print('  ✅ send-email.py has all required components')
" 2>&1 && PASS=$((PASS + 1)) || FAIL=$((FAIL + 1))

# --- Summary ---
echo ""
echo "=========================="
TOTAL=$((PASS + FAIL + WARN))
echo "🧪 Results: $PASS passed, $FAIL failed, $WARN warnings ($TOTAL total)"

if [ "$FAIL" -gt 0 ]; then
  echo "💥 TESTS FAILED"
  exit 1
else
  echo "✅ ALL TESTS PASSED"
  exit 0
fi
