# byte-by-byte Prompt Architecture Review
*Reviewed: 2026-04-04 | Reviewer: Subagent*

---

## Executive Summary

The pipeline has **three systemic problems** that are causing recurring failures:

1. **AI News hallucination pattern** — appears in 6+ qa-log entries (Days 1, 3, 7, 11, 20, 26, 29). No structural fix yet deployed.
2. **Generate/review-and-send handoff is fragile** — review-and-send makes multiple unstated assumptions about generate's output, with no signal file, no byte threshold check, and no recovery path for partial content.
3. **Prompt duplication/bloat** — `daily-prompt.md` is a full rewrite of `weekday-prompt.md` + `saturday-prompt.md` + `sunday-prompt.md` combined. This creates two authoritative sources that will diverge.

---

## 1. Prompt-by-Prompt Analysis

### `weekday-prompt.md` (~7KB)
**Clarity:** Good. Steps are numbered, content format is explicit.

**Issues:**
- **Review-day path sends Telegram in weekday-prompt but NOT in normal-day path.** The prompt says "STOP — Do NOT send Telegram, email, or commit" for normal days, but the review-day path in the SAME prompt says to send Telegram AND email AND commit. This inconsistency means review days bypass the review-and-send cron — they are fully self-contained. This may be intentional, but it's not documented and conflicts with what review-and-send expects.
- **Missing state-check idempotency.** If `advance-state.sh` fails mid-run, a retry would re-generate content for a day already partially written, potentially overwriting good archive files.
- **AI News Section:** The fallback instruction ("If no search tool works, fall back to CONCEPT mode") is too permissive. An LLM that can't access web search will silently fall back to CONCEPT mode without flagging this as a degradation.
- **Token risk:** ~7KB is acceptable. The pattern-based algorithms section (IS_FIRST_IN_PATTERN logic) adds conditional complexity that's fine.

**Edge cases not handled:**
- What if `/tmp/bbb-section-N.txt` doesn't exist (generate.sh failed silently)?
- What if the ARCHIVE_PATH in section files contains a directory that doesn't exist?

---

### `review-and-send-prompt.md` (~3KB)
**Clarity:** Clear in intent, but has dangerous assumptions.

**Issues:**
- **Assumes `/tmp/bbb-quiz-2.json` and `/tmp/bbb-quiz-4.json` exist.** If generate failed or wrote to wrong paths, these polls will silently fail or the LLM will invent quiz content.
- **Step 0 file type detection is incomplete.** It checks for `*-deepdive.md` (Saturday) and `*-week-review.md` (Sunday) — but if it's Saturday and deepdive failed, it will find 0 files and return "No content generated today." It has no recovery path.
- **No minimum byte check in Step 0.** "If 5 section files exist" — but there's no `>500 bytes` guard here. Placeholder files (e.g., "TBD" or error traces) would pass this check.
- **AI URL verification is token-expensive.** "Verify at least 2 URLs using web_fetch" during review adds latency and can cause timeouts. This should be selective, not mandatory.
- **Loop until clean** (Step 3) has no max iteration limit. An LLM that keeps finding issues in its own fixes can spin forever and timeout.
- **Contradiction with weekday-prompt review day path:** weekday-prompt sends Telegram on review days internally; review-and-send also expects to send. On review days, delivery could double-send.

**What would an LLM do if it hits an error mid-way?** It would either stop and report, or try to continue with whatever state exists. Because there's no recovery protocol defined, behavior is unpredictable.

---

### `saturday-prompt.md` (~2KB)
**Clarity:** Good and concise.

**Issues:**
- **Writes `echo "ready" > /tmp/bbb-content-ready` signal file** — but `review-and-send-prompt.md` does NOT check for this file. The signal file is written but never read. Either review-and-send should check it, or this should be removed to avoid creating a false assumption.
- **"IMPORTANT: Only write the deepdive archive file"** — this is a clear, correct guard against the placeholder file problem.
- **Topic selection is vague:** "Pick the most complex topic" with a 3-step priority list. If the generator script doesn't produce a Hard LeetCode problem or Advanced system design topic (which depends on current indices), the LLM might make a subjective choice that changes week to week.

**Edge cases not handled:**
- What if all 5 section files are missing (generate.sh failure)?
- What if advance-state.sh fails after writing the deepdive?

---

### `sunday-prompt.md` (~2KB)
**Clarity:** Good.

