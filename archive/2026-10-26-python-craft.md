🎨 **前端 / Frontend (Python Craft Synthesis)**
*Day 142 · Expert Synthesis — Python 性能调优全景*

---

## 场景 / Scenario

你在优化一个处理 100K 并发用户的 Python 后端服务。老板说延迟从 50ms 爬到了 800ms。你怎么系统性地找到并修复瓶颈？

You're optimizing a Python backend serving 100K concurrent users. Latency jumped from 50ms to 800ms. How do you systematically diagnose and fix it?

---

## 诊断流程 / Diagnosis Flow

```
高延迟
  │
  ├── CPU 绑定？ → cProfile / py-spy
  ├── I/O 阻塞？ → asyncio + 连接池
  ├── 内存泄漏？ → memory_profiler / tracemalloc
  └── GIL 竞争？ → 换 multiprocessing 或 C 扩展
```

---

## 工具箱 / Full Toolkit (覆盖已学 50 个话题的精华)

### 1. 性能剖析 (Day 97 综合)

```python
# cpu profiling — 找热点函数
import cProfile, pstats, io

pr = cProfile.Profile()
pr.enable()
your_function()
pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats(20)  # top 20 hotspots
print(s.getvalue())
```

```bash
# line-level profiling — 找热点行
pip install line_profiler
kernprof -l -v your_script.py
```

### 2. 异步 I/O 优化 (Day 48/49 综合)

```python
import asyncio
import aiohttp

# 错误：串行请求
# for url in urls:
#     result = requests.get(url)  # blocks GIL!

# 正确：并发请求
async def fetch_all(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)  # concurrent, not parallel

async def fetch_one(session, url):
    async with session.get(url) as r:
        return await r.json()
```

### 3. 连接池 (Day 78 综合)

```python
# SQLAlchemy connection pooling
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://...",
    pool_size=20,          # steady-state connections
    max_overflow=10,       # burst capacity
    pool_timeout=30,       # wait before raising PoolTimeoutError
    pool_recycle=1800,     # recycle connections every 30min
)
```

### 4. 缓存策略 (Day 101 综合)

```python
from functools import lru_cache
import redis.asyncio as aioredis

# L1: in-process LRU (microseconds)
@lru_cache(maxsize=1024)
def get_config(key: str) -> str:
    ...

# L2: Redis (< 1ms on same datacenter)
redis_client = aioredis.from_url("redis://localhost")

async def get_user(user_id: int) -> dict:
    cache_key = f"user:{user_id}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    user = await db.fetch_user(user_id)  # L3: DB
    await redis_client.setex(cache_key, 300, json.dumps(user))
    return user
```

### 5. GIL 绕过 (Day 54 综合)

```python
from concurrent.futures import ProcessPoolExecutor
import numpy as np

# CPU-bound: use multiprocessing to bypass GIL
def cpu_heavy(data: list[float]) -> float:
    arr = np.array(data)
    return float(np.fft.fft(arr).real.sum())

with ProcessPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(cpu_heavy, chunks))
```

---

## 性能清单 / Production Checklist

| 问题 | 工具 | 修复 |
|------|------|------|
| 函数太慢 | cProfile | 算法优化/缓存 |
| I/O 阻塞 | asyncio profiler | async + 连接池 |
| 内存泄漏 | tracemalloc | 清理引用/生成器 |
| CPU 密集 | py-spy | ProcessPool/Cython |
| DB 慢查询 | EXPLAIN ANALYZE | 索引/查询优化 |

---

## 📚 References

- https://docs.python.org/3/library/profile.html — cProfile docs
- https://github.com/benfred/py-spy — py-spy sampling profiler
- https://docs.sqlalchemy.org/en/20/core/pooling.html — Connection pooling

## 🧒 ELI5

Python 慢了就像汽车发动机有问题。先插诊断仪（profiler）看哪里卡，可能是某个零件太热（CPU），可能是燃油管堵了（I/O），可能是内存漏油了（leak）。找到问题才能修，不要瞎猜乱换零件。
