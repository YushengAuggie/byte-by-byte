# 🏗️ 系统设计 / System Design — Day 97 (Synthesis)
**Expert Phase · Synthesis Mode**

## 缓存、队列与一致性：三角权衡深度拆解

想象你是 Meta/字节跳动的高级架构师，需要同时应对：
- 10亿 DAU 的 Feed 系统
- 秒杀/热点事件瞬间百倍流量
- 跨数据中心的最终一致性

这不是单一设计题，而是真实系统中**最难的三角权衡**。

---

## 三角关系：缓存 × 消息队列 × 一致性

```
           ┌─────────────────────┐
           │    Client (CDN)     │
           └──────────┬──────────┘
                      │
           ┌──────────▼──────────┐
           │   API Gateway /     │
           │   Load Balancer     │
           └──┬──────────────┬───┘
              │              │
   ┌──────────▼──┐      ┌───▼──────────┐
   │  Cache Layer │      │  Queue Layer  │
   │  (Redis L1)  │      │  (Kafka)      │
   └──────┬───────┘      └──────┬────────┘
          │                     │
   ┌──────▼──────────────────────▼───────┐
   │         DB Cluster (Primary/Replica) │
   │         + CDC (Change Data Capture)  │
   └─────────────────────────────────────┘
```

---

## 为什么这样设计？核心权衡

### 1. 缓存策略选择

| 策略 | 优势 | 风险 | 适用场景 |
|------|------|------|----------|
| Cache-Aside | 精确控制、缓存未命中可容忍 | 缓存击穿、代码侵入 | 读多写少（用户 profile） |
| Write-Through | 写入即更新，强一致 | 写放大、延迟增加 | 金融交易记录 |
| Write-Behind | 高吞吐写入、DB 压力小 | 数据可能丢失 | 计数器、日志 |
| Read-Through | 代码简洁 | 冷启动慢 | ORM 场景 |

**真实教训**：Twitter 的热点用户（Obama, Elon）导致缓存被无效化后雪崩。解法：**特殊缓存层 + 读穿策略**，不走普通 invalidation。

### 2. 消息队列：解耦还是增加复杂度？

**用队列（Kafka/SQS）当：**
- 下游系统处理速度不匹配（削峰填谷）
- 需要 event sourcing / audit trail
- 多个消费者需要同一事件

**不用队列当：**
- 需要同步确认（支付成功页面）
- 延迟要求 < 10ms（游戏同步）
- 团队没有运维能力

### 3. 一致性模型选择

```
Strong → Sequential → Causal → Eventual
  ↑                               ↑
高延迟、高成本              低延迟、可扩展
Spanner/TiDB             DynamoDB/Cassandra
```

**真实 Meta 架构**：`TAO（The Associations and Objects）` 系统用 **Causal Consistency**，不是 Strong。为什么？因为你看到帖子比朋友晚 100ms 完全可以接受，但写 4ms 的强一致代价太高。

---

## 综合设计：Feed 系统 + 热点事件

```python
# 热点检测 + 动态缓存调整
class HotKeyDetector:
    def __init__(self, redis_client, threshold=1000):
        self.redis = redis_client
        self.threshold = threshold  # requests/sec

    def track_and_decide(self, key: str) -> str:
        count = self.redis.incr(f"hotkey:{key}")
        self.redis.expire(f"hotkey:{key}", 60)

        if count > self.threshold:
            # Hot key: replicate to local cache
            return "LOCAL_CACHE"
        return "REDIS_CACHE"

# Fan-out 策略动态切换
def get_fanout_strategy(user_follower_count: int) -> str:
    if user_follower_count < 1000:
        return "PUSH"    # 写扩散: 发布时推送到所有粉丝 timeline
    elif user_follower_count < 1_000_000:
        return "HYBRID"  # 混合：小 V push，大 V pull
    else:
        return "PULL"    # 读扩散: 读取时实时聚合（大 V 专用）
```

---

## 别踩这个坑

❌ **缓存穿透**：查询不存在的 key，每次都打 DB。
✅ 解法：布隆过滤器（Bloom Filter）预检 + 缓存空值

❌ **缓存雪崩**：大量 key 同时过期，DB 被打垮。
✅ 解法：TTL 加随机抖动（`ttl = base_ttl + random(0, 300)`）

❌ **分布式锁滥用**：每个操作都加锁，吞吐量下降 10x。
✅ 解法：只在 critical section 加锁；用 CAS（Compare-And-Swap）替代锁

---

## 📚 References
- [Twitter's architecture at scale](https://blog.x.com/engineering/en_us/topics/infrastructure/2023/twitter-recommendation-algorithm)
- [Facebook TAO paper](https://www.usenix.org/system/files/conference/atc13/atc13-bronson.pdf)
- [AWS well-architected caching](https://docs.aws.amazon.com/wellarchitected/latest/framework/reliability.html)

## 🧒 ELI5
就像超市：热门商品（缓存）放收银台旁边，不热门的才去仓库拿（数据库）。但如果所有商品同时清空，收银台就崩了——所以要分批补货，而且先检查仓库有没有货（布隆过滤器）再去找。
