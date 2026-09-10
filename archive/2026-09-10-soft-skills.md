# 🗣️ 软技能 / Soft Skills — Day 131 (Synthesis)
**主题：Principal/Staff 级别的影响力框架 — 没有汇报关系时如何推动变革**
**Topic: Principal/Staff-Level Influence — Driving Change Without Direct Authority**

---

## 为什么这道题考的是你的级别 / Why This Question Reveals Your Level

Staff 和 Principal 工程师最大的误解是：「我只要把技术做好就行了」。

错。**技术做得好只是门票，推动它被采用才是真正的工作。**

The biggest misconception about Staff/Principal engineers: "I just need to write great code."

Wrong. **Technical excellence is the entry ticket. Getting it adopted is the actual job.**

---

## 场景 / STAR Scenario

> "Tell me about a time you influenced a major technical decision without having the authority to mandate it."

---

## ❌ 初级回答 / Junior Answer

「我在技术评审会上提了我的方案，解释了为什么更好，最后大家采纳了。」

问题：被动等待，没有利益相关者管理，运气成分大。

---

## ✅ Staff 级别回答框架 / Staff-Level Answer Framework

**S（Situation）：** 不同团队的服务认证体系各自为战（JWT 自签、OAuth 混用、API key 明文），新的安全审计要求统一。

**T（Task）：** 我没有权限强制推行，但需要在 3 个团队间对齐，推动采用统一的 Auth SDK。

**A（Action）：**
1. **先做侦察（reconnaissance）：** 花一周分别和 3 个团队 TL 一对一，了解他们的痛点和顾虑。不是来说服，而是来倾听。
2. **把问题变成共同的敌人：** 把「我要推一个方案」转化成「我们共同面临一个安全风险，一起解决」。
3. **写 RFC，不是 Spec：** RFC（Request for Comments）邀请反馈，Spec 是命令。给每个团队 2 周评论期。
4. **接受有意义的修改：** 团队 B 提出保留 JWT 兼容性，我研究后认为合理，接受了这个建议。他们因此成为推行的盟友。
5. **做试点，不做强制：** 第一个团队自愿试点，成功后数据说话，其他团队自然跟进。

**R（Result）：** 4 个月后 3 个团队全部迁移。安全审计通过。更重要的是：这个 RFC 流程被采用为整个 Org 的技术决策框架。

---

## 关键原则 / Key Principles for Senior/Staff

### 1. 影响力始于理解，而非说服
**Influence begins with understanding, not persuasion.**
先问「你担心什么？」再问「你怎么看我的方案？」

### 2. 创造选项，不是二选一
给出 3 个方案（A/B/C），你偏向 B，但让别人选。人们更愿意接受自己「选择」的结论。

### 3. 时间换信任
强推一个月 vs 慢推三个月——慢的反而更快落地，因为没有阻力。

### 4. 把你的成功和他人的成功绑定
「这个 SDK 上线后，你们的 on-call 告警会减少 30%」比「这样更安全」更有说服力。

---

## 面试追问准备 / Prepare for Follow-ups

- "What if one team still refused after your RFC process?"
  → 升级路径：找共同的 Manager/Director，但带着数据和已有的共识来，不是告状

- "How do you know when to stop pushing?"
  → 有时「不是现在」是对的答案。评估阻力来源：技术顾虑（可解决）还是政治（需等待时机）

---

## 📚 References
- https://staffeng.com/guides/work-on-what-matters
- https://lethain.com/finding-the-right-company/
- https://www.amazon.com/Staff-Engineer-Leadership-beyond-management/dp/1736417916

## 🧒 ELI5
你想让班里所有同学都用同一款笔记本格式。你不是班长，没有权力强制。
最聪明的做法：先问大家现在用什么格式有什么烦恼，再设计一个解决大家烦恼的格式，邀请大家来改进它，然后找最愿意尝试的同学先用。其他人看到效果好，自然跟上。
