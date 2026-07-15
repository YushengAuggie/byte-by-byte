# Python Craft — Day 91
**Date:** 2026-07-15 | **Category:** Testing | **Topic:** Fixtures & Factories — pytest, factory_boy

---

## 🎨 前端 / Python Craft
**Fixtures & Factories — pytest, factory_boy**

---

### 真实场景 / Real Scenario

你在测试一个 UserService，每个测试需要不同状态的用户（新用户/老用户/管理员/封禁用户）。  
**你在做什么？**重复写 `User(name="test", email="...", role="admin", ...)` 20 遍？

You're testing a UserService; each test needs users in different states.  
**What are you doing?** Writing `User(name="test", email="...", role="admin", ...)` 20 times?

---

### pytest Fixtures — 依赖注入的测试工具 / DI for Tests

```python
# conftest.py — shared fixtures live here
import pytest
from myapp.models import User, db

@pytest.fixture
def db_session():
    """每个测试得到干净的 DB / Clean DB per test"""
    db.create_all()
    yield db.session
    db.session.rollback()
    db.drop_all()

@pytest.fixture  
def basic_user(db_session):
    """普通用户 fixture / Basic user fixture"""
    user = User(name="Alice", email="alice@example.com", role="user")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def admin_user(db_session):
    """管理员 fixture / Admin user fixture"""
    user = User(name="Bob", email="bob@example.com", role="admin")
    db_session.add(user)
    db_session.commit()
    return user

# test_user_service.py
def test_regular_user_cannot_delete(basic_user, user_service):
    with pytest.raises(PermissionError):
        user_service.delete_user(basic_user.id, actor=basic_user)

def test_admin_can_delete(admin_user, basic_user, user_service):
    user_service.delete_user(basic_user.id, actor=admin_user)
    assert User.query.get(basic_user.id) is None
```

**Fixture 作用域 / Scope:**
```python
@pytest.fixture(scope="session")   # 整个测试会话共享 / shared across session
@pytest.fixture(scope="module")    # 模块内共享 / shared per module
@pytest.fixture(scope="function")  # 默认：每个测试独立 / default: per test
```

---

### factory_boy — 工厂模式生成测试数据

```python
# pip install factory-boy
import factory
from factory.faker import Faker
from myapp.models import User, Post

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    # 默认值 — 每次调用自动生成不重复的数据
    name = Faker("name")              # "John Smith", "Maria Garcia"...
    email = factory.LazyAttribute(
        lambda o: f"{o.name.lower().replace(' ', '.')}@example.com"
    )
    role = "user"
    is_active = True
    created_at = factory.Faker("date_time_this_year")

class AdminUserFactory(UserFactory):
    """继承 UserFactory，只覆盖 role / Inherit, override role"""
    role = "admin"

class PostFactory(factory.Factory):
    class Meta:
        model = Post
    
    title = Faker("sentence", nb_words=6)
    author = factory.SubFactory(UserFactory)  # 自动创建关联对象!
    published = True

# 使用 / Usage
user = UserFactory()                  # 一个随机用户
admin = AdminUserFactory()            # 一个随机管理员
banned = UserFactory(is_active=False) # 覆盖某字段
users = UserFactory.create_batch(10)  # 批量创建 10 个

# pytest 里结合使用 / Combine with pytest
@pytest.fixture
def user():
    return UserFactory()

def test_post_by_user(user):
    post = PostFactory(author=user)
    assert post.author.role == "user"
```

---

### ❌ 常见错误 vs ✅ 正确做法

```python
# ❌ 硬编码测试数据 — 脆弱，维护噩梦
def test_something():
    user = User(
        id=1, name="Test User", email="test@test.com",
        role="admin", created_at=datetime(2024, 1, 1)
    )
    # ... 20 个测试，每个都这样写

# ✅ 工厂 + 只指定测试关心的字段
def test_admin_action():
    admin = AdminUserFactory()        # 其他字段自动填充
    assert admin.role == "admin"      # 只测你关心的

# ❌ 测试间共享可变 fixture 状态
@pytest.fixture(scope="session")
def user():
    return User(name="Shared")  # 危险！测试互相影响

# ✅ 默认 function scope，每测试新实例
@pytest.fixture  # scope="function" 默认
def user():
    return UserFactory()
```

---

### 猜输出 / Guess the Output

```python
class SequenceUserFactory(factory.Factory):
    class Meta:
        model = User
    name = factory.Sequence(lambda n: f"User {n}")

u1 = SequenceUserFactory()
u2 = SequenceUserFactory()
print(u1.name, u2.name)
```

**A)** `User 0`, `User 0`  
**B)** `User 0`, `User 1`  
**C)** `User 1`, `User 2`  
**D)** Error

<details><summary>答案 / Answer</summary>

**B) `User 0`, `User 1`**  
`factory.Sequence` 维护全局计数器，每次调用递增。适合需要唯一值的字段（如 email、username）。

</details>

---

### 何时用 / When to Use

| 场景 | 工具 |
|------|------|
| 简单 unit test，不需要 DB | `factory.Factory` (non-Django/SQLAlchemy) |
| 需要 DB 写入 | `factory.DjangoModelFactory` 或 SQLAlchemy 版 |
| 共享 setup/teardown | pytest fixture |
| 需要唯一字段 | `factory.Sequence` 或 `factory.Faker` |
| 关联对象 | `factory.SubFactory` |

**何时 NOT 用 factory_boy:**
- 测试只需要简单 dict/对象，直接构造即可
- 数据结构非常简单（用 dataclass 或 namedtuple）

---

### 📚 References

- [pytest fixtures docs](https://docs.pytest.org/en/stable/reference/fixtures.html)
- [factory_boy docs](https://factoryboy.readthedocs.io/)
- [Testing with factory_boy — Real Python](https://realpython.com/testing-third-party-apis-with-mock-servers/)

### 🧒 ELI5

Fixture = 每次测试前自动摆好桌子、测试后收拾干净  
Factory = 一个"生成器"，帮你造测试需要的假数据，想要几个就造几个，每个都不重样

Fixture = automatically set up the table before each test, clean up after  
Factory = a "generator" that creates fake test data on demand, each one unique
