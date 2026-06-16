# 🐍 Python 实战 / Python Craft — Day 67
**主题 / Topic:** Repository Pattern — Clean Data Access Layer
**类型 / Category:** Design Patterns (Week 5)
**预计阅读 / Read time:** ~2 min

---

## 🐍 Python Craft

**Repository Pattern — 干净的数据访问层 / Clean Data Access Layer**

---

### 🎯 场景 / Scenario

你在构建一个用户服务。刚开始用 SQLite 测试，后来要切换到 PostgreSQL，再后来要加 Redis 缓存层。每次切换都要改业务逻辑代码？**不行。**

Repository Pattern 的目标：**业务逻辑完全不知道数据从哪来。**

*You're building a user service — started with SQLite for tests, now migrating to PostgreSQL, then adding a Redis cache layer. Rewriting business logic every time? Nope. The Repository Pattern's goal: business logic has zero knowledge of where data comes from.*

---

### 🧠 核心概念 / Core Concept

```
业务逻辑 Business Logic
      ↕
  Repository Interface  ← 定义契约 / Defines contract
      ↕
  Repository Implementation
      ↕
  Database / Cache / API  ← 细节隐藏在这里 / Details hidden here
```

---

### 🐍 实现 / Implementation

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List
import sqlite3

# Domain model — pure Python, no DB dependency
@dataclass
class User:
    id: int
    name: str
    email: str

# Repository interface — the contract
class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        ...

    @abstractmethod
    def save(self, user: User) -> User:
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        ...

# SQLite implementation
class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE)"
        )

    def get_by_id(self, user_id: int) -> Optional[User]:
        row = self.conn.execute(
            "SELECT id, name, email FROM users WHERE id=?", (user_id,)
        ).fetchone()
        return User(*row) if row else None

    def save(self, user: User) -> User:
        self.conn.execute(
            "INSERT OR REPLACE INTO users VALUES (?,?,?)",
            (user.id, user.name, user.email)
        )
        self.conn.commit()
        return user

    def find_by_email(self, email: str) -> Optional[User]:
        row = self.conn.execute(
            "SELECT id, name, email FROM users WHERE email=?", (email,)
        ).fetchone()
        return User(*row) if row else None

# In-memory implementation — perfect for tests!
class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._store: dict[int, User] = {}

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._store.get(user_id)

    def save(self, user: User) -> User:
        self._store[user.id] = user
        return user

    def find_by_email(self, email: str) -> Optional[User]:
        return next(
            (u for u in self._store.values() if u.email == email),
            None
        )

# Business logic — zero database knowledge
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo  # dependency injected!

    def register(self, user_id: int, name: str, email: str) -> User:
        if self.repo.find_by_email(email):
            raise ValueError(f"Email {email} already registered")
        user = User(id=user_id, name=name, email=email)
        return self.repo.save(user)

# --- Usage ---
# Production
prod_repo = SQLiteUserRepository("users.db")
service = UserService(prod_repo)

# Tests — no DB, fast, isolated
test_repo = InMemoryUserRepository()
test_service = UserService(test_repo)
u = test_service.register(1, "Alice", "alice@example.com")
assert u.name == "Alice"
print("✅ Test passed!")
```

---

### ❌ vs ✅

```python
# ❌ Anti-pattern: business logic touches DB directly
def register_user(user_id, name, email):
    conn = sqlite3.connect("users.db")  # DB detail in business logic!
    existing = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if existing:
        raise ValueError("Email taken")
    conn.execute("INSERT INTO users VALUES (?,?,?)", (user_id, name, email))
    conn.commit()

# ✅ Repository: business logic is DB-agnostic
def register_user(user_id, name, email, repo: UserRepository):
    if repo.find_by_email(email):
        raise ValueError("Email taken")
    return repo.save(User(id=user_id, name=name, email=email))
    # Test with InMemoryUserRepository, ship with PostgreSQLUserRepository
```

---

### 🔄 何时用 / When to Use

**✅ 用 Repository Pattern 当：**
- 需要测试业务逻辑，不想真正连 DB
- 可能切换数据库（SQLite → PostgreSQL）
- 需要多数据源（DB + Cache + API）

**❌ 别过度使用：**
- 小型脚本 / 一次性工具
- 只有一层逻辑，直接 ORM 就够了

---

### 📚 参考资料 / References

1. [Repository Pattern — Martin Fowler PoEAA](https://martinfowler.com/eaaCatalog/repository.html)
2. [Python Design Patterns — Repository](https://python-patterns.guide/)
3. [Architecture Patterns with Python — Cosmic Python](https://www.cosmicpython.com/book/chapter_02_repository.html)

---

### 🧒 ELI5

*Repository 就像外卖 App：你只管点餐，不管食物从哪家厨房来、怎么送到。换了配送商，你的点餐体验不变。*

*Repository is like a food delivery app: you just place orders, not caring which kitchen or courier. Swap the delivery service, your ordering experience stays the same.*
