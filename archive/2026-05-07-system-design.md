# 🏗️ 系统设计 / System Design — Day 37
**主题 / Topic:** Design a Ticket Booking System (Ticketmaster)
**难度 / Difficulty:** Advanced | **阶段 / Phase:** Mastery

---

## 想象你在设计... / Imagine You're Designing...

你在设计一个像 Ticketmaster 的票务平台。Taylor Swift 巡演票刚开放预售，**10 万人同时抢票**，每张票库存只有一张。系统必须保证：不能超卖、不能同一张票卖给两个人、同时支撑几十万并发请求。

You're building a ticket booking platform like Ticketmaster. Taylor Swift presale just dropped — **100K users rushing simultaneously**, and each seat has exactly one ticket. The system must guarantee: no overselling, no double-booking, while handling massive concurrent load.

---

## 架构图 / Architecture Diagram

```
                        ┌─────────────┐
                        │  CDN / WAF  │  (static assets, DDoS protection)
                        └──────┬──────┘
                               │
                     ┌─────────▼──────────┐
                     │    API Gateway      │
                     │  (rate limiting,    │
                     │   auth, routing)    │
                     └────┬──────────┬────┘
                          │          │
              ┌───────────▼──┐  ┌────▼──────────────┐
              │ Queue Service │  │  Booking Service  │
              │  (virtual     │  │  (stateless,      │
              │   waiting     │  │   horizontally    │
              │   room)       │  │   scaled)         │
              └───────────────┘  └────┬──────────────┘
                                      │
              ┌───────────────────────▼────────────────────┐
              │              Redis Cluster                  │
              │  (seat locks: SETNX, TTL=10min,            │
              │   available seat inventory)                 │
              └───────────────────────┬────────────────────┘
                                      │
              ┌───────────────────────▼────────────────────┐
              │           PostgreSQL (Primary)              │
              │  tickets table: seat_id, status, user_id   │
              │  orders table: order_id, payment_status     │
              │  SELECT FOR UPDATE → serialized writes      │
              └────────────────────────────────────────────┘
                          │
              ┌───────────▼──────────┐
              │   Payment Service    │
              │  (Stripe/PayPal,     │
              │   async webhook)     │
              └──────────────────────┘
```

---

## 核心设计决策 / Key Design Decisions

### 1. 座位锁定 (Seat Locking) — 乐观锁 vs 悲观锁

**两阶段流程 / Two-phase flow:**
```
Phase 1: Soft Lock (用户选座时)
  Redis SETNX seat:{id}:lock {user_id} EX 600
  → 成功：进入支付流程
  → 失败：座位已被锁，提示用户选其他位置

Phase 2: Hard Commit (支付成功后)
  BEGIN TRANSACTION
    SELECT * FROM tickets WHERE seat_id = ? AND status = 'available' FOR UPDATE
    UPDATE tickets SET status = 'sold', user_id = ? WHERE seat_id = ?
    INSERT INTO orders (...)
  COMMIT
  → 同时 DEL Redis lock
```

**为什么用两阶段？** 纯 DB 锁撑不住 10 万并发；纯 Redis 锁在支付成功后还需要 DB 原子提交。两阶段各司其职。

### 2. 虚拟等候室 (Virtual Waiting Room)

高热度演唱会开售前，用户先进等候室队列（SQS/Kafka），按 FIFO 逐批放入系统，避免瞬间流量将数据库打垮。这是 Ticketmaster、12306 都在用的方案。

### 3. 防超卖 (Oversell Prevention)

```sql
-- DB level constraint
ALTER TABLE tickets ADD CONSTRAINT unique_seat UNIQUE (event_id, seat_id);
-- + Redis atomic decrement for inventory
WATCH inventory:{event_id}
MULTI
  DECR inventory:{event_id}  -- atomic, fails if 0
EXEC
```

---

## 为什么这样设计？/ Why This Design?

| 方案 | 优点 | 缺点 |
|------|------|------|
| 纯 DB 行锁 | 强一致性 | 10万并发把 DB 打死 |
| 纯 Redis | 高性能 | 宕机丢数据，支付后仍需 DB |
| **Redis + DB 两阶段** | 性能 + 一致性 | 复杂度高，需处理锁过期 |

---

## ❌ 别踩这个坑 / Common Mistakes

1. **忘记锁过期处理** — 用户选了座位但放弃支付，10分钟后 Redis TTL 到期，座位自动释放。必须用 expiry + cleanup job 双保险。
2. **在 Redis 里扣库存但不做 DB 回写** — Redis 挂了库存就没了，一定要 DB 是最终 source of truth。
3. **不做幂等** — 支付回调可能重复触发，order_id 要做唯一性校验，防止重复出票。
4. **没有 Circuit Breaker** — 支付服务超时时要快速失败，释放座位锁，别让用户无限等待。

---

## 📐 规模估算 / Scale Estimation

```
Peak: 100K concurrent users
Seat lock ops: ~100K/s (Redis handles this easily)
DB writes (final purchase): ~1K-5K/s (much lower, filtered by Redis)
Read throughput: CDN + Redis cache handles 95% of seat map reads
Storage: 1M events × 50K seats = 50B rows (partitioned by event_id)
```

---

## 📚 References
- [System Design Interview — Ticket Master](https://bytebytego.com/courses/system-design-interview/design-a-ticketing-system) — ByteByteGo
- [Redis SETNX docs](https://redis.io/commands/setnx/)
- [PostgreSQL SELECT FOR UPDATE](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE)

## 🧒 ELI5
就像抢限量球鞋：你先抢到一张"号码牌"（Redis 锁），然后拿着号码牌去收银台付钱（DB 写入），付完才算真的买到。号码牌有过期时间，10 分钟不来就还给别人。

Like getting a numbered ticket at the deli counter. You grab a ticket (Redis lock), then bring it to the cashier (DB write) to actually complete the purchase. If you don't show up in 10 minutes, your number expires and goes back in the pool.
