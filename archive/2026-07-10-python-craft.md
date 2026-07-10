# Python Craft: Logging Best Practices — structlog, Correlation IDs
*Day 87 — Python Craft #31 | 2026-07-10*

---

## 🐍 Python 工程实践 / Python Craft

### 生产级日志：structlog + 关联 ID
### Production Logging: structlog + Correlation IDs

---

### 真实场景 / Real Scenario

你在做一个微服务 dashboard，用户反馈"偶发 500 错误"。你打开日志，看到的是：

```
ERROR: database connection failed
ERROR: user not found
ERROR: timeout after 30s
```

这些日志没有任何**上下文**——你不知道是哪个请求、哪个用户、哪次调用链出了问题。

**结构化日志 + Correlation ID** 就是解决这个问题的工具。

---

### 为什么用 structlog / Why structlog

```python
# ❌ 传统日志：字符串拼接，无法机器解析
import logging
logging.error(f"User {user_id} login failed: {error}")
# 输出: ERROR User 12345 login failed: db timeout

# ✅ structlog：结构化，每个字段独立
import structlog
log = structlog.get_logger()
log.error("login_failed", user_id=user_id, error=str(error), duration_ms=42)
# 输出: {"event": "login_failed", "user_id": 12345, "error": "db timeout", "duration_ms": 42}
```

结构化日志的好处：
- **可查询**：`jq '.[] | select(.error == "db timeout")'`
- **可聚合**：Datadog/Grafana 直接解析 JSON 字段
- **一致性**：所有服务用相同格式，统一告警规则

---

### Correlation ID：跨服务追踪 / Correlation ID: Cross-Service Tracing

```python
import uuid
import structlog
from contextvars import ContextVar

# Thread-safe context variable (works with asyncio too)
correlation_id_var: ContextVar[str] = ContextVar('correlation_id', default='')

def get_logger():
    return structlog.get_logger().bind(
        correlation_id=correlation_id_var.get()
    )

# Middleware: inject correlation ID on every request
class CorrelationIdMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Use incoming header or generate new one
        headers = dict(scope.get("headers", []))
        corr_id = headers.get(b"x-correlation-id", b"").decode()
        if not corr_id:
            corr_id = str(uuid.uuid4())
        
        # Set for this request's context
        token = correlation_id_var.set(corr_id)
        try:
            await self.app(scope, receive, send)
        finally:
            correlation_id_var.reset(token)

# Usage in your service
log = get_logger()
log.info("payment_processed", amount=100, currency="USD")
# Output: {"event": "payment_processed", "amount": 100, 
#           "currency": "USD", "correlation_id": "abc-123-def"}
```

---

### 完整 structlog 配置 / Full Setup

```python
import logging
import structlog

def configure_logging(env: str = "production"):
    shared_processors = [
        structlog.contextvars.merge_contextvars,          # thread-local context
        structlog.processors.add_log_level,               # add "level" field
        structlog.processors.TimeStamper(fmt="iso"),      # ISO timestamp
        structlog.stdlib.add_logger_name,                 # add logger name
    ]
    
    if env == "development":
        # Human-readable in dev
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer()
        ]
    else:
        # JSON in production (parseable by log aggregators)
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,         # structured exceptions
            structlog.processors.JSONRenderer()
        ]
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )

# pip install structlog
```

---

### ❌ vs ✅ 常见错误 / Common Mistakes

**❌ 在日志中记录敏感信息**
```python
log.info("user_authenticated", password=user.password, token=jwt_token)
```

**✅ 只记录标识符，不记录内容**
```python
log.info("user_authenticated", user_id=user.id, token_prefix=jwt_token[:8])
```

**❌ 日志级别乱用**
```python
log.error("user not found")  # 这只是 404，不是 error
```

**✅ 合理的日志级别**
```
DEBUG  → 开发调试，生产关闭
INFO   → 正常业务事件（请求完成、任务执行）
WARNING → 非预期但可恢复（重试、降级）
ERROR  → 需要人工介入（DB 连接失败、第三方超时）
CRITICAL → 系统级故障（OOM、数据损坏）
```

---

### When to Use / When NOT to Use

**✅ 用结构化日志：**
- 任何生产环境服务
- 需要 Datadog/ELK/Grafana 集成
- 微服务架构（必须有 correlation ID）

**❌ 不适合：**
- 简单脚本（logging.basicConfig 够用）
- 性能极端敏感的热路径（日志序列化有开销）

---

### 📚 References

- [structlog docs](https://www.structlog.org/en/stable/)
- [12-Factor App: Logs](https://12factor.net/logs)
- [Datadog: Structured Logging Best Practices](https://www.datadoghq.com/blog/python-logging-best-practices/)

### 🧒 ELI5

想象你要找医院里某个病人的所有记录。传统日志就像护士把所有事都写在一张大纸上，字迹潦草。结构化日志像电子病历——每个字段分开存，一键搜索"张三的所有检查记录"。Correlation ID 就是病历号，让所有医生的记录都能关联到同一个病人。
