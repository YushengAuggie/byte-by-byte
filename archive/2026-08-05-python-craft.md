# 🎨 前端 / Python Craft — Day 108

## WebSocket Server — Simple Implementation

> Week 12 · Networking & APIs · Expert Level

---

## 🎯 真实场景 / Real Scenario

你在构建一个实时协作工具（想想 Figma、Google Docs、或者实时交易面板）。HTTP 的请求-响应模式不够用了 — 你需要服务器**主动推送**数据给客户端，不是客户端不停轮询。

You're building a real-time collaborative tool (think Figma, live trading dashboard, or multiplayer game). HTTP request-response doesn't cut it — you need the server to **push data proactively**, not have clients poll every second.

---

## 📡 WebSocket 是什么 / What is WebSocket

```
HTTP:  Client → Request → Server → Response → Connection closed
       (每次都要重新握手)

WS:    Client → Upgrade Request → Server → 101 Switching Protocols
       ════════════ Persistent Bidirectional Channel ════════════
       Client ←→ Server  (随时互发消息，低延迟)
```

**关键**：WebSocket 是在 HTTP 握手后升级的持久 TCP 连接。一次握手，永久双向通道。

---

## 🐍 简单实现 / Simple Implementation

### 方法一：用 `websockets` 库 (推荐)

```python
# pip install websockets
import asyncio
import websockets
import json
from datetime import datetime

# Connected clients registry
connected_clients: set[websockets.WebSocketServerProtocol] = set()

async def broadcast(message: str):
    """Send message to all connected clients"""
    if connected_clients:
        # asyncio.gather sends to all concurrently
        await asyncio.gather(
            *[client.send(message) for client in connected_clients],
            return_exceptions=True  # don't fail if one client disconnects
        )

async def handler(websocket: websockets.WebSocketServerProtocol):
    """Handle a single WebSocket connection lifecycle"""
    client_id = id(websocket)
    connected_clients.add(websocket)
    print(f"✅ Client {client_id} connected. Total: {len(connected_clients)}")
    
    try:
        # Notify everyone of new connection
        await broadcast(json.dumps({
            "type": "system",
            "msg": f"User {client_id} joined",
            "time": datetime.now().isoformat()
        }))
        
        # Listen for messages from this client
        async for raw_message in websocket:
            data = json.loads(raw_message)
            print(f"📨 From {client_id}: {data}")
            
            # Echo back to all clients (simple chat relay)
            await broadcast(json.dumps({
                "type": "message",
                "from": client_id,
                "body": data.get("body", ""),
                "time": datetime.now().isoformat()
            }))
    
    except websockets.exceptions.ConnectionClosed as e:
        print(f"⚠️  Client {client_id} disconnected: {e.code}")
    finally:
        connected_clients.discard(websocket)
        await broadcast(json.dumps({
            "type": "system",
            "msg": f"User {client_id} left"
        }))

async def main():
    # Start WebSocket server on port 8765
    async with websockets.serve(handler, "localhost", 8765):
        print("🚀 WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
```

### 测试客户端 / Test Client

```python
# pip install websockets
import asyncio
import websockets
import json

async def client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as ws:
        # Send a message
        await ws.send(json.dumps({"body": "Hello from client!"}))
        
        # Listen for responses
        async for message in ws:
            data = json.loads(message)
            print(f"Received: {data}")

asyncio.run(client())
```

---

## ⚡ 生产级要点 / Production Considerations

```python
# ❌ 新手错误：不处理断线重连
async for msg in websocket:
    process(msg)  # 如果断了就抛异常，连接丢失

# ✅ 正确：用 ping/pong 保活 + 异常处理
async with websockets.serve(
    handler,
    "localhost", 8765,
    ping_interval=20,     # 每20s发ping
    ping_timeout=10,      # 10s没收到pong就断开
    max_size=1_048_576,   # 限制消息大小 1MB
):
    ...
```

---

## 🔄 WebSocket vs SSE vs Long Polling

| | WebSocket | SSE | Long Polling |
|--|-----------|-----|-------------|
| 方向 | 双向 | 单向(服务器→客户端) | 单向 |
| 协议 | ws:// | HTTP | HTTP |
| 复杂度 | 中等 | 简单 | 简单 |
| 适用 | 聊天/游戏/协作 | 实时通知/feed | 简单更新 |
| 浏览器支持 | ✅ | ✅ | ✅ |

**选择原则**: 如果只需要服务器推送用 SSE，双向通信才用 WebSocket。

---

## 🏗️ 生产架构注意 / Production Architecture

```
Client → [Load Balancer]
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
  [WS Pod]  [WS Pod]  [WS Pod]
    │         │         │
    └─────[Redis Pub/Sub]─────┘
         (跨Pod广播消息)

问题: Client A 在 Pod 1，Client B 在 Pod 2
      Pod 1 直接 broadcast 只到本Pod的连接！
解决: 用 Redis Pub/Sub 做跨Pod消息传递
```

---

## 📚 References
- https://websockets.readthedocs.io/en/stable/
- https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
- https://ably.com/topic/websockets

## 🧒 ELI5
普通 HTTP 就像寄信：你写一封，对方回一封，每次都要重新写信封。WebSocket 就像打电话：接通后可以随时说话，不需要每次重拨。实时游戏、股票行情、聊天室都用"打电话"的方式。

HTTP is like mailing letters: write, wait, reply, repeat. WebSocket is like a phone call: once connected, either side can talk anytime. Real-time games, live stock prices, and chat apps all use the "phone call" approach.
