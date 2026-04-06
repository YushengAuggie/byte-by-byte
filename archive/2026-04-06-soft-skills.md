🗣️ **软技能 Day 16 / Soft Skills Day 16**

### ❓ 面试问题 / The Question
"Tell me about a time your team had a production outage. What was your role?"
（告诉我一次你们团队遇到生产环境故障的经历。你的角色是什么？）

### 💡 为什么问这个？ / Why this matters
面试官想看你的**危机处理能力（Crisis Management）**、**责任心（Ownership）**以及**事后复盘（Post-mortem/Blameless Culture）**的态度。高级/Staff 工程师不仅要能修 Bug，还要能稳住阵脚、协调沟通，并确保问题不再发生。
*The interviewer wants to see your crisis management skills, ownership, and attitude towards post-mortems (blameless culture). Senior/Staff engineers don't just fix bugs; they stabilize the situation, coordinate communication, and ensure the issue doesn't recur.*

### 📝 STAR 拆解 / STAR Breakdown
- **Situation (情境)**: 描述故障的严重程度（例如：支付网关宕机，影响了 20% 的用户）。
- **Task (任务)**: 你需要做什么（快速止血、定位根本原因、通知利益相关者）。
- **Action (行动)**: **你的具体贡献**。你是否主导了回滚（Rollback）？你是否在 Slack 上组织了沟通？你是否查看了 Datadog/Splunk 日志？
- **Result (结果)**: 故障恢复时间（MTTR）。更重要的是，**事后复盘（Post-mortem）**得出了什么 Action Items（例如：增加监控告警、改进 CI/CD 流程）。

### ❌ 错误示范 vs ✅ 正确示范
- ❌ **Bad**: "服务器挂了，我查了半天日志发现是别人的代码有问题，然后我让他改了。" (Blaming others, no systemic improvement / 甩锅，没有系统性改进)
- ✅ **Good**: "我们在发布新版本后 CPU 飙升导致服务不可用。我立刻提议先**回滚（Rollback）**止血。恢复后，我主导了排查，发现是一个低效的正则引起的。事后我组织了无指责复盘（Blameless Post-mortem），并推动在 CI 中加入了性能回归测试。" (Focus on mitigation first, blameless culture, systemic fix / 强调先止血、无指责文化、系统性修复)

### 🌟 Senior/Staff 进阶技巧 / Senior/Staff Tips
高级工程师在故障中通常扮演 "Incident Commander"（故障指挥官）的角色。强调你如何**隔离沟通噪音**（让排查的人专心排查，你负责向管理层汇报进度），以及你如何推动架构层面的容灾设计（Resiliency）。

### 🔑 核心收获 / Key Takeaways
1. **Mitigation over Investigation (先止血，后排查)**: 回滚永远是第一选择。
2. **Blameless Culture (对事不对人)**: 故障是系统性问题，不是个人的错。
3. **Actionable Post-mortems (可执行的复盘)**: 故障的价值在于改进系统。

### 📚 延伸阅读 / References
- [Google SRE Book: Incident Response](https://sre.google/sre-book/managing-incidents/)
- [Atlassian: Incident Management](https://www.atlassian.com/incident-management)
- [PagerDuty: Incident Response Guide](https://response.pagerduty.com/)

### 🧒 ELI5 (Explain Like I'm 5)
就像厨房突然起火了。初级厨师可能会慌张地找是谁弄倒了油瓶；高级主厨会立刻拿灭火器把火扑灭（止血），然后安抚外面的客人（沟通），最后大家坐下来讨论怎么把灶台改得更安全（复盘），而不是开除那个弄倒油瓶的人。