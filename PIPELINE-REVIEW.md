# byte-by-byte Pipeline Review (Reliability & Code Quality)

Date: 2026-04-04
Reviewer: subagent (pipeline/code audit)
Repo: `/Users/davidding/.openclaw/workspace/byte-by-byte`

## Executive summary (what’s most likely to bite again)

**Highest-risk failure modes observed in code:**

1. **`generate.sh` idempotency guard is wrong.** It uses `state.json:lastSentDate` to decide “already generated for today”, but `lastSentDate` is also set by `advance-state.sh` (and represents sent/advanced day, not “generated”). This can skip generation incorrectly (and can also mask partial generation). This is a prime source of “nothing generated” or stale content.
2. **Partial-day sends are allowed by `verify-and-send.sh` + `send-email.py`.** `verify-and-send.sh` explicitly proceeds with <5 sections; `send-email.py` sends whatever it finds (and can send just 1 section). This matches `email-send-log.json` showing multiple days with `sections: 1`. If “sections: 1” is ever unintended, this is the culprit.
3. **Race between generation (8:00) and review/send (8:05) is not handled by a completion signal.** There’s no lockfile or “done” marker; review may start while generation/LLM writing is incomplete.
4. **State advancement depends on `/tmp/*` files, which are not durable across reboots and can be clobbered.** `advance-state.sh` reads `/tmp/bbb-day-info.json` and section files `/tmp/bbb-section-*.txt`. If `/tmp` is cleared or overwritten, state advancement can’t proceed or can proceed with mismatched info.
5. **Doorkeeper in `send-email.py` helps but is still bypassable for review/weekend content.** Placeholder filtering/length thresholds are not uniformly applied across review/weekend paths.

**Recommendation:** Introduce a single durable “run artifact” directory per date (e.g., `runs/YYYY-MM-DD/`) with:
- `plan.json` (topics chosen)
- `generation_complete` (touch file)
- `qa_complete` (touch file)
- `sent_email.json`
And make all scripts read those artifacts rather than `/tmp`.

---

## 1) Script-by-script review (`scripts/`)

### `scripts/generate.sh`
**Purpose:** Phase 1: pick topics + write per-section plan to `/tmp/bbb-section-*.txt` OR write `/tmp/bbb-review.txt`.

**Key reliability issues / edge cases**

- **Idempotency guard uses `lastSentDate` incorrectly.**
  - Code:
    ```bash
    LAST_SENT=$(python3 -c "... state.get('lastSentDate','')")
    if [ "$LAST_SENT" = "$TODAY" ]; then
      echo "Already generated... Skipping."
      exit 0
    fi
    ```
  - But `lastSentDate` is set in `advance-state.sh` (after verifying archives) and is semantically “state advanced / day considered sent”, not “generation already done”.
  - Consequence: if state advanced early (or erroneously), `generate.sh` will refuse to generate even if archives are missing/corrupt. This can lead to missed sends or stale output.

- **Depends on config variable indirection**: `STATE_FILE="$BBB_REPO_DIR/state.json"` while `REPO_DIR` is already that directory. If `config.env` has wrong `BBB_REPO_DIR`, it points to wrong state.

- **Index bounds / exhaustion not handled.** It clamps topic index with `min(idx, len(items)-1)`, so when indices exceed content length, it silently repeats the last topic forever.
  - This is a **silent failure** (keeps “working” but content repeats).
  - Better: fail hard if index >= len(items).

- **Writes to `/tmp` only; not atomic**: if multiple runs overlap, files can interleave.

- **Review day detection (day % 5 == 0) is hard-coded**. OK if spec, but ensure Sunday/Saturday special formats are aligned with other prompts (currently weekend handled mostly by prompts + archive naming, not by this script).

**Suggested fixes**
- Replace idempotency guard with a **per-date sentinel**:
  - e.g., if `archive/${TODAY}-*.md` already exists AND passes size/placeholder checks, skip.
  - Or create `runs/${TODAY}/planned.json` and check existence.
