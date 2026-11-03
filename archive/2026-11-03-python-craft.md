# 🐍 Python Craft — Day 146 (Synthesis)
**深入 Python 异步 I/O：从 select() 到 asyncio 的演进**
**Python Async I/O Deep Dive: From select() to asyncio — What's Actually Happening**

---

## 🎯 你在做一个高并发 Python 服务，遇到瓶颈了 / Real Scenario

你有一个 FastAPI 服务，需要同时处理 1000 个 WebSocket 连接。用 threading？每个线程 ~8MB 栈，1000 线程 = 8GB RAM。用 asyncio？单线程处理 1000 连接，内存几十 MB。

**但 asyncio 到底是怎么工作的？**

---

## 🏗️ 从 OS 层往上看 / From OS Primitives Up

### Layer 1: OS — select/poll/epoll

```python
import select
import socket

# 老方法：select() — O(n) 扫描所有 fd
# Linux 内核的 epoll — O(1)，现代 asyncio 的底层
rlist, wlist, xlist = select.select(
    [sock1, sock2, sock3],  # 监听可读
    [],                      # 监听可写
    [],                      # 监听异常
    timeout=1.0              # 超时
)
# → 返回已经就绪的 socket，而不是阻塞等待
```

**epoll 的关键 / epoll key insight:**
- `select`: 每次调用都要把整个 fd 列表传给内核 → O(n)
- `epoll`: 内核维护一个就绪列表，你只需要问"谁好了？" → O(1)

---

### Layer 2: asyncio Event Loop — 封装了 epoll

```python
import asyncio
import selectors
import concurrent.futures

# asyncio 的核心循环（简化版）/ Simplified event loop internals
class SimpleEventLoop:
    def __init__(self):
        self._ready = []      # ready-to-run callbacks
        self._selector = selectors.DefaultSelector()  # epoll on Linux
    
    def run_forever(self):
        while True:
            # 1. 执行所有已就绪的 callbacks
            for callback in self._ready:
                callback()
            self._ready.clear()
            
            # 2. 等待 I/O 事件（epoll_wait）
            events = self._selector.select(timeout=0.001)
            
            # 3. 把就绪的 I/O 事件转换为 callbacks
            for key, mask in events:
                callback = key.data
                self._ready.append(callback)
```

---

### Layer 3: Coroutines — 用户态的协作式调度

```python
import asyncio
import time

async def fetch_user(user_id: int) -> dict:
    print(f"[{time.time():.2f}] 开始获取用户 {user_id}")
    await asyncio.sleep(1)  # ← yields control back to Event Loop
    print(f"[{time.time():.2f}] 完成获取用户 {user_id}")
    return {"id": user_id, "name": f"user_{user_id}"}

async def main():
    # 串行: 3 秒 / Serial: 3s
    # for uid in [1, 2, 3]:
    #     await fetch_user(uid)
    
    # 并发: ~1 秒！/ Concurrent: ~1s!
    results = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )
    print(results)

asyncio.run(main())
```

**输出 / Output:**
```
[0.00] 开始获取用户 1
[0.00] 开始获取用户 2  ← 几乎同时开始 / nearly simultaneous
[0.00] 开始获取用户 3
[1.00] 完成获取用户 1
[1.00] 完成获取用户 2
[1.00] 完成获取用户 3
Total: ~1s instead of 3s ✅
```

---

## ⚠️ 陷阱：什么时候 asyncio 没用 / When asyncio Fails You

```python
import asyncio
import concurrent.futures

async def cpu_bound_task():
    # ❌ 这个会阻塞整个 Event Loop！
    # This BLOCKS the event loop — no other coroutines can run
    result = sum(range(10_000_000))  # CPU-intensive
    return result

def cpu_bound_task_sync():
    return sum(range(10_000_000))

# ✅ 正确做法：把 CPU 密集型扔到 ProcessPoolExecutor
async def main_correct():
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        # run_in_executor releases the GIL and runs in separate process
        r1, r2 = await asyncio.gather(
            loop.run_in_executor(pool, cpu_bound_task_sync),
            loop.run_in_executor(pool, cpu_bound_task_sync),
        )
    return r1, r2

asyncio.run(main_correct())
```

**规则 / Rule:**
- I/O 密集型 → `asyncio` + `await` ✅
- CPU 密集型 → `ProcessPoolExecutor` ✅  
- 混合 → 先找瓶颈，再选工具

---

## 🚀 生产级限流模式 / Production Semaphore Pattern

```python
import asyncio
import aiohttp

async def fetch_all_with_limit(urls: list[str], concurrency: int = 10):
    semaphore = asyncio.Semaphore(concurrency)  # max 10 concurrent
    
    async def fetch_one(url: str):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return await resp.json()
    
    return await asyncio.gather(*[fetch_one(url) for url in urls])

# pip install aiohttp
```

---

## 🔑 核心对比综合 / Key Concepts Summary

| 概念 | 本质 |
|------|------|
| `async def` | 返回 coroutine 对象，还没执行 |
| `await` | 交出控制权，等 I/O 完成后恢复 |
| Event Loop | 单线程调度器，底层是 epoll |
| `asyncio.gather` | 并发启动多个 coroutine |
| `Semaphore` | 限制最大并发数，防止资源耗尽 |
| GIL | asyncio 不受 GIL 影响（单线程），CPU 密集型仍受限 |

---

## 📚 References

1. [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
2. [How the heck does async/await work in Python — Brett Cannon](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/)
3. [Python Concurrency: asyncio vs threading — RealPython](https://realpython.com/python-concurrency/)

---

## 🧒 ELI5

想象一个厨师（Event Loop）同时管理 10 个锅。
他不是同时用 10 只手，而是：把一个菜放锅里开火，然后去处理别的锅，等锅里的菜发出"嘟嘟声"（I/O 完成），他再回来翻炒。
`await` 就是那个"把菜放锅里然后去忙别的"的动作。
CPU 密集型相当于厨师必须站在锅旁不停搅拌——这时候就需要多请一个厨师（ProcessPoolExecutor）。
