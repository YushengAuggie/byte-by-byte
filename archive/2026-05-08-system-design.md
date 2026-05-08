# 🏗️ 系统设计 / System Design — Design a Payment System (Stripe)

> Day 38 · Mastery Phase · ~3 min read

---

## 想象你在设计...

你被要求为一个电商平台设计支付系统，类似 Stripe。每天需要处理数百万笔交易，支持信用卡、数字钱包等多种支付方式，同时保证资金安全和高可用性。

*Imagine you're designing a payment system for an e-commerce platform like Stripe. You need to handle millions of transactions daily, support credit cards and digital wallets, and guarantee both fund security and high availability.*

---

## 架构图 / Architecture Diagram

```
Client (Browser/App)
       │
       ▼
  [API Gateway]
  (TLS, auth, rate limit)
       │
  ┌────┴────┐
  │         │
  ▼         ▼
[Payment   [Fraud
 Service]   Detection]
  │              │
  │◄─────────────┘
  │         (async scoring)
  ▼
[Payment Processor]
(Stripe, Adyen, Braintree)
       │
  ┌────┴────────────┐
  │                 │
  ▼                 ▼
[Ledger DB]    [Event Bus]
(PostgreSQL     (Kafka)
 + double-entry)    │
                    ├──► [Notification Service]
                    ├──► [Analytics Pipeline]
                    └──► [Reconciliation Service]

[Idempotency Store]  ←── All write requests keyed here
(Redis)
```

---

## 核心设计决策 / Key Design Decisions

### 1. 幂等性 (Idempotency) — 最关键
支付最怕的是**重复扣款**。每个支付请求必须携带唯一 `idempotency_key`，服务端在 Redis 中记录已处理的请求。

*The biggest fear in payments is double-charging. Every payment request carries a unique `idempotency_key`. The service stores processed requests in Redis — if the same key comes again, return the cached result.*

```
POST /v1/charges
Idempotency-Key: user-123-order-456-attempt-1
```

### 2. 双重记账 (Double-Entry Ledger)
银行用了几百年的方法。每笔交易产生两条记录：借方 + 贷方，总和必须为 0。这样账目永远对得上。

*Banks have used this for centuries. Every transaction creates two entries: debit + credit, always summing to zero. This makes reconciliation trivial and catches bugs immediately.*

### 3. 状态机 (State Machine)
支付状态：`PENDING → PROCESSING → AUTHORIZED → CAPTURED → SETTLED` (or `FAILED`, `REFUNDED`)

每个状态转移必须是原子的，使用数据库事务 + 乐观锁防止并发问题。

*Each state transition must be atomic, using DB transactions + optimistic locking to prevent race conditions.*

### 4. 异步欺诈检测 (Async Fraud Detection)
欺诈检测不能阻塞支付流程（延迟太高）。用 Kafka 异步处理：先放行，发现欺诈后退款，同时标记账户。

*Fraud detection can't block the payment flow (too slow). Use Kafka for async processing: approve first, refund + flag if fraud detected. This is the industry standard — 100% fraud prevention is impossible anyway.*

---

## 为什么这样设计？ / Why These Choices?

| 决策 | 原因 |
|------|------|
| Redis 幂等存储 | 快速 O(1) 查找，支付窗口内有效即可 |
| PostgreSQL 账本 | ACID 事务、强一致性，资金不能用最终一致 |
| Kafka 事件流 | 解耦下游服务，支持重放审计 |
| 状态机 | 防止非法状态转移（不能从 FAILED 直接变 CAPTURED）|

---

## 别踩这个坑 / Common Mistakes

❌ **直接调用支付网关不处理超时** — 网络超时后你不知道是否扣款成功，必须轮询查询最终状态

❌ **数据库金额用 float** — 浮点数精度问题会导致 $0.01 的差异。**永远用整数存分 (cents)**

❌ **忽略退款流程** — 退款和收款一样复杂，需要独立设计

❌ **单点支付网关** — Stripe 也会宕机，需要备用支付通道 (Adyen, Braintree)

✅ **正确做法：** 幂等键 + 整数金额 + 状态机 + 多通道降级

---

## 📚 参考资料 / References

- [Stripe API Idempotent Requests](https://stripe.com/docs/api/idempotent_requests)
- [Ledger — How Stripe's ledger works](https://stripe.com/blog/ledger-stripe-system-for-tracking-and-validating-money-movement)
- [System Design: Payment System (ByteByteGo)](https://blog.bytebytego.com/p/design-a-payment-system)

---

## 🧒 ELI5

想象你去超市买东西，把购物清单给收银员（支付请求）。收银员把你的名字写在小本本上（幂等键），这样就算你说了两遍"我要结账"，也只收你一次钱。收银员在账本上写"顾客减少 $50，超市增加 $50"（双重记账）。如果你的信用卡被盗，超市会事后发现然后退款——不会为了检查每张卡把所有人都堵在收银台前（异步欺诈检测）。

*Imagine buying groceries. The cashier writes your name in a notebook (idempotency key) so even if you say "charge me" twice, you only pay once. They record "customer -$50, store +$50" in the ledger (double-entry). If your card was stolen, the store discovers it later and refunds — they don't block the checkout line to verify every card (async fraud detection).*
