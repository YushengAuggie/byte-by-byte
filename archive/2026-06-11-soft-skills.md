# Day 63 — 软技能 / Soft Skills

🗣️ **软技能 / Soft Skills** · Day 63 · Expert Phase · Decision Making

---

## Behavioral Question

> **"Tell me about a time you had to make a decision with incomplete information. How did you decide whether it was reversible?"**  
> **"讲一个你在信息不全的情况下做决策的经历。你如何判断它是否可逆?"**

---

### 为什么面试官问这个 / Why Interviewers Ask This

Senior+ 工程师每天都在**信息不全**的情况下做决策。面试官想看:
1. **你如何区分可逆 vs 不可逆决策** — 这决定了你该花多少时间
2. **你是否会被"分析瘫痪"困住** — 还是能在不确定中前进
3. **你如何控制下行风险** — 万一错了,代价多大?能不能回滚?

*Interviewers want to see if you can move forward under uncertainty while controlling downside risk.*

---

### 核心框架:Bezos 的"双向门" / The One-Way vs Two-Way Door

亚马逊的经典心智模型:

- **双向门(可逆)/ Two-way door:** 决策错了可以走回来。比如:加一个 feature flag、改一个配置、试一个新库。**快速决策,低成本试错。** 不要让这类决策走重型评审流程。
- **单向门(不可逆)/ One-way door:** 一旦走过去就回不来。比如:删除生产数据、公开 API 契约、选择数据库引擎、对外承诺。**慢决策,多收集信息,多方评审。**

> 关键 insight:**大多数决策是可逆的**,但我们常常错误地用对待单向门的谨慎去处理双向门,导致团队变慢。

---

### STAR 框架分解 / STAR Breakdown

**Situation:** 什么决策?信息缺了哪一块?时间压力多大?

**Task:** 你的角色 — 是你拍板,还是你给出建议?

**Action(核心):**
1. **先分类:** 这是单向门还是双向门?(明确说出你的判断依据)
2. **如果可逆:** 设计安全网 — feature flag、灰度发布、可回滚的迁移。然后**快速决策并执行**。
3. **如果不可逆:** 列出关键未知项,定向收集信息(原型、A/B、专家咨询),设定一个"信息足够好"的停止线。
4. **量化下行:** "最坏情况是什么?能承受吗?"

**Result:** 决策结果 + **你后来如何验证判断对错** + 学到了什么。

---

### ❌ Bad vs ✅ Good

❌ **Bad:** "我们没有足够信息,所以我等了两周收集更多数据。" → 暴露了无法在不确定中行动。

✅ **Good:** "我判断这是个可逆决策——加个 feature flag 就能秒回滚。所以我们当天就上线灰度,用真实流量验证假设,两小时拿到数据,比讨论两周更可靠。"

---

### Senior / Staff Tips

- 明确说出"reversible / irreversible"这个词 — 展示你有结构化的决策心智模型
- 强调**决策速度本身也是一种成本** — 慢决策让整个团队等待
- Staff 级别:展示你**帮团队建立了这种决策文化**,而不只是自己会做

---

### Key Takeaways

- 可逆决策 → 快、轻、本地化;不可逆决策 → 慢、重、多评审
- 把不确定性变成"可控的下行风险",而不是行动的借口
- 永远准备好回答:"你后来怎么知道这个决策是对的?"

---

### 📚 References
- [Jeff Bezos 2015 Shareholder Letter — One-way vs two-way doors](https://www.sec.gov/Archives/edgar/data/1018724/000119312516530910/d168744dex991.htm)
- [Reversible vs Irreversible Decisions (Farnam Street)](https://fs.blog/reversible-irreversible-decisions/)

🧒 **ELI5:** 有些门推开还能再推回来(随便试),有些门一关就锁死(要想清楚再走)。先看清是哪种门,再决定要多小心。
