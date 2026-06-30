# 🐍 Python Craft — Day 78
**Topic:** Connection Pooling — DB, HTTP, Redis
**Category:** Practical Patterns | Week 7 | Phase: Expert

---

## 真实场景 / Real Scenario

你在做一个高并发后端服务。每次请求都要查数据库，每次都新建一个 TCP 连接。服务上线后，DB 报错：`too many connections`，响应时间飙升到 2 秒以上。

You have a high-concurrency backend. Each request creates a new TCP connection to the database. After launch, DB throws `too many connections` and response time spikes to 2+ seconds.

**根本原因：** 建立 TCP 连接 + TLS 握手 ≈ 50-200ms。100 QPS = 每秒新建 100 个连接。

---

## 为什么需要连接池 / Why Connection Pooling

```
没有连接池 / Without pooling:
  Request → [TCP handshake] → [Auth] → Query → [Teardown]
  每次 50-200ms 额外开销，DB 连接数随流量线性增长

有连接池 / With pooling:
  Request → [Get from pool] → Query → [Return to pool]
  一次握手，反复复用，DB 连接数上限可控
```

---

## 三个场景的连接池 / Three Scenarios

### 1. 数据库连接池 — SQLAlchemy

```python
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

# pool_size: 保持的常驻连接数
# max_overflow: 高峰时额外允许建立的连接数
# pool_timeout: 等待连接超时 (seconds)
# pool_recycle: 连接最大存活时间，防止 MySQL 8小时断连
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,  # test connection health before use
)

# 用法：with 语句自动归还连接
def get_user(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM users WHERE id = :id"),
            {"id": user_id}
        )
        return result.fetchone()
```

**关键参数解读：**
```
pool_size=10      → 10 个连接随时待命
max_overflow=20   → 最大并发 30 个连接
pool_pre_ping     → 像心跳，防止用到已断开的连接
pool_recycle      → 超时自动重建，防止数据库端踢掉连接
```

### 2. HTTP 连接池 — httpx/requests

```python
import httpx
import asyncio

# 全局 client，跨请求共享连接池
# 不要在每个函数里 `with httpx.AsyncClient() as c:`（这会关闭连接池！）
http_client = httpx.AsyncClient(
    limits=httpx.Limits(
        max_connections=100,       # 总连接数上限
        max_keepalive_connections=20,  # 保持的 keepalive 连接
        keepalive_expiry=30,       # keepalive 超时秒数
    ),
    timeout=httpx.Timeout(connect=5.0, read=30.0),
)

async def fetch_user_profile(user_id: str) -> dict:
    response = await http_client.get(f"https://api.example.com/users/{user_id}")
    response.raise_for_status()
    return response.json()

# 在应用关闭时清理
async def shutdown():
    await http_client.aclose()
```

### 3. Redis 连接池 — redis-py

```python
import redis

# 创建连接池（全局单例）
pool = redis.ConnectionPool(
    host="localhost",
    port=6379,
    db=0,
    max_connections=50,
    decode_responses=True,
)

# 每次使用时从池里借连接
def cache_get(key: str):
    r = redis.Redis(connection_pool=pool)
    return r.get(key)

def cache_set(key: str, value: str, ttl: int = 300):
    r = redis.Redis(connection_pool=pool)
    r.setex(key, ttl, value)
```

---

## ❌ 常见错误 / Common Mistakes

```python
# ❌ 错误：每个请求创建新 client（销毁了连接池！）
async def bad_request():
    async with httpx.AsyncClient() as client:
        return await client.get("https://api.example.com/data")

# ✅ 正确：全局 client，复用连接
_client = httpx.AsyncClient()
async def good_request():
    return await _client.get("https://api.example.com/data")

# ❌ 错误：不设 pool_recycle，MySQL 8小时后断连
engine = create_engine("mysql://...", pool_size=10)

# ✅ 正确：设置 recycle 和 pre_ping
engine = create_engine("mysql://...", pool_size=10, 
                        pool_recycle=3600, pool_pre_ping=True)
```

---

## 连接池调参指南 / Tuning Guide

```
pool_size = CPU核数 × 2 ~ 4 (通用起点)

Web 服务:
  - 如果主要是 I/O 等待：pool_size = 20-50 (async 场景)
  - 如果 CPU 密集：pool_size = CPU 核数 × 2

DB 侧考虑:
  - PostgreSQL 每个连接约消耗 5-10MB 内存
  - 100 个服务实例 × 10 连接 = 1000 DB 连接
  - 使用 PgBouncer 做连接池代理，聚合到 DB 侧

监控指标:
  - pool.size (已创建)
  - pool.checked_out (使用中)
  - pool.overflow (超出 pool_size 的额外连接)
  - pool.timeout_count (等待超时次数 → 需要加大 pool_size)
```

---

## 📚 References

- 🔗 [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
- 🔗 [httpx Connection Limits](https://www.python-httpx.org/advanced/resource-limits/)
- 🔗 [Redis-py Connection Pool Docs](https://redis-py.readthedocs.io/en/stable/connections.html#connection-pools)

---

## 🧒 ELI5

你去一家咖啡馆，没有连接池的情况是：每次你要点咖啡，店员都要先跑出去找一把新椅子、拼一张新桌子，然后你喝完咖啡，桌子椅子全部销毁。每次 50 秒，效率极低。

连接池就是：**咖啡馆提前摆好 10 张桌子**，你来了直接坐，喝完还回去，下一个客人继续用。桌子不会销毁，反复复用，大家等待时间从 50 秒变成 1 秒。
