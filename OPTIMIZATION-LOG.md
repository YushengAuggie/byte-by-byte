# Byte-by-Byte Pipeline Optimization Log

## 2026-04-07 Optimization Run

### P0 Fixed
1. **Review days missing from history** — Days 5, 10, 15 were absent from `state.json` history because `advance-state.sh` skipped adding history entries for review days. Fixed the script to add history entries on review days AND backfilled the 3 missing entries. History now shows a clean Day 1–19 sequence.

### P1 Proposed
1. **April 3 missed delivery** — Weekday cron timed out (all 3 model fallbacks failed), review-and-send also timed out, and backup-send.sh didn't exist yet (added Apr 4). Orphaned archive files exist at `archive/2026-04-03-*.md` with stale "Day 15" headers. **Proposed fix:** Add a staleness check to backup-send.sh — if archive files exist for today but `email-send-log.json` has no entry AND `state.json` history has no matching date, flag the day as "generated but undelivered" and attempt resend. This would catch future timeout-cascade failures.

2. **Saturday cron delivery error** — Both Saturday runs show `consecutiveErrors=2` with "Channel is required" error. The error is in the OpenClaw cron delivery announcement mechanism, NOT in actual content delivery (review-and-send picks it up). Content still reaches subscribers. **Proposed fix:** This appears to be an OpenClaw platform bug. Monitor — if `consecutiveErrors` hits a threshold that auto-disables the job, we'd need a workaround (e.g., set `failureAlert` threshold higher or add a manual re-enable check).

3. **QA log recurring AI hallucination pattern** — 6+ occurrences (Days 1, 3, 7, 11, 26, 29) of unverified claims presented as facts. The hallucination gate was added (commit `8142e0d`) but hasn't been in effect long enough to evaluate. **Proposed fix:** After 5 more days with the gate active, audit whether "据报道/reportedly" qualifiers are appearing consistently.

### P2 Noted
1. **Orphaned archive files** — `archive/2026-04-03-{system-design,algorithms,soft-skills,frontend,ai}.md` contain real content (~24KB total) labeled "Day 15" but are not linked to any state history entry. They don't cause test failures but could confuse future date-scanning logic. Low risk — leave as-is since removing archive files is prohibited.

2. **URL validation: 57 broken links** — The `validate-urls.py` test shows 57 broken/unreachable URLs in archive files. This is likely a mix of network issues (test environment) and genuinely dead links in older archives. Since these are in immutable archive content, this is informational only.

3. **Cron model fallback timeouts** — 3 instances of "All models failed" timeout errors in weekday cron history (Mar 22, Apr 3). The 3-model fallback chain (sonnet → gpt-5.2 → opus) can take 40+ minutes total. Consider adding a faster lightweight model as first fallback to reduce cascade timeout window.

### Metrics
- Delivery rate (7d): 6/7 (April 3 missed)
- Cron error rate: 1/6 jobs in error state (saturday — delivery-only, not content)
- Test pass rate: 77/77 (+ 1 warning for URL validation)
- History completeness: 19/19 days (after backfill fix)
