# Python Craft — Day 89: Mocking — unittest.mock, When to Mock vs Not

## 🐍 Python Craft — Week 9: Testing
**Mocking — unittest.mock, When to Mock vs Not**

---

### 真实场景 / Real Scenario

你在写一个服务，它调用外部 Stripe API 来处理支付。你怎么测试？真的发起请求太慢、有副作用、还要钱。这就是 Mock 的用武之地。

*You're writing a service that calls the Stripe API for payments. How do you test it? Real requests are slow, have side effects, and cost money. That's where mocking comes in.*

---

### 核心概念 / Core Concepts

```python
from unittest.mock import Mock, MagicMock, patch, call
```

**Mock vs MagicMock:**
- `Mock`: 普通 mock，不支持魔术方法 (`__len__`, `__iter__` 等)
- `MagicMock`: 支持所有魔术方法，是更安全的默认选择

---

### 三种使用方式 / Three Usage Patterns

#### 1. `patch` as decorator — 最常用 / Most Common

```python
import stripe
from unittest.mock import patch

class PaymentService:
    def charge(self, amount: int, token: str) -> dict:
        charge = stripe.Charge.create(amount=amount, currency="usd", source=token)
        return {"id": charge.id, "status": charge.status}

# Test: patch replaces stripe.Charge.create for the duration of the test
@patch("stripe.Charge.create")
def test_charge_success(mock_create):
    # Arrange: configure what the fake returns
    mock_create.return_value = Mock(id="ch_123", status="succeeded")

    # Act
    service = PaymentService()
    result = service.charge(1000, "tok_visa")

    # Assert behavior
    assert result == {"id": "ch_123", "status": "succeeded"}

    # Assert the mock was called correctly
    mock_create.assert_called_once_with(amount=1000, currency="usd", source="tok_visa")
```

#### 2. `patch` as context manager — 精确控制范围

```python
def test_charge_api_error():
    with patch("stripe.Charge.create") as mock_create:
        mock_create.side_effect = stripe.error.CardError("Declined", "card_declined", 402)

        service = PaymentService()
        with pytest.raises(stripe.error.CardError):
            service.charge(1000, "tok_declined")
```

#### 3. 直接创建 Mock — 用于依赖注入

```python
def test_charge_with_injected_client():
    mock_stripe = MagicMock()
    mock_stripe.Charge.create.return_value = Mock(id="ch_456", status="succeeded")

    service = PaymentService(stripe_client=mock_stripe)  # DI-friendly design
    result = service.charge(500, "tok_visa")
    assert result["status"] == "succeeded"
```

---

### 常用 Mock 配置 / Common Mock Configurations

```python
m = MagicMock()

# Return values
m.method.return_value = "hello"
m.method.side_effect = [1, 2, 3]        # returns 1, then 2, then 3
m.method.side_effect = ValueError("!")  # raises on call

# Verify calls
m.method.assert_called_once()
m.method.assert_called_with(42, key="val")
m.method.call_count  # how many times called
m.method.call_args_list  # all calls: [call(1), call(2), ...]

# Reset
m.reset_mock()
```

---

### ❌ 什么时候不该 Mock / When NOT to Mock

这是最重要的判断力 / This is the most important judgment call:

```python
# ❌ 别 Mock 你自己的代码逻辑
# Don't mock your own business logic — that defeats the purpose
@patch("myapp.services.calculate_total")  # DON'T mock this
def test_order():
    ...  # You're now testing nothing real

# ✅ Mock 外部边界
# DO mock external boundaries:
# - HTTP calls (requests, httpx, aiohttp)
# - Database (when doing unit tests, not integration tests)
# - Time: datetime.now(), time.time()
# - File system (for unit tests; use tmp_path for integration)
# - External services (Stripe, SendGrid, AWS S3)
# - Random/UUID generation
```

**规则 / Rule of Thumb:**

| Mock ✅ | 不要 Mock ❌ |
|---|---|
| 外部 HTTP 调用 | 你自己写的纯函数 |
| 数据库（单元测试）| 框架内部逻辑 |
| `datetime.now()` | 简单的数据转换 |
| 第三方 SDK | 你想测的核心算法 |
| 文件/网络 IO | ORM 查询（用 integration test）|

---

### 高级技巧 / Advanced: Spy with `wraps`

```python
import json

# wraps: call the real function but also track calls
with patch("json.dumps", wraps=json.dumps) as mock_dumps:
    result = json.dumps({"key": "value"})
    assert result == '{"key": "value"}'  # real behavior preserved
    mock_dumps.assert_called_once()       # but we can inspect calls
```

---

### 📚 References
- [unittest.mock Official Docs](https://docs.python.org/3/library/unittest.mock.html)
- [Python Testing with pytest — Brian Okken](https://pythontest.com/pytest-book/)
- [Stop Over-Mocking — Harry Percival](https://www.obeythetestinggoat.com/)
- [pytest-mock plugin](https://pytest-mock.readthedocs.io/)

### 🧒 ELI5
Mock 就像是拍电影时用的道具。真正的飞机太贵，所以他们用模型飞机。测试时真正的数据库太慢，所以我们用"假数据库"——它长得像数据库，但只是个演员。

*Mocking is like movie props. A real airplane is expensive, so they use a model. In tests, a real database is slow, so we use a "fake database" — it looks like a database but it's just an actor.*
