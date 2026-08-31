# 🗣️ 软技能 / Soft Skills — Day 122 (Synthesis)
**场景题：你发现你们的 On-Call 文化正在把团队压垮**
**Scenario: You Discover Your On-Call Culture is Breaking the Team**

---

## 为什么这个场景重要

Day 43 讲过 on-call 基础，Day 62 讲过事故处理。但 Staff 工程师面对的更难的问题是：**系统性问题**——不是某次事故，而是一整个文化在慢慢侵蚀团队。这类题测的是你能不能从执行者变成系统改造者。

---

## 场景设定

> 你是一位 Staff Engineer。过去三个月，团队的 on-call 每周平均被叫醒 4 次（凌晨 1-5 点），离职率上升了 30%，最近一个季度有两个高级工程师辞职，理由都是"精力耗尽"。你的 EM 知道有问题，但觉得"这就是创业公司的代价"。

**面试官问：** "你会怎么处理这件事？"

---

## STAR 拆解

**Situation（背景）：**
系统告警频繁，但大部分是低优先级或误报（alert fatigue）。团队没有 on-call rotation 的明确 SLA，也没有事后的 postmortem 改进闭环。

**Task（你的角色）：**
作为 Staff Engineer，你不直接管人，但你对技术方向和系统健康负有责任。你需要在没有直接汇报关系的情况下推动变化。

**Action（行动）：**
1. **先用数据说话，不讲感受**
   ```
   拉 PagerDuty 数据 → 3 个月 on-call 事件日志
   分类：P0 真实事故 vs P1/P2 可以白天处理的告警
   结论：73% 的告警是误报或低优先级
   ```
2. **构建"关注它的商业理由"**
   不是"团队很累"（EM 可以无视）→ 而是"以现在的离职率，3 个月后我们没有人能 on-call"
3. **提出具体方案，不只是投诉**
   - 告警分级：重新定义什么是 P0（必须立即响应）
   - 告警降噪：关掉 6 个月内从未升级的告警
   - 轮班 SLA：每人每季度不超过 X 次夜间叫醒
   - Postmortem 闭环：每次 on-call 后必须有 action item

4. **处理 EM 的阻力**
   先单独聊，给 EM 一个"赢"的方式：把这个改善作为他的 Q4 OKR。不是对抗，是合作。

**Result（结果）：**
6 周后，夜间告警减少 60%，工程师满意度提升，季度末没有新的离职。

---

## ❌ Bad vs ✅ Good

**❌ 差的回答：**
"我会和 EM 说团队很累，建议我们减少 on-call 频率。"
→ 没有数据，没有方案，被动等待。

**✅ 好的回答（Staff 级别）：**
"我收集了 3 个月的 PagerDuty 数据，发现 73% 的告警不需要凌晨响应。我建立了一个告警分级框架，并向 EM 展示了如果这个趋势继续下去，6 个月后团队的 bus factor 会降到 2。我们在 6 周内落地了改善，减少了 60% 的夜间告警。"

---

## Senior / Staff 差异点

| Level | 关注点 |
|-------|--------|
| Senior | 解决眼前的事故，做好自己的 on-call |
| Staff | 发现系统性问题，推动组织层面的改进 |
| Principal | 影响跨团队的工程文化，建立标准 |

---

## 关键 Takeaways

1. **数据 > 感受** — "我们很累"被忽视，"离职率+30%" 不能被忽视
2. **带着方案去，不只是问题** — Staff 级别不是投诉者，是提案者
3. **给利益相关者一个"赢"的方式** — 让 EM 的 OKR 受益于你的改善

---

## 📚 References
- [Google SRE Book — On-Call](https://sre.google/sre-book/being-on-call/)
- [PagerDuty On-Call Best Practices](https://www.pagerduty.com/resources/learn/on-call-management/)
- [Increment Magazine — On-Call Culture](https://increment.com/on-call/)

## 🧒 ELI5
想象值夜班的保安每晚被假警报叫醒 4 次。聪明的做法不是"保安要多点休息"，而是：找出哪些警报是假的，把它们关掉。用数字证明问题，给出解法，让老板觉得这是他的好主意。
