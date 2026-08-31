# 🎨 Python Craft — Day 122 (Synthesis)
**asyncio + Redis Pub/Sub：构建实时通知系统的内核**
**asyncio + Redis Pub/Sub: The Core of a Real-Time Notification System**

---

## 你在做一个 dashboard，需要...

实时推送通知给多个连接的 WebSocket 客户端，后端事件来自多个微服务。
这是 Day 48（asyncio 基础）+ Day 51（Python Web 服务器）+ Day 32（设计聊天系统）的交汇点。

---

## 问题：为什么不用线程？

```python
# ❌ 这样做：每个 WebSocket 连接一个线程
# 1000 个连接 = 1000 个线程 = ~1GB 内存 + GIL 争抢
import threading
def handle_ws(conn):
    while True:
        msg = conn.recv()
        broadcast(msg)

# ✅ asyncio：1000 个连接共享一个线程
# event loop 处理 I/O 等待，协程在等待时让出控制权
```

---

## 完整实现：asyncio + aioredis Pub/Sub

```python
import asyncio
import json
import aioredis
from typing import Set

# Global set of connected WebSocket queues
# Each connected client gets one asyncio.Queue
connected_clients: Set[asyncio.Queue] = set()

async def redis_listener(redis_url: str):
    """Subscribe to Redis channel and broadcast to all WebSocket clients."""
    redis = await aioredis.from_url(redis_url)
    pubsub = redis.pubsub()
    await pubsub.subscribe("notifications")
    
    async for message in pubsub.listen():
        if message["type"] != "message":
            continue
        payload = message["data"].decode()
        # Fan-out: send to every connected client's queue
        dead_clients = set()
        for queue in connected_clients:
            try:
                queue.put_nowait(payload)
            except asyncio.QueueFull:
                dead_clients.add(queue)  # slow/disconnected client
        connected_clients -= dead_clients  # cleanup

async def websocket_handler(websocket):
    """Handle one WebSocket connection."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=100)
    connected_clients.add(queue)
    try:
        while True:
            # Wait for a message from Redis fan-out
            msg = await asyncio.wait_for(queue.get(), timeout=30)
            await websocket.send(msg)
    except (asyncio.TimeoutError, ConnectionError):
        pass  # client disconnected or timed out
    finally:
        connected_clients.discard(queue)

async def publisher_example(redis_url: str):
    """Simulate a microservice publishing an event."""
    redis = await aioredis.from_url(redis_url)
    event = json.dumps({"type": "order_shipped", "order_id": "abc123"})
    await redis.publish("notifications", event)
    await redis.aclose()

# Run everything on the same event loop
async def main():
    await asyncio.gather(
        redis_listener("redis://localhost:6379"),
        # websocket_handler(ws) would be added per connection
    )
```

---

## 关键 asyncio 模式解析

```
asyncio.Queue(maxsize=100)
  → 背压控制：队列满了就丢弃（慢客户端不拖累快客户端）
  → 每个客户端独立队列 → 互相隔离

asyncio.wait_for(queue.get(), timeout=30)
  → 30 秒无消息 → 发 ping 或断开
  → 避免僵尸连接积累

asyncio.gather(redis_listener, ...)
  → 并发运行多个协程（不是并行！）
  → event loop 在 await 点切换
```

---

## 常见坑 ⚠️

**坑 1：在 async 函数里调用 time.sleep()**
```python
# ❌ 阻塞整个 event loop！
async def bad():
    time.sleep(1)  # blocks all coroutines

# ✅
async def good():
    await asyncio.sleep(1)  # yields control
```

**坑 2：线程安全问题**
asyncio 不是线程安全的。如果你用 `threading` 和 `asyncio` 混用：
```python
# ❌ 从线程写 asyncio Queue
queue.put_nowait(item)  # not safe from another thread

# ✅
loop.call_soon_threadsafe(queue.put_nowait, item)
```

---

## 性能数字参考

| 方案 | 10K 连接内存 | CPU |
|------|------------|-----|
| Thread-per-conn | ~10 GB | 高（上下文切换） |
| asyncio | ~50 MB | 低（单线程 I/O） |
| asyncio + uvloop | ~50 MB | 更低（C 实现 event loop） |

---

## 📚 References
- [aioredis Docs — Pub/Sub](https://aioredis.readthedocs.io/en/latest/examples/pubsub/)
- [asyncio Queues — Python Docs](https://docs.python.org/3/library/asyncio-queue.html)
- [uvloop — Drop-in Faster Event Loop](https://github.com/MagicStack/uvloop)

## 🧒 ELI5
想象一个邮递员（Redis）把信送到大楼前台，前台（asyncio event loop）再把信分发给各个房间（WebSocket 客户端）。线程方案相当于每个房间派一个专职员工等待，很浪费；asyncio 相当于一个前台同时服务所有房间，有信才去敲门。
