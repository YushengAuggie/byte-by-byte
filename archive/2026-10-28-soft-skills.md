🗣️ **软技能 / Soft Skills** — Synthesis: Writing a Staff-Level Promotion Packet

Senior → Staff 升职的核心难点不是"做了什么"，而是**如何讲清楚你的 scope、leverage、impact**。所有 60 道行为题的本质其实都是在训练这三件事的叙事能力。今天综合一个 **Staff 升职 packet 的写作框架**。

The hardest part of Senior → Staff isn't *what you did* — it's **articulating scope, leverage, and impact**. All 60 behavioral questions trained these three narrative muscles. Today: a synthesis — the **Staff promo packet framework**.

---

### 为什么重要 / Why This Matters

Staff+ 是公司对你的赌注：你是不是能让 **整个组织** 变得更好，而不只是写好自己的代码。Promo committee 看的是 **lasting change**，不是 shipped tickets。

Staff+ is a bet that you make the **org** better, not just your tickets. Committees look for **lasting change**.

---

### Staff Packet 的 STAR+L 框架 / STAR+L Framework

> **S**ituation · **T**ask · **A**ction · **R**esult · **L**everage

传统 STAR 卡在"你一个人做了什么"。Staff 层级必须加 **L (Leverage)**：你的工作如何通过别人放大？

| 要素 | Senior 版本 | Staff 版本 |
|---|---|---|
| Situation | "Service was slow" | "Company's largest revenue surface had 2x latency SLO breach impacting 3 PMs' roadmaps" |
| Task | "I was asked to fix it" | "I proposed and secured funding for a 6-month platform migration" |
| Action | "I rewrote the hot path" | "I wrote the RFC, built the first vertical slice, then enabled 4 teams to migrate independently via a self-serve toolkit" |
| Result | "p99 dropped 40%" | "p99 dropped 40%, 4 teams migrated with zero on-call support from me, pattern adopted by 2 other orgs" |
| **Leverage** | — | "My RFC + toolkit → 25 engineers now ship 2x faster on this platform" |

---

### ❌ Bad vs ✅ Good — 真实 Promo Bullet

**❌ Bad (Senior-level thinking):**
> "Led migration of auth service to new framework. Reduced p99 by 40%."

Promo committee 心里：*So what? Did anyone else benefit? What was hard?*

**✅ Good (Staff-level narrative):**
> "Identified org-wide risk: 7 services relied on a deprecated auth library with 2 known CVEs. Instead of fixing them one-by-one (6 months × 7 teams), I designed a **shared migration framework** (RFC #412), built a reference migration, and ran weekly office hours. **Outcome**: all 7 services migrated in 8 weeks; framework reused for 3 subsequent library migrations; 2 teams promoted engineers using this work."

**三个 staff signal**: (1) org-wide problem framing, (2) leverage via framework not fix, (3) second-order outcomes (reuse, promotions).

---

### Senior/Staff 层级的 3 个常见陷阱 / 3 Common Pitfalls

1. **"Hero narrative" 陷阱** — 全写"我一个人救火"。Staff 该写的是"我设计了一个系统，让火不再发生"。
2. **缺少 counterfactual** — 不说明"如果没有我这个工作会怎样"。Promo committee 的默认假设：别人也能做。你要显式反驳。
3. **Impact 单位错了** — Senior 以 service/feature 为单位；Staff 以 **org / quarterly plan / headcount saved** 为单位。把 "40% latency reduction" 翻译成 "$X in prevented revenue loss" 或 "unblocked 2 PM roadmaps"。

---

### Key Takeaways

- **Scope**: 讲 problem framing，不要讲 task assignment
- **Leverage**: 每个 bullet 都问"这个工作如何通过别人放大？"
- **Impact in business units**: latency → revenue, bugs → trust, migrations → engineer-weeks saved
- **Written artifacts win**: RFC、design doc、postmortem 是最硬的 staff 证据
- **Peer feedback is signal**: Promo committee 更信 cross-team peers 的反馈，不信你 manager

---

### 📚 References
- Will Larson, *StaffEng*: https://staffeng.com/guides/promo-packets/
- Gergely Orosz, "The Scoop on Promo Packets": https://blog.pragmaticengineer.com/software-engineering-promotions/
- Tanya Reilly, *The Staff Engineer's Path* (O'Reilly, 2022): https://www.oreilly.com/library/view/the-staff-engineers/9781098118723/

### 🧒 ELI5
升职就像写简历，但要讲一个故事：不是"我拧了很多螺丝"，而是"我发明了一把扳手，整个工厂的人现在都用它拧螺丝，省了一半时间"。
