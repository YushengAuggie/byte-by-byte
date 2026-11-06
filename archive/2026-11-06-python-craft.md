# 🐍 Python Craft — Day 149 (Synthesis)
**构建高性能 Python 服务的完整工具链 — 从并发到可观测性**
**The Complete High-Performance Python Service Toolkit**

---

## 场景 / Scenario

你在设计一个 Python 后端服务，需要处理：高并发 API 请求、后台任务调度、定期数据处理、完善的可观测性。过去 50 天覆盖了各种独立工具，今天把它们串联成一套完整的生产级架构。

---

## 完整服务架构 / Complete Service Architecture

```
┌─────────────────────────────────────────────────────┐
│                  FastAPI / ASGI App                  │
│         (uvicorn, asyncio event loop, Day 48)        │
└──────────────┬──────────────────┬───────────────────┘
               │                  │
    ┌──────────▼──────┐  ┌────────▼──────────┐
    │  Request Layer   │  │  Background Tasks  │
    │ - Rate Limiting  │  │ - celery/rq        │
    │   (Day 83)       │  │ - asyncio.gather   │
    │ - Input Validate │  │   (Day 49)         │
    │   (Day 112)      │  │ - Circuit Breaker  │
    │ - Auth/Secrets   │  │   (Day 81)         │
    │   (Day 111)      │  └───────────────────┘
    └──────────┬──────┘
               │
    ┌──────────▼──────────────────────────┐
    │          Data & Cache Layer          │
    │ - Connection Pool (Day 78)           │
    │ - Redis: lru_cache + TTL (Day 101)   │
    │ - DB Migrations: Alembic (Day 103)   │
    │ - Serialization: msgpack (Day 102)   │
    └──────────┬──────────────────────────┘
               │
    ┌──────────▼──────────────────────────┐
    │        Observability Layer           │
    │ - structlog + correlation IDs (87)   │
    │ - cProfile / line_profiler (Day 97)  │
    │ - Retry + Backoff (Day 79)           │
    │ - Config: pydantic-settings (Day 86) │
    └─────────────────────────────────────┘
```

---

## 整合代码：生产级 FastAPI 服务骨架 / Production FastAPI Skeleton

```python
# app/main.py — Production-grade FastAPI with everything wired up

import structlog
import uvicorn
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.config import Settings  # pydantic-settings (Day 86)
from app.db import init_db_pool   # connection pool (Day 78)
from app.middleware import RateLimiter  # token bucket (Day 83)
from app.cache import cache_client     # Redis wrapper (Day 101)

log = structlog.get_logger()          # structured logging (Day 87)
settings = Settings()                 # validated config

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize resources
    await init_db_pool(settings.DATABASE_URL)
    await cache_client.connect(settings.REDIS_URL)
    log.info("app.started", env=settings.ENV)
    yield
    # Shutdown: clean up
    await cache_client.disconnect()
    log.info("app.stopped")

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    import uuid
    request_id = str(uuid.uuid4())[:8]
    # Bind to all subsequent log calls in this request
    with structlog.contextvars.bound_contextvars(request_id=request_id):
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

# Each endpoint gets: validated input, cached response, circuit-broken external calls
```

---

## 关键综合洞察 / Key Synthesis Insights

### 1. 并发选型决策树
```
任务类型?
├── IO密集 (HTTP/DB calls) → asyncio + httpx (Day 48/49)
├── CPU密集 (计算/压缩)   → multiprocessing.Pool (Day 47)
├── 混合型                 → asyncio + ProcessPoolExecutor (Day 52)
└── 后台任务               → Celery (Day 41) 或 asyncio.create_task
```

### 2. 错误处理层级
```python
# 三层防御: 输入验证 → 重试 → 熔断
@validate_input(UserSchema)           # pydantic (Day 112)
@retry(max_attempts=3, backoff=2.0)   # tenacity (Day 79)
@circuit_breaker(threshold=5)         # (Day 81)
async def call_external_service(data): ...
```

### 3. 测试金字塔回顾
```
E2E Tests (5%)           ← testcontainers (Day 96)
Integration Tests (25%)  ← pytest + real DB (Day 96)
Unit Tests (70%)         ← mocks + hypothesis (Day 89, 92)
```

---

## 别踩这个坑 / Common Pitfalls

❌ **在 async 函数里用同步 `requests`** — 会阻塞整个事件循环，用 `httpx` 或 `aiohttp`

❌ **全局 `lru_cache` 缓存 DB 连接** — `lru_cache` 是进程级的，用 connection pool

❌ **日志里写 f-string** — `log.info(f"user {user_id}")` 每次都构建字符串。用 `log.info("user", user_id=user_id)`（structlog 惰性求值）

✅ **Correlation ID 贯穿全链路** — 从 HTTP 请求到 DB 查询到外部调用，同一个 ID，调试时救命

---

## 📚 References

- https://docs.python.org/3/library/asyncio.html
- https://www.structlog.org/en/stable/
- https://fastapi.tiangolo.com/advanced/
- https://twelve-factor.net/

## 🧒 ELI5

就像一家餐厅：前台（FastAPI）接受点餐并验证；收银机（pydantic）确认金额；厨房（asyncio）同时做多道菜；冰箱（Redis缓存）存常用食材；监控摄像头（structlog）记录一切。每个工具各司其职，串在一起才是真正的生产级服务。
