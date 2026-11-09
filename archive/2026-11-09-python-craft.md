# 🐍 Python Craft — Day 151 (Synthesis)

> **综合深化 / Expert Synthesis:** 50个 Python Craft 话题全部完成。今天深度对比——Python 异步编程的三个时代。

---

## Python 并发模型全景：threading vs multiprocessing vs asyncio — 最终决战

50个话题学完了，今天把所有并发相关知识串成一张清晰的决策图。

---

### 三种模型的本质区别

```
threading           multiprocessing        asyncio
    |                      |                  |
共享内存             独立内存空间            单线程事件循环
OS线程调度           OS进程调度             协作式调度
受 GIL 限制          绕过 GIL              无 GIL 问题
I/O密集型OK          CPU密集型OK           I/O密集型最优
```

**GIL 的本质:** CPython 在任意时刻只允许一个线程执行 Python 字节码。
- threading: 多线程，但 GIL 让 CPU 密集任务无法真正并行
- multiprocessing: 多进程，每个进程有自己的 GIL，真正并行
- asyncio: 单线程，根本不需要 GIL，通过协作式切换避免竞争

---

### 决策树（收藏这个）

```
任务类型是什么?
    │
    ├── I/O 密集 (网络、文件、DB)
    │       │
    │       ├── 需要高并发 (>1000 connections)?
    │       │       └── asyncio + aiohttp/asyncpg ✅
    │       │
    │       └── 普通并发 (<100)?
    │               └── ThreadPoolExecutor ✅
    │
    └── CPU 密集 (数学运算、图像处理、ML推理)
            │
            ├── 任务可分片?
            │       └── ProcessPoolExecutor / multiprocessing.Pool ✅
            │
            └── NumPy/Pandas?
                    └── 它们释放 GIL，threading 也行 ✅
```

---

### 实战代码对比: 抓取100个 URL

```python
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor
import requests

URLS = [f"https://httpbin.org/delay/0.1" for _ in range(20)]

# ---- Method 1: Sequential (baseline) ----
def fetch_sequential():
    results = [requests.get(url).status_code for url in URLS]
    return results
# ~2+ seconds for 20 requests

# ---- Method 2: ThreadPoolExecutor ----
def fetch_threaded():
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(lambda u: requests.get(u).status_code, URLS))
    return results
# ~0.3 seconds — 10x speedup

# ---- Method 3: asyncio (best for I/O) ----
async def fetch_one(session, url):
    async with session.get(url) as resp:
        return resp.status

async def fetch_async():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in URLS]
        return await asyncio.gather(*tasks)
# ~0.15 seconds — 20x speedup, lower memory than threading
```

---

### asyncio 的隐藏陷阱（高频面试点）

```python
# ❌ 常见错误: 在 async 函数里用同步阻塞调用
async def bad():
    import time
    time.sleep(1)  # 阻塞整个事件循环！所有协程都卡住
    
# ✅ 正确: 使用 asyncio.sleep 或在 executor 中运行同步代码
async def good():
    await asyncio.sleep(1)  # 释放控制权，其他协程可以运行

async def good_sync():
    loop = asyncio.get_event_loop()
    # 把 CPU 密集或阻塞操作放到线程池
    result = await loop.run_in_executor(None, blocking_function)
```

**关键理解:** `async/await` 只是语法糖，本质是在单线程中的协作式切换。
你不能在异步代码里混同步阻塞，就像你不能在协程里睡觉。

---

### Python 3.12+ 的新变化: Sub-Interpreters

Python 3.12 开始引入 per-interpreter GIL，允许多个解释器各有独立 GIL 运行在同一进程内。这是继 asyncio 后最重要的并发进化。

```python
# 未来的写法 (PEP 684, Python 3.12+)
import _interpreters  # experimental API
# Eventually: 在同一进程内真正并行运行 Python 代码
# 内存隔离比 threading，但比 multiprocessing 轻量
```

---

### 面试考点速记

| 问题 | 答案 |
|------|------|
| GIL 是什么? | CPython 全局解释器锁，保护内存管理 |
| threading 能做 CPU 并行吗? | 不能（GIL），但 I/O 可以 |
| asyncio 用几个线程? | 1个（事件循环线程），可以配合 executor |
| 1000个 DB 连接用什么? | asyncio + asyncpg/aiomysql |
| 图像批量处理用什么? | ProcessPoolExecutor |

---

### 📚 References
- https://docs.python.org/3/library/asyncio.html — asyncio official docs
- https://realpython.com/async-io-python/ — Real Python asyncio guide
- https://www.youtube.com/watch?v=X7vBbelRXn0 — Python GIL explained (David Beazley)
- https://peps.python.org/pep-0703/ — PEP 703: Making the GIL Optional

### 🧒 ELI5
三种并发就像餐厅的三种服务模式：
- **threading**: 多个服务员，但厨房只有一把刀（GIL），还是得排队切菜
- **multiprocessing**: 开多家分店，每家都有自己的厨房，真的独立
- **asyncio**: 一个超级服务员，同时照顾所有桌，趁客人看菜单的时候去给别桌倒水
大多数后端服务是"等网络"，所以 asyncio 那个超级服务员最高效。
