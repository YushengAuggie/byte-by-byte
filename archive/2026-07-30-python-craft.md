# 🐍 Python Craft — Day 44 (Expert)
**Date:** 2026-07-30 | **Topic:** HTTP Internals — What Happens in requests.get()
**Category:** Networking & APIs | **Week 11**

---

## 场景 / Scenario

你在做一个后端服务，调用第三方 API：

```python
import requests
response = requests.get("https://api.example.com/data")
```

这一行背后发生了什么？面试官问你 HTTP 调用慢，你从哪里开始排查？

You call an external API. It's slow. Where do you even begin debugging? Understanding what `requests.get()` actually does is essential for backend engineers.

---

## 完整调用链 / The Full Call Stack

```
requests.get(url)
    ↓
1. DNS 解析 (DNS Resolution)
   → OS 查 /etc/hosts → 本地 DNS 缓存 → 递归 DNS 查询
   → 返回 IP 地址（可缓存）

2. TCP 握手 (TCP Handshake)  [~1 RTT]
   → SYN → SYN-ACK → ACK
   → 建立连接（有状态，有成本）

3. TLS 握手 (TLS Handshake)  [~1-2 RTT]
   → Client Hello → Server Hello + Certificate
   → Key Exchange → Finished
   → 证书验证 + 密钥协商

4. HTTP 请求发送
   → GET /data HTTP/1.1
   → Host: api.example.com
   → User-Agent, Accept, etc.

5. 服务器处理 + 响应

6. 连接复用 / 关闭
   → Connection: keep-alive → 复用 TCP 连接
   → Connection: close → 关闭，下次重新握手
```

---

## 用 requests 暴露每一层 / Exposing Each Layer

```python
import requests
import time

# 方法1: 用 hooks 计时
def log_timing(response, *args, **kwargs):
    print(f"Elapsed: {response.elapsed.total_seconds():.3f}s")

session = requests.Session()
session.hooks['response'].append(log_timing)

# 方法2: PreparedRequest 看原始内容
req = requests.Request('GET', 'https://httpbin.org/get')
prepared = session.prepare_request(req)
print(prepared.headers)  # 看实际发出的 headers

# 方法3: response.elapsed 各阶段分解
resp = session.get('https://httpbin.org/get')
print(resp.elapsed)  # timedelta of server processing time

# 方法4: urllib3 level — 看连接池
import urllib3
urllib3.disable_warnings()
http = urllib3.PoolManager()
r = http.request('GET', 'https://httpbin.org/get')
# PoolManager 自动复用连接，减少握手开销
```

---

## 性能优化实战 / Production Optimizations

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ✅ Session 复用 TCP 连接（最重要！）
session = requests.Session()

# ✅ 连接池配置
adapter = HTTPAdapter(
    pool_connections=10,   # 连接池数量（per host）
    pool_maxsize=20,       # 每个 host 最多多少连接
    max_retries=Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504]
    )
)
session.mount('https://', adapter)
session.mount('http://', adapter)

# ✅ 合理超时（分开 connect 和 read）
response = session.get(
    'https://api.example.com/data',
    timeout=(3.05, 27)   # (connect_timeout, read_timeout)
)

# ❌ 不设超时 = 可能永远挂起
# requests.get(url)  # 危险！

# ❌ 每次请求新建 Session = 每次都要握手
# for url in urls:
#     requests.get(url)  # 每次 TCP+TLS，很慢
```

---

## 猜猜输出 / What Does This Print?

```python
import requests

s1 = requests.Session()
s2 = requests.Session()

r1 = s1.get("https://httpbin.org/get")
r2 = s1.get("https://httpbin.org/get")  # Same session
r3 = s2.get("https://httpbin.org/get")  # Different session

print(r1.elapsed > r2.elapsed)  # A: True  B: False  C: 不一定
```

**答案 / Answer: A — True（大概率）**  
`r1` 需要建立新连接（DNS+TCP+TLS），`r2` 复用已有连接，所以 `r1.elapsed > r2.elapsed`。`r3` 又是新连接，所以也比 r2 慢。

---

## ❌ vs ✅ 常见错误 / Common Mistakes

```python
# ❌ 在循环里每次都创建新 session
for item in items:
    r = requests.get(url)  # 每次握手，N 倍延迟

# ✅ Session 提取到循环外
session = requests.Session()
for item in items:
    r = session.get(url)   # 复用连接，快很多

# ❌ 不处理超时
r = requests.get(url)

# ✅ 总是设置超时
r = requests.get(url, timeout=(3, 10))

# ❌ 手动实现重试
for _ in range(3):
    try:
        r = session.get(url)
        break
    except Exception:
        pass

# ✅ 用 urllib3 的 Retry 配置
# （上面的 HTTPAdapter 例子）
```

---

## 排查慢 HTTP 调用的思路 / Debugging Slow HTTP

```
慢在哪？
├── DNS 慢？→ dig/nslookup 测，考虑 DNS 缓存或 /etc/hosts
├── TCP 连接慢？→ 是否跨地区？连接池是否满了？
├── TLS 慢？→ 考虑 TLS session resumption，HTTP/2
├── 服务器处理慢？→ 看 response.elapsed，加 tracing
└── 读取慢？→ 响应体大，考虑流式读取 stream=True
```

---

## 🧒 ELI5
`requests.get()` 就像打电话：先查电话簿（DNS），拨号建立连接（TCP），说暗号确认是对的人（TLS），然后才能说话（HTTP）。Session 就是保持线路畅通，不挂电话，下次直接说话。  
`requests.get()` is like making a call: look up the number (DNS), dial and connect (TCP), verify identity (TLS), then talk (HTTP). A Session keeps the line open so you skip the first three steps next time.

---

## 📚 References
- [requests docs — Advanced Usage](https://docs.python-requests.org/en/latest/user/advanced/)
- [urllib3 Connection Pooling](https://urllib3.readthedocs.io/en/stable/advanced-usage.html#customizing-pool-behavior)
- [HTTP/1.1 vs HTTP/2 vs HTTP/3 — High Performance Browser Networking](https://hpbn.co/)
- [Everything You Need to Know About TLS — Cloudflare Blog](https://blog.cloudflare.com/tls-1-3-overview-and-q-and-a/)
