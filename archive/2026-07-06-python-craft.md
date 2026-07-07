# 🎨 前端 / Frontend (Python Craft) — Day 83 · Rate Limiting: Token Bucket & Sliding Window

**主题 / Topic:** 限流算法 — Token Bucket & Sliding Window Log (实现级)
**Rate Limiting in Code — Two Production-Ready Implementations**

---

## 场景 / Real-World Scenario

你在构建一个公开 API。产品要求："每个用户每分钟最多 100 次请求"。  
You're building a public API. Requirement: "max 100 requests per user per minute."

听起来简单，但坑在细节里：
- 计数器重置方式（固定窗口 vs 滑动窗口）
- 高并发下的原子性问题
- 分布式部署时的同步问题

---

## 算法 1: Token Bucket（令牌桶）

**核心思想**: 桶里有令牌，每个请求消耗一个，令牌按固定速率补充。可以**短暂突发**（桶满时）。

```python
import time
import threading

class TokenBucket:
    """
    Token Bucket rate limiter.
    Allows bursting up to `capacity` requests, 
    then throttles to `rate` requests/second.
    """
    def __init__(self, capacity: int, rate: float):
        self.capacity = capacity      # max burst size
        self.rate = rate              # tokens added per second
        self.tokens = float(capacity) # start full
        self.last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self):
        """Add tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now

    def allow(self) -> bool:
        """Returns True if request is allowed."""
        with self._lock:  # thread-safe
            self._refill()
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

# Usage
limiter = TokenBucket(capacity=10, rate=2)  # burst 10, then 2/sec

for i in range(12):
    result = "✅ allowed" if limiter.allow() else "❌ throttled"
    print(f"Request {i+1}: {result}")
    # Requests 1-10: allowed (burst)
    # Request 11-12: throttled (bucket empty)
```

**特点 / Characteristics:**
- ✅ 允许突发流量 (burst)
- ✅ 平均速率受控
- ❌ 可能在窗口边界出现双倍请求（固定窗口问题部分保留）

---

## 算法 2: Sliding Window Log（滑动窗口日志）

**核心思想**: 记录每次请求的时间戳，丢弃超出窗口的旧记录，计数剩余记录。**更精确，但内存更贵**。

```python
import time
from collections import deque
import threading

class SlidingWindowLog:
    """
    Sliding Window Log rate limiter.
    Most accurate, but O(requests) memory per user.
    """
    def __init__(self, limit: int, window_seconds: float):
        self.limit = limit
        self.window = window_seconds
        self.log: deque = deque()
        self._lock = threading.Lock()

    def allow(self) -> bool:
        with self._lock:
            now = time.monotonic()
            cutoff = now - self.window
            
            # Remove timestamps outside the window
            while self.log and self.log[0] <= cutoff:
                self.log.popleft()
            
            if len(self.log) < self.limit:
                self.log.append(now)
                return True
            return False

# Usage
limiter = SlidingWindowLog(limit=5, window_seconds=10)

# Simulate: 5 requests at t=0, then 1 more after 5 seconds
for i in range(5):
    print(f"t=0, req {i+1}: {'✅' if limiter.allow() else '❌'}")
# All 5: ✅ allowed

time.sleep(5)
print(f"t=5s, req 6: {'✅' if limiter.allow() else '❌'}")  # ❌ still in window

time.sleep(6)  # now t=11s, first 5 requests are outside 10s window
print(f"t=11s, req 7: {'✅' if limiter.allow() else '❌'}")  # ✅ allowed
```

---

## 对比 / Comparison

```
Algorithm          | Memory    | Accuracy  | Burst | Best For
-------------------|-----------|-----------|-------|------------------
Fixed Window       | O(1)      | Low ⚠️    | No    | Simple counters
Token Bucket       | O(1)      | Medium    | Yes ✅ | API with bursts
Sliding Window Log | O(requests)| High ✅   | No    | Strict per-user
Sliding Window Counter | O(1) | High ✅   | No    | Production APIs ✅

```

**生产推荐 / Production Pick:** 滑动窗口计数器 (Sliding Window Counter) — O(1) 内存 + 高精度。但 Token Bucket 在需要允许合法突发时更好（比如视频编码 API）。

---

## Redis 分布式版本 / Distributed (Redis) Version

```python
import redis
import time

r = redis.Redis()

def sliding_window_redis(user_id: str, limit: int, window: int) -> bool:
    """
    Distributed sliding window using Redis sorted sets.
    Key insight: sorted set score = timestamp → range delete = window cleanup
    """
    key = f"rate:{user_id}"
    now = time.time()
    cutoff = now - window
    
    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, cutoff)      # remove old entries
    pipe.zadd(key, {str(now): now})             # add current
    pipe.zcard(key)                             # count in window
    pipe.expire(key, window + 1)               # TTL cleanup
    results = pipe.execute()
    
    count = results[2]
    return count <= limit

# pip install redis
```

**为什么用 pipeline?** 减少网络往返，且 Redis 单线程保证原子性。

---

## 猜猜输出 / Quiz

```python
limiter = TokenBucket(capacity=3, rate=1)
# 立即发送 4 个请求
results = [limiter.allow() for _ in range(4)]
print(results)
```

**A)** `[True, True, True, True]`  
**B)** `[True, True, True, False]` ← ✅  
**C)** `[True, False, False, False]`  
**D)** `[False, False, False, False]`

---

## 📚 References

- [Cloudflare Blog — How Cloudflare does rate limiting](https://blog.cloudflare.com/counting-things-a-lot-of-different-things/)
- [Redis ZADD documentation](https://redis.io/commands/zadd/)
- [Stripe Engineering — Rate Limiters](https://stripe.com/blog/rate-limiters)
- [System Design Interview — Rate Limiter](https://bytebytego.com/courses/system-design-interview/design-a-rate-limiter)

---

## 🧒 ELI5

令牌桶：想象一个水桶，每秒自动滴水进去，每次请求舀一勺水。桶满了可以连续舀很多勺（突发），桶空了就得等。  
滑动窗口：贴一张纸，每次请求写下时间，每次来了新请求把超过一分钟的记录划掉，数数剩下多少条。

Token Bucket = a bucket that refills slowly. You can gulp fast if it's full (burst), but then you have to wait.  
Sliding Window = a sticky note of timestamps. Cross out old ones, count what's left.
