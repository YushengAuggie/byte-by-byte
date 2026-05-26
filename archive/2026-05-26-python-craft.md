# 🐍 Python Craft — Day 5
**Topic:** WSGI/ASGI — How Web Servers Handle Requests
**Date:** 2026-05-26 | **Phase:** Expert | **Category:** Concurrency & Parallelism

---

## 🎨 Python Craft — WSGI/ASGI: Web 服务器如何处理请求
**⏱️ 预计阅读时间 / Estimated reading time: 2 min**

---

### 真实场景 / Real Scenario

你在生产环境用 Nginx + Gunicorn + Django 部署了一个 API。面试官问："收到一个 HTTP 请求，从 Nginx 到你的 Django view 函数，中间发生了什么？"

You deploy Nginx + Gunicorn + FastAPI. The interviewer asks: "What happens between the HTTP request arriving at Nginx and your view function executing?"

---

### WSGI：同步时代的标准

```
Client → Nginx (reverse proxy) → Gunicorn (WSGI server) → Django/Flask App

WSGI 接口：一个 Python 可调用对象
  def application(environ, start_response):
      start_response('200 OK', [('Content-Type', 'text/plain')])
      return [b'Hello World']

# environ: HTTP 请求信息 (method, path, headers, body)
# start_response: 回调，设置状态码和响应头
```

**Gunicorn 工作模型：**
```
Master Process
  ├── Worker 1 (处理请求 A)
  ├── Worker 2 (处理请求 B)
  └── Worker 3 (等待)

每个 Worker = 一个 OS 进程或线程
Worker 在处理 I/O 时会 block（等数据库/文件）
→ 这就是 WSGI 的性能瓶颈
```

---

### ASGI：异步时代的标准

```
Client → Nginx → Uvicorn (ASGI server) → FastAPI/Django Channels App

ASGI 接口：
  async def application(scope, receive, send):
      # scope: connection 信息
      # receive: async 函数，接收请求体
      # send: async 函数，发送响应

# 同一个 Worker 可以同时处理多个 I/O-bound 请求
# 无需多进程/线程切换
```

**ASGI 对比 WSGI：**
```
WSGI Worker:
  请求A ──[处理]──[等DB 50ms]──[等DB 50ms]──[返回]
  请求B                                              [等待...]

ASGI Worker (async):
  请求A ──[处理]──[await DB]─────────────────[返回]
  请求B           ──[处理]──[await DB]──[返回]
```

---

### 代码示例 / Code Snippet

```python
# WSGI (Flask)
from flask import Flask
app = Flask(__name__)

@app.route('/sync')
def sync_view():
    import time
    time.sleep(0.1)  # BLOCKS the whole worker!
    return 'Done'

# ASGI (FastAPI)
from fastapi import FastAPI
import asyncio
app = FastAPI()

@app.get('/async')
async def async_view():
    await asyncio.sleep(0.1)  # yields control, other requests proceed
    return {'status': 'done'}

# Run:
# WSGI: gunicorn app:app -w 4
# ASGI: uvicorn app:app --workers 4
```

---

### ❌ 常见误区 vs ✅ 正确理解

❌ **"FastAPI 一定比 Flask 快"**
✅ FastAPI 在 **I/O-bound** 场景（数据库查询、HTTP 调用）下快得多。CPU-bound 场景（图片处理、加密）下区别不大，因为 asyncio 不能突破 GIL。

❌ **"用了 async/await 就是 ASGI"**
✅ 必须用 ASGI server（Uvicorn/Daphne）运行，用 Gunicorn 运行 FastAPI 会退化成 WSGI 模式。

---

### 何时用哪个 / When to Use

| 场景 | 推荐 |
|------|------|
| 大量数据库查询 / 外部 API 调用 | ASGI + FastAPI |
| WebSocket / SSE / 长连接 | 必须用 ASGI |
| 纯 CPU 计算（ML inference）| WSGI + Gunicorn + multiprocessing |
| 已有大型 Django 项目 | Django + Gunicorn（或迁移到 ASGI channels）|

---

### 📚 References
- [PEP 3333 — Python WSGI Spec](https://peps.python.org/pep-3333/)
- [ASGI Spec](https://asgi.readthedocs.io/en/latest/)
- [Uvicorn Performance](https://www.uvicorn.org/deployment/)
- [FastAPI docs — Concurrency](https://fastapi.tiangolo.com/async/)

### 🧒 ELI5
WSGI 就像一个收银台——同时只能服务一个顾客，别人排队等。ASGI 就像手机点餐系统——你下单后服务员去做其他事，做好了叫号通知你，一个人能同时服务很多桌。
