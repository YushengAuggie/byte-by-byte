# Python Craft — Day 93: Testing Async Code — pytest-asyncio Patterns

🎨 **前端 Python Craft** — Week 9 · Testing

---

## 场景 / Scenario

你在构建一个异步微服务（FastAPI + asyncio），需要测试：
- 异步数据库查询（async ORM）
- 外部 HTTP 调用（httpx AsyncClient）
- 后台任务（asyncio.create_task）

普通的 `pytest` 直接测 `async def` 会报错。怎么办？

*You're building an async FastAPI microservice and need to test async db queries, HTTP calls, and background tasks. Vanilla pytest can't call `async def` directly. What do you do?*

---

## 核心工具 / Core Tools

```bash
pip install pytest-asyncio anyio httpx
```

---

## 基础：让 pytest 认识 async / Make pytest async-aware

```python
# conftest.py
import pytest

# Option 1: Global mode (recommended for all-async projects)
# pytest.ini or pyproject.toml:
# [tool.pytest.ini_options]
# asyncio_mode = "auto"

# Option 2: Per-test decorator
@pytest.mark.asyncio
async def test_something():
    result = await my_async_function()
    assert result == expected
```

---

## 模式 1：测试异步函数 / Pattern 1: Test Async Functions

```python
import pytest
import asyncio

async def fetch_user(user_id: int) -> dict:
    await asyncio.sleep(0.01)  # simulates DB call
    return {"id": user_id, "name": "Alice"}

@pytest.mark.asyncio
async def test_fetch_user():
    user = await fetch_user(1)
    assert user["id"] == 1
    assert user["name"] == "Alice"
```

---

## 模式 2：Mock 异步依赖 / Pattern 2: Mock Async Dependencies

```python
from unittest.mock import AsyncMock, patch

# ❌ Common mistake: using MagicMock for async functions
# MagicMock() is NOT awaitable — will raise TypeError

# ✅ Correct: use AsyncMock
@pytest.mark.asyncio
async def test_with_async_mock():
    mock_db = AsyncMock()
    mock_db.fetch.return_value = {"id": 1, "name": "Bob"}

    result = await mock_db.fetch(1)
    assert result["name"] == "Bob"
    mock_db.fetch.assert_awaited_once_with(1)

# Patch async method on a class
@pytest.mark.asyncio
@patch("myapp.services.UserService.get_user", new_callable=AsyncMock)
async def test_service(mock_get_user):
    mock_get_user.return_value = {"id": 42}
    from myapp.services import UserService
    result = await UserService().get_user(42)
    assert result["id"] == 42
```

---

## 模式 3：Async Fixtures / Pattern 3: Async Fixtures

```python
import pytest_asyncio  # separate from pytest.mark.asyncio

@pytest_asyncio.fixture
async def db_connection():
    conn = await create_test_db()  # async setup
    yield conn
    await conn.close()  # async teardown

@pytest.mark.asyncio
async def test_query(db_connection):
    result = await db_connection.execute("SELECT 1")
    assert result is not None
```

---

## 模式 4：测试并发行为 / Pattern 4: Test Concurrent Behavior

```python
@pytest.mark.asyncio
async def test_concurrent_calls():
    """Ensure 3 calls run concurrently, not sequentially."""
    import time
    start = time.monotonic()
    
    results = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )
    
    elapsed = time.monotonic() - start
    assert len(results) == 3
    # Should take ~10ms (concurrent), not ~30ms (sequential)
    assert elapsed < 0.05
```

---

## ❌ vs ✅ 常见坑 / Common Mistakes

```python
# ❌ Mistake 1: Forgetting @pytest.mark.asyncio
async def test_foo():  # Will be COLLECTED but NOT RUN as coroutine
    result = await fetch_user(1)  # silently skipped in old pytest versions

# ✅ Fix: Always mark or set asyncio_mode = "auto"

# ❌ Mistake 2: Using regular Mock for async method
mock = MagicMock()
await mock.fetch(1)  # TypeError: object MagicMock can't be used in await

# ✅ Fix: AsyncMock
mock = AsyncMock()
await mock.fetch(1)  # works

# ❌ Mistake 3: Event loop scope mismatch
# Using session-scoped async fixture with function-scoped test
# → "Task attached to different event loop" error

# ✅ Fix: Match fixture scope to loop scope
@pytest_asyncio.fixture(scope="session")
async def session_client():
    async with httpx.AsyncClient() as client:
        yield client
# Add to pytest.ini: asyncio_mode = "auto"
```

---

## 何时用 anyio vs asyncio / When to use anyio vs asyncio

```python
# anyio: when your code supports both asyncio and trio
import pytest
import anyio

@pytest.mark.anyio
async def test_with_anyio():
    await anyio.sleep(0.01)
    assert True

# asyncio: when you're asyncio-only (most FastAPI apps)
@pytest.mark.asyncio
async def test_with_asyncio():
    await asyncio.sleep(0.01)
```

---

## 📚 References
- https://pytest-asyncio.readthedocs.io/en/latest/
- https://docs.python.org/3/library/unittest.mock.html#unittest.mock.AsyncMock
- https://anyio.readthedocs.io/en/stable/testing.html
- https://fastapi.tiangolo.com/advanced/async-tests/

## 🧒 ELI5
普通测试就像检查一个同步机器：按一个按钮，等它完成，看结果。异步测试像在游乐园同时坐三个游乐设施——你要告诉裁判（pytest）「等我坐完所有的再来看结果」，而不是每次只坐一个。`pytest-asyncio` 就是那个懂得等多任务同时完成的智能裁判。

*Normal tests are like pressing a button and waiting. Async tests are like riding 3 roller coasters simultaneously — you need the judge (pytest) to know "wait for all of them to finish before checking the result." pytest-asyncio is the smart judge that understands async.*
