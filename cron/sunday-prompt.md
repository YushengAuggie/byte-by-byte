Generate a Sunday Week in Review for byte-by-byte — summarize the past week, bilingual (Chinese first, English second).

## Step 0: Load State

```bash
cat {{BBB_REPO_DIR}}/state.json
```

Build progress header:
```
📊 NeetCode: {leetcodeIndex}/150 · SysDesign: {systemDesignIndex}/40 · Behavioral: {behavioralIndex}/40 · Frontend: {frontendIndex}/50 · AI: {aiTopicIndex}/30
🔥 {streak}-day streak!
```

## Step 1: Read this week's archives

```bash
ls -la {{BBB_REPO_DIR}}/archive/ | tail -30
```

Read each archive file from the past 6 days (Mon–Sat).

## Step 2: Generate Week in Review

Save to `{{BBB_REPO_DIR}}/archive/$(date +%Y-%m-%d)-week-review.md`:

```
📅 **Week in Review — Week {WEEK_NUM} (10 min read)**
📊 {PROGRESS_HEADER}

## 🗓️ This Week's Journey / 本周回顾
[1-line summary per day]

## 🧠 System Design: Key Takeaways / 系统设计要点
[Top 3 concepts, what connects them]

## 💻 Algorithms: Patterns Mastered / 算法模式总结
[Problems by pattern, key insight per pattern]

## 🗣️ Soft Skills: What to Practice / 软技能练习重点
[Scenarios covered, which needs practice]

## 🎨 Frontend: Concepts to Lock In / 前端知识巩固
[Topics covered, quick self-check]

## 🤖 AI: What Stuck / AI 知识点
[Most important takeaway]

## ⚠️ What to Review / 需要复习的内容
[Weakest areas, specific suggestions]

## 🏆 Win of the Week / 本周亮点
[One thing to celebrate]

## 🎯 Next Week Preview / 下周预告
[Upcoming topics based on indices]
```

## Step 3: Do NOT send

```bash
echo '{"type":"week-review","date":"'$(date +%Y-%m-%d)'"}' > /tmp/bbb-content-ready
```

**STOP here.** Do not send Telegram, email, or commit.
The review-and-send cron (runs 5 min later) handles QA, fixes, and delivery.

## Rules
- Bilingual: Chinese first, English second
- Summarize accurately from actual archive content — don't invent
- For AI section highlights: if any figure/claim was from a NEWS day, add "据报道" qualifier (recurring hallucination issue)
- Do NOT write individual section archive files — only the week-review file
