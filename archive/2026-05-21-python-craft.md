# 🐍 Python Craft — Day 3
## asyncio 基础 — 事件循环、协程、await
## asyncio Basics — Event Loop, Coroutines, await

> **主题 / Topic:** Concurrency & Parallelism · Week 1 | **Phase:** Mastery | **预计时间 / Read time:** 2 min

---

## 🎯 场景 / Scenario

你在做一个 dashboard，需要同时从 5 个 API 拉取数据。如果用同步代码，总耗时 = 所有 API 的时间之和。用 asyncio，总耗时 ≈ 最慢那个 API 的时间。
*You're building a dashboard that fetches data from 5 APIs simultaneously. Synchronous code: total time = sum of all API calls. With asyncio: total time ≈ slowest single API call.*

---

## 🧠 核心概念 / Core Concepts

### 事件循环是什么 / What is the Event Loop?
想象一个餐厅服务员（事件循环），只有一个人，但同时服务 10 桌。每当一桌在等厨房（I/O 等待），他就去服务另一桌。没有真正的并行，但效率极高。
*Imagine a single waiter (event loop) serving 10 tables. While one table waits for food (I/O), the waiter serves another. No true parallelism, but very efficient.*

### 协程 vs 线程 / Coroutines vs Threads
| | 协程 Coroutines | 线程 Threads |
|---|---|---|
| **切换** | 主动让出 (`await`) | OS 抢占 |
| **开销** | 极低 (~KB) | 较高 (~MB) |
| **共享状态** | 单线程，无锁问题 | 需要 Lock |
| **适用** | I/O 密集 | CPU 密集 / I/O 密集 |

---

## 💻 代码示例 / Code

```python
import asyncio
import time

# async def 定义协程函数 / defines a coroutine function
async def fetch_data(name: str, delay: float) -> str:
    print(f"[{name}] Starting fetch...")
    await asyncio.sleep(delay)  # yield control back to event loop
    print(f"[{name}] Done after {delay}s")
    return f"{name}: result"

async def main():
    start = time.time()

    # asyncio.gather: run coroutines CONCURRENTLY (not sequentially)
    results = await asyncio.gather(
        fetch_data("API-A", 1.0),
        fetch_data("API-B", 2.0),
        fetch_data("API-C", 0.5),
    )

    elapsed = time.time() - start
    print(f"\nAll done in {elapsed:.1f}s")  # ~2.0s, not 3.5s
    print(results)

asyncio.run(main())

# Output:
# [API-A] Starting fetch...
# [API-B] Starting fetch...
# [API-C] Starting fetch...
# [API-C] Done after 0.5s
# [API-A] Done after 1.0s
# [API-B] Done after 2.0s
# All done in 2.0s  ← concurrent, not 3.5s sequential!
```

---

## ⚠️ 常见陷阱 / Common Mistakes

**❌ 在协程里用阻塞函数：**
```python
async def bad():
    time.sleep(1)  # BLOCKS the entire event loop! 💀
```

**✅ 正确做法：**
```python
async def good():
    await asyncio.sleep(1)  # yields, event loop can run other tasks
    # Or run blocking code in a thread pool:
    await asyncio.to_thread(blocking_function, args)
```

---

## 🔑 何时用 / 何时不用 / When to Use / When NOT to Use

**✅ 用 asyncio:**
- HTTP 请求（`aiohttp`, `httpx`）
- 数据库查询（`asyncpg`, `aiosqlite`）  
- 文件 I/O（大量并发小文件）

**❌ 不用 asyncio:**
- CPU 密集计算（用 `multiprocessing`）
- 简单脚本（同步代码更易读）
- 依赖同步库（避免混用，复杂度爆炸）

---

## 🔗 与前面课题的联系 / Connection to Previous Topics
- Day 1: `threading` — 线程适合 I/O 但有 GIL 限制
- Day 2: `multiprocessing` — 绕过 GIL，适合 CPU 任务
- **Day 3: `asyncio`** — 单线程高并发，适合网络 I/O ← *今天 / Today*

**选择口诀:** I/O 密集 + 高并发 → asyncio；CPU 密集 → multiprocessing；简单 I/O → threading

---

## 📚 References
- [Python Docs — asyncio](https://docs.python.org/3/library/asyncio.html)
- [Real Python — Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/)
- [FastAPI — Why asyncio matters for web frameworks](https://fastapi.tiangolo.com/async/)

---

## 🧒 ELI5
`asyncio` 就像一个聪明的厨师：不等第一道菜烤好才开始切第二道菜，而是放进烤箱后就去做别的，烤箱响了再回来。`await` 就是"放进烤箱，先去干别的"这个动作。
*`asyncio` is like a smart chef: instead of standing and staring at the oven, they put dish 1 in the oven (`await`), then start chopping for dish 2. When the oven beeps, they come back. `await` = "start something slow, go do other work."*
