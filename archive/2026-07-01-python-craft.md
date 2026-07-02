# 🐍 Python Craft — Day 79
## Retry with Backoff — tenacity, 手动实现 / Manual Implementation
**Category: Practical Patterns | Week 7**
**预计阅读时间 / Est. read time: 2 min**

---

## 🌍 真实场景 / Real-World Scenario

你在做一个调用第三方 API 的服务（支付、邮件、AI 推理接口）。偶发的网络抖动或 429 Rate Limit 会让请求失败，但这不是永久性错误——重试一下就好。问题是：**怎么重试才对？**

You're calling third-party APIs (payments, email, AI inference). Flaky networks and 429s cause transient failures—retrying helps, but *how* you retry matters a lot.

**错误做法：** 立刻重试 → 打爆对方服务器 → 自己被封
**正确做法：** 指数退避 + 抖动 (Exponential Backoff + Jitter)

---

## 🔧 方案一：手动实现 / Manual Implementation

```python
import time
import random
import requests
from typing import Callable, Any

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
) -> Any:
    """
    Retry func with exponential backoff + optional jitter.
    Raises the last exception if all retries fail.
    """
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        except (requests.RequestException, TimeoutError) as e:
            last_exception = e
            
            if attempt == max_retries:
                break  # no more retries
            
            # Exponential backoff: 1s, 2s, 4s, 8s...
            delay = min(base_delay * (2 ** attempt), max_delay)
            
            # Add jitter to avoid thundering herd
            if jitter:
                delay *= (0.5 + random.random())  # delay * [0.5, 1.5]
            
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.1f}s...")
            time.sleep(delay)
    
    raise last_exception

# Usage
def call_payment_api():
    response = requests.post("https://api.stripe.com/charge", timeout=5)
    response.raise_for_status()
    return response.json()

result = retry_with_backoff(call_payment_api, max_retries=3)
```

---

## 🚀 方案二：tenacity（推荐用于生产）/ tenacity (Production Recommended)

```python
# pip install tenacity
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import requests

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    retry=retry_if_exception_type(requests.RequestException),
    reraise=True,  # re-raise the last exception on failure
)
def call_openai_api(prompt: str) -> dict:
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json={"model": "gpt-4", "messages": [{"role": "user", "content": prompt}]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

# tenacity handles: 1s → 2s → 4s backoff automatically
```

---

## ⚖️ 关键对比 / Key Comparison

| | 手动实现 | tenacity |
|--|---------|---------|
| 灵活性 | 完全可控 | 通过装饰器配置 |
| 可读性 | 需要写样板代码 | 声明式，一目了然 |
| 功能 | 基础 | before/after 钩子、统计、async 支持 |
| 适合场景 | 理解原理、极简依赖 | 生产代码 ✅ |

---

## ❌ 别这么做 / What NOT to Do

```python
# ❌ 立刻重试，无退避 — 打垮服务器
for i in range(3):
    try:
        result = call_api()
        break
    except Exception:
        pass  # 立刻再试！

# ❌ 对所有异常都重试 — 包括 400 Bad Request（永远不会成功）
# 只重试瞬态错误（5xx, 429, timeout），不重试 4xx！

# ✅ 正确：区分可重试 vs 不可重试
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
```

---

## 🎯 什么时候用 / When to Use

**适合重试的场景：**
- 网络超时 / 抖动
- HTTP 429 (Rate Limited) — 一定要重试
- HTTP 5xx (Server Error) — 通常可以重试

**不适合重试的场景：**
- HTTP 4xx (Client Error) — 请求本身有问题，重试没用
- 数据库唯一键冲突 — 重复写入会更糟
- 幂等性未保证的操作（避免重复扣款！）

---

## 📚 参考资料 / References
- [tenacity docs](https://tenacity.readthedocs.io/en/latest/)
- [AWS: Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Google SRE Book: Handling Overload](https://sre.google/sre-book/handling-overload/)

## 🧒 ELI5
服务器忙了，你重试请求——但别立刻一遍遍狂刷，那会让它更忙。就像打电话占线，等 1 秒再打，再占线等 2 秒，再等 4 秒……越等越久，给对方喘息的机会。这就是指数退避。
When a server is busy, don't hammer it instantly. Like a busy phone line: wait 1s, then 2s, then 4s... Give the server room to breathe. That's exponential backoff.
