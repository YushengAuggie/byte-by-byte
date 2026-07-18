# 🐍 Python Craft — Integration Testing: testcontainers (Week 9, Day 37)

> **Saturday — Deep Dive day.** This is a brief reference; full Python Craft content resumes Monday.

## Topic: Integration Testing — testcontainers, Real DB Tests

Unit tests mock everything. Integration tests use *real* services — Postgres, Redis, Kafka — spun up via Docker containers.

### testcontainers-python basics

```python
# pip install testcontainers[postgres]
from testcontainers.postgres import PostgresContainer
import psycopg2

def test_user_repository():
    with PostgresContainer("postgres:15") as pg:
        conn = psycopg2.connect(pg.get_connection_url())
        cur = conn.cursor()
        
        # Run your actual schema migrations
        cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT)")
        conn.commit()
        
        # Test your real repository layer
        cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id", ("Alice",))
        user_id = cur.fetchone()[0]
        conn.commit()
        
        cur.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        result = cur.fetchone()
        assert result[0] == "Alice"
```

### Key principle: Test at the right level

| Layer | Mock? | Test with? |
|-------|-------|------------|
| Unit (pure logic) | Yes | pytest + unittest.mock |
| Service (DB I/O) | **No** | testcontainers |
| API (HTTP layer) | No | FastAPI TestClient |
| E2E | No | Real staging env |

### With pytest fixtures

```python
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def pg_container():
    with PostgresContainer("postgres:15") as pg:
        yield pg  # reuse same container for all tests in session
        # container auto-stops after all tests finish
```

**Key insight:** `scope="session"` means one container for all tests — fast. `scope="function"` means one per test — isolated but slow.

See the [Saturday Deep Dive](./2026-07-18-deepdive.md) for today's main content.
