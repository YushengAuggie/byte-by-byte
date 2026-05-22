# 🐍 Python Craft — Day 49

**主题 / Topic:** asyncio Patterns — gather, Semaphore, Queue  
**类别 / Category:** Concurrency & Parallelism (Week 1, Day 4)

---

## 真实场景 / Real Scenario

你在写一个爬虫，需要并发抓取 1000 个 URL。直接 `asyncio.gather(*all_1000_tasks)` 会在 0.1 秒内发出 1000 个请求 — 立刻触发对方服务器的限流，或者让你自己的网络连接耗尽。  

You're writing a scraper to fetch 1000 URLs concurrently. Naively doing `asyncio.gather(*all_1000_tasks)` fires 1000 requests in 0.1 seconds — instantly triggering rate limits or exhausting your own connection pool.

**解决方案：** `asyncio.Semaphore` + `asyncio.Queue`

---

## 核心模式 / Core Patterns

### 1. `asyncio.gather` — 并发等待多个协程

```python
import asyncio

async def fetch(url: str) -> str:
    await asyncio.sleep(0.1)  # simulate network I/O
    return f"result from {url}"

async def main():
    urls = ["url1", "url2", "url3"]
    
    # Run all concurrently, wait for ALL to finish
    results = await asyncio.gather(*[fetch(u) for u in urls])
    # returns list in same order as inputs
    print(results)  # ['result from url1', 'result from url2', 'result from url3']
    
    # Handle individual errors without cancelling others
    results = await asyncio.gather(
        *[fetch(u) for u in urls],
        return_exceptions=True  # exceptions become results, not raised
    )

asyncio.run(main())
```

---

### 2. `asyncio.Semaphore` — 限制并发数（生产关键！）

```python
import asyncio
import aiohttp

async def fetch_with_limit(session, url, semaphore):
    async with semaphore:  # acquire → run → release
        async with session.get(url) as resp:
            return await resp.text()

async def crawl(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)  # max 10 at a time
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_limit(session, url, semaphore) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

# pip install aiohttp
# asyncio.run(crawl(urls, max_concurrent=10))
```

**Semaphore 工作原理：** 内部有一个计数器（初始=max_concurrent）。每次 `async with semaphore` 将计数器减 1；如果计数器为 0，新任务等待；任务完成后计数器加 1，唤醒等待者。

---

### 3. `asyncio.Queue` — 生产者消费者模式

```python
import asyncio

async def producer(queue: asyncio.Queue, items: list):
    for item in items:
        await queue.put(item)  # blocks if queue is full
    
    # Signal workers to stop
    for _ in range(NUM_WORKERS := 3):
        await queue.put(None)  # sentinel value

async def worker(queue: asyncio.Queue, worker_id: int):
    while True:
        item = await queue.get()  # blocks if queue is empty
        if item is None:
            break  # received sentinel, stop
        
        # Process item
        await asyncio.sleep(0.1)  # simulate work
        print(f"Worker {worker_id} processed: {item}")
        queue.task_done()  # mark item as done

async def main():
    queue = asyncio.Queue(maxsize=100)  # bounded queue
    NUM_WORKERS = 3
    
    # Start workers
    workers = [asyncio.create_task(worker(queue, i)) for i in range(NUM_WORKERS)]
    
    # Run producer
    await producer(queue, list(range(10)))
    
    # Wait for workers to finish
    await asyncio.gather(*workers)

asyncio.run(main())
```

---

## ❌ vs ✅ 常见错误 / Common Mistakes

```python
# ❌ 无限制并发 — 可能耗尽资源
results = await asyncio.gather(*[fetch(url) for url in huge_list])

# ✅ 用 Semaphore 限速
sem = asyncio.Semaphore(50)
async def bounded_fetch(url):
    async with sem:
        return await fetch(url)
results = await asyncio.gather(*[bounded_fetch(url) for url in huge_list])

# ❌ 在 async 函数中用 time.sleep（会阻塞整个 event loop！）
async def bad():
    time.sleep(1)  # blocks event loop, nothing else runs

# ✅ 用 asyncio.sleep
async def good():
    await asyncio.sleep(1)  # yields control, other tasks can run
```

---

## 何时用哪个 / When to Use What

| 场景 | 工具 |
|------|------|
| 并发执行固定数量任务 | `asyncio.gather` |
| 限制同时运行的任务数 | `asyncio.Semaphore` |
| 解耦生产者和消费者速率 | `asyncio.Queue` |
| 一个任务失败不影响其他 | `gather(return_exceptions=True)` |

---

## 📚 References
- [Python asyncio docs — Synchronization Primitives](https://docs.python.org/3/library/asyncio-sync.html)
- [Real Python — Async IO in Python](https://realpython.com/async-io-python/)
- [aiohttp docs](https://docs.aiohttp.org/en/stable/)

## 🧒 ELI5
`gather` 就像让很多人同时干活。`Semaphore` 就是说"同时最多 10 个人进厕所"——限制并发数，防止挤崩。`Queue` 是一条传送带——生产者往上放东西，消费者从另一头取——两边速度不用一样。
