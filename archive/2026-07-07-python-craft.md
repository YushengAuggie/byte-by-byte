# 🐍 Python Craft — Day 84
## 依赖注入 — 不依赖框架 / Dependency Injection — Without Frameworks

---

## 中文部分

### 为什么 Python 开发者经常忽视 DI？

很多 Python 开发者觉得依赖注入是 Java Spring 的东西，Python 不需要。
**事实**：Python 不需要框架，但 DI 的思想非常有用，特别是在：
- 编写可测试的代码（替换真实 DB/HTTP 为 mock）
- 管理跨模块的共享资源（DB 连接池、配置）
- 避免全局状态和隐式依赖

---

### 什么是依赖注入？

```python
# ❌ 没有 DI：硬编码依赖
class UserService:
    def __init__(self):
        self.db = PostgresDB(host="prod-db.company.com")  # 隐式依赖！
        self.cache = Redis(host="prod-redis.company.com")  # 无法替换！
    
    def get_user(self, user_id: str):
        cached = self.cache.get(f"user:{user_id}")
        if not cached:
            return self.db.query(f"SELECT * FROM users WHERE id={user_id}")
        return cached

# 问题：
# - 测试时会真的连接 prod DB
# - 无法注入 mock
# - 高耦合，改 DB 就要改这个类
```

```python
# ✅ 有 DI：依赖从外部注入
from typing import Protocol

class Database(Protocol):
    def query(self, sql: str) -> dict: ...

class Cache(Protocol):
    def get(self, key: str) -> dict | None: ...
    def set(self, key: str, value: dict) -> None: ...

class UserService:
    def __init__(self, db: Database, cache: Cache):
        self.db = db      # 注入进来，不自己创建
        self.cache = cache
    
    def get_user(self, user_id: str):
        cached = self.cache.get(f"user:{user_id}")
        if not cached:
            result = self.db.query(f"SELECT * FROM users WHERE id={user_id}")
            self.cache.set(f"user:{user_id}", result)
            return result
        return cached
```

---

### 三种 DI 模式（不用框架）

#### 1️⃣ 构造函数注入（最常用）

```python
# production
service = UserService(db=PostgresDB(), cache=RedisCache())

# testing
service = UserService(db=FakeDB(), cache=FakeCache())

# 优点：依赖清晰可见，无隐式魔法
```

#### 2️⃣ 简单 DI 容器（手写）

```python
class Container:
    """A dead-simple DI container."""
    
    def __init__(self):
        self._factories: dict = {}
        self._instances: dict = {}
    
    def register(self, name: str, factory, singleton: bool = True):
        self._factories[name] = (factory, singleton)
    
    def resolve(self, name: str):
        factory, singleton = self._factories[name]
        
        if singleton:
            if name not in self._instances:
                self._instances[name] = factory(self)
            return self._instances[name]
        
        return factory(self)  # new instance each time

# Usage
container = Container()
container.register("db", lambda c: PostgresDB(host="localhost"))
container.register("cache", lambda c: RedisCache(host="localhost"))
container.register(
    "user_service",
    lambda c: UserService(db=c.resolve("db"), cache=c.resolve("cache"))
)

# App startup
user_service = container.resolve("user_service")

# Test override
test_container = Container()
test_container.register("db", lambda c: FakeDB())
test_container.register("cache", lambda c: FakeCache())
test_container.register(
    "user_service",
    lambda c: UserService(db=c.resolve("db"), cache=c.resolve("cache"))
)
```

#### 3️⃣ 函数式 DI（适合 FastAPI/异步）

```python
# FastAPI 风格的依赖注入
from functools import lru_cache

@lru_cache  # singleton
def get_db_connection():
    return PostgresDB(host=settings.DB_HOST)

@lru_cache
def get_cache():
    return RedisCache(host=settings.REDIS_HOST)

# 函数接受依赖作为参数（便于测试时替换）
def get_user(
    user_id: str,
    db: Database = None,
    cache: Cache = None
) -> dict:
    db = db or get_db_connection()
    cache = cache or get_cache()
    # ... rest of logic

# Test
def test_get_user():
    result = get_user("123", db=FakeDB(), cache=FakeCache())
    assert result["id"] == "123"
```

---

### 什么时候用 vs 不用

```
✅ 用 DI 的场景:
- 组件需要在测试中被替换 (DB, HTTP, email)
- 配置因环境不同而变化 (dev/staging/prod)
- 组件是共享资源 (连接池, 配置)
- 遵循 SOLID 原则的生产代码

❌ 不需要 DI 的场景:
- 简单脚本, 一次性工具
- 没有外部依赖的纯函数
- 框架已经处理 (Django views, FastAPI dependencies)
```

---

### 与框架对比

```
手写 DI         vs   FastAPI Depends   vs   Python-inject/dependency-injector
简单, 无魔法        语法优雅, async 友好      功能完整, 适合大项目
测试最简单          FastAPI 绑定             学习曲线较高
适合中小项目         推荐用于 FastAPI 项目     适合企业级应用
```

---

## English Summary

**The Big Idea**: Dependency Injection is just "pass your dependencies in, don't create them inside". In Python, you don't need a framework — constructor injection + a simple container gets you 90% of the benefits.

**Key Benefits**:
- Testability: swap real DB for fake in tests
- Flexibility: change implementations without changing business logic
- Visibility: dependencies are explicit in `__init__`, not hidden

**Production Pattern**: Use a simple container at app startup to wire everything together. In tests, build your own container with fake implementations.

---

## 📚 References
- [Python DI without frameworks — Real Python](https://realpython.com/python-dependency-injection/)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [dependency-injector PyPI](https://python-dependency-injector.ets-labs.org/)

## 🧒 ELI5
Imagine you're building a toy car. A car with "no DI" comes with its engine glued in — you can never swap it. A car with DI has a slot where you can plug in any engine. Want to test without a real engine? Plug in a fake one! Want to upgrade to a faster engine later? Just swap the plug. That's dependency injection — design your code to accept parts from outside instead of building them in.
