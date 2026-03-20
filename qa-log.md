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

## 2026-03-16 — Day 3

- **Section:** AI (News)
- **Issue:** Specific unverifiable figures present: BuzzFeed 2025 loss ($57.3M), stock price ($0.70), Meta "Avocado" delay date (May 2026), Palantir demo quote ("left-click right-click left-click"). Web search unavailable at QA time to verify.
- **Root cause:** Recurring pattern — AI news content often contains plausible but hallucinated specifics. Disclaimer was added (improvement from Day 1), but specific figures still appear without sourcing.
- **Fix:** Consider instructing the AI news generator to avoid specific financial figures and specific future dates unless citing a named source inline (e.g., "per Bloomberg, $57.3M"). Disclaimer is necessary but not sufficient.

## 2026-03-18 — Day 5 (Review Day)
- **Section:** Algorithms (Q2 quiz question)
- **Issue:** Two Sum code skeleton is missing the `target` parameter. `def mystery(nums):` references `target` inside the function body, which would cause a `NameError` at runtime. Correct signature is `def mystery(nums, target):`.
- **Root cause:** Review day content is generated as pattern-recognition quizzes (students identify the algorithm, not run it). Self-review likely validated conceptual correctness without testing whether the code skeleton is syntactically executable.
- **Fix:** Add an explicit check in review day generation: "For any code snippet in quiz questions, verify all referenced variables are either defined locally, passed as parameters, or explicitly marked as pseudo-code/skeleton with a comment." Consider adding `# target is passed as argument` or simply correcting the signature.

## 2026-03-20 — Day 7
- **Section:** AI (News)
- **Issue:** Meta story framing overstates source. Content claims Meta will "significantly reduce reliance on third-party content moderation contractors" but the actual Meta blog post (verified via URL fetch) focuses on an AI support assistant and advanced AI enforcement systems — with no mention of contractor workforce reduction. Additionally, Samsung's $73B/22% figures and Alexa Plus UK £19.99/mo price are specific claims that could not be independently verified.
- **Root cause:** Recurring pattern (Days 1, 3, 7). The AI news generator makes plausible editorial inferences that go beyond what sources actually say, and includes specific figures (prices, percentages) without in-line sourcing. Self-review does not systematically check whether editorial framing matches the linked source content.
- **Fix:** This is the third time this pattern has appeared. Escalate fix priority: add a post-generation step where the generator re-reads its own source URLs and checks whether each claim is directly supported. For any claim about workforce changes, business strategy, or financial figures, require an inline quote from the source or add explicit "reportedly" / "per [source]" attribution.
