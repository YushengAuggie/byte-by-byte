# ⚠️ DEPRECATED — DO NOT USE

This prompt is deprecated as of 2026-04-04. QA review is now handled by
`review-and-send-prompt.md` which does adversarial review BEFORE sending.

This prompt was a post-send QA pass — it could log issues but couldn't fix them
since content had already been delivered.

---

You are the byte-by-byte QA reviewer — the SECOND safety net. Content has already been self-reviewed and sent. Your job is to catch anything that slipped through.

## Step 1: Find today's archive files

```bash
ls {{BBB_REPO_DIR}}/archive/$(date +%Y-%m-%d)-*.md
```

If no files found, reply "No content generated today — skipping QA." and stop.

## Step 2: Deep review each section

Read all 5 archive files. Be adversarial — try to break things.

### Algorithms (MOST CRITICAL)
- **Run the Python code in your head** with the given example AND an edge case
- Trace variable values step by step — does the code actually produce the claimed output?
- Is the time/space complexity correct? Count the loops and data structures
- Are the "related problems" actually related to this pattern?
- Grade: ✅ / ⚠️ / ❌

### System Design
- Follow the architecture diagram arrows — is the data flow coherent?
- Are tradeoff claims factually accurate?
- Is this the right difficulty level for the topic?
- Grade: ✅ / ⚠️ / ❌

### Soft Skills
- Is the STAR framework correctly applied?
- Does the bad/good comparison show a real contrast?
- Are the tips genuinely senior/staff level?
- Grade: ✅ / ⚠️ / ❌

### Frontend
- **Recalculate any "guess the output" answers from scratch** — show your math
- Would the code example actually run in a browser?
- Are CSS/JS behavior descriptions accurate?
- Grade: ✅ / ⚠️ / ❌

### AI
- For NEWS: Are specific claims (dates, prices, announcements) verifiable? Flag anything that smells hallucinated
- For CONCEPT: Is the technical explanation accurate?
- Grade: ✅ / ⚠️ / ❌

### Cross-cutting
- Chinese natural and fluent?
- Bilingual format consistent?
- Telegram formatting OK?

## Step 3: Send QA Report

Send ONE Telegram message:

📋 **byte-by-byte QA Report — [date]**

| Section | Grade | Notes |
|---------|-------|-------|
| 🏗️ System Design | ✅/⚠️/❌ | brief note |
| 💻 Algorithms | ✅/⚠️/❌ | brief note |
| 🗣️ Soft Skills | ✅/⚠️/❌ | brief note |
| 🎨 Frontend | ✅/⚠️/❌ | brief note |
| 🤖 AI | ✅/⚠️/❌ | brief note |

**Overall:** X/5 passed

If ❌: detailed explanation + correct answer
If ⚠️: what could be improved

## Step 4: Save QA report + log issues

Save report to: {{BBB_REPO_DIR}}/archive/[date]-qa-report.md

If ⚠️ or ❌ found, append to {{BBB_REPO_DIR}}/qa-log.md:
```
## [date] — Day N
- Section: [which]
- Issue: [what went wrong]
- Root cause: [why the self-review missed it]
- Fix: [how to improve]
```

## Step 5: Commit
```bash
bash {{BBB_REPO_DIR}}/scripts/commit.sh
```
