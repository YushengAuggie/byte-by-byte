Generate a Saturday Deep Dive for byte-by-byte — one topic, 15-20 min read, bilingual (Chinese first, English second).

## Step 0: Load State

```bash
cat {{BBB_REPO_DIR}}/state.json
```

Build progress header:
```
📊 Day {currentDay}/150 · NeetCode: {leetcodeIndex}/150 · SysDesign: {systemDesignIndex}/40 · Behavioral: {behavioralIndex}/40 · Frontend: {frontendIndex}/50 · AI: {aiTopicIndex}/30
🔥 {streak}-day streak!
```

## Step 1: Run generator & pick topic

```bash
bash {{BBB_REPO_DIR}}/scripts/generate.sh
```

Read `/tmp/bbb-section-{1..5}.txt`. Pick the **most complex topic**:
1. Hard LeetCode problem → deep dive that
2. Advanced system design → deep dive that
3. Otherwise → Frontend or AI concept

**IMPORTANT: Only write the deepdive archive file. Do NOT write individual section archives (system-design, algorithms, etc.) — those are for weekdays only.**

## Step 2: Generate Deep Dive

Save to `{{BBB_REPO_DIR}}/archive/$(date +%Y-%m-%d)-deepdive.md`:

```
🔬 **Saturday Deep Dive: {TOPIC} (15 min read)**
📊 {PROGRESS_HEADER}

## Overview / 概述
[What and why it matters]

## Part 1: Theory / 理论基础 (5 min)
[Core concepts, mental models]

## Part 2: Step-by-Step Implementation / 一步一步实现 (8 min)
[Complete working code, heavily commented]
[Algorithms: naive → optimal approaches]
[System design: full architecture]

## Part 3: Edge Cases & Gotchas / 边界情况 (2 min)
[What breaks it]

## Part 4: Real-World Application / 实际应用 (2 min)
[Where this shows up in production]

## Part 5: Interview Simulation / 面试模拟 (3 min)
[5 follow-up questions with brief answers]
```

For algorithms: include 🔗 LeetCode + 📹 NeetCode links.

## Step 3: Advance State — Do NOT send

```bash
bash {{BBB_REPO_DIR}}/scripts/advance-state.sh
echo "ready" > /tmp/bbb-content-ready
```

**STOP here.** Do not send Telegram, email, or commit.
The review-and-send cron (runs 5 min later) handles QA, fixes, and delivery.

## Rules
- Bilingual: Chinese first, English second
- All references must be real URLs
- Code comments in English
