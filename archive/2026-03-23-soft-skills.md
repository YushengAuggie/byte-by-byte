# 🗣️ 软技能 Day 8 / Soft Skills Day 8
**题目 / Question:** 你如何处理模糊不清的需求？ / How do you approach working with ambiguous requirements?
**分类 / Category:** Ambiguity · Senior/Staff Level · Foundation Phase

---

## 🎯 为什么这很重要 / Why This Matters

在大厂，**模糊是常态，而非例外**。产品经理不可能把每个细节都想清楚，业务方也不总知道自己真正想要什么。能优雅处理模糊需求，是区分 senior 工程师和 staff 工程师的核心能力之一。

*In big tech, ambiguity is the norm, not the exception. PMs can't anticipate every detail, and stakeholders don't always know what they really want. Navigating ambiguity gracefully separates senior engineers from staff engineers.*

---

## ⭐ STAR 拆解 / STAR Breakdown

**情境 Situation:** 描述一个需求不清晰的真实场景  
*Describe a real scenario where requirements were unclear*

**任务 Task:** 你被分配了什么？你需要负责什么？  
*What were you assigned? What were you accountable for?*

**行动 Action:** 你具体做了哪些事来厘清需求、推进工作？  
*What specific steps did you take to clarify and move forward?*

**结果 Result:** 量化影响——节省了多少时间？避免了什么返工？  
*Quantify impact — time saved, rework avoided, team unblocked?*

---

## ❌ 差的回答 vs ✅ 好的回答 / Bad vs Good Answer

### ❌ 差的回答
> "需求不清楚的时候，我就等产品经理把需求整理清楚，再开始做。"  
> "When requirements are unclear, I wait for the PM to clarify everything before starting."

**问题：** 被动等待，没有主动推进。这在面试中是红牌。  
*Problem: Passive waiting shows no ownership or initiative — a red flag in interviews.*

---

### ✅ 好的回答（结构化）

**S:** 我们在设计一个新的通知系统，PM 只说"用户应该能收到重要通知"，但没有定义什么是"重要"，也没有给出频率和渠道的要求。

*S: We were designing a new notification system. The PM only said "users should receive important notifications" — no definition of "important," no frequency or channel requirements.*

**T:** 我是 tech lead，需要在两周内给出技术方案，但需求太模糊无法开始。

*T: I was the tech lead, needing to deliver a technical plan in two weeks, but the requirements were too vague to start.*

**A:** 我做了三件事：
1. **先列假设清单**：把我理解的"默认行为"写成文档，发给 PM 确认（"我假设通知包括订单状态变更和系统告警，是否正确？"）
2. **识别 reversible vs irreversible 决策**：渠道选择（邮件/推送）容易改，数据库 schema 难改——对难改的部分花更多时间对齐
3. **用 spike + timebox**：花一天做技术调研验证假设，而不是等两周后再发现方向错了

*A: I did three things:*
*1. Made an assumption document — wrote down my "default understanding," sent to PM for confirmation*
*2. Identified reversible vs irreversible decisions — channel choice is easy to change; DB schema is hard — spent more alignment time on hard decisions*
*3. Used a spike + timebox — one day of research to validate assumptions rather than discover wrong direction two weeks later*

**R:** 提前 4 天完成方案，避免了一次因误解"重要通知"而可能导致的数据库重新设计（估计 1.5 周返工）。

*R: Delivered the plan 4 days early, avoiding a potential DB redesign from misunderstanding "important notifications" (estimated 1.5 weeks of rework).*

---

## 👑 Senior/Staff 进阶技巧 / Senior/Staff Tips

1. **区分"紧急不可逆"和"可以先行"** — 并非所有模糊都需要澄清后才能动手。  
   *Distinguish "critical & irreversible" ambiguity from "can start anyway." Not all ambiguity blocks progress.*

2. **用"约束条件反问"** — 不要问"你想要什么"，而是"有哪些约束条件？"（deadline、预算、不能动哪些系统）  
   *Ask about constraints rather than desires: "What can't change?" uncovers real requirements faster.*

3. **两次沟通法则** — 如果你向同一个人问了两次同样的问题还没答案，换个方式：写 RFC，开会对齐，或者向上升级。  
   *Two-ask rule: If you've asked the same person twice with no answer, escalate the format — write an RFC, schedule alignment, or escalate.*

4. **让数据说话** — "我们先做一个小实验来验证假设"比"我不确定需求是什么"更有说服力。  
   *Let data clarify: "Let's run a small experiment" is more powerful than "I'm not sure what we need."*

---

## 🎯 关键要点 / Key Takeaways

- 🔑 模糊是工程师的日常，主动澄清是职业素养
- 🔑 区分"必须澄清"和"可以默认处理"的需求
- 🔑 把假设写成文档，发出去确认，保留记录
- 🔑 先行动，后优化——不要等到 100% 清晰

*Ambiguity is daily life in engineering. Proactive clarification is professional maturity. Document assumptions. Move forward on reversible decisions, pause on irreversible ones.*

---

## 📚 References

- [Gergely Orosz: "The Art of Asking Questions"](https://newsletter.pragmaticengineer.com/)
- [StaffEng.com: Staff-level behaviors](https://staffeng.com/guides/engineering-strategy)
- [Amazon LP: "Bias for Action" principle](https://www.amazon.jobs/content/en/our-workplace/leadership-principles)

## 🧒 ELI5

如果老师说"画一幅漂亮的画"，你不知道要画什么。聪明的做法是先问："可以是动物吗？用什么颜色？多大？" 然后开始画，完成后再调整。而不是坐在那里什么都不做，等老师来告诉你每一步。

*If a teacher says "draw something beautiful" without details, the smart move is to ask: "Can it be an animal? What colors? How big?" Then start drawing and adjust. Not sit frozen waiting for the teacher to specify every brushstroke.*
