# byte-by-byte QA Log

This file tracks issues found during QA reviews to improve content quality over time.

---

## 2026-03-14 — Day 1

- **Section:** Frontend
- **Issue:** Wrong answer for "guess the output" CSS box model question. Answer marked as C) 160px but correct answer is B) 150px (100 content + 40 padding + 10 border = 150). The box model diagram in the same section correctly computed 150px, creating an internal contradiction.
- **Fix:** Add a self-check step to the frontend prompt: "After writing the answer to the 'guess the output' question, verify it by tracing through the math explicitly before finalizing." Or add a post-generation verification step for any numerical answer.

- **Section:** AI (News mode)
- **Issue:** Story 1 cited specific pricing ($5/$25/M, $3/$15/M) and a specific date ("March 13") as hard facts. These details are plausible but potentially hallucinated, which could mislead readers.
- **Fix:** Update the AI news prompt to instruct: "For any specific numbers (pricing, percentages, dates), add a note that details are unverified and readers should check official sources. Do not present specific pricing or release dates as confirmed facts unless you have high confidence."

## 2026-03-15 — Day 2

- **Section:** Frontend
- **Issue:** In the `flex: 1 vs flex: 1 1 auto` gotcha, the code example uses `content: "longer text"` as a CSS property on a regular `div` — `content` only works on `::before`/`::after` pseudo-elements. The example would not behave as expected in a real browser, potentially confusing readers who try to test it.
- **Root cause:** Self-review validated the conceptual accuracy (which is correct) but didn't flag the invalid CSS property usage on a non-pseudo element.
- **Fix:** Update the frontend prompt or review checklist: "For any CSS code examples, verify that each property is valid on the target selector type. Check that `content` is only used with pseudo-elements."
