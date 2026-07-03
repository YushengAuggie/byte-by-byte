# 🎨 Python Craft — Day 27
**主题 / Topic:** Circuit Breaker — Protect Downstream Services
**类别 / Category:** Practical Patterns | **Week 7**
**预计阅读 / Read time:** 2 min

---

## 真实场景 / Real Scenario

你在构建一个微服务，调用了一个支付 API。这个 API 有时会挂掉，每次请求都要等 30 秒超时才返回错误。于是你的服务也开始级联超时，用户全卡住了。

You're calling a payment API. It sometimes goes down, and each request waits 30s before timing out. Your service starts cascading — users get stuck.

**没有熔断器：** 10% 的请求失败 → 都等超时 → 线程堆积 → 雪崩  
**有熔断器：** 10% 失败 → 熔断器跳闸 → 立即返回错误 → 系统保持健康

Without circuit breaker: 10% failures → all wait timeout → thread pileup → cascade failure  
With circuit breaker: 10% failures → circuit trips → fast-fail → system stays healthy

---

## 三个状态 / Three States

```
   ┌──────────┐  失败率超阈值   ┌──────────┐
   │  CLOSED  │──────────────► │   OPEN   │
   │ (正常)   │               │ (熔断)   │
   └──────────┘               └──────┬───┘
        ▲                            │ 等待恢复时间
        │                            ▼
        │                     ┌─────────────┐
        └─────────────────────│ HALF-OPEN   │
          探测成功              │ (探测中)    │
                               └─────────────┘
```

- **CLOSED:** 正常通过所有请求，统计失败率
- **OPEN:** 直接快速失败，不调用下游，保护资源
- **HALF-OPEN:** 放入少量探测请求，判断下游是否恢复

---

## 代码实现 / Implementation

```python
import time
from enum import Enum
from functools import wraps

class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,   # failures before tripping
        recovery_timeout: float = 30,  # seconds before trying again
        success_threshold: int = 2,    # successes to close from half-open
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self._state = State.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: float = 0
    
    @property
    def state(self) -> State:
        if self._state == State.OPEN:
            # Check if recovery timeout has elapsed
            if time.time() - self._last_failure_time >= self.recovery_timeout:
                self._state = State.HALF_OPEN
                self._success_count = 0
        return self._state
    
    def call(self, func, *args, **kwargs):
        if self.state == State.OPEN:
            raise Exception("Circuit breaker OPEN — fast failing")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        if self._state == State.HALF_OPEN:
            self._success_count += 1
            if self._success_count >= self.success_threshold:
                self._state = State.CLOSED  # fully recovered
                self._failure_count = 0
        elif self._state == State.CLOSED:
            self._failure_count = 0  # reset on success
    
    def _on_failure(self):
        self._last_failure_time = time.time()
        self._failure_count += 1
        if self._failure_count >= self.failure_threshold:
            self._state = State.OPEN


# Usage
cb = CircuitBreaker(failure_threshold=3, recovery_timeout=10)

def call_payment_api(amount: float):
    # Simulate: raise ConnectionError if API is down
    return {"status": "ok", "charged": amount}

try:
    result = cb.call(call_payment_api, 99.99)
    print(f"✅ Charged: {result}")
except Exception as e:
    print(f"❌ Payment failed: {e}")
    # Return cached response or graceful degradation
```

---

## ❌ 常见错误 vs ✅ 正确做法

**❌ 错误:** 直接重试失败请求（指数退避不够，仍然有雪崩风险）
```python
# Bad: keeps hammering a dead service
for i in range(3):
    try:
        result = call_api()
        break
    except:
        time.sleep(2 ** i)
```

**✅ 正确:** 用熔断器 + 退避组合，快速失败 + 定时恢复
```python
# Good: fail fast, recover gracefully
cb = CircuitBreaker(failure_threshold=5, recovery_timeout=30)
try:
    result = cb.call(call_api)
except Exception:
    # Serve cached data or return degraded response
    result = get_cached_or_default()
```

---

## 生产级选择 / Production Options

| 库 / Library | 特性 |
|-------------|------|
| `pybreaker` | 轻量，最常用 |
| `resilience4j` (Java) | 企业级，Spring Boot |
| `Hystrix` | Netflix 出品，已停止维护 |
| Istio / Envoy | Sidecar 层熔断，不侵入代码 |

```bash
pip install pybreaker
```

---

## 📚 References
- [Martin Fowler: Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
- [pybreaker on PyPI](https://pypi.org/project/pybreaker/)
- [AWS Architecture — Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)

## 🧒 ELI5
家里的电路保险丝，一旦电流过大就跳闸保护整个电路。熔断器模式同理：一旦下游服务挂了，就立刻"跳闸"停止调用，保护整个系统不雪崩。等一会儿再试探性地恢复。

Like a circuit breaker in your home — when too much current flows, it trips to protect everything. In code: when a downstream service fails too much, stop calling it immediately to protect your whole system. Try again after a cooldown.
