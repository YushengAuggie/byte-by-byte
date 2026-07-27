# Python Craft — Day 101
**Caching Patterns — lru_cache, Redis, Memoization · Day 41**

---

## 🎨 Python Craft — 缓存模式 / Caching Patterns — lru_cache, Redis, Memoization

---

### 真实场景 / Real Scenario

你在做一个 dashboard，需要频繁计算用户权限矩阵（每次查询都要 JOIN 5 张表，耗时 200ms）。请求量增加后，你的 DB CPU 飙到 90%。

You're building a dashboard. Computing the permission matrix requires 5-table JOINs (200ms each). As traffic scales, your DB CPU hits 90%.

**解法：缓存。但缓存哪一层？怎么缓存？**  
**Solution: Cache. But which layer, and how?**

---

### 三层缓存策略 / Three-Layer Caching Strategy

```
Layer 1: In-Process (lru_cache)     ← 最快, 进程内, 重启丢失
Layer 2: Local Cache (dict + TTL)   ← 简单自制, 无并发保护
Layer 3: Distributed (Redis)        ← 跨进程/实例, 持久化可选
```

---

### Layer 1: functools.lru_cache

```python
from functools import lru_cache
import time

# Pure functions only — no side effects, no mutable args
@lru_cache(maxsize=128)
def get_permissions(user_id: int, role: str) -> frozenset:
    """Cache up to 128 unique (user_id, role) combos"""
    # Simulated expensive DB call
    time.sleep(0.2)
    return frozenset(["read", "write"] if role == "admin" else ["read"])

# First call: 200ms
perms = get_permissions(42, "admin")

# Second call: ~0ms (cache hit!)
perms = get_permissions(42, "admin")

# Check cache stats
print(get_permissions.cache_info())
# CacheInfo(hits=1, misses=1, maxsize=128, currsize=1)

# Manual cache clear (e.g., after role change)
get_permissions.cache_clear()
```

**⚠️ lru_cache 的限制 / Limitations:**
- 参数必须是 hashable（不能传 list, dict）
- 无 TTL（永不过期，除非 maxsize 满了 LRU 淘汰）
- 进程级别，多进程/多实例不共享

---

### Layer 1.5: cache_with_ttl (手动实现)

```python
import time
from functools import wraps

def ttl_cache(ttl_seconds=60):
    """Decorator: in-memory cache with TTL"""
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(*args):
            key = args
            now = time.monotonic()
            
            if key in cache:
                result, expires_at = cache[key]
                if now < expires_at:
                    return result  # Cache hit
            
            result = func(*args)
            cache[key] = (result, now + ttl_seconds)
            return result
        
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorator

@ttl_cache(ttl_seconds=300)  # 5-minute TTL
def get_user_profile(user_id: int) -> dict:
    return {"id": user_id, "name": "Alice"}  # Expensive DB call
```

---

### Layer 3: Redis 缓存 (分布式)

```python
import redis
import json
import hashlib
from functools import wraps

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def redis_cache(ttl=300, prefix="cache"):
    """Redis-backed cache decorator"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build cache key
            key_data = f"{prefix}:{func.__name__}:{args}:{sorted(kwargs.items())}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()[:16]
            full_key = f"{prefix}:{func.__name__}:{cache_key}"
            
            # Try cache first
            cached = r.get(full_key)
            if cached:
                return json.loads(cached)
            
            # Miss: compute + store
            result = func(*args, **kwargs)
            r.setex(full_key, ttl, json.dumps(result))
            return result
        
        return wrapper
    return decorator

@redis_cache(ttl=300, prefix="permissions")
def get_user_permissions(user_id: int) -> list:
    # Shared across ALL instances — scales horizontally!
    return ["read", "write"]  # Expensive computation
```

---

### Cache Invalidation Strategies 缓存失效策略

```python
# 1. Time-based (TTL) — simplest
r.setex("user:42:perms", 300, json.dumps(perms))

# 2. Event-based — explicit invalidation on write
def update_user_role(user_id, new_role):
    db.update(user_id, role=new_role)
    r.delete(f"permissions:get_user_permissions:{user_id}")  # Invalidate!

# 3. Write-through — update cache AND DB together
def update_and_cache(user_id, data):
    db.update(user_id, data)
    r.setex(f"user:{user_id}", 300, json.dumps(data))

# 4. Cache-aside (most common pattern)
def get_user(user_id):
    cached = r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    user = db.get(user_id)          # DB miss
    r.setex(f"user:{user_id}", 300, json.dumps(user))
    return user
```

---

### 常见错误 ❌ vs 正确做法 ✅

```python
# ❌ Cache stampede (thundering herd)
# All 1000 requests hit DB simultaneously when cache expires
def bad_cache(key):
    val = r.get(key)
    if not val:
        val = expensive_query()  # 1000 concurrent calls!
        r.setex(key, 60, val)
    return val

# ✅ Probabilistic Early Expiration (PER) to prevent stampede
import random
import math

def good_cache(key, beta=1.0):
    val, expiry = r.get_with_ttl(key)
    remaining = expiry - time.time()
    # Refresh early with some probability as TTL shrinks
    if remaining - beta * math.log(random.random()) < 0:
        val = expensive_query()
        r.setex(key, 60, val)
    return val
```

---

### When to Use / When NOT to Use

| Use Cache | Don't Cache |
|-----------|-------------|
| Read > Write ratio | Financial transactions (stale = bad) |
| Expensive computation | Data that changes every request |
| Stable reference data | Per-user private mutations |
| Public/shared data | When consistency is critical |

---

### 📝 Quiz
```json
{"question":"以下哪种情况最不适合用缓存？","options":["用户权限矩阵（每分钟变化一次）","商品价格（实时竞价）","网站首页静态内容","热门搜索词自动补全"],"correct_index":1}
```

---

### 📚 References
- [Python functools.lru_cache docs](https://docs.python.org/3/library/functools.html#functools.lru_cache)
- [Redis Caching Patterns](https://redis.io/docs/manual/patterns/)
- [Cache Stampede / Thundering Herd](https://en.wikipedia.org/wiki/Cache_stampede)

### 🧒 ELI5
**缓存就像你的记忆：**  
第一次学 2×3=6，算了好一会儿。  
之后每次问你，直接说 "6"，不用重新算。  
但如果答案变了（比如题目改了），你得清除记忆重新学。

**Cache = your memory:**  
First time 2×3=6 takes effort.  
After that — instant answer, no thinking needed.  
But if the answer changes, clear the memory and recompute!
