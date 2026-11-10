# 混沌工程与韧性架构 — 系统容错能力的构建框架

> Day 152 | System Design Synthesis | 2026-11-10

---

🏗️ **系统设计 / System Design** *(3 min)*

**混沌工程：主动破坏以验证系统韧性**
**Chaos Engineering: Breaking Things Deliberately to Build Resilient Systems**

---

### 想象你在设计...

你是 Netflix 的 Sr. Engineer。你的分布式系统覆盖 3 个 AWS Region，每天处理数十亿请求。问题不是"会不会出故障"，而是"出故障时能不能自愈"。

*You're a Sr. Engineer at Netflix. Your distributed system spans 3 AWS regions, handling billions of requests daily. The question isn't "will it fail" but "will it recover on its own."*

---

### 混沌工程流程 / Chaos Engineering Pipeline

```
     ┌─────────────────────────────────────────┐
     │         Chaos Engineering Loop          │
     └─────────────────────────────────────────┘
              │
     ┌────────▼────────┐
     │  Define Steady  │  ← e.g., p99 latency < 100ms,
     │  State Baseline │    error rate < 0.1%
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │ Hypothesize     │  ← "Even if Pod X dies,
     │ Resilience      │    steady state holds"
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │ Inject Failure  │  ← Chaos Monkey (Pod kill)
     │ (small blast    │    Chaos Kong (AZ outage)
     │  radius first)  │    Chaos Gorilla (Region)
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │ Observe &       │  ← Datadog metrics (Day 42)
     │ Measure Impact  │    Jaeger traces (Day 68)
     └────────┬────────┘
              │
     ┌────────▼────────┐
     │ Fix Gaps /      │  ← Circuit breaker (Day 81),
     │ Update Runbooks │    retry with backoff (Day 79)
     └─────────────────┘
```

---

### 为什么这样设计 / Key Tradeoffs

| 原则 | 说明 |
|------|------|
| **Blast Radius** | 从单个 Pod 开始，逐步扩大到 AZ → Region。从不在 Production 全量注入。 |
| **Steady State First** | 没有基线指标，就没有验证。先跑 A/B testing (Day 56) 建基线。 |
| **Automate in CI/CD** | 把混沌实验嵌入 Pipeline，让韧性测试像单元测试一样常态化。 |

---

### 别踩这个坑 / Common Mistakes

❌ **直接在 Production 全量注入** — 先在 Staging 验证，再逐步升级  
❌ **没有自动回滚** — 混沌实验必须有 kill switch  
❌ **只测单节点** — 级联故障（Cascading Failure）才是真正的敌人  
❌ **孤立实验** — 混沌工程要结合 On-call Runbook，否则只是制造事故

---

### 知识连接 / Synthesis Map

本主题综合了我们之前覆盖的多个系统：
- **监控告警** (Day 42) — 需要 Datadog/Prometheus 观测稳态
- **分布式追踪** (Day 68) — Jaeger traces 帮助定位级联故障根因
- **熔断器** (Day 81) — Circuit Breaker 是混沌实验中最常发现缺失的模式
- **A/B 测试平台** (Day 56) — 稳态基线定义需要实验框架支撑

---

### 🧒 ELI5

混沌工程就像消防演练——你不能等真正着火才知道逃生路线在哪。主动"点火"，找出哪些地方没有灭火器。

*Chaos engineering is like fire drills — you don't wait for a real fire to find out your exits are blocked. Set small fires intentionally to find the gaps.*

---

### 📚 References

- https://principlesofchaos.org — The official Chaos Engineering principles
- https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116 — Netflix Simian Army original post
- https://github.com/Netflix/chaosmonkey — Open source Chaos Monkey
