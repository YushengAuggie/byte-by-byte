# 🏗️ 系统设计 / System Design — Day 129 (Synthesis)

**流处理 vs 批处理 vs Lambda架构 — 三大数据处理范式的终极对比**
**Stream vs Batch vs Lambda Architecture — The Ultimate Comparison**

---

## 🌍 背景 / Background

想象你在构建一个数据平台，需要同时支持：
- 实时欺诈检测（毫秒级响应）
- 每日销售报表（TB级数据）
- 用户行为分析仪表盘（秒级延迟）

*You're building a data platform that needs: real-time fraud detection (ms latency), daily sales reports (TB-scale), and user behavior dashboards (second-level latency). These three requirements map to three data processing philosophies.*

---

## 三大范式 / Three Paradigms

### 1. 批处理 / Batch Processing (MapReduce, Spark)

```
[Data Lake/S3] → [Spark Job @ 2am] → [DWH/Redshift] → [BI Dashboard]
```

- **优势**: 吞吐量极高，容错简单，适合历史数据
- **劣势**: 高延迟（小时级），不适合实时决策
- **When to use**: 报表、模型训练、数据仓库ETL

### 2. 流处理 / Stream Processing (Kafka + Flink/Spark Streaming)

```
[Events] → [Kafka] → [Flink] → [Real-time Aggregation] → [Redis/Cassandra]
```

- **优势**: 低延迟（毫秒~秒级），即时洞察
- **劣势**: 状态管理复杂，exactly-once语义难实现
- **When to use**: 欺诈检测、实时推荐、IoT监控

### 3. Lambda架构 / Lambda Architecture

```
                    ┌─────────────────────────┐
[Events] ───────────┤ Speed Layer (Flink)     ├──► Serving Layer
    │               │ [low latency, recent]   │        │
    │               └─────────────────────────┘        │
    └─ [Kafka/S3] ──► Batch Layer (Spark)    ──────────┘
                      [high throughput, all data]
```

Lambda = Batch Layer（准确、完整）+ Speed Layer（快速、近似）+ Serving Layer（合并查询）

**优势**: 兼顾准确性和实时性
**劣势**: 同一逻辑需要写两次（批处理 + 流处理），维护成本高

---

## Kappa架构 — Lambda的进化 / Kappa Architecture

**核心思想**: 只保留流处理层，批处理通过"重放历史数据"来实现。

```
[Kafka (infinite retention)] → [Flink] → [Serving Layer]
                                  ↑
                           Reprocess from
                           beginning when needed
```

- 代码只写一次，更易维护
- 适合 Kafka 能保存足够长历史数据的场景
- Netflix、LinkedIn 大量采用

---

## 🔑 关键权衡对比 / Key Tradeoffs

| 维度 | 批处理 | 流处理 | Lambda | Kappa |
|------|--------|--------|--------|-------|
| 延迟 | 小时级 | 毫秒~秒级 | 混合 | 秒级 |
| 吞吐量 | 极高 | 中高 | 高 | 中高 |
| 复杂度 | 低 | 中 | 最高 | 中 |
| 历史数据 | ✅ 天然支持 | ⚠️ 需回放 | ✅ 支持 | ✅ 需长retention |
| 代码维护 | 单套 | 单套 | 双套 | 单套 |

---

## 别踩的坑 / Common Mistakes

1. **过度设计**: 大多数公司不需要Lambda架构，批处理+简单流处理就够了
2. **忽视exactly-once**: 流处理的重复消费问题会导致数据不准确（双重扣款、重复计数）
3. **状态无限增长**: Flink/Spark Streaming的状态需要设置TTL，否则OOM
4. **Kafka retention不够**: 要支持重放，Kafka需要保留足够长的数据（有时需要数周）

**与已覆盖话题的连接**:
- Day 13: 消息队列是流处理的基础设施（Kafka）
- Day 51: 分布式文件系统（HDFS/GFS）是批处理的存储层
- Day 39: 分布式缓存（Redis）是流处理结果的 Serving Layer

---

## 📚 延伸阅读 / References
- [The Log: What every software engineer should know](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying) — Jay Kreps (LinkedIn)
- [Questioning the Lambda Architecture](https://www.oreilly.com/radar/questioning-the-lambda-architecture/) — O'Reilly
- [Apache Flink Architecture](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/flink-architecture/)

---

## 🧒 ELI5
批处理就像每天晚上清点收银机——准确但慢。流处理就像实时看 POS 机——快但复杂。Lambda 架构两个都有——准确又快，但要维护两套代码，很累。Kappa 说：我只用流处理，历史数据重放就行了。

*Batch is like counting cash nightly—accurate but slow. Streaming is like watching live POS transactions—fast but complex. Lambda has both. Kappa says: just streaming, replay history when needed.*
