# 🐍 Python Craft — Day 129 (Synthesis)

**异步 + 并发综合实战：构建高吞吐量的任务调度器**
**Async + Concurrency Synthesis: Building a High-Throughput Task Scheduler**

*综合 asyncio、线程池、进程池的核心知识，解决实际工程问题*

---

## 🎯 场景 / Scenario

你需要构建一个任务调度器，同时处理：
- **IO密集型任务**：HTTP 请求、数据库查询（asyncio 最优）
- **CPU密集型任务**：图像处理、数据压缩（multiprocessing 最优）
- **混合任务**：读文件后压缩（需要结合两者）

*Build a task scheduler handling IO-bound (HTTP/DB), CPU-bound (compression/image processing), and mixed tasks — each requires a different concurrency primitive.*

---

## 🏗️ 架构设计 / Architecture

```
TaskScheduler
├── asyncio event loop          (IO tasks)
├── ThreadPoolExecutor          (blocking IO, legacy code)
└── ProcessPoolExecutor         (CPU tasks)
```

---

## 💻 完整实现 / Full Implementation

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable


class TaskType(Enum):
    IO = "io"           # pure async
    BLOCKING_IO = "blocking_io"   # thread pool
    CPU = "cpu"         # process pool


@dataclass
class Task:
    name: str
    task_type: TaskType
    fn: Callable
    args: tuple = ()


class HybridScheduler:
    def __init__(self, max_workers: int = 4):
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=max_workers)
        self._results: dict[str, Any] = {}

    async def run(self, tasks: list[Task]) -> dict[str, Any]:
        """Run all tasks concurrently, routing each to the right executor."""
        coros = [self._dispatch(task) for task in tasks]
        results = await asyncio.gather(*coros, return_exceptions=True)
        return dict(zip([t.name for t in tasks], results))

    async def _dispatch(self, task: Task) -> Any:
        loop = asyncio.get_running_loop()
        match task.task_type:
            case TaskType.IO:
                # Native coroutine — runs directly in event loop
                return await task.fn(*task.args)
            case TaskType.BLOCKING_IO:
                # Offload to thread pool (avoids blocking event loop)
                return await loop.run_in_executor(
                    self.thread_pool, task.fn, *task.args
                )
            case TaskType.CPU:
                # Offload to process pool (bypasses GIL)
                return await loop.run_in_executor(
                    self.process_pool, task.fn, *task.args
                )

    def __del__(self):
        self.thread_pool.shutdown(wait=False)
        self.process_pool.shutdown(wait=False)


# --- Example usage ---

async def fetch_url(url: str) -> str:
    """Simulated async HTTP call."""
    await asyncio.sleep(0.1)  # real: aiohttp.get(url)
    return f"fetched: {url}"

def compress_data(data: bytes) -> int:
    """CPU-bound: simulate compression work."""
    time.sleep(0.2)  # real: zlib.compress(data)
    return len(data)

def read_from_legacy_db(query: str) -> list:
    """Blocking IO — legacy sync DB driver."""
    time.sleep(0.05)
    return [{"id": 1, "query": query}]


async def main():
    scheduler = HybridScheduler(max_workers=4)

    tasks = [
        Task("fetch_1", TaskType.IO, fetch_url, ("https://api.example.com/1",)),
        Task("fetch_2", TaskType.IO, fetch_url, ("https://api.example.com/2",)),
        Task("compress", TaskType.CPU, compress_data, (b"x" * 1000,)),
        Task("db_query", TaskType.BLOCKING_IO, read_from_legacy_db, ("SELECT 1",)),
    ]

    start = time.time()
    results = await scheduler.run(tasks)
    elapsed = time.time() - start

    for name, result in results.items():
        print(f"{name}: {result}")
    print(f"\nTotal: {elapsed:.2f}s (sequential would be ~0.45s)")


asyncio.run(main())
```

**输出示例**:
```
fetch_1: fetched: https://api.example.com/1
fetch_2: fetched: https://api.example.com/2
compress: 1000
db_query: [{'id': 1, 'query': 'SELECT 1'}]

Total: 0.21s (sequential would be ~0.45s)
```

---

## 🔑 关键洞察 / Key Insights

| 任务类型 | 使用 | 原因 |
|---------|------|------|
| async IO (aiohttp) | `await coroutine` | 不阻塞事件循环 |
| 同步阻塞IO | `run_in_executor(thread_pool)` | 线程解放事件循环，GIL不影响IO |
| CPU密集 | `run_in_executor(process_pool)` | 独立进程绕过GIL |
| 混合任务 | 先 process_pool，再 await IO | 分阶段路由 |

**最常见的错误**: 在 asyncio 事件循环里直接调用阻塞函数（`requests.get`），导致整个事件循环卡死。

---

## 📚 References
- [asyncio docs — Running in executors](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)
- [Python Concurrency: asyncio vs threading vs multiprocessing](https://realpython.com/python-concurrency/)
- [asyncio Patterns — Lynn Root](https://www.roguelynn.com/words/asyncio-we-did-it-wrong/)

---

## 🧒 ELI5
你有三种工人：闪电侠（asyncio，等待很多事情但不累）、普通工人开多个窗口（线程，阻塞IO）、克隆人（多进程，CPU重活）。聪明的调度器知道派哪种工人干哪种活。

*You have 3 worker types: The Flash (asyncio, waits on many things effortlessly), workers in separate booths (threads, blocking IO), and clones (processes, CPU-heavy). A smart scheduler knows who to send for what job.*
