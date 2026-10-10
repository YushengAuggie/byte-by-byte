# 🐍 Python Craft — Day 137 (Synthesis)
## Python 异步 + 并发全景：threading vs multiprocessing vs asyncio 终极对比
## Python Concurrency Model: The Definitive Comparison

> **综合模式 / Synthesis Mode** — 回顾并整合之前覆盖的并发三大模型，给出决策框架。

---

### 🎯 问题 / The Problem

你有一个任务要并发执行。Python 里有三种方式：`threading`、`multiprocessing`、`asyncio`。选哪个？大多数人凭感觉，但其实有清晰的决策树。

*You need concurrency. Python gives you three tools. Most people guess. There's actually a clear decision tree.*

---

### 🧠 三大模型原理 / Three Models Explained

```
┌─────────────────────────────────────────────────────┐
│              Python 并发三大模型                      │
├──────────────┬──────────────────┬────────────────────┤
│   threading  │  multiprocessing │      asyncio       │
├──────────────┼──────────────────┼────────────────────┤
│ 共享内存      │ 独立进程/内存     │ 单线程事件循环      │
│ 受 GIL 限制  │ 无 GIL 限制      │ 受 GIL，但不在乎   │
│ I/O 并发 ✓   │ CPU 并行 ✓       │ I/O 并发 ✓✓✓      │
│ 上下文切换贵  │ 进程启动慢        │ 极低开销           │
└──────────────┴──────────────────┴────────────────────┘
```

---

### 🌳 决策树 / Decision Tree

```
你的任务是什么？
│
├─ CPU 密集型（矩阵运算、图像处理、加密）
│   └─ → multiprocessing.Pool  ← GIL 释放，真正并行
│
├─ I/O 密集型（HTTP 请求、数据库、文件）
│   ├─ 已有 async 库支持（httpx, asyncpg, aiofiles）？
│   │   └─ YES → asyncio  ← 单线程，零开销，最优雅
│   └─ 库是同步的（requests, psycopg2, boto3）？
│       └─ → threading 或 concurrent.futures.ThreadPool
│
└─ 混合型（ML pipeline：数据加载 I/O + 模型推理 CPU）
    └─ → asyncio for I/O + ProcessPoolExecutor for CPU
```

---

### 🔬 代码对比 / Code Comparison

**场景：并发请求 10 个 URLs**

```python
import time
import asyncio
import httpx
from concurrent.futures import ThreadPoolExecutor
import requests

URLS = [f"https://httpbin.org/delay/1"] * 5  # each takes ~1s

# ❌ 方式1：串行 (~5s)
def sequential():
    return [requests.get(u).status_code for u in URLS]

# ✓ 方式2：threading (~1s, 但有 GIL 和线程开销)
def with_threads():
    with ThreadPoolExecutor(max_workers=5) as ex:
        return list(ex.map(lambda u: requests.get(u).status_code, URLS))

# ✓✓ 方式3：asyncio (~1s, 更低开销，更高并发上限)
async def with_asyncio():
    async with httpx.AsyncClient() as client:
        tasks = [client.get(u) for u in URLS]
        responses = await asyncio.gather(*tasks)
        return [r.status_code for r in responses]
```

**结论：** asyncio 的并发上限远高于 threading（1000+ 协程 vs ~100 线程），且内存开销更小。

---

### ⚠️ 经典陷阱 / Classic Traps

```python
# ❌ 陷阱1：在 asyncio 中调用阻塞函数
async def bad():
    time.sleep(1)  # 阻塞整个事件循环！所有协程卡死
    
# ✅ 正确：用 run_in_executor 把阻塞调用丢进线程池
async def good():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, time.sleep, 1)

# ❌ 陷阱2：用 multiprocessing 处理 I/O
# 进程启动耗时 ~100ms，比 I/O 本身还慢

# ❌ 陷阱3：threading + CPU 密集型任务
# GIL 让线程轮流执行，实际上是串行！
```

---

### 🧩 高级组合模式 / Advanced Combo Pattern

```python
# ML Pipeline: asyncio for data loading + ProcessPool for inference
import asyncio
from concurrent.futures import ProcessPoolExecutor

executor = ProcessPoolExecutor(max_workers=4)

async def pipeline(batch_urls):
    loop = asyncio.get_event_loop()
    
    # 1. Async I/O: fetch data concurrently
    async with httpx.AsyncClient() as client:
        data_list = await asyncio.gather(*[client.get(u) for u in batch_urls])
    
    # 2. CPU work: run in process pool (escapes GIL)
    results = await asyncio.gather(*[
        loop.run_in_executor(executor, cpu_heavy_inference, d.content)
        for d in data_list
    ])
    return results
```

---

### 📊 性能基准对比 / Performance Benchmark

| 场景 | Sequential | Threading | asyncio | multiprocessing |
|------|-----------|-----------|---------|-----------------|
| 100 HTTP 请求 | 100s | 2s | 1s | ❌ 不适合 |
| 4核 CPU 矩阵运算 | 4s | 4s (GIL!) | ❌ | 1s |
| 1000 并发连接 | - | OOM | ✓ | ❌ |

---

### 📚 参考资料 / References

- [Python asyncio docs](https://docs.python.org/3/library/asyncio.html)
- [Real Python: Python Concurrency Overview](https://realpython.com/python-concurrency/)
- [David Beazley: Understanding the GIL (PyCon 2010)](https://www.dabeaz.com/GIL/)

### 🧒 ELI5

假设你要洗100个碗：
- **串行**：一个个洗，最慢
- **多线程**：几个人一起洗，但厨房只有一个水槽（GIL）——对洗碗（I/O）有用，对切菜（CPU）没用
- **多进程**：多个厨房同时工作，真正并行，但搬厨房费时间（进程启动慢）
- **asyncio**：一个人洗，但碗泡着的时候不闲着，继续处理其他事——I/O 等待时间近乎为零
