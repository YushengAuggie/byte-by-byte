🎨 **Python Craft — Synthesis**: `asyncio` Internals — What Actually Runs When You `await`

你写了 `await fetch(url)`。谁在跑？事件循环到底是什么？今天综合我们之前讲过的 **asyncio basics、gather、Semaphore、GIL、generators、context managers**，深入 CPython asyncio 的真实执行流程。

You write `await fetch(url)`. Who runs it? What *is* the event loop? Today synthesizes previously-covered asyncio basics, gather, Semaphore, GIL, generators, context managers — into one real CPython execution story.

---

### 1. `async def` 是一个 generator 的包装 / `async def` is a generator wrapper

```python
import dis

async def hello():
    x = await something()
    return x

dis.dis(hello)
# You'll see GET_AWAITABLE, SEND, YIELD_VALUE, RESUME...
```

**事实**：coroutine 底层就是 generator (PEP 492/525)。`await` 编译成 `YIELD_VALUE` + `RESUME`。`asyncio` 的事件循环就是一个 **generator driver** — 它反复 `send(None)` 直到协程 raise `StopIteration`。

Reality: coroutines compile down to generators. `await` becomes `YIELD_VALUE` + `RESUME`. The event loop is literally a generator driver that `.send(None)` repeatedly until `StopIteration`.

---

### 2. 事件循环的真实 run loop / The actual run loop

CPython `asyncio/base_events.py` 的 `_run_once()` 简化版：

```python
# cpython/Lib/asyncio/base_events.py (simplified)
def _run_once(self):
    # 1. Compute how long until the next scheduled timer
    timeout = self._compute_timeout()
    # 2. Block on OS-level selector (kqueue/epoll/iocp)
    event_list = self._selector.select(timeout)
    # 3. Dispatch ready file descriptors → mark callbacks ready
    self._process_events(event_list)
    # 4. Run all callbacks whose scheduled_time <= now
    ntodo = len(self._ready)
    for _ in range(ntodo):
        handle = self._ready.popleft()
        handle._run()         # <-- this calls coro.send(None) one step
```

**关键**：事件循环是 **单线程**。GIL 不是问题（本来就一个线程）。真正的并发来自：**I/O 阻塞交给 OS kernel (epoll)**，CPU 空出来跑别的协程。

Key: event loop is single-threaded. GIL is irrelevant (one thread). True concurrency comes from offloading I/O waits to the OS (epoll/kqueue) while the CPU runs other coroutines.

---

### 3. 一次 `await aiohttp.get(url)` 的完整生命周期

```
your coro          event loop          selector (epoll)       socket
   │─── await ────▶│                        │                   │
   │               │── register fd ────────▶│                   │
   │               │                        │                   │
   │  <── YIELDS ──│  (coroutine suspended, loop runs others)   │
   │               │                        │                   │
   │               │                        │◀── fd readable ───│
   │               │◀── event ──────────────│                   │
   │               │─ callback: _step(coro) │                   │
   │◀── RESUME ────│  via coro.send(result) │                   │
   │               │                        │                   │
   │─ return value ▶ StopIteration          │                   │
```

**可运行代码** / Runnable example — 看懂为什么 asyncio 快但不是魔法：

```bash
pip install aiohttp
```

```python
# save as asyncio_demo.py — compare serial vs concurrent I/O
import asyncio, time, aiohttp

async def fetch(session, url):
    async with session.get(url) as r:
        return len(await r.text())

async def main():
    urls = ["https://httpbin.org/delay/1"] * 10
    async with aiohttp.ClientSession() as s:
        t0 = time.perf_counter()
        # Concurrent: 10 requests ≈ 1 second (OS waits in parallel)
        results = await asyncio.gather(*(fetch(s, u) for u in urls))
        print(f"concurrent: {time.perf_counter()-t0:.2f}s, bytes={sum(results)}")

asyncio.run(main())
# concurrent: ~1.1s   (vs serial ~10s)
```

---

### 4. 常见陷阱的内部原因 / Pitfalls — Explained by Internals

| Pitfall | 内部原因 Why |
|---|---|
| `time.sleep(1)` 在协程里卡死整个循环 | `time.sleep` 是阻塞 syscall，不会 yield，事件循环拿不回控制权 |
| CPU-bound 代码不加速 | 单线程 + GIL；`await` 不会让 CPU 并行。要用 `run_in_executor` + ProcessPool |
| 忘记 `await` 一个 coroutine，静默不执行 | coroutine 是 lazy generator，没人 drive 它就永远不跑。Python 3.11+ 会给 `RuntimeWarning` |
| `asyncio.gather` 中一个失败全失败 | 默认 `return_exceptions=False`；要容错传 `True` |
| 用 `requests` 替代 `aiohttp` | `requests` 是 blocking 的，不管你 `async def` 包多少层都阻塞 loop |

---

### 5. Senior takeaway

**何时该用 asyncio**：I/O-bound、>100 并发连接、WebSocket/SSE、API gateway、爬虫。
**何时别用**：CPU-bound (用 `multiprocessing`)、简单脚本 (`threading` 更易懂)、生态不支持 (比如老 ORM)。

**调试神器**：
- `asyncio.get_event_loop().set_debug(True)` → 慢 callback 警告
- `PYTHONASYNCIODEBUG=1` 环境变量
- `asyncio.all_tasks()` → 看谁 pending 没完成
- `aiomonitor` → 远程 inspect 事件循环

---

### 📚 References
- PEP 492 — `async`/`await`: https://peps.python.org/pep-0492/
- CPython `asyncio` source: https://github.com/python/cpython/tree/main/Lib/asyncio
- David Beazley, "Build Your Own Async": https://www.dabeaz.com/talks.html

### 🧒 ELI5
协程像可以"按暂停"的函数。事件循环是一个负责按暂停和播放按钮的小管家。当你要等快递 (I/O)，小管家按暂停让你坐一边，去跑其他函数；快递到了再按播放让你继续。全程只有一个小管家 (单线程)，但同时能"照看"几百件事情，因为真正等待的工作交给了操作系统。
