# 🏗️ 系统设计 Day 14 / System Design Day 14
## 微服务 vs 单体架构 / Microservices vs Monolith

> **难度 / Difficulty:** Intermediate · **阶段 / Phase:** Growth · **预计阅读 / Read time:** 3 min

---

## 🌍 真实场景 / Real-World Scenario

想象你在一家初创公司工作，产品刚上线，代码都在一个仓库里。随着用户量增长到百万级别，你开始思考：要不要把代码拆成独立的服务？什么时候该拆？怎么拆？

Imagine you're at a startup. Your entire product lives in one codebase. As you scale to millions of users, you face the classic question: should you break it apart into microservices? When? How?

---

## 🏛️ 架构图 / Architecture Diagrams

### 单体架构 / Monolith
```
┌─────────────────────────────────────────┐
│              Monolith App               │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │  Users   │ │ Orders   │ │Payments │ │
│  │ Module   │ │ Module   │ │ Module  │ │
│  └────┬─────┘ └────┬─────┘ └────┬────┘ │
│       └─────────────┴─────────────┘     │
│                    │                    │
│          ┌─────────▼─────────┐         │
│          │   Single Database │         │
│          └───────────────────┘         │
└─────────────────────────────────────────┘
         │ Deploy everything together │
```

### 微服务架构 / Microservices
```
Client ──► API Gateway
               │
      ┌────────┼────────┐
      ▼        ▼        ▼
 ┌────────┐ ┌──────┐ ┌──────────┐
 │ Users  │ │Orders│ │ Payments │
 │Service │ │Svc   │ │ Service  │
 └───┬────┘ └──┬───┘ └───┬──────┘
     │         │          │
  ┌──▼──┐  ┌──▼──┐   ┌───▼───┐
  │ DB  │  │ DB  │   │  DB   │
  └─────┘  └─────┘   └───────┘
   (独立部署, message queue 通信)
```

---

## ⚖️ 核心权衡 / Key Tradeoffs

### 为什么选单体？/ Why Monolith?
- **简单** — 一个代码库，一次部署，本地开发直接跑
- **低延迟** — 模块间函数调用，无网络开销
- **事务一致性** — 一个数据库，ACID 事务天然支持
- **适合阶段** — 团队 < 20 人，产品 PMF 还没验证时

### 为什么选微服务？/ Why Microservices?
- **独立扩展** — Payment 服务流量暴增，只扩它，不动 Users 服务
- **技术异构** — 推荐系统用 Python/ML，API 层用 Go，各自最优
- **故障隔离** — 一个服务崩了，不影响整体
- **团队自治** — 不同团队独立发布，互不阻塞
- **适合阶段** — 团队 > 50 人，有专门 DevOps/Platform 团队时

### 对比表 / Comparison
| 维度 | 单体 | 微服务 |
|------|------|--------|
| 部署复杂度 | 低 ✅ | 高 ❌ |
| 开发速度(早期) | 快 ✅ | 慢 ❌ |
| 独立扩展 | ❌ | ✅ |
| 故障隔离 | ❌ | ✅ |
| 数据一致性 | 容易 ✅ | 需要设计 ❌ |
| 运维成本 | 低 ✅ | 高 ❌ |

---

## 🪤 别踩这个坑 / Common Mistakes

**❌ 坑1: 过早微服务化 (Premature Microservices)**
刚起步就拆服务，结果团队只有3个人要维护10个服务+Kubernetes。
> "We went microservices on day one, and it almost killed us." — every startup that tried it too early

**✅ 正确做法:** 先做"模块化单体"(Modular Monolith)，内部模块化，边界清晰，后期再物理拆分。

**❌ 坑2: 分布式单体 (Distributed Monolith)**
拆成多个服务，但服务之间强耦合，必须同步部署。既有微服务的复杂性，又没有微服务的好处。

**✅ 正确做法:** 服务间通过 API 或消息队列解耦，不共享数据库。

**❌ 坑3: 忽视跨服务事务**
订单服务扣库存成功，支付服务失败了，数据不一致。

**✅ 正确做法:** 使用 Saga 模式或最终一致性设计。

---

## 📚 References
- [Martin Fowler — Microservices](https://martinfowler.com/articles/microservices.html)
- [Martin Fowler — Monolith First](https://martinfowler.com/bliki/MonolithFirst.html)
- [AWS — Microservices vs Monolithic Architecture](https://aws.amazon.com/microservices/)

## 🧒 ELI5
单体就像一家小餐厅，一个厨房做所有菜，简单高效。微服务像大型餐厅连锁，每家分店专做一类菜，可以独立扩张，但管理更复杂。刚开始开一家店，别一上来就开连锁。

Monolith = one kitchen that cooks everything. Simple, fast to start. Microservices = a food court where each stall specializes. Great at scale, but way more management. Start with one kitchen; split when it gets too crowded.
