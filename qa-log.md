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

## 2026-03-26 — Day 11

- **Section:** AI (News)
- **Issue:** Story 1 includes "91% on a legal-document benchmark" as a specific figure. Story 2 claims DoD designated Anthropic as a "supply chain risk" — notable claim sourced only from a personal WordPress blog (radicaldatascience.wordpress.com). Neither figure was independently verifiable at QA time.
- **Root cause:** This is the 5th+ recurrence of the same pattern. Specific benchmark numbers and notable institutional claims are presented as facts without inline primary source attribution. Self-review does not check whether specific figures are verifiable.
- **Fix (escalated):** This pattern has now recurred on Days 1, 3, 7, 20, and 26. Escalate to structural fix: add a visible disclaimer at the top of every AI News section ("Figures and claims based on cited sources; verify before sharing"), AND instruct the generator to mark any claim from a non-primary source with "reportedly" or "per [source]".

## 2026-03-27 — Day 12

- **Section:** Frontend
- **Issue:** "Guess the output" quiz answer (C: 3) is correct in production/non-Strict-Mode React, but misleading for readers in a typical dev environment. React 18 Strict Mode double-invokes render functions, so the displayed count would be 6, not 3, in a standard `create-react-app` or Next.js dev build.
- **Root cause:** The code example even includes a comment in the "BadComponent" section about React 18 Strict Mode double-invokes, but that knowledge wasn't applied to validate the quiz answer in the *other* code block.
- **Fix:** For any "guess the output" quiz involving render counts or side-effect counts, explicitly state the environment assumption (production mode vs dev/Strict Mode). Add a parenthetical like "(in production / without Strict Mode)" to the answer, or note the Strict Mode difference.

## 2026-03-20 — Day 7
- **Section:** AI (News)
- **Issue:** Meta story framing overstates source. Content claims Meta will "significantly reduce reliance on third-party content moderation contractors" but the actual Meta blog post (verified via URL fetch) focuses on an AI support assistant and advanced AI enforcement systems — with no mention of contractor workforce reduction. Additionally, Samsung's $73B/22% figures and Alexa Plus UK £19.99/mo price are specific claims that could not be independently verified.
- **Root cause:** Recurring pattern (Days 1, 3, 7). The AI news generator makes plausible editorial inferences that go beyond what sources actually say, and includes specific figures (prices, percentages) without in-line sourcing. Self-review does not systematically check whether editorial framing matches the linked source content.
- **Fix:** This is the third time this pattern has appeared. Escalate fix priority: add a post-generation step where the generator re-reads its own source URLs and checks whether each claim is directly supported. For any claim about workforce changes, business strategy, or financial figures, require an inline quote from the source or add explicit "reportedly" / "per [source]" attribution.

## 2026-03-28 — Day 13 (Saturday Deep Dive)

- **Section:** System Design / Deep Dive Architecture
- **Issue:** Architecture diagram shows single Kafka consumer group with Consumer 0→Email, Consumer 1→SMS, Consumer 2→Push, but partition key is `user_id`. In reality, each consumer in a single group gets ALL event types for its assigned users, not just one notification channel. The diagram implies channel-based routing which contradicts how Kafka consumer groups work with a user_id partition key.
- **Root cause:** The code's `_handler_map` routing pattern is actually correct for a single consumer group (each consumer routes internally), but the diagram was drawn as if it were a separate-consumer-group pub/sub pattern. Self-review validated the code and the diagram independently without checking their consistency with each other.
- **Fix:** For future deep dives with architecture diagrams: after writing both the diagram and the code, do a cross-check — trace one message through the diagram and verify the code implements the same data flow. Consider clarifying in the diagram: either (A) show internal routing arrows within consumers, or (B) use three separate consumer groups.

- **Section:** References
- **Issue:** `https://stripe.com/blog/message-queues` returns HTTP 404. The correct Stripe reference for idempotency/exactly-once patterns is `https://stripe.com/blog/idempotency` (confirmed 200 OK).
- **Root cause:** Reference URL was not verified before publication. A real Stripe blog post exists on the topic but at a different slug.
- **Fix:** For deep dive reference URLs, do a HEAD request check (or note them as "unverified") before including. At minimum, note that URLs should be verified by the reader.

## 2026-03-29 — Week Review (Day 13 recap)
- **Section:** AI
- **Issue:** Week review repeats "GPT-5.4 已实现原生电脑操作（GUI）" as a weekly highlight fact — re-asserting a claim flagged as potentially hallucinated in the Day 11 QA report (GPT-5.4 is not a known real model name; "91% legal benchmark" is unverified). No disclaimer added.
- **Root cause:** Week review generator pulls AI highlights from the weekly content and summarizes them without applying the "unverified claim" filter. The claim passed self-review because it was consistent with the source material (the Day 11 issue), but the source material itself was flagged by QA and wasn't corrected. Once a hallucinated claim enters the archive, downstream recaps inherit it without re-validation.
- **Fix:** (1) When generating week reviews, cross-check AI highlight claims against the QA log for the same week — if a claim was flagged as unverified, apply "reportedly / 据报道" in the recap. (2) Longer term: when Day QA flags an AI claim, add a correction note to that day's archive so week review generation can detect it.
