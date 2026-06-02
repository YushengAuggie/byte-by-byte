# 系统设计：设计 A/B 测试平台 / Design an A/B Testing Platform

> 📅 Day 56 · 🎯 Expert Phase · ⏱️ 3 min read

---

## 🏗️ 系统设计 / System Design

### 想象你在设计...

你是某大型电商的平台工程师。产品经理想同时测试 **10 个不同的按钮颜色**，数据科学家想测试 **新推荐算法**，增长团队想测试 **注册流程**。所有实验都需要统计显著性、样本隔离、实时监控。你怎么设计这个系统？

*You're a platform engineer at a large e-commerce company. Product managers want to test 10 different button colors simultaneously, data scientists want to test a new recommendation algorithm, and the growth team wants to test the registration flow. All experiments need statistical significance, sample isolation, and real-time monitoring. How do you design this system?*

---

### 核心需求 / Core Requirements

**功能需求 / Functional:**
- 创建/管理实验 (experiment CRUD)
- 用户分桶 (user bucketing / traffic splitting)
- 事件追踪 (event tracking & metrics collection)
- 结果分析 + 统计显著性 (statistical significance)
- 实验互斥 / 互相影响检测

**非功能需求 / Non-functional:**
- 低延迟分桶: < 5ms p99
- 高吞吐: 1M events/sec
- 实验隔离: 修改一个不影响另一个
- 数据一致性: 同一用户永远进同一个桶

---

### ASCII 架构图

```
┌──────────────────────────────────────────────────────────┐
│                     Client (Web/App)                      │
└────────────────────────┬─────────────────────────────────┘
                         │  1. GET /assign?userId=xxx&expKey=btn_color
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Assignment Service (stateless)              │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Hash(userId + salt) % 100 → bucket → variant   │    │
│  │  Cache: Redis (experiment config TTL=60s)        │    │
│  └─────────────────────────────────────────────────┘    │
└──────────┬──────────────────────────┬───────────────────┘
           │                          │
    2. Read config               3. Return variant
           │
    ┌──────▼──────┐
    │  Config DB  │  (Postgres — experiments, variants, allocation %)
    │  + Redis    │  (hot path: cached config)
    └─────────────┘

                         │  4. User sees variant → clicks
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Event Collection Service                    │
│         Kafka → Flink/Spark → Data Warehouse            │
│         (ClickHouse / BigQuery for OLAP queries)        │
└──────────────────────────┬──────────────────────────────┘
                           │
                    ┌──────▼───────┐
                    │ Stats Engine │  (T-test, Chi-squared,
                    │              │   Bayesian inference)
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Dashboard   │  (Real-time p-values,
                    │  (Grafana)   │   sample sizes, CI)
                    └──────────────┘
```

---

### 关键设计决策 / Key Design Decisions

#### 1. 分桶策略 (Bucketing Strategy)

```python
def assign_variant(user_id: str, experiment_key: str, variants: list) -> str:
    # Deterministic: same user always gets same variant
    # Salt per-experiment prevents correlation between experiments
    salt = f"{experiment_key}:{user_id}"
    bucket = int(hashlib.md5(salt.encode()).hexdigest(), 16) % 100
    
    # variants = [{"name": "control", "weight": 50}, {"name": "treatment", "weight": 50}]
    cumulative = 0
    for variant in variants:
        cumulative += variant["weight"]
        if bucket < cumulative:
            return variant["name"]
    return variants[-1]["name"]  # fallback
```

**为什么用 MD5 hash？** 
- 均匀分布 (uniform distribution)
- 确定性：同一 userId 永远同一结果
- 快速：< 1μs

#### 2. 实验互斥 (Mutual Exclusion)

```
Experiment Layer Architecture:
┌──────────────────────────────────────────┐
│  Layer 1: UI Experiments (20% traffic)   │
│    ├── Exp A: Button Color (50/50)        │
│    └── Exp B: Font Size (33/33/33)       │
├──────────────────────────────────────────┤
│  Layer 2: Algo Experiments (100% traffic)│
│    └── Exp C: Ranking Algorithm (50/50)  │
├──────────────────────────────────────────┤
│  Layer 3: Onboarding (New Users Only)    │
│    └── Exp D: Signup Flow (50/50)        │
└──────────────────────────────────────────┘
```

同一 Layer 内互斥；不同 Layer 可正交叠加。*(Mutual exclusion within a layer; different layers are orthogonal — user can be in Exp A and Exp C simultaneously without interference.)*

#### 3. 指标收集 (Metrics Collection)

**Guardrail Metrics (护栏指标):** 不能降低的指标 (latency, error rate, revenue)
**Primary Metric:** 实验的核心目标 (CTR, conversion rate)
**Secondary Metrics:** 了解副作用

---

### 为什么这样设计？/ Key Tradeoffs

| 方案 | 优点 | 缺点 |
|------|------|------|
| Client-side assignment | 无网络延迟 | 配置泄露，A/B 不一致 |
| Server-side (our approach) | 安全，可审计 | 需要 API call |
| Edge assignment (CDN) | 极低延迟 | 复杂，有限逻辑 |

**统计方法:** Frequentist (T-test) vs Bayesian — Bayesian 允许提前停止实验，但需要先验知识。大多数平台两者都提供。

---

### 别踩这个坑 / Common Mistakes

🚫 **网络效应 (Network Effects):** 社交产品中，用户 A 的行为会影响用户 B，违反实验独立性假设 → 解决：按 cluster/group 分桶而非个人

🚫 **过早停止实验 (Peeking Problem):** 每天看 p-value，看到 p < 0.05 就停 → 造成 false positive → 解决：预先计算样本量，用 Sequential Testing 或 Bonferroni correction

🚫 **新奇效应 (Novelty Effect):** 用户对新设计有短暂兴趣，长期效果未必好 → 解决：运行足够长时间（至少 1-2 周）

🚫 **SRM (Sample Ratio Mismatch):** 分配比例与实际进入比例不符，说明实验实现有 bug → 每次实验开始时做 SRM check

---

### 📚 References

- [Trustworthy Online Controlled Experiments (Kohavi et al.)](https://experimentguide.com/)
- [Airbnb Experimentation Platform](https://medium.com/airbnb-engineering/experimentation-measurement-at-airbnb-8ee2f5c89bde)
- [Netflix Experimentation Platform](https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15b)

### 🧒 ELI5

想象你开了一家冰淇淋店，想知道巧克力口味还是草莓口味更受欢迎。你让单号桌的客人选巧克力，双号桌的客人选草莓，然后数哪边的客人吃得更开心。这就是 A/B 测试！关键是要保证每张桌子的客人是随机分配的。

*Imagine you run an ice cream shop and want to know if chocolate or strawberry is more popular. You give odd-numbered tables chocolate, even-numbered tables strawberry, then count who's happier. That's A/B testing! The key is making sure customers are randomly assigned to tables.*
