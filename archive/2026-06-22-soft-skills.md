# 🗣️ 软技能 / Soft Skills — Day 59
**Topic:** Crisis Management — On-Call for a System You Didn't Build
**Question:** How do you handle being on-call for a system you didn't build?
**Date:** 2026-06-22 | **Level:** Senior/Staff

---

## 为什么这很重要 / Why This Matters

这是面试里经典的高分题。每个工程师都会被要求 on-call 一个不熟悉的系统。面试官想看的是：
- 你在不确定环境下的系统思维
- 你是否会主动建立 context，而不是被动等着出事
- 你怎么在压力下保持冷静

This is a classic high-signal interview question. Every engineer gets paged for systems they don't own. The interviewer wants to see your systematic thinking under uncertainty, proactive behavior, and composure under pressure.

---

## STAR 分解 / STAR Breakdown

**Situation（背景）:**
"我接手了另一个团队的支付处理服务的 on-call。那个服务是他们三年前写的，文档很少，原作者已经离职了。"

**Task（任务）:**
"我需要在第一次 on-call 前确保自己能处理任何 P0 事故，同时不能打扰原团队的工作。"

**Action（行动）:**
1. **主动 context 建立** — 接手前两周，每天花 30 分钟读代码、traces、历史 alert。重点看过去 6 个月的 incident tickets，找出 top 5 告警类型。
2. **制作 runbook** — 把每种告警写成 runbook：症状、常见原因、第一步排查命令、升级标准。没有 runbook 的告警我不接受接手。
3. **预演** — 找原团队 senior 工程师做一次 shadowing，他们 walk through 一个 P1 场景，我主导排查，他们纠错。
4. **建立 escalation 路径** — 明确什么情况应该立刻叫醒谁，而不是自己扛。

**Result（结果）:**
"第一个月接了 3 个告警，2 个独立解决，1 个在 15 分钟内升级。MTTR 比原团队历史平均低了 20%，因为 runbook 比他们之前的文档更新更清晰。"

---

## ❌ Bad vs ✅ Good

❌ **差答案：**
"我会边学边做，出了问题再去找人问。"
— 没有准备，等到出事才行动，让人担心你能否独立应对。

✅ **好答案：**
"我会在 on-call 开始前主动建立 context，写 runbook，做 shadowing，并明确升级路径。出事了按流程走，不超出我能力范围就独立处理，超出就快速升级。"

❌ **陷阱回答：**
"我相信自己能学得很快。" — 这是关于过程和系统性思维的问题，不是能力问题。

---

## Senior/Staff 加分点 / Senior/Staff Tips

**Staff level 思维 — 不只是个人 on-call：**
1. **把 runbook 标准化** — 将自己做的 runbook 模板推广到整个 org，减少 knowledge silos
2. **做 alert 质量审查** — 接手后发现 30% 的 alert 是 noisy，提议做 alert fatigue review，降低 false positive 率
3. **推动 ownership 模型改进** — 提出"服务转移 checklist"，防止下次又有人接手残缺系统

**关键词 / Key Phrases:**
- "Proactive context building before the first page"
- "Alert-to-runbook mapping"
- "Clear escalation criteria — I know exactly when to call someone"
- "Service handoff checklist"

---

## 关键要点 / Key Takeaways

1. **接手前主动建立 context** — 不要等到 3 AM 才去读代码
2. **Runbook 是硬性要求** — 没有 runbook 的服务不应该接
3. **知道何时升级** — 快速升级不是失败，犹豫不决才是
4. **把经验制度化** — 把你学到的转化为团队资产

---

## 🧒 ELI5

想象你要帮同学照顾他的宠物狗，但你从没见过这只狗。好的做法是：事先问清楚狗的习惯、医疗记录、遇到紧急情况打谁的电话。而不是等狗生病了再说"我不知道怎么办"。On-call 就是这只狗。

---

## 📚 References
- Google SRE Book — Being On-Call: https://sre.google/sre-book/being-on-call/
- PagerDuty Runbook Guide: https://www.pagerduty.com/resources/learn/what-is-a-runbook/
- Increment — On-Call: https://increment.com/on-call/
