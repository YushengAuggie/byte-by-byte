# 🏗️ 系统设计 / System Design — Day 22
**主题 / Topic:** Design a Unique ID Generator
**难度 / Difficulty:** Intermediate | **阶段 / Phase:** Growth

---

## 想象你在设计... / Imagine You're Designing...

你在构建一个分布式电商平台，每秒要处理数十万笔订单。每笔订单需要一个**全局唯一、有序的 ID**。问题来了：数据库自增 ID 在单机没问题，但多台服务器同时生成 ID 怎么办？

You're building a distributed e-commerce platform handling hundreds of thousands of orders per second. Each order needs a **globally unique, roughly-ordered ID**. A database auto-increment works fine on one machine — but what happens when 50 servers are generating IDs simultaneously?

---

## 架构图 / Architecture

```
Clients → Load Balancer
              │
    ┌─────────┼─────────┐
    │         │         │
 Server1   Server2   Server3
 (DC1)     (DC1)     (DC2)
    │         │         │
    └─────────┴─────────┘
              │
         ID Generator
       (Snowflake-style)

Snowflake 64-bit ID:
┌──────────────────┬─────────┬─────────┬────────────────┐
│   41 bits        │  5 bits │  5 bits │   12 bits      │
│  timestamp (ms)  │  data-  │ machine │  sequence #    │
│  since epoch     │  center │   ID    │ (per ms reset) │
└──────────────────┴─────────┴─────────┴────────────────┘
(+1 sign bit = 64 bits total; 10 bits worker = 5 DC + 5 machine)

Max: ~4096 IDs/ms per machine
     1024 machines total (32 DC × 32 machines)
     ~69 years of timestamps
```

---

## 三种核心方案 / Three Core Approaches

### 方案一：UUID (v4)
```
优点 / Pros:  无需协调，简单
缺点 / Cons:  128 bits，无序，索引性能差
Use case:     非高频场景，不关心顺序
```

### 方案二：数据库自增 + 多主
```
Server A: 1, 3, 5, 7... (步长2, 起始1)
Server B: 2, 4, 6, 8... (步长2, 起始2)

优点 / Pros:  简单，有序
缺点 / Cons:  扩容麻烦，单点风险
Use case:     小规模分布式
```

### 方案三：Snowflake（Twitter）✅ 推荐
```python
import time

class SnowflakeGenerator:
    EPOCH = 1288834974657  # Twitter epoch (Nov 4 2010)
    
    def __init__(self, datacenter_id, machine_id):
        self.datacenter_id = datacenter_id  # 0-31
        self.machine_id = machine_id        # 0-31
        self.sequence = 0
        self.last_timestamp = -1
    
    def generate(self):
        ts = int(time.time() * 1000)
        
        if ts == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFFF  # 12 bits
            if self.sequence == 0:
                # Sequence overflow — wait for next ms
                while ts <= self.last_timestamp:
                    ts = int(time.time() * 1000)
        else:
            self.sequence = 0
        
        self.last_timestamp = ts
        
        return (
            ((ts - self.EPOCH) << 22) |
            (self.datacenter_id << 17) |
            (self.machine_id << 12)   |
            self.sequence
        )

gen = SnowflakeGenerator(datacenter_id=1, machine_id=5)
id1 = gen.generate()
id2 = gen.generate()
print(id1 < id2)  # True — always monotonically increasing!
```

---

## 关键权衡 / Key Tradeoffs

| 方案 | 有序性 | 分布式友好 | 复杂度 |
|------|--------|-----------|--------|
| UUID | ❌ 无序 | ✅ 完全独立 | 低 |
| DB 自增 | ✅ 有序 | ⚠️ 需协调 | 中 |
| Snowflake | ✅ 时间有序 | ✅ 无协调 | 中 |

**为什么 Snowflake 好？/ Why Snowflake Wins:**
- 无需中心化协调（每台机器独立生成）
- 时间有序 → B-tree 索引友好，写入局部性好
- 高吞吐：每机器 4096 IDs/ms = 400万/秒

**Snowflake 弱点：**
- 依赖系统时钟 — 时钟回拨会产生重复 ID！
- 解决方案：拒绝生成 / 等待 / NTP 同步保护

---

## 别踩这个坑 / Common Mistakes

❌ **坑1: 用 UUID 当主键在 MySQL 中**
UUID 无序 → 每次插入都可能触发 B-tree 页分裂 → 写性能劣化 50%+

✅ **正确：** 用 Snowflake/ULID，保证单调递增

❌ **坑2: 忽略时钟回拨**
NTP 校时可能让时钟往回走 → Snowflake 生成重复 ID

✅ **正确：** 检测 `ts < last_timestamp`，抛出异常或等待

❌ **坑3: 直接暴露 Snowflake ID**
Snowflake ID 包含 datacenter/machine 信息 → 信息泄露

✅ **正确：** 对外用 hash/encode，内部用 Snowflake

---

## 📚 References
- [Twitter Snowflake — Original Blog Post](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake)
- [Instagram's Sharded IDs](https://instagram-engineering.com/sharding-ids-at-instagram-1cf5a71e5a5c)
- [System Design Interview — Unique ID Generator (ByteByteGo)](https://bytebytego.com/courses/system-design-interview/design-a-unique-id-generator-in-distributed-systems)

---

## 🧒 ELI5

想象每个服务器都是一个售票员，卖演唱会门票。
- UUID = 随机生成票号，没有顺序，混乱
- 数据库自增 = 只有一个售票窗口，大家排队，慢
- Snowflake = 每个售票员有自己的"窗口编号+时间戳"，自动组合成唯一票号，又快又有序！

Imagine each server is a ticket seller at a concert.
- UUID = random ticket numbers, no order, chaotic
- DB auto-increment = one ticket window, everyone queues, slow
- Snowflake = each seller combines their booth number + timestamp to make unique ordered tickets — fast AND sorted!
