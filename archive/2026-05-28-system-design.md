# 🏗️ 系统设计 / System Design — Day 44
## Design a Feature Flag System (LaunchDarkly)
**难度 / Difficulty:** Advanced | **阶段 / Phase:** Expert | **用时 / Time:** ~3 min

---

## 真实场景 / Real-World Scenario

想象你在 Meta 负责一个每天服务 30 亿用户的 News Feed 系统。你要上线一个全新的推荐算法 — 但你**不敢直接全量发布**：万一出了 Bug，全球用户都受影响。

你需要的是**功能开关 (Feature Flag)**：先放 0.1% 的流量，再 1%，再 10%... 一旦出问题立即关闭，零停机回滚。

Imagine you're at Meta, responsible for a News Feed serving 3 billion daily users. You're shipping a new recommendation algorithm — but you can't just deploy it to everyone at once. If it breaks, the entire world is affected.

You need **Feature Flags**: start at 0.1% traffic, then 1%, then 10%... and kill it instantly if anything goes wrong. Zero-downtime rollback.

---

## 系统架构 / Architecture

```
                    ┌────────────────────────────┐
                    │     Admin Dashboard         │
                    │  (Create/Edit/Target Flags)  │
                    └────────────┬───────────────┘
                                 │ Config Changes
                    ┌────────────▼───────────────┐
                    │      Flag Control Plane     │
                    │  - Flag CRUD API            │
                    │  - Targeting Rules Engine   │
                    │  - Audit Log                │
                    └────────────┬───────────────┘
                                 │ Write
              ┌──────────────────▼──────────────────┐
              │           PostgreSQL                  │
              │  (flags, rules, environments, users)  │
              └──────────────────┬──────────────────┘
                                 │ CDC / PubSub
              ┌──────────────────▼──────────────────┐
              │         Redis (Flag Cache)            │
              │  flag_key → {rules, rollout%}         │
              └────┬─────────────────────────┬───────┘
                   │ SSE/Long Poll              │
         ┌─────────▼────────┐      ┌──────────▼────────┐
         │   SDK (Server)    │      │   SDK (Browser)   │
         │  Node / Python    │      │   React / Next    │
         └─────────┬────────┘      └──────────┬────────┘
                   │                           │
         ┌─────────▼───────────────────────────▼───────┐
         │              Your Application                 │
         │   if (flags.isEnabled("new_algo", userId)):  │
         │       return new_recommendation()            │
         └──────────────────────────────────────────────┘
```

---

## 核心概念 / Key Concepts

### 1. Flag 评估 (Evaluation)
每次 `isEnabled(flagKey, user)` 调用要**极快** — 不能每次都打数据库。
SDK 在本地内存缓存全部 flag 规则，通过 SSE/WebSocket 接收增量更新。

Every `isEnabled(flagKey, user)` call must be **extremely fast** — no DB lookups per call.
The SDK caches all flag rules in-memory and receives incremental updates via SSE/WebSocket.

### 2. 灰度策略 / Targeting Rules (in priority order)
```
Rule 1: userId in ["user_123", "user_456"] → true (内测用户/beta users)
Rule 2: country == "US" AND email ends with "@company.com" → true (内部员工/internal)  
Rule 3: rollout = 10% (hash(userId) % 100 < 10) → true (随机灰度/random rollout)
Rule 4: default → false
```

### 3. 一致性哈希灰度 / Consistent Rollout
用 `hash(userId + flagKey) % 100` 而非 `random()` — 保证同一用户每次看到**相同结果**。

Use `hash(userId + flagKey) % 100` not `random()` — ensures the same user always gets the same result.

```python
import hashlib

def should_enable(user_id: str, flag_key: str, rollout_pct: int) -> bool:
    # Deterministic: same user always gets same result
    seed = f"{user_id}:{flag_key}"
    hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return (hash_val % 100) < rollout_pct
```

---

## 为什么这样设计？/ Key Tradeoffs

| 决策 / Decision | 原因 / Why |
|---|---|
| SDK 本地缓存 rules | P99 评估 <1ms；无单点故障 |
| SSE 推送更新 | 实时性 <100ms；比轮询更高效 |
| hash(userId+flagKey) | 跨服务一致性；可复现 |
| 按环境隔离 | prod/staging/dev 互不干扰 |
| 审计日志 | 合规；回溯事故 "谁在什么时候改了什么" |

---

## 别踩这个坑 / Common Mistakes

**❌ 坑 1: Flag 永不清理**
Feature flags 是技术债。很多公司有数千个"废弃"flag 还在代码里。
建立 TTL 机制：flag 超过 90 天自动提醒清理。

Feature flags are tech debt. Many companies have thousands of "dead" flags still in code.
Build TTL: auto-alert to clean up flags older than 90 days.

**❌ 坑 2: 把 flag 用作配置系统**
Feature flags ≠ 配置管理。不要把数据库连接字符串、超时时间放进 flag。
用专门的配置系统 (AWS AppConfig, Consul)。

Feature flags ≠ config management. Don't put DB connection strings or timeouts in flags.
Use dedicated config systems (AWS AppConfig, Consul).

**❌ 坑 3: Flag 评估打数据库**
每次请求都去 DB 查询 flag = 系统瘫痪。必须本地缓存 + 增量推送。

Evaluating flags against DB on every request = system meltdown. Must use local cache + push updates.

---

## 扩展问题 / Follow-up Questions

- 如何支持 A/B/C 多变量测试？(multivariate flags)
- 如何实现 flag 依赖关系？(flag A 必须先开启 flag B 才能生效)
- 怎么做 flag 评估的可观测性？(哪些用户看到了哪个变体？)

---

## 📚 References
- [LaunchDarkly Architecture Blog](https://launchdarkly.com/blog/how-launchdarkly-serves-over-300-billion-feature-flags/)
- [Feature Toggles — Martin Fowler](https://martinfowler.com/articles/feature-toggles.html)
- [OpenFeature — open standard for feature flags](https://openfeature.dev/)

## 🧒 ELI5
Feature flags 就像给代码装了"电灯开关"。你把新功能写好但先关着，然后可以只给自己、或者1%的用户开灯试试，不满意就关掉——完全不用重新部署。

Feature flags are like installing light switches in your code. You write the new feature but keep it "off", then flip it on for just yourself, or 1% of users. If something's wrong, flip it off instantly — no redeployment needed.