- Add strict bounds check for indices and abort if out-of-range.
- Use a lock (`flock`) to prevent concurrent `generate.sh` runs.

---

### `scripts/advance-state.sh`
**Purpose:** Phase 2: verify archives exist and look non-stub; then advance `state.json` and indices.

**Good:**
- Checks missing files and “too small” content; checks some placeholder markers.
- Has an “already advanced” guard: if `currentDay >= nextDay`, exit 0.

**Partial execution / idempotency issues (Task #5)**

- **Not crash-safe / not atomic state update**
  - Writes state.json in-place. If interrupted during write (power loss), state.json can corrupt.
  - Suggested: write to `state.json.tmp` then `mv` atomically.

- **Depends on `/tmp/bbb-day-info.json`**
  - If `/tmp` cleared, it refuses to run. This blocks advancement even if archives exist.
  - Also if `/tmp/bbb-day-info.json` is from a previous day but archives are today’s, it could advance using stale `nextDay` (guarded somewhat by `currentDay >= nextDay`, but mismatch possible if old info has bigger nextDay).

- **Double-run safety**
  - If run twice with same `/tmp/bbb-day-info.json`, second run exits 0 due to `currentDay >= nextDay`.
  - That is good, but only if `currentDay` advanced successfully the first time.

- **Index advancement depends on presence of `/tmp/bbb-section-*.txt`**
  - If those files are missing (but archives exist), it will still set `currentDay` and `lastSentDate`, but may not advance indices or record history correctly because it only iterates section files if they exist.
  - This can create a mismatch: content generated/archived but indices not advanced -> duplicates later.

- **Placeholder detection is imperfect**
  - Uses `grep -qi "placeholder\|deep dive day\|content is not generated\|deepdive\.md\|week-review\.md"`.
  - Historical placeholder bug might include other patterns (“TBD”, “coming soon”, Chinese equivalents). Consider a canonical header marker in stubs.

**Suggested fixes**
- Stop depending on `/tmp` for metadata; derive `NEXT_DAY` from state directly (currentDay + 1) and confirm against archive contents.
- Make state update atomic (temp file + rename).
- Make index advancement deterministic from `state` (increment by 1 each run for normal day; AI depends on NEWS/CONCEPT mode which should be derivable from archive or plan file).

---

### `scripts/send-email.py`
**Purpose:** Build HTML digest from archive files and send via Gmail SMTP. Also dedup via `email-send-log.json`.

**Doorkeeper review (Task #2)**

Current `validate_email_content()` checks:
- no empty content
- placeholder words
- min plain text length 800 per section
- unclosed code blocks (` ``` ` count)

**Does it catch the historical failure modes?**
- **Placeholder files sent as real email content**: partially.
  - It checks for several placeholder markers.
  - However, it only checks placeholders *in the content that made it into `plain_parts`*.
  - `send-email.py` already skips files containing markers in `PLACEHOLDER_MARKERS` for weekday sections, but **review/weekend content is not placeholder-filtered before doorkeeper**.

**Gaps / additional checks recommended**

1. **Validate expected number of sections for day type**
   - For weekday: require 5 sections unless explicitly configured to allow partial send.
   - For review day: require 1 section and it must be `review`.
   - For weekend: require exactly one of `deepdive` or `week-review` (or both? define explicitly).
   - Right now, it will happily send 1 weekday section (and log `sections=1`).

2. **Ensure no template artifacts**
   - Common LLM/template markers: `{{`, `}}`, `TODO`, `FIXME`, `TBD`, `[link]`, “(fill in)” etc.

3. **Minimum content length 800**
   - 800 chars per section is **probably OK** for weekday sections (bilingual content is usually long).
   - But it may be too high for a concise section (e.g., short Soft Skills) and too low for catching “1 paragraph placeholder”.
   - Better: per-section thresholds:
     - System design / algorithms / frontend: e.g., 1200+
     - Soft skills: e.g., 600+
     - AI news: variable; but require at least N links and N bullets.

4. **Link sanity**
   - If section contains `References`, ensure at least 1 URL.
   - For algorithms: ensure LeetCode URL matches `https://leetcode.com/problems/<slug>/`.

5. **Detect “wrong day” send**
   - Cross-check header date inside content if present; or ensure archive filename date matches today.

**Other `send-email.py` concerns**
- **Dedup guard ignores corrupted log**: if `email-send-log.json` is corrupt it proceeds, causing duplicates.
- **Sends individually per recipient**; if partial failures, it exits 1 but some recipients may have received it. On retry, those recipients may get duplicates.
  - Better: send one message with BCC or track per-recipient success.

---

### `scripts/send-telegram.py`
**Purpose:** send Telegram message via calling `openclaw message send` with retries.

**Issues / gaps**
- Doesn’t validate message length (Telegram limits). Might fail silently after retries.
- Timeout 30s may be tight if gateway is slow.
- No dedup idempotency: repeated calls can duplicate messages.

**Suggestion**
- Add optional `--dedup-key` stored in a local log.

---

### `scripts/commit.sh`
**Purpose:** update README progress, regenerate RSS/index, commit and push.

**Idempotency issues**
- Commit message uses `TODAY` (wall clock) but `CURRENT_DAY` from state; if state day doesn’t correspond to today (missed days), commit message misleading.

**Failure modes**
- README update regex could fail silently if markers changed; script doesn’t check substitution count.
- `git pull --rebase` on push failure can still fail (conflicts) and script will exit (set -e) after `git pull --rebase` failure; OK but might leave repo mid-rebase.

---

### `scripts/verify-and-send.sh`
**Purpose:** “backup cron” at 8:10 per comment (but not present in local crontab). Verifies archives exist, advances state, sends email, generates index, commits.

**Major reliability problem**
- **Allows partial sends intentionally**:
  ```bash
  if [ "$NORMAL_COUNT" -gt 0 ] && [ "$NORMAL_COUNT" -lt 5 ]; then
    echo "WARNING ... Sending what we have."
  fi
  ```
  Combined with `send-email.py` behavior, this explains `sections: 1` days.

**Race / mismatch**
- It calls `advance-state.sh` even if only some archives exist (because it doesn’t enforce 5). `advance-state.sh` *will* fail if missing files, but wrapper swallows failure and continues.
  - Then it proceeds to send email anyway.

**Suggestion**
- Decide policy:
  - If partial send is acceptable, explicitly label it “PARTIAL SEND” and send alert.
  - If not acceptable, **block send unless full set exists** (weekday 5, review 1, weekend 1).

---

### `scripts/setup.sh`
**Purpose:** create OpenClaw cron jobs.

**Issues**
- Interactive prompt (`read -p`) makes it non-automation-friendly.
- It checks existing jobs by `openclaw cron list | grep -c "byte-by-byte"` which is brittle.

---

### `scripts/test.sh`
**Purpose:** local test suite.

**Issues**
- Uses `set -uo pipefail` (no `-e`) and manual PASS/FAIL. Fine.
- “Cron prompt placeholders” check currently requires `{{BBB_REPO_DIR}}` to exist; some prompts might not need it.

---

### `scripts/check-exhaustion.sh`
**Purpose:** content exhaustion check.

**Issue**
- Warn threshold variable says `WARN_THRESHOLD=10` but comment in header says ≤5 days; minor.

---

### `scripts/fix-history.py`
**Purpose:** fill gaps in `state.json` history based on archive directory.

**Risk**
- Assigns synthetic day numbers by incrementing max existing day and skipping review day numbers. This can mismatch actual day numbers if there are missing dates.
- Sets `difficultyPhase` to "Foundation" always (wrong after day ranges).

---

### `scripts/validate-urls.py`
**Purpose:** HEAD check URLs.

**Risk**
- HEAD requests often blocked; will report false negatives.
- Disables TLS verification (ok for internal check but less strict).

---

### `scripts/verify-neetcode.py`
**Purpose:** validate neetcode list.

**Seems fine.**

---

## 2) Specific assessment: `validate_email_content()`

### Does it catch historical “placeholder files sent” bugs?
**It helps, but not complete.**

It catches:
- obvious placeholder words in final included sections
- too-short sections

It can still miss:
- placeholders that don’t contain those specific words
- weekend/review placeholder stubs (not filtered before doorkeeper)
- partial sends (1 section) that are “real” but not intended

### What else should it check?
Add:
- **Day-type expected section count** and enforce it.
- **Stronger placeholder signature**: require a “Generated on” marker; or forbid `ARCHIVE_PATH:`/`INSTRUCTIONS:` blocks.
- **Per-section structural checks** (Algorithms must include complexity + code fence; AI news must include >=2 links; etc.).

### Is 800 chars minimum too high/low?
- For weekday bilingual sections, **800 is probably a bit low** for catching weak output.
- But it might be **too high** for some short Soft Skills prompts if you ever decide to keep them concise.

Best approach: set different thresholds by section slug and day type.

---

## 3) Design: `scripts/backup-send.sh` (no LLM dependency)

Goal: cron at **08:30**.

Behavior:
1. Check `email-send-log.json` for today.
2. If not sent: check archive files for today.
3. If archives exist and look complete: run `send-email.py`.
4. Send Telegram alert about backup send attempt/outcome.

**Key point:** must handle all day types.

### Proposed completeness rules
- **Weekday (normal)**: require 5 files:
  - `${TODAY}-system-design.md`, `-algorithms.md`, `-soft-skills.md`, `-frontend.md`, `-ai.md`
- **Review day**: require `${TODAY}-review.md`
- **Saturday**: require `${TODAY}-deepdive.md`
- **Sunday**: require `${TODAY}-week-review.md`

If multiple exist, prefer in this order: review > saturday deepdive > sunday week-review > normal 5.

### Script (write this file)

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
source "$REPO_DIR/config.env"

TODAY=$(date +%Y-%m-%d)
ARCHIVE_DIR="$BBB_REPO_DIR/archive"
SEND_LOG="$BBB_REPO_DIR/email-send-log.json"

# Helper: send telegram alert (best-effort)
alert() {
  local msg="$1"
  python3 "$BBB_REPO_DIR/scripts/send-telegram.py" "$msg" || true
}

already_sent() {
  [ -f "$SEND_LOG" ] || return 1
  python3 - "$SEND_LOG" "$TODAY" <<'PY'
import json, sys
path, today = sys.argv[1], sys.argv[2]
try:
  data = json.load(open(path))
  sys.exit(0 if today in data else 1)
except Exception:
  sys.exit(1)
PY
}

# Helper: basic file check
ok_file() {
  local f="$1"
  [ -f "$f" ] || return 1
  local size
  size=$(wc -c < "$f" | tr -d ' ')
  [ "$size" -ge 500 ] || return 1
  # placeholder keywords (extendable)
  if grep -qiE "placeholder|content is not generated|deep dive day|week-review\.md|deepdive\.md|TODO|FIXME" "$f"; then
    return 1
  fi
  return 0
}

detect_day_type() {
  # echoes type: review|sat|sun|weekday|none
  if ok_file "$ARCHIVE_DIR/${TODAY}-review.md"; then echo "review"; return 0; fi
  if ok_file "$ARCHIVE_DIR/${TODAY}-deepdive.md"; then echo "sat"; return 0; fi
  if ok_file "$ARCHIVE_DIR/${TODAY}-week-review.md"; then echo "sun"; return 0; fi

  local need=(system-design algorithms soft-skills frontend ai)
  local have=0
  for s in "${need[@]}"; do
    if ok_file "$ARCHIVE_DIR/${TODAY}-${s}.md"; then
      have=$((have+1))
    fi
  done
  if [ "$have" -eq 5 ]; then echo "weekday"; return 0; fi
  echo "none"; return 0
}

main() {
  if already_sent; then
    echo "✅ backup-send: already sent today ($TODAY); nothing to do."
    exit 0
  fi

  local dtype
  dtype=$(detect_day_type)

  if [ "$dtype" = "none" ]; then
    echo "❌ backup-send: no complete archives for $TODAY; aborting."
    alert "🚨 byte-by-byte BACKUP SEND: No complete archives for ${TODAY}. Email not sent."
    exit 1
  fi

  echo "📦 backup-send: detected day type=$dtype; sending email..."
  alert "⚠️ byte-by-byte BACKUP SEND triggered (${TODAY}, type=${dtype}). Attempting send-email.py now."

  if python3 "$BBB_REPO_DIR/scripts/send-email.py"; then
    alert "✅ byte-by-byte BACKUP SEND succeeded (${TODAY}, type=${dtype})."
    exit 0
  else
    alert "🚨 byte-by-byte BACKUP SEND FAILED (${TODAY}, type=${dtype}). Check logs/output."
    exit 1
  fi
}

main "$@"
```

Notes:
- This script **does not** advance state or commit. It only ensures delivery. (If you want it to also advance, do so only after confirming completeness; otherwise it may move state incorrectly.)
- Uses `send-telegram.py` for alerting; that’s not an LLM dependency.

---

## 4) Race condition: 08:00 generate vs 08:05 review-and-send

### What happens today?
- There is no crontab present on this machine (`crontab -l` says none), but OpenClaw cron jobs are created by `scripts/setup.sh`.
- The pipeline relies on “8:00 generate” producing archive files before “8:05 review/send” reads them.
- If generation runs long or hangs, review/send can start with:
  - missing files
  - stub placeholders
  - partially-written files

### Proposed solution
Implement an explicit completion signal.

**Option A (best): lock + completion marker**
- `generate` step writes to a temp location, then atomically moves into `archive/` when done.
- When everything is written, touch `archive/${TODAY}.complete`.
- `review-and-send` must wait (with timeout) for `.complete`.

**Option B: polling with backoff in review job**
- In review-and-send prompt/script, do:
  - wait up to 15 minutes for all required archives to exist and be >N bytes
  - if not, abort and send alert

**Option C: merge jobs**
- One cron job runs the whole pipeline sequentially (generate → QA → send → advance → commit). This removes the race entirely.

---

## 5) `advance-state.sh` partial execution safety (double-run, crash mid-execution)

### If it runs twice
- If first run successfully advanced state, second run sees `currentDay >= nextDay` and exits 0. ✅
- However, if first run advanced `currentDay` but crashed before incrementing some indices/history (possible if `/tmp` missing mid-run), second run will not fix it (because guard exits). ⚠️

### If it crashes mid-execution
- Primary risk: **corrupted `state.json`** due to non-atomic write.
- Secondary risk: partially incremented indices, missing history entry.

**Mitigations**
- atomic write pattern
- maintain a transaction log / run id
- compute new state purely from old state + deterministic plan file

---

## Additional observations from logs/data

### `email-send-log.json` indicates many partial sends
Entries show multiple dates with `"sections": 1` (e.g., 2026-03-18, 2026-03-25, 2026-03-28, 2026-04-01, 2026-04-04).

This strongly suggests:
- either weekend/review days being logged as 1 section (expected)
- OR weekday partial sends slipping through (likely due to `verify-and-send.sh` policy)

You should decide whether `sections: 1` is expected for weekends/review only. If yes, enforce via doorkeeper and verify scripts.

---

## Action checklist (highest ROI)

1. **Fix `generate.sh` idempotency guard** (stop using `lastSentDate`).
2. **Harden doorkeeper** to enforce expected section count/day type.
3. **Make `advance-state.sh` atomic** and independent of `/tmp` for critical data.
4. **Add completion marker** to remove 8:00 vs 8:05 race.
5. **Decide policy on partial sends** and make scripts consistent.

---

## Proposed file additions (not yet committed here)

- `scripts/backup-send.sh` (as above)
- `runs/` directory (optional future improvement)
- `archive/${TODAY}.complete` marker logic

---

_End of review._
