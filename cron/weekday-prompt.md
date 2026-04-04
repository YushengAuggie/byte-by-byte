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

### Section 2: Algorithms (4 min) — PATTERN-BASED TEACHING
💻 **算法 Day N / Algorithms Day N** — #NUM TITLE (DIFFICULTY) — PATTERN

Read `/tmp/bbb-section-2.txt` carefully. It contains pattern context:
- `IS_FIRST_IN_PATTERN`: if "yes", this is the FIRST problem in a new pattern block. **Start with the pattern template** before the problem.
- `PATTERN_TEMPLATE_NAME`, `WHEN_TO_USE`, `SIGNALS`, `PYTHON_TEMPLATE`, `TEMPLATE_KEY_INSIGHT`: the reusable pattern template.
- `POSITION_IN_BLOCK`: e.g., "3/7" means 3rd of 7 problems in this pattern.
- `BLOCK_PROBLEMS`: all problems in this pattern block for context.

**If IS_FIRST_IN_PATTERN = yes:**
Start the section with a **Pattern Introduction** box:
```
🧩 **新模式 / New Pattern: {PATTERN_TEMPLATE_NAME}**
📍 This block: {BLOCK_PROBLEMS count} problems

**什么时候用 / When to use:** {WHEN_TO_USE}
**识别信号 / Signals:** {SIGNALS}

**通用模版 / Template:**
{PYTHON_TEMPLATE}

**核心洞察 / Key Insight:** {TEMPLATE_KEY_INSIGHT}
```
Then proceed with today's problem, explicitly showing how it maps to the template.

**If IS_FIRST_IN_PATTERN = no:**
Start with: `🧩 **{PATTERN} ({POSITION_IN_BLOCK})** — building on the template from Day X`
Show how today's problem is a **variation** of the template. Highlight what's different from previous problems in this block.

Content for every problem:
- 🔗 LeetCode link + 🟢🟡🔴 badge + 📹 NeetCode link
- Real-world analogy → problem → **map to pattern template** → Python solution with trace → complexity
- 举一反三: connect to other problems in the SAME pattern block
- 📚 References + 🧒 ELI5
- **Also write** `/tmp/bbb-quiz-2.json`: `{"question":"...","options":[4 items],"correct_index":N}`

### Section 3: Soft Skills (2 min)
🗣️ **软技能 Day N / Soft Skills Day N**
- Why this matters → STAR breakdown → ❌ Bad vs ✅ Good → Senior/Staff tips → Key Takeaways
- 📚 References + 🧒 ELI5

### Section 4: Frontend — React/TypeScript 实战 (2 min)
🎨 **前端 Day N / Frontend Day N**
Focus on **practical, production-ready** React/TypeScript/Next.js knowledge:
- Start with a **real scenario**: "你在做一个 dashboard，需要..." / "You're building a dashboard and need to..."
- Show a **code snippet** that demonstrates the concept (React component, hook, or TypeScript type)
- "猜猜这段代码输出什么？" quiz with A/B/C/D (for hooks/JS behavior topics)
- **Common mistake** → **correct approach** (❌ vs ✅ code comparison)
- **When to use / when NOT to use** — practical decision framework
- 📚 References (MDN, React docs, real blog posts) + 🧒 ELI5
- **Also write** `/tmp/bbb-quiz-4.json`: `{"question":"...","options":[4 items],"correct_index":N}`

### Section 5: AI (2 min)
🤖 **AI Day N**
- **NEWS mode**: Search the web for 3-5 real current AI stories. Use whatever search tool is available (`web_search`, `web_fetch`, or your built-in web browsing). DO NOT write from memory. Each story: source URL + "为什么你应该关心". If no search tool works, fall back to CONCEPT mode instead: read the CONCEPT topic from `/tmp/bbb-section-5.txt` and generate a concept explanation.
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
**If any file missing, re-generate it before advancing.**

## STOP — Do NOT send Telegram, email, or commit

Content generation and state advancement are complete. **Do not send anything.**
The review-and-send cron (runs at 8:05) will handle QA, fixes, and delivery.

## Rules
- Bilingual: Chinese first, English second
- All references must be real URLs — never fabricate
- Code comments in English
- Each section standalone and readable
- If any Telegram message exceeds 4000 characters, split it into 2 messages at a natural section break (e.g., after a `---` divider). Telegram's limit is 4096 chars.
