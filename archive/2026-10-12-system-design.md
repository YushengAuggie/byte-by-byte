# 系统设计 / System Design — Day 137 (Synthesis)
## 零停机部署全景对比 / Zero-Downtime Deployment Patterns

> 📊 综合 Day 14 微服务、Day 53 功能开关、Day 56 A/B 测试、Day 42 监控

---

🏗️ **系统设计 / System Design**
**专题综合：零停机部署四大模式对决**
**Expert Synthesis: Blue-Green vs Canary vs Shadow vs Feature Flags**

---

### 想象这个场景 / The Scenario

你在一家电商公司，每天有 500 万 DAU。上线新版本结账流程——出了问题就是直接损失收入。你会用哪种部署策略？

You're at an e-commerce company with 5M DAU. Rolling out a new checkout flow — a bug means lost revenue. Which deployment pattern do you pick?

---

### 四大模式速览 / The Four Patterns

```
┌─────────────────────────────────────────────────────────┐
│  BLUE-GREEN                                             │
│  LB ──→ [Blue  v1] 100%   (switch instantly)           │
│      ──→ [Green v2]  0%                                 │
│                    ↓ cutover                            │
│  LB ──→ [Blue  v1]  0%                                 │
│      ──→ [Green v2] 100%                               │
├─────────────────────────────────────────────────────────┤
│  CANARY                                                 │
│  LB ──→ [Stable v1] 95%                                │
│      ──→ [Canary v2]  5% → 20% → 50% → 100%          │
│          (watch SLOs at each step)                      │
├─────────────────────────────────────────────────────────┤
│  SHADOW TRAFFIC                                         │
│  LB ──→ [Production v1] 100%  (real responses)        │
│      ──→ [Shadow    v2] 100%  (responses discarded)   │
│          (validate correctness silently)                │
├─────────────────────────────────────────────────────────┤
│  FEATURE FLAGS                                          │
│  Both v1/v2 code deployed; flag controls which runs    │
│  flag=off → old path; flag=on(10%) → gradual rollout   │
└─────────────────────────────────────────────────────────┘
```

---

### 核心权衡 / Key Tradeoffs

| 模式 | 回滚速度 | 资源开销 | 数据库问题 | 最适场景 |
|------|---------|---------|----------|---------|
| Blue-Green | 瞬间 | 2× 成本 | 最难（两个版本并存） | 大版本发布 |
| Canary | 快（减流量） | ~1.05× | 向前兼容即可 | 风险可控的功能 |
| Shadow | N/A | 2× 成本 | 无（不影响真实用户） | 验证正确性 |
| Feature Flags | 毫秒（toggle） | 最低 | 解耦部署与发布 | 所有场景 |

**实战结论：** 现代团队通常 Canary + Feature Flags 结合使用。Canary 控制基础设施层，Feature Flags 控制功能层。

---

### 别踩这些坑 / Common Mistakes

**坑 1：Blue-Green 忘了数据库迁移**
新版本用了新 schema，旧版本还在运行时读不了新字段 → 切换后立刻回滚。
**解法：** 先向后兼容部署（新字段可 NULL），再切流量，最后清理旧字段。

**坑 2：Canary 没有自动熔断**
5% 流量跑着出现 error_rate 飙升，但没有自动停止推进 → 到 50% 才发现问题。
**解法：** 定义明确的 SLO 阈值（如 p99 latency < 200ms，error rate < 0.1%），超出自动暂停。

**坑 3：Feature Flags 永远不清理**
2 年后代码库里有 200 个 flag，没人知道哪些还活着 → "flag debt"。
**解法：** 每个 flag 创建时设置 TTL / owner，定期审计。

---

### 📚 References
- https://martinfowler.com/bliki/BlueGreenDeployment.html
- https://martinfowler.com/bliki/CanaryRelease.html
- https://launchdarkly.com/blog/what-are-feature-flags/

### 🧒 ELI5
蓝绿=换电池（瞬间切）。金丝雀=先给5%用户试试。影子流量=在背后偷偷测试不影响用户。功能开关=遥控器随时开关。
Blue-Green = swap a battery (instant). Canary = let 5% of users try first. Shadow = secret parallel test users never see. Feature flag = remote control you can toggle any time.
