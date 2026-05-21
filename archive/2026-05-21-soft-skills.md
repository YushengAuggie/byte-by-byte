# 🗣️ 软技能 / Soft Skills — Day 48
## 影响力 / Impact

> **题目 / Question:** Tell me about the most impactful thing you've built. Why was it impactful?
> **级别 / Level:** Senior/Staff | **Phase:** Mastery | **预计时间 / Read time:** 2 min

---

## 🎯 为什么这道题重要 / Why This Matters

Senior/Staff 面试最看重"影响力"——不是你写了多少代码，而是你的工作影响了多少人、多少系统、多少业务结果。这道题考察你能否将技术工作与业务价值直接挂钩。
*Senior/Staff interviews center on impact — not lines of code, but how many people, systems, and business outcomes your work affected. This tests whether you can directly link technical work to business value.*

---

## ⭐ STAR 框架 / STAR Breakdown

| | 中文 | English |
|---|---|---|
| **Situation** | 公司面临什么问题？规模、背景 | What problem was the company facing? Scale, context |
| **Task** | 你的角色和责任是什么？ | What was your role and ownership? |
| **Action** | 具体做了什么技术决策？ | What specific technical decisions did you make? |
| **Result** | 量化结果（用户、收入、延迟、成本） | Quantified results (users, revenue, latency, cost) |

---

## ❌ 差回答 vs ✅ 好回答 / Bad vs Good

**❌ 差：**
> "我做了一个 API 重构，让代码更整洁了。"

*"I refactored an API, made the code cleaner."*

问题：没有规模、没有结果、没有业务价值。
*Problem: No scale, no results, no business value.*

---

**✅ 好：**
> "我在 2024 年重新设计了我们的实时通知系统。当时系统每天丢失约 0.8% 的消息，影响到 200 万活跃用户的核心 UX。我主导了从 HTTP polling 迁移到 WebSocket + Kafka 的架构，协调了 3 个团队，用 8 周完成了零停机迁移。上线后消息丢失率降到 <0.01%，DAU 提升了 12%，因为用户不再频繁刷新页面。这个系统现在每天处理 4 亿条消息。"

*"I redesigned our real-time notification system in 2024. The system was dropping ~0.8% of messages per day, affecting 2M active users' core UX. I led the migration from HTTP polling to WebSocket + Kafka, coordinated 3 teams, and completed zero-downtime migration in 8 weeks. After launch, message loss dropped to <0.01%, and DAU increased 12% because users stopped manual refreshing. The system now handles 400M messages per day."*

---

## 👑 Senior/Staff 加分技巧 / Senior/Staff Tips

1. **谈架构决策，不只是实现** — "我选择 Kafka 而不是 RabbitMQ，因为我们需要消息回放能力。"
   *Talk about architectural decisions, not just implementation.*

2. **量化多维影响** — 用户数量 + 性能指标 + 业务指标（三者都说）
   *Quantify multi-dimensional impact: users + performance + business metrics (all three).*

3. **说明为什么是你** — "在我之前，团队尝试过两次，都因为……而失败。我的方案解决了……"
   *Explain why it required you specifically — what previous attempts failed at.*

4. **提长期影响** — 这个系统后来被其他团队复用了吗？成了平台能力？
   *Mention long-term ripple effects — was it reused by other teams? Did it become a platform capability?*

---

## 💡 关键要点 / Key Takeaways

- 影响力 = 规模 × 深度 × 持久性 / *Impact = Scale × Depth × Durability*
- 用真实数字，哪怕是近似值（"约 200 万"比"很多用户"好）
  *Use real numbers, even approximations ("~2M" beats "many users")*
- Staff 级别要展示跨团队影响，不只是自己团队
  *Staff level: show cross-team impact, not just your own team*

---

## 📚 References
- [Lenny's Newsletter — How to talk about impact in interviews](https://www.lennysnewsletter.com/p/how-to-talk-about-impact)
- [Engineer's Ladder — Calibrating for Senior/Staff](https://progression.fyi/)
- [Gergely Orosz — The Staff Engineer's Path](https://www.engguidebook.com/)

---

## 🧒 ELI5
面试官想知道你不只是"搬砖工"，而是改变了游戏规则的人。就像问"你做过最厉害的沙堡是什么"——你要说的不是"我用了很多沙子"，而是"我做了一个 3 层城堡，10 个人在里面住了一周"。
*The interviewer wants to know you're not just a code monkey but a game-changer. Like "what's the coolest sandcastle you've built?" — don't say "I used lots of sand." Say "I built a 3-tier castle where 10 people lived for a week."*
