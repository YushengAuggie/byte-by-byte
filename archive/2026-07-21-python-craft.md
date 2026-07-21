# Python Craft — Day 96

**Day 96 | Week 9 | Integration Testing — testcontainers, Real DB Tests**

---

## 🐍 Python Craft
### Integration Testing — testcontainers & Real DB Tests

---

### 🏭 真实场景 / Real Scenario

你在做一个 User Service，用 SQLAlchemy + PostgreSQL。Unit tests 用 SQLite mock 了，但上线后发现 PostgreSQL 的 `JSONB` 查询在 SQLite 里行为完全不同，导致生产 Bug。

You're building a User Service with SQLAlchemy + PostgreSQL. Your unit tests use SQLite mocks, but you ship a bug because `JSONB` queries behave differently. Sound familiar?

**解决方案：Integration Testing with real containers.**

---

### 🐳 testcontainers — 用真实 DB 跑测试

```python
# pip install testcontainers[postgres] pytest pytest-asyncio sqlalchemy psycopg2-binary

import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# ── Fixture: spin up a real Postgres container ──
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg  # Container lives for entire test session

@pytest.fixture(scope="session")
def engine(postgres_container):
    url = postgres_container.get_connection_url()
    engine = create_engine(url)
    # Run migrations
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                metadata JSONB DEFAULT '{}'::jsonb
            )
        """))
        conn.commit()
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()   # Undo changes after each test
    session.close()

# ── The actual integration test ──
def test_jsonb_query(db_session):
    """Test JSONB query — would fail with SQLite mock!"""
    from sqlalchemy import text
    
    # Insert user with JSONB metadata
    db_session.execute(text(
        "INSERT INTO users (email, metadata) VALUES (:email, :meta)"
    ), {"email": "user@test.com", "meta": '{"role": "admin", "tier": 2}'})
    db_session.commit()
    
    # Query using JSONB operator (PostgreSQL-specific!)
    result = db_session.execute(text(
        "SELECT email FROM users WHERE metadata->>'role' = 'admin'"
    )).fetchone()
    
    assert result is not None
    assert result.email == "user@test.com"
```

---

### ⚡ Async version with asyncpg

```python
# pip install testcontainers[postgres] pytest-asyncio asyncpg sqlalchemy[asyncio]

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest_asyncio.fixture(scope="session")
async def async_engine(postgres_container):
    # testcontainers URL is sync; convert for asyncpg
    sync_url = postgres_container.get_connection_url()
    async_url = sync_url.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(async_url)
    yield engine
    await engine.dispose()

@pytest.mark.asyncio
async def test_async_insert(async_engine):
    async with AsyncSession(async_engine) as session:
        async with session.begin():
            await session.execute(text(
                "INSERT INTO users (email) VALUES ('async@test.com')"
            ))
        result = await session.execute(
            text("SELECT COUNT(*) FROM users WHERE email = 'async@test.com'")
        )
        assert result.scalar() == 1
```

---

### 📦 其他容器 / Other Containers

```python
from testcontainers.redis import RedisContainer
from testcontainers.kafka import KafkaContainer
from testcontainers.mysql import MySqlContainer

# Redis integration test
@pytest.fixture(scope="session")
def redis_client():
    with RedisContainer("redis:7-alpine") as redis:
        import redis as r
        client = r.Redis.from_url(redis.get_connection_url())
        yield client

def test_cache_set_get(redis_client):
    redis_client.set("key", "value", ex=60)
    assert redis_client.get("key") == b"value"
```

---

### 🧹 Transaction Rollback Pattern

```python
# ── Pattern: use transactions for test isolation ──
@pytest.fixture
def isolated_session(engine):
    """Each test gets a clean slate via rollback."""
    connection = engine.connect()
    transaction = connection.begin()          # Begin outer transaction
    Session = sessionmaker(bind=connection)
    session = Session()
    
    yield session
    
    session.close()
    transaction.rollback()                    # Undo ALL changes
    connection.close()
```

**为什么这比 teardown DELETE 快：** rollback 是 O(1)，DELETE 要扫表。

Why this beats `DELETE FROM` teardown: rollback is O(1); DELETE scans the table.

---

### ❌ vs ✅ 对比

```python
# ❌ Bad: SQLite mock hides PostgreSQL-specific behavior
@pytest.fixture
def mock_db():
    engine = create_engine("sqlite:///:memory:")
    # JSONB, pg-specific functions, window functions all silently break

# ✅ Good: Real container = real behavior
@pytest.fixture(scope="session")
def real_db():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield create_engine(pg.get_connection_url())
```

---

### 🎯 When to Use What

| Testing Layer | Tool | Speed |
|---|---|---|
| Unit | pytest + mocks | ⚡⚡⚡ |
| Integration | testcontainers | ⚡⚡ (~2-5s startup) |
| E2E | docker-compose | ⚡ |

**经验法则：** Unit tests → fast feedback；Integration tests → catch "it works on my machine" bugs。

---

### 📚 References
- [testcontainers-python docs](https://testcontainers-python.readthedocs.io/)
- [pytest fixtures docs](https://docs.pytest.org/en/stable/fixture.html)
- [Testing with SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)

### 🧒 ELI5
Unit test 是用积木假装是真房子。Integration test 是在真正的地基上盖房子，看会不会塌。testcontainers 帮你在测试时自动搭一个"临时真房子"用完即拆。
