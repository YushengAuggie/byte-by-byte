# 🎨 前端 / Frontend — Day 119 (Python Craft Synthesis)
## Python 性能调优全景：从 profiling 到生产优化
## Python Performance Tuning: From Profiling to Production

---

### 真实场景 / Real Scenario

你在做一个 API 服务，某个端点 P99 延迟 800ms，需要优化到 <200ms。你从哪里开始？

You're running an API service. One endpoint has P99 latency of 800ms — needs to be <200ms. Where do you start?

**答案：先 profile，再优化。不要猜！/ Answer: Profile first, then optimize. Never guess!**

---

### 第一步：找瓶颈 / Step 1: Find the Bottleneck

```python
# cProfile — 找函数级别热点
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
your_slow_function()
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # top 20 slowest functions

# line_profiler — 找行级别热点 (pip install line-profiler)
# @profile decorator, then: kernprof -l -v script.py

# memory_profiler — 找内存泄漏 (pip install memory-profiler)  
# @profile decorator, then: python -m memory_profiler script.py
```

---

### 第二步：常见瓶颈 & 修复方法 / Common Bottlenecks & Fixes

#### 🔴 N+1 Query Problem (最常见 / Most Common)
```python
# ❌ 每个 user 单独查询
users = User.query.all()
for user in users:
    orders = Order.query.filter_by(user_id=user.id).all()  # N queries!

# ✅ 一次 JOIN
users_with_orders = User.query.options(
    joinedload(User.orders)
).all()
```

#### 🔴 Missing Caching
```python
from functools import lru_cache
import redis

# In-process cache (同一进程)
@lru_cache(maxsize=1000)
def get_user_permissions(user_id: int) -> list[str]:
    return db.query_permissions(user_id)  # expensive DB call

# Distributed cache (跨进程/服务)
r = redis.Redis()
def get_user_permissions_cached(user_id: int) -> list[str]:
    key = f"perms:{user_id}"
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    perms = db.query_permissions(user_id)
    r.setex(key, 300, json.dumps(perms))  # TTL 5 min
    return perms
```

#### 🔴 Sync I/O in Async Context
```python
# ❌ Blocking call inside async — 阻塞整个事件循环
async def get_data():
    result = requests.get(url)  # 同步！blocks event loop

# ✅ Use async client
import httpx
async def get_data():
    async with httpx.AsyncClient() as client:
        result = await client.get(url)  # non-blocking
```

---

### 猜猜输出 / Quiz — What's the Output?

```python
import time
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

start = time.time()
result = fib(35)
elapsed = time.time() - start
print(f"fib(35)={result}, took {elapsed:.6f}s")
```

**A)** fib(35)=9227465, took ~3.5s (指数级)
**B)** fib(35)=9227465, took ~0.000001s (缓存命中)
**C)** RecursionError: maximum recursion depth exceeded
**D)** fib(35)=9227465, took ~0.001s (第一次调用，但有 lru_cache 加速)

<details><summary>答案 / Answer</summary>
**D** — `lru_cache` 是 memoization，**第一次调用**时缓存中间结果，把指数级变成线性级 O(n)。大约 0.0001~0.001s。每次子调用只算一次，所以不会是 3.5s。
</details>

---

### When to Use / When NOT to Use

✅ **Profile 有依据时才优化:** "感觉慢" 不如 "cProfile 显示 80% 时间在 X 函数"
✅ **lru_cache:** 纯函数 + 重复调用 + 有限参数空间
✅ **Redis 缓存:** 跨进程共享、需要 TTL、需要主动失效
❌ **不要 premature optimization:** 可读性 > 微优化（<1ms 的）
❌ **lru_cache on methods:** 会持有 self 引用，导致内存泄漏

---

### 📚 References
- https://docs.python.org/3/library/profile.html — cProfile 官方文档
- https://github.com/pyutils/line_profiler — line-profiler
- https://realpython.com/python-profiling/ — 完整 profiling 教程

### 🧒 ELI5
优化代码就像找家里漏水的地方。不是每个水管都检查一遍（猜），而是先看水表哪里用水最多（profiling），然后集中修那个地方。Python 的 cProfile 就是你的水表。

Optimizing code is like finding a water leak. Don't check every pipe (guessing). Look at the water meter to see where most water goes (profiling), then fix THAT pipe. cProfile is your water meter.