**Issues:**
- **"Skip email digest (optional — only send if Sunday digest is configured)"** — this is ambiguous. The LLM will either always skip or always send depending on how it interprets "configured." Should be explicit.
- **Reads "past 6 days" from archive/** — but if Saturday deepdive wasn't generated, Sunday review will have a gap. The prompt doesn't address missing days.
- **No review gate** — unlike Saturday, Sunday has no self-review step. The "Summarize accurately from actual archive content — don't invent" rule is a single bullet at the end, not an enforced gate.
- **Writes `echo "ready" > /tmp/bbb-content-ready`** — same issue as Saturday: review-and-send doesn't check this.

---

### `daily-prompt.md` (~22KB — THE BIG ONE)
**Clarity:** Very thorough, but **this is the prompt that caused the 55-minute timeout.**

**Critical problems:**
1. **Duplication.** This is a superset of weekday + saturday + sunday prompts combined, plus a built-in review gate. It is 3x larger than weekday-prompt.md. Running this prompt means the LLM processes the full weekend paths even on weekdays.
2. **It includes its own send logic.** daily-prompt.md sends Telegram, polls, email, AND commits — all in one session. This means if daily-prompt is the active cron, review-and-send is irrelevant (or would double-send). **These two prompts cannot coexist as active crons without clear separation.**
3. **Review gate is inline.** The Step 3 review gate (switch roles, verify everything) adds significant processing time after already generating 5 sections. On slow days or complex algorithm content, this alone can push runtime to 45+ minutes.
4. **AI Section Step 5 is redundant.** It re-states the web_search requirement already stated in Step 2's Section 5 definition, with slightly different wording. An LLM reading sequentially will encounter two AI-search instructions that might be interpreted differently.
5. **Token count:** ~22KB. This caused a 55-minute timeout previously and has not been fixed. If this is the active cron prompt, it needs to be split.

**Recommendation:** Determine which prompt is actually active in the cron config. If it's `daily-prompt.md`, it should be replaced by the smaller `weekday-prompt.md` + weekend-specific prompts. If `daily-prompt.md` is kept, all weekend logic must be removed and the review gate extracted to `review-and-send-prompt.md`.

---

### `qa-prompt.md` (~2KB)
**Clarity:** Clear and well-scoped.

**Issues:**
- **This is a THIRD review pass** (after self-review in generate, and review-and-send). It reads content that has already been sent. Its only output is a Telegram message and log append — it cannot fix anything retroactively.
- **It has no mechanism to trigger regeneration.** If it finds a ❌, it logs it but the day's content has already been delivered. The qa-prompt is useful for pattern detection but creates false confidence if users think it's a quality gate.
- **The QA report format** in qa-prompt differs slightly from the QA report format in review-and-send-prompt (table layout vs bullet list). This causes inconsistent log formats that make the qa-log harder to parse.

---

## 2. QA Log Analysis — Top 3 Recurring Issues

Reading `qa-log.md` entries (Days 1, 3, 7, 11, 12, 13, 20, 26, 27, 28, 29):

### Issue #1: AI News Hallucination (6+ occurrences — HIGHEST PRIORITY)
**Pattern:** Specific figures (prices, percentages, benchmark scores, dates), institutional claims ("DoD designated Anthropic as supply chain risk"), and model names (e.g., "GPT-5.4") appear as facts without verifiable inline sourcing. The disclaimer instruction added after Day 1 reduced frequency but didn't eliminate the pattern.

**Root cause:** The LLM is instructed to "search the web" for news but no mechanism enforces that all claims actually came from search results. When search results are ambiguous or limited, the LLM fills gaps with plausible-sounding details from training data.

**Fix priority:** CRITICAL. Once a hallucinated claim enters an archive file, it propagates to week reviews and recap content (confirmed on Day 29).

### Issue #2: Frontend "Guess the Output" Wrong Answers (Days 1, 12, 15)
**Pattern:** Math errors in box-model calculations, React Strict Mode double-invoke confusion, invalid CSS on non-pseudo elements. Self-review passes because it validates *conceptual* correctness, not the specific numerical answer.

**Root cause:** The review instruction says "calculate from scratch" but LLMs tend to verify their own answers by re-reading their own work rather than independently computing. Closed-loop verification doesn't catch the original error.

**Fix priority:** HIGH. Wrong answers sent to subscribers undermine trust and the learning goal.

### Issue #3: Architecture Diagram / Code Consistency (Days 13, 28)
**Pattern:** The diagram shows one data flow, the code implements a different one. Each is internally consistent; they contradict each other. Self-review catches code bugs and diagram logic bugs separately but not cross-section contradictions.

**Root cause:** Generation is sequential — the diagram is written first, code second. By the time code is generated, the LLM doesn't re-read the diagram to check consistency. The review gate doesn't include a "trace one message through diagram AND code" step.

**Fix priority:** MEDIUM-HIGH. Affects the Saturday deep dive disproportionately.

---

## 3. Proposed Prompt Improvements

### Fix 1: AI News — Structural Hallucination Prevention

Add to the **AI Section** in all prompts (weekday-prompt.md and daily-prompt.md):

```markdown
### Section 5: AI News — MANDATORY SOURCING RULES

**Before writing any story:**
1. Run web_search: `"AI news this week {CURRENT_MONTH} {CURRENT_YEAR}"`
2. For EACH story you include: paste the headline and source URL you found, then write the story
3. NEVER include specific figures (prices, percentages, benchmark scores) unless they appear word-for-word in a search result you read
4. For ANY claim about a specific organization's strategy, internal decision, or financial result: prefix with "reportedly" / "据报道" and name the source inline
5. If search is unavailable or returns <3 usable results: use CONCEPT mode instead. Do not attempt to write news from memory.

**Anti-hallucination gate (required before saving):**
For each story, verify: "Did I read this figure/claim in a search result, or am I inferring it?"
- If inferred → add "reportedly" or remove the specific figure
- If from search → include the URL as inline citation
```

### Fix 2: Frontend Quiz — Independent Answer Verification

Replace the current review instruction with a forced trace:

```markdown
### Frontend Review Gate (REQUIRED)

For the "guess the output" question:
1. Copy the exact code snippet
2. Execute it mentally line by line, showing variable state at each step:
   - Before first render: [variable states]
   - After first render: [variable states]  
   - After event: [variable states]
3. If your trace produces a different answer than what you wrote: UPDATE the answer and the /tmp/bbb-quiz-4.json correct_index
4. For any answer involving counts/renders: explicitly state "assuming production mode / without React Strict Mode"
5. For any CSS calculation: show the arithmetic (e.g., 100 + 40 + 10 = 150, not 160)
```

### Fix 3: Diagram/Code Cross-Consistency Check

Add to Saturday deep dive generation (saturday-prompt.md) and daily-prompt.md Saturday path:

```markdown
### Deep Dive Cross-Check (after writing both diagram and code)

Trace ONE specific request through the system:
1. Pick the example from your content (e.g., "user sends notification")
2. Follow it through the ASCII diagram: box1 → box2 → box3
3. Find the corresponding code path and verify it matches the diagram flow
4. If they differ: fix the diagram OR fix the code, not both — pick the canonical source of truth

This check is REQUIRED. Do not skip.
```

### Fix 4: Reduce daily-prompt.md Token Count

**Option A (recommended):** Deprecate `daily-prompt.md` entirely. Use:
- `weekday-prompt.md` for Mon–Fri cron
- `saturday-prompt.md` for Sat cron
- `sunday-prompt.md` for Sun cron

**Option B:** Remove all weekend paths from `daily-prompt.md` and reduce it to weekday-only with clear path detection. Trim the AI section which is repeated verbatim in two places.

**Immediate reduction (if keeping daily-prompt.md):** Remove the duplicate AI-section instructions (appears once in Section 5 generation and once in Step 3 review). Remove the full Section 4 quiz JSON examples (they're obvious). Estimated savings: ~4KB.

### Fix 5: Clarify Review Day Ownership

The weekday-prompt.md review-day path sends Telegram/email/commit internally. The review-and-send-prompt.md also expects to handle review days. This must be resolved:

**Option A:** Remove Telegram/email/commit from weekday-prompt review-day path. Let review-and-send handle all delivery (consistent with normal days).

**Option B:** Keep weekday-prompt self-contained on review days. Add an explicit check in review-and-send: "If today's only archive file is `*-review.md` AND it was committed in the last 10 minutes, skip — it was already sent by the generate cron."

**Recommendation:** Option A. Delivery should always go through review-and-send for consistency and auditability.

---

## 4. Generate → Review-and-Send Handoff Analysis

### Current Assumptions review-and-send makes about generate's output

| Assumption | Explicit check? | Risk |
|---|---|---|
| Archive files exist for today | ✅ Step 0 checks `ls archive/${TODAY}-*.md` | Low |
| 5 section files exist (normal day) | ⚠️ Checks by name, not by content | Medium |
| Each section file is >500 bytes | ⚠️ Only mentioned in step 0 description, no actual byte check | High |
| `/tmp/bbb-quiz-2.json` exists with valid JSON | ❌ Not checked | High |
| `/tmp/bbb-quiz-4.json` exists with valid JSON | ❌ Not checked | High |
| State was already advanced by generate | ❌ Not checked; advancing twice would corrupt state | High |
| Today's date matches archive filename | ✅ Implicit via `${TODAY}` variable | Low |

### What happens if generate wrote partial output?

**Scenario:** generate.sh completes sections 1-3, then times out. Three archive files exist, two are missing.

**Current behavior:** review-and-send Step 0 lists files. It finds 3 files, not 5. The day type check falls through (not review, not deepdive, not week-review, not 5 sections). It hits the `If no archive files for today` check — but this is FALSE (there ARE files). **The current prompt logic doesn't have a "partial files" branch.** The LLM will likely attempt to send whatever exists, which means a partial newsletter gets delivered.

**Scenario 2:** generate completed all 5 sections but advance-state.sh failed. State is still at Day N-1. review-and-send sends content successfully. Now state.json is inconsistent — it shows Day N-1 as current but archive has Day N files.

### Should review-and-send check a "ready" signal file?

**Yes — but the signal already half-exists.** Saturday and Sunday prompts write `echo "ready" > /tmp/bbb-content-ready` but weekday-prompt does not. And review-and-send checks nothing.

**Proposed signal protocol:**

In weekday-prompt.md (at the end of Step 2 verification block):
```bash
# Write ready signal with metadata
echo "{\"day\":$(cat {{BBB_REPO_DIR}}/state.json | python3 -c 'import json,sys;print(json.load(sys.stdin)[\"currentDay\"])'),\"sections\":5,\"date\":\"$(date +%Y-%m-%d)\"}" > /tmp/bbb-content-ready
```

In review-and-send-prompt.md (new Step 0a before Step 0):
```bash
# Check ready signal
if [ -f /tmp/bbb-content-ready ]; then
  cat /tmp/bbb-content-ready
  # Verify the date matches today
  SIGNAL_DATE=$(cat /tmp/bbb-content-ready | python3 -c 'import json,sys;print(json.load(sys.stdin)["date"])')
  TODAY=$(date +%Y-%m-%d)
  if [ "$SIGNAL_DATE" != "$TODAY" ]; then
    echo "WARNING: Ready signal is from $SIGNAL_DATE, not today ($TODAY). Generate may have failed."
    # Continue anyway — check actual files
  fi
else
  echo "WARNING: No /tmp/bbb-content-ready signal. Generate may have failed or timed out."
  # Continue with file-based checks
fi
```

Add a minimum file size check to the Step 0 day-type detection:

```bash
# Verify all 5 section files meet minimum size (>500 bytes)
MISSING_OR_SMALL=""
for section in system-design algorithms soft-skills frontend ai; do
  FILE="{{BBB_REPO_DIR}}/archive/${TODAY}-${section}.md"
  if [ ! -f "$FILE" ] || [ $(wc -c < "$FILE") -lt 500 ]; then
    MISSING_OR_SMALL="${MISSING_OR_SMALL} ${section}"
  fi
done
if [ -n "$MISSING_OR_SMALL" ]; then
  echo "ERROR: Missing or too-small sections:${MISSING_OR_SMALL}"
  echo "Cannot send partial content. Stopping."
  exit 1
fi
```

### Max iteration guard for review loop

In review-and-send, the "loop until clean" instruction needs a ceiling:

```markdown
**Maximum 2 fix iterations.** If issues remain after 2 rounds of fixes:
- Mark remaining issues as ⚠️ in the QA report
- Send with the warning
- Do NOT continue looping
This prevents timeout from infinite self-correction loops.
```

---

## 5. Summary Table — Recommended Changes by File

| File | Priority | Change |
|---|---|---|
| `weekday-prompt.md` | HIGH | Add AI News sourcing gate (Fix 1). Remove review-day Telegram/email/commit (Fix 5 Option A). Add ready signal write. |
| `weekday-prompt.md` | MEDIUM | Add frontend independent trace (Fix 2). Handle missing /tmp/bbb-section-N.txt gracefully. |
| `review-and-send-prompt.md` | HIGH | Add ready signal check + minimum byte check (Section 4 above). Add max 2 iteration limit. Add /tmp/bbb-quiz-*.json existence checks. |
| `review-and-send-prompt.md` | MEDIUM | Remove expensive "verify 2 URLs" requirement — replace with "flag suspicious claims for ⚠️". |
| `saturday-prompt.md` | HIGH | Either remove `echo ready >` signal or make it consistent with weekday signal format. |
| `saturday-prompt.md` | MEDIUM | Add cross-consistency diagram/code check (Fix 3). |
| `sunday-prompt.md` | HIGH | Make email-digest decision explicit (not "optional"). Add review gate for summary accuracy. |
| `sunday-prompt.md` | LOW | Either remove `echo ready >` signal or standardize. |
| `daily-prompt.md` | CRITICAL | Either deprecate (replace with 3 separate crons) or strip weekend paths and cut to ~8KB. This prompt is the root cause of the 55-min timeout. |
| `qa-prompt.md` | LOW | Standardize QA report format with review-and-send report format (use same table). |

---

## 6. One-Sentence Triage Priorities

1. **Today:** Add the AI News sourcing gate to prevent the recurring hallucination pattern (6+ occurrences, propagates to week reviews).
2. **This week:** Fix the generate/review-and-send handoff — add the ready signal and minimum byte checks before allowing delivery.
3. **This week:** Determine whether `daily-prompt.md` or `weekday-prompt.md` is the active cron. If daily-prompt.md, it must be replaced — it caused the 55-min timeout.
