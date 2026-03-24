Generate bilingual (Chinese first, English second) tech content for byte-by-byte. 5 sections on weekdays, review quiz on review days.

## Step 0: Load State

```bash
cat {{BBB_REPO_DIR}}/state.json
```

From state.json, build a progress header:
```
📊 Day {currentDay}/150 · NeetCode: {leetcodeIndex}/150 · SysDesign: {systemDesignIndex}/40 · Behavioral: {behavioralIndex}/40 · Frontend: {frontendIndex}/50 · AI: {aiTopicIndex}/30
🔥 {streak}-day streak!
```
Streak = count consecutive days with history entries going backward. Omit if 0.

## Step 1: Run generator

```bash
bash {{BBB_REPO_DIR}}/scripts/generate.sh
```

This writes section info to `/tmp/bbb-section-{1..5}.txt` (normal) or `/tmp/bbb-review.txt` (review day, day % 5 == 0). It does NOT advance state.

```bash
[ -f /tmp/bbb-review.txt ] && echo "REVIEW" || echo "NORMAL"
```

---

## REVIEW DAY (if /tmp/bbb-review.txt exists)

Read `/tmp/bbb-review.txt` for REVIEW_DAY, PAST_TOPICS, ARCHIVE_PATH. Generate a review quiz:

```
🔄 **复习日 Day N / Review Day N**
今天是复习日！回顾过去4天的内容。

### 📝 Quick Quiz — 3 Mini-Reviews
Pick 3 topics from 3 different sections.

**Q1: [🏗️ System Design]** [question testing understanding, not recall]
<details><summary>显示答案 / Show Answer</summary>
[3-4 sentence answer]
</details>

**Q2: [💻 Algorithms]** [question]
<details><summary>显示答案 / Show Answer</summary>
[answer]
</details>

**Q3: [🗣️/🎨/🤖]** [question]
<details><summary>显示答案 / Show Answer</summary>
[answer]
</details>

💡 *复习巩固记忆，螺旋式上升。*
📅 明天继续新内容！
```

Save to ARCHIVE_PATH → verify file exists → advance state → send Telegram → send email → commit:
```bash
ls -la {{BBB_REPO_DIR}}/archive/$(date +%Y-%m-%d)-review.md
bash {{BBB_REPO_DIR}}/scripts/advance-state.sh
python3 {{BBB_REPO_DIR}}/scripts/send-email.py
bash {{BBB_REPO_DIR}}/scripts/commit.sh
```
**STOP after review day. Do not generate 5 sections.**

---

## NORMAL DAY — Generate 5 Sections

For each section (1-5), read `/tmp/bbb-section-N.txt` and write content to its ARCHIVE_PATH.

### Section 1: System Design (3 min)
🏗️ **系统设计 Day N / System Design Day N**
- Real-world scenario ("想象你在设计...")
- ASCII architecture diagram
- Key tradeoffs (为什么这样设计？)
- Common mistakes (别踩这个坑)
- 📚 References (3 real URLs) + 🧒 ELI5

### Section 2: Algorithms (4 min)
💻 **算法 Day N / Algorithms Day N** — #NUM TITLE (DIFFICULTY) — PATTERN
- 🔗 LeetCode link + 🟢🟡🔴 badge + 📹 NeetCode link
- Real-world analogy → problem → key insight → Python solution with trace → complexity
- 举一反三 / Pattern Recognition with related problems
- 📚 References + 🧒 ELI5
- **Also write** `/tmp/bbb-quiz-2.json`: `{"question":"...","options":[4 items],"correct_index":N}`

### Section 3: Soft Skills (2 min)
🗣️ **软技能 Day N / Soft Skills Day N**
- Why this matters → STAR breakdown → ❌ Bad vs ✅ Good → Senior/Staff tips → Key Takeaways
- 📚 References + 🧒 ELI5

### Section 4: Frontend (2 min)
🎨 **前端 Day N / Frontend Day N**
- "猜猜这段代码输出什么？" quiz with A/B/C/D
- Code examples + gotchas + mini challenge
- 📚 References + 🧒 ELI5
- **Also write** `/tmp/bbb-quiz-4.json`: `{"question":"...","options":[4 items],"correct_index":N}`

### Section 5: AI (2 min)
🤖 **AI Day N**
- **NEWS mode**: Use `web_search` to find 3-5 real current AI stories. DO NOT write from memory. Each story: source URL + "为什么你应该关心". If web_search is unavailable or returns no results, fall back to CONCEPT mode instead: read the CONCEPT topic from `/tmp/bbb-section-5.txt` and generate a concept explanation.
- **CONCEPT mode**: Intuitive explanation → how it works → applications → runnable Python snippet (≤15 lines, include pip install)
- 📚 References + 🧒 ELI5

## Verify & Advance State

After writing ALL 5 files:
```bash
TODAY=$(date +%Y-%m-%d)
for s in system-design algorithms soft-skills frontend ai; do
  FILE="{{BBB_REPO_DIR}}/archive/${TODAY}-${s}.md"
  [ ! -f "$FILE" ] && echo "MISSING: $FILE" && exit 1
  echo "✅ ${s}: $(wc -c < "$FILE") bytes"
done
bash {{BBB_REPO_DIR}}/scripts/advance-state.sh
```
**If any file missing, re-generate it before continuing.**

## Review Gate

Re-read each archive. Verify:
- Algorithms: trace the code with example input. Fix if wrong.
- Frontend: calculate the quiz answer yourself. Fix if wrong.
- AI NEWS: every story must come from web_search. If not, search now.
- System Design: diagram data flow is logical.

## Send via Telegram

Order: Progress+SysDesign → Algorithms → AlgoQuizPoll → SoftSkills → Frontend → FrontendQuizPoll → AI

- Message 1: progress header + system design content (channel: telegram, target: {{TELEGRAM_TARGET}})
- Message 2: algorithms content
- Poll 2b: quiz from /tmp/bbb-quiz-2.json (pollAnonymous: false)
- Message 3: soft skills
- Message 4: frontend
- Poll 4b: quiz from /tmp/bbb-quiz-4.json (pollAnonymous: false), then "🧩 Did you get it right?"
- Message 5: AI

## Send Email & Commit (MANDATORY)

```bash
python3 {{BBB_REPO_DIR}}/scripts/send-email.py
bash {{BBB_REPO_DIR}}/scripts/commit.sh
```

## Rules
- Bilingual: Chinese first, English second
- All references must be real URLs — never fabricate
- Code comments in English
- Each section standalone and readable
- If any Telegram message exceeds 4000 characters, split it into 2 messages at a natural section break (e.g., after a `---` divider). Telegram's limit is 4096 chars.
