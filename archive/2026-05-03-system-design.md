# 🏗️ 系统设计 / System Design — Design Uber / Lyft (Ride Sharing)

> **Day 33 · Mastery Phase · ~3 min read**

---

## 想象你在设计 Uber

你是 Uber 的架构师。每天有 **2000 万次** 打车请求。你需要：
- 实时匹配乘客和司机（延迟 < 5 秒）
- 追踪数百万司机的实时位置
- 计算动态路线和价格（surge pricing）
- 保证司机和乘客的消息可靠传递

Imagine you're Uber's architect. 20M rides/day. You need real-time driver matching, live location tracking, route calculation, and reliable messaging — all at global scale.

---

## ASCII Architecture Diagram

```
[Rider App]          [Driver App]
     |                    |
     v                    v
[API Gateway / Load Balancer]
     |
     +--------+----------+----------+
     |        |          |          |
[Location   [Trip      [Dispatch  [Surge
 Service]   Service]   Engine]    Pricing]
     |        |          |          |
     v        v          v          v
[Redis      [Postgres  [Kafka     [ML
 Geo-index]  RDS]      Event Bus] Service]
                            |
                       [Notification
                         Service]
                       (WebSocket/
                        Push/SMS)
```

---

## 核心组件 / Core Components

### 1. Location Service — 实时位置更新
- 司机 App 每 **4 秒** 发送 GPS 坐标
- 存储在 **Redis + Geo Index**（`GEOADD`, `GEORADIUS`）
- 支持 `GEORADIUS(lat, lng, radius=2km)` 快速找附近司机

### 2. Dispatch Engine — 匹配算法
```
1. 乘客请求 → Location Service 找 nearby drivers (2km)
2. 按评分、ETA、方向 排序候选司机
3. 依次发 offer（司机有 15s 接单窗口）
4. 超时 → 扩大范围到 5km 重试
```

### 3. Trip Service — 行程状态机
```
REQUESTED → ACCEPTED → DRIVER_ARRIVING 
         → RIDE_IN_PROGRESS → COMPLETED / CANCELLED
```
用 **Postgres** 持久化，用 **Kafka** 发布状态变更事件。

### 4. Surge Pricing — 动态定价
- 每 1 分钟统计：需求量 / 供给量 = 倍率
- 倍率 > 1.5x → 触发 surge notification
- 用 ML 模型预测未来 10 分钟需求（防止价格震荡）

---

## 为什么这样设计？ / Key Tradeoffs

| 选择 | 原因 |
|------|------|
| Redis Geo vs PostGIS | Redis 延迟更低（<1ms），适合高频位置更新 |
| WebSocket vs HTTP polling | 双向实时通信，推送位置更新更高效 |
| Kafka for events | 解耦各服务，支持重放 + 审计日志 |
| Separate Dispatch Engine | 匹配逻辑复杂，隔离后可独立扩容/替换算法 |

---

## 别踩这个坑 / Common Mistakes

❌ **用数据库存储实时位置** — SQL 无法承受每秒数百万次写入
✅ **用 Redis Geo** + 定期异步持久化到 DB

❌ **单体匹配服务** — 高峰期成为瓶颈
✅ **Dispatch Engine 水平扩展** + 按城市分片

❌ **乘客 pull 模式查询司机位置** — 轮询浪费带宽
✅ **WebSocket push** — 只推变化的位置

❌ **忽略 GPS 漂移** — 司机在隧道/地下停车场时位置失真
✅ **位置置信度评分** + 地图匹配（map-matching）算法

---

## 数据规模估算 / Capacity Estimation

- 司机: 5M active drivers globally
- 位置更新: 5M × (1 update/4s) = **1.25M writes/sec** to Redis
- 行程数据: 20M rides/day × 1KB = ~20GB/day → Postgres + S3 archive

---

## 📚 References

- [Uber Engineering — How we built a real-time geospatial platform](https://www.uber.com/blog/engineering/)
- [Uber H3 Geospatial Indexing](https://eng.uber.com/h3/)
- [System Design Interview — Uber (ByteByteGo)](https://bytebytego.com/courses/system-design-interview/design-uber)

---

## 🧒 ELI5

把 Uber 想象成一个巨大的 "出租车调度中心"。Redis 就是调度员的白板，实时标注每辆出租车的位置。Kafka 就是电话录音系统，记录每个电话（事件）。Dispatch Engine 就是调度员本人——他拿起白板，找最近的空车，然后打电话问"你愿意接这个单吗？"

Think of Uber as a giant taxi dispatch center. Redis is the dispatcher's whiteboard showing all taxi locations. Kafka is the call recording system. The Dispatch Engine is the dispatcher — grabbing the nearest free driver and asking "want this ride?"
