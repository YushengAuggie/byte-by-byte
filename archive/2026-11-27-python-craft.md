# 🐍 Python Craft — Day 159 (Synthesis)
**主题 / Topic:** Python 底层串讲：从 GIL 到 asyncio 到内存——用一个并发服务器把所有碎片拼起来

---

## 场景：你被要求用纯 Python 写一个高并发 HTTP 服务器

这是一道经典面试问题，也是把我们学过的 Python 内功串起来的绝佳场景。

---

## 知识图谱回顾

```
我们学过的 Python 并发工具：
                    
  threading ──────────────┐
  (Day 1, GIL-bound)      │
                           ▼
  multiprocessing ────── 什么时候用哪个？
  (Day 2, CPU-bound)      │
                           ▼
  asyncio ──────────────── 底层：单线程 event loop
  (Day 3-4, I/O-bound)    │
                           ▼
  concurrent.futures ───── 统一接口（Thread/ProcessPool）
  (Day 7)                 
```

**今天的问题：写一个能处理 10,000 并发连接的 HTTP 服务器**

---

## 三种实现，三种权衡

### 实现 1：threading（❌ 不适合）

```python
import threading, socket

def handle_client(conn):
    data = conn.recv(1024)
    conn.send(b"HTTP/1.1 200 OK\r\n\r\nHello")
    conn.close()

server = socket.socket()
server.bind(('', 8080))
server.listen()

while True:
    conn, _ = server.accept()
    t = threading.Thread(target=handle_client, args=(conn,))
    t.start()
    # 10,000 个连接 = 10,000 个线程 = 崩溃 💥
    # 每个线程 ~8MB stack → 80GB RAM...
```

**GIL 复习：** I/O 时会释放 GIL，所以线程在 I/O 密集型场景下"能用"——但内存是致命的。

---

### 实现 2：asyncio（✅ 正确选择）

```python
import asyncio

async def handle_client(reader, writer):
    data = await reader.read(1024)          # 非阻塞 I/O，让出 event loop
    writer.write(b"HTTP/1.1 200 OK\r\n\r\nHello")
    await writer.drain()                    # 等待缓冲区清空
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8080)
    async with server:
        await server.serve_forever()

asyncio.run(main())
# 10,000 个连接 → 10,000 个 coroutine（每个仅几 KB）✅
```

**核心洞察 / Key Insight:**
```
线程模型：一个连接 = 一个线程（系统资源）
协程模型：一个连接 = 一个协程（Python 对象，~2KB）
```

---

### 实现 3：混合模式（CPU 密集型任务怎么办？）

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

executor = ProcessPoolExecutor(max_workers=4)  # CPU 核心数

async def handle_request(reader, writer):
    data = await reader.read(1024)
    
    if b"compress" in data:
        # CPU 密集型：丢到进程池，不阻塞 event loop
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, compress_data, data)
    else:
        result = b"HTTP/1.1 200 OK\r\n\r\nHello"
    
    writer.write(result)
    await writer.drain()
```

---

## 内存模型串讲

```python
import tracemalloc, asyncio

tracemalloc.start()

async def coroutine_overhead():
    """测量协程的内存开销"""
    tasks = [asyncio.create_task(asyncio.sleep(1)) for _ in range(10000)]
    snapshot = tracemalloc.take_snapshot()
    top = snapshot.statistics('lineno')
    print(f"Top memory: {top[0].size / 1024:.1f} KB for 10K tasks")
    for t in tasks:
        t.cancel()

asyncio.run(coroutine_overhead())
# 输出约：~5MB for 10K tasks（每个协程 ~500 bytes）
```

---

## 生产级注意事项

```python
# 1. Graceful shutdown（我们学过的 Signal handling）
import signal

def shutdown():
    loop.stop()

loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGTERM, shutdown)

# 2. Connection limiting（Semaphore pattern）
semaphore = asyncio.Semaphore(1000)  # 最多 1000 并发

async def limited_handler(reader, writer):
    async with semaphore:
        await handle_client(reader, writer)

# 3. 超时保护
async def handle_with_timeout(reader, writer):
    try:
        await asyncio.wait_for(handle_client(reader, writer), timeout=30.0)
    except asyncio.TimeoutError:
        writer.close()
```

---

## 决策树 / When to Use What

```
任务类型？
├── I/O 密集（网络/文件/DB）
│   ├── 高并发 (>1000) → asyncio ✅
│   └── 低并发，代码简单 → threading ✅
├── CPU 密集（数学/压缩/加密）
│   └── multiprocessing / ProcessPoolExecutor ✅
└── 两者混合
    └── asyncio + run_in_executor ✅
```

---

## 📚 References
- https://docs.python.org/3/library/asyncio.html
- https://realpython.com/async-io-python/
- https://docs.python.org/3/library/concurrent.futures.html

## 🧒 ELI5
想象一个服务员（单线程 asyncio）vs. 10,000 个服务员（线程）。一个超级服务员记住所有桌子在等什么，趁等厨房的时间去服务其他桌——效率远高于雇 10,000 个服务员（工资/内存太高）。这就是 async 的核心思想。
