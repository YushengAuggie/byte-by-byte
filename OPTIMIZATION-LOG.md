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

## 2026-04-10 Optimization Run

### Issues Found

**P0 Critical:**
- None. All 7 days in the past week had content delivered via both Telegram and email.

**P1 Quality:**
1. **Apr 9 missing from state history** — Archives exist, email sent, QA report present, but `state.json` history jumps from Day 20 (2026-04-08) to Day 21 (2026-04-10), skipping Apr 9 entirely. Content was delivered (so not P0) but the history gap means Apr 9 topics won't appear in future review days or week-review summaries. The advance-state script likely ran but didn't record the history entry properly — possibly a race condition or the state was overwritten by the Day 21 run.
2. **Saturday cron still erroring** — `consecutiveErrors: 2` with "Channel is required when multiple channels are configured" error. Content delivery is NOT affected (review-and-send picks it up) but the cron itself shows error state. Same issue noted in Apr 7 report — unfixed. The Saturday cron job is missing `delivery.channel` specification.
3. **Optimizer cron timeout** — This cron (byte-by-byte optimizer) timed out on its last run (Apr 7) at 600s. `consecutiveErrors: 1`. The previous run tried to make code changes + run tests which caused the timeout. Current simplified report-only version should resolve this.

**P2 Maintenance:**
1. **Apr 3 still has orphaned archives** — 5 archive files (~24KB) with no email delivery or QA report. Known from Apr 7 — low risk, leave as-is.
2. **History gaps for weekends** — Mar 21 (Sat), Mar 22 (Sun), Mar 29 (Sun), Apr 5 (Sun) missing from history. This is expected since weekday cron runs Mon-Fri, but the Saturday and Sunday crons exist. The Saturday deep dive on Apr 4 IS in history (Day 17), and Apr 5 week-review archive exists but has no history entry. Sunday's advance-state may not be recording history.
3. **Mar 30 (Monday) completely missing** — No archives, no email log, no history. Likely a weekday cron failure early in the project. Too old to action.

### Metrics
- Delivery rate (7d): **7/7** ✅ (Apr 4–10, all delivered)
- Email delivery (7d): **7/7** ✅
- Cron errors: 2 jobs in error state (optimizer — timeout; saturday — channel config)
- History completeness: 21 entries / ~27 calendar days (gap analysis above)
- State: Day 21, all indices advancing normally

### Trend vs Last Run (Apr 7)
- Delivery rate: improved (6/7 → 7/7)
- Apr 3 orphan issue: unchanged (expected — not actionable)
- Saturday cron error: unchanged (needs delivery.channel fix)
- New issue: Apr 9 history gap (P1)
