# 🐍 Python Craft — 综合 Day 51: Python 异步全栈 — asyncio + aiohttp + 生产模式

> **综合模式 / Synthesis Mode:** 之前覆盖了 threading、multiprocessing、asyncio 基础与进阶、gRPC、WebSocket、连接池等。今天综合串联：**生产级异步 Python 服务架构**。

---

## 现实场景 / Real Scenario

你要写一个后端服务：同时处理数百个并发 API 请求，每个请求需要查询外部 HTTP API + Redis + DB。
同步写法？慢成灾。多线程？GIL 限制。**正确答案：asyncio + aiohttp + 连接池。**

---

## 把之前学的串联起来

```
Day 48: asyncio basics        → event loop, coroutine, await
Day 49: asyncio patterns      → gather, Semaphore, Queue  
Day 51: WSGI/ASGI             → how web servers handle async requests
Day 77: context managers      → async with, async for
Day 78: connection pooling     → aiohttp.ClientSession, asyncpg pool
```

今天把这些拼成一个**完整的生产异步服务**。

---

## 完整示例：并发 API 聚合服务

```python
import asyncio
import aiohttp
import asyncpg
import time
from contextlib import asynccontextmanager

# ─── Connection Pool Manager ───────────────────────────────────────────
class AppState:
    """Shared state with connection pools (init once, share everywhere)"""
    def __init__(self):
        self.http_session: aiohttp.ClientSession | None = None
        self.db_pool: asyncpg.Pool | None = None

@asynccontextmanager
async def lifespan(app_state: AppState):
    """ASGI lifespan: init pools on startup, cleanup on shutdown"""
    # Startup
    app_state.http_session = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=10),
        connector=aiohttp.TCPConnector(limit=100)  # max 100 concurrent connections
    )
    app_state.db_pool = await asyncpg.create_pool(
        dsn="postgresql://user:pass@localhost/db",
        min_size=5,
        max_size=20
    )
    print("✅ Pools initialized")
    
    yield  # app runs here
    
    # Shutdown
    await app_state.http_session.close()
    await app_state.db_pool.close()
    print("✅ Pools closed")

# ─── Semaphore-limited concurrent fetcher ──────────────────────────────
async def fetch_with_limit(
    session: aiohttp.ClientSession,
    url: str,
    sem: asyncio.Semaphore
) -> dict:
    async with sem:  # max N concurrent requests at a time
        async with session.get(url) as resp:
            return await resp.json()

async def fetch_many(session: aiohttp.ClientSession, urls: list[str]) -> list[dict]:
    sem = asyncio.Semaphore(20)  # rate limit: 20 concurrent
    tasks = [fetch_with_limit(session, url, sem) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # Filter out exceptions
    return [r for r in results if not isinstance(r, Exception)]

# ─── DB query with pool ─────────────────────────────────────────────────
async def get_users_from_db(pool: asyncpg.Pool, user_ids: list[int]) -> list[dict]:
    async with pool.acquire() as conn:  # borrow connection from pool
        rows = await conn.fetch(
            "SELECT id, name FROM users WHERE id = ANY($1)",
            user_ids
        )
        return [dict(r) for r in rows]

# ─── Aggregator: parallel HTTP + DB ────────────────────────────────────
async def aggregate_user_data(state: AppState, user_ids: list[int]):
    urls = [f"https://api.example.com/scores/{uid}" for uid in user_ids]
    
    # Run HTTP fetches and DB query concurrently
    scores_task = fetch_many(state.http_session, urls)
    users_task = get_users_from_db(state.db_pool, user_ids)
    
    scores, users = await asyncio.gather(scores_task, users_task)
    return {"users": users, "scores": scores}
```

---

## 性能对比 / Performance Comparison

```
同步顺序调用 10 个 API（每个 100ms）：
  total = 10 × 100ms = 1000ms  ❌

asyncio.gather 并发：
  total ≈ 100ms (all run simultaneously)  ✅

asyncio + Semaphore(3)：
  total ≈ ceil(10/3) × 100ms ≈ 400ms  ✅ (rate-limited but still fast)
```

---

## 生产关键点

| 反模式 ❌ | 正确做法 ✅ |
|---|---|
| 每次请求创建新 `aiohttp.ClientSession` | 全局单例，生命周期管理 |
| `asyncio.sleep` 在同步代码里 | 用 `time.sleep` 会阻塞事件循环！用 `asyncio.sleep` |
| 无限并发 `gather` | 用 `Semaphore` 限制并发数 |
| 忘记关闭连接池 | 用 `asynccontextmanager` 或 ASGI lifespan |
| 在 async 函数里调用同步阻塞 IO | 用 `loop.run_in_executor` 包装 |

---

## 一句话总结

> **asyncio + 连接池 + Semaphore = 生产级 Python 异步服务的三件套。**

---

## 📚 References
- https://docs.aiohttp.org/en/stable/client_advanced.html — aiohttp 连接池与 Session 管理
- https://magicstack.github.io/asyncpg/current/ — asyncpg 高性能 PostgreSQL 异步驱动
- https://fastapi.tiangolo.com/async/ — FastAPI 异步最佳实践

## 🧒 ELI5
同步代码像一个收银员一次只服务一位顾客；asyncio 像一个收银员在等一个顾客刷卡时，同时帮下一个顾客扫码——等待的时间不浪费了。连接池是"提前备好的收银台"，不用每次开关。
