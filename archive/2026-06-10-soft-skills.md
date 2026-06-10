# Day 62 — 软技能 / Soft Skills

🗣️ **软技能 / Soft Skills** · Day 62 · Expert Phase · Crisis Management

---

## Behavioral Question

> **"Describe a time you led an incident response. What was your role and what did you learn?"**  
> **"描述一次你主导事故响应的经历。你的角色是什么？学到了什么？"**

---

### 为什么面试官问这个 / Why Interviewers Ask This

这道题不是在考你技术能力，而是在考：
1. **你在压力下是否保持清醒** — panic 还是 structured thinking？
2. **你如何协调多人** — 是英雄主义独自解决，还是有效分工？
3. **你的复盘能力** — 解决问题之后有没有真正学到东西？

Senior+ 工程师的标志：他们**让危机变得可管理**，而不仅仅是"修了 bug"。

*Interviewers want to see: calm under pressure, structured coordination, and genuine learning — not just technical heroics.*

---

### STAR 框架分解 / STAR Breakdown

**Situation（背景）:** 什么服务？什么规模的影响？多少用户受到影响？

**Task（任务）:** 你的角色是什么？是 IC、Tech Lead 还是 IC 之一？你是被分配来的还是主动承担的？

**Action（行动）— 这是核心，要细说：**

事故响应的标准结构：
1. **Triage（分类诊断）** — 定性：是部分降级还是全面宕机？影响面有多大？
2. **Communicate（沟通）** — 立刻同步利益相关方，哪怕你还不知道根因
3. **Mitigate first（先缓解）** — rollback、feature flag 关闭、限流——不等根因分析
4. **Root cause（根因）** — 慢慢来，但要彻底
5. **Fix（修复）** — 临时补丁 vs 永久修复的权衡
6. **Postmortem（事后复盘）** — blameless，重点在系统不在人

**Result（结果）:** 多快恢复？影响多少用户？后续改变了什么？

---

### ❌ 弱回答 vs ✅ 强回答

**❌ 弱（Junior 味道）:**
> "我们的服务挂了，我找到了 bug，修了，上线了，恢复了。"

问题：没有协调，没有沟通，没有系统性思考，没有学到什么。

**✅ 强（Senior/Staff 味道）:**
> "我们的支付服务在黑色星期五凌晨 2 点开始报错率飙升。我接到告警后：
> 
> 首先，**5 分钟内建了一个 War Room**，拉来 on-call、QA、SRE，明确分工——一人挖日志，一人跟踪 DB 指标，我协调并对外沟通。
> 
> **10 分钟内**，我们决定先回滚昨天的部署——不确定是不是根因，但这是最快降低风险的路径。回滚后错误率立即下降 80%。
> 
> **45 分钟后**，根因定位：新版本里一个 DB connection pool 的配置在高并发下触发了连接耗尽。
> 
> **事后**，我主导了 blameless postmortem，发现我们缺少 connection pool 耗尽的告警，缺少回滚 runbook。这两个都在 2 周内上线了。
> 
> 最重要的学习：**永远先 mitigate，再 investigate**。"

---

### Senior/Staff 加分点 / Senior/Staff Tips

- **"我建立了清晰的指挥链"** — 事故中最大的混乱来自多人同时操作
- **"我更新了状态页面"** — 主动对外沟通，减少内部噪音
- **"我保护了团队"** — 确保疲惫的队友能交班，而不是 24 小时连轴转
- **"我们改变了系统"** — 不是修了 bug 就完了，是改变了 observability 或流程
- **Blameless postmortem** — 这个词会让面试官眼睛一亮

---

### Key Takeaways / 核心要点

1. 事故中领导力 ≠ 最快找到 bug。领导力 = 让团队有效协作
2. "先缓解，再根因" 是 SRE 文化的核心原则
3. 好的事后复盘比事故本身更能体现工程成熟度
4. 面试时要给出**数字**：多少 QPS 受影响？多少分钟恢复？

---

### 📚 References

- [Google SRE Book — Managing Incidents](https://sre.google/sre-book/managing-incidents/)
- [Atlassian — Incident Management Guide](https://www.atlassian.com/incident-management)
- [Blameless Postmortem Culture — GitHub Engineering](https://github.blog/engineering/engineering-principles/blameless-postmortems/)

---

### 🧒 ELI5

就像学校里火灾演习：有人喊"着火了"，你不要自己冲过去抢着灭火——你要先通知老师（沟通），让大家按序撤离（缓解影响），然后再找是哪个同学在厕所抽烟（根因）。领导力是让每个人都知道该做什么，而不是自己一个人当消防员。

*Like a fire drill: don't be the lone hero with the extinguisher. First alert others (communicate), evacuate (mitigate), then find the cause. Leadership means everyone knows their role, not one person does everything alone.*
