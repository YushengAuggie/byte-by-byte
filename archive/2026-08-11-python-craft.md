# 🎨 Python Craft — Day 112
## Input Validation — Never Trust User Input, pydantic

**分类 / Category:** Security & Production
**难度 / Difficulty:** Expert

---

## 真实场景 / Real Scenario

你在构建一个 REST API 端点，接收用户提交的订单数据。如果你直接信任用户输入，攻击者可以：
- 注入负数金额（免费下单）
- 提交超长字符串（数据库溢出）
- 发送意外的 JSON 字段（覆盖内部字段）

You're building a REST API endpoint for order submissions. Trusting user input directly lets attackers:
- Submit negative amounts (free orders)
- Send huge strings (DB overflow)
- Pass unexpected fields (overwrite internal fields)

**规则：外部输入永远不信任 / Rule: External input is never trusted.**

---

## ❌ 危险写法 / Dangerous Pattern

```python
from flask import request, jsonify
import json

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json  # ← 完全信任用户输入！
    
    # 直接用 data['amount'] — 没有类型检查，没有范围检查
    # 攻击者可以传 amount: -9999, user_id: "admin", extra_field: "injected"
    order = Order(
        user_id=data['user_id'],      # ← SQL injection risk
        amount=data['amount'],        # ← could be negative, string, etc.
        items=data['items'],          # ← unbounded list size
    )
    db.save(order)
    return jsonify({"status": "ok"})
```

---

## ✅ 正确写法 — pydantic v2

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from decimal import Decimal
from typing import Annotated
import uuid

# Define what valid input looks like
class OrderItem(BaseModel):
    product_id: uuid.UUID           # must be valid UUID
    quantity: Annotated[int, Field(gt=0, le=100)]  # 1-100 only
    
class CreateOrderRequest(BaseModel):
    user_id: uuid.UUID
    amount: Annotated[Decimal, Field(gt=0, le=10_000)]  # positive, max $10k
    items: Annotated[list[OrderItem], Field(min_length=1, max_length=50)]
    currency: str = Field(default="USD", pattern=r'^[A-Z]{3}$')  # ISO 4217
    
    # Custom validator: amount must match sum of items
    @model_validator(mode='after')
    def validate_amount_matches_items(self) -> 'CreateOrderRequest':
        # In real code: look up item prices and verify
        if len(self.items) == 0:
            raise ValueError("Order must have at least one item")
        return self
    
    # Strip any extra fields — don't let attacker inject 'is_admin': True
    model_config = {"extra": "forbid"}  # ← critical!

# In your endpoint:
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

app = FastAPI()

@app.post('/order')
async def create_order(raw_body: dict):
    try:
        # Validate — raises ValidationError if anything is wrong
        order_req = CreateOrderRequest(**raw_body)
    except ValidationError as e:
        # Return structured error, don't expose internals
        raise HTTPException(status_code=422, detail=e.errors())
    
    # ✅ Now order_req is type-safe, validated, and bounded
    order = Order(
        user_id=str(order_req.user_id),
        amount=float(order_req.amount),
        items=[{"id": str(i.product_id), "qty": i.quantity} 
               for i in order_req.items]
    )
    db.save(order)
    return {"status": "created", "order_id": str(uuid.uuid4())}
```

---

## 猜猜这个会怎样？/ What happens here?

```python
class User(BaseModel):
    name: str
    age: int
    model_config = {"extra": "forbid"}

data = {"name": "Alice", "age": 25, "is_admin": True}
user = User(**data)  # What happens?
```

**A)** 正常创建，`is_admin` 被忽略  
**B)** 抛出 ValidationError: extra fields not permitted ✅  
**C)** 正常创建，`is_admin` 作为额外属性存储  
**D)** 抛出 AttributeError  

**答案 B** — `extra="forbid"` 会拒绝任何未声明字段，防止字段注入攻击。

---

## When to Use / When NOT to Use

| ✅ 使用 pydantic 验证 | ❌ 不需要 |
|-----------------------|---------|
| 所有外部 HTTP 输入 | 纯内部函数调用 |
| 配置文件读取 | 已经过验证的内部 DTO |
| CLI 参数解析 | 性能极敏感的热路径 |
| 数据库输入前 | 简单类型断言 |

---

## 常见错误 vs 正确方式 / Common Mistakes

```python
# ❌ 只验证类型，不验证范围
class Bad(BaseModel):
    age: int  # age=-5 passes!

# ✅ 验证类型 + 范围 + 语义
class Good(BaseModel):
    age: Annotated[int, Field(ge=0, le=150)]  # 0-150 only

# ❌ 允许额外字段 (默认行为)
class Unsafe(BaseModel):
    name: str
    # extra fields silently ignored — attacker can probe schema

# ✅ 拒绝额外字段
class Safe(BaseModel):
    name: str
    model_config = {"extra": "forbid"}
```

---

## 📝 Quiz

```json
{"question":"pydantic 中 model_config = {'extra': 'forbid'} 的主要安全作用是什么？","options":["防止 SQL 注入","阻止攻击者通过额外字段探测或注入数据","加速序列化速度","自动加密字段内容"],"correct_index":1}
```

/tmp/bbb-quiz-4.json written above.

---

## 📚 References
- [Pydantic v2 Docs — Field Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [FastAPI + Pydantic Security](https://fastapi.tiangolo.com/tutorial/security/)

## 🧒 ELI5
就像餐厅不让顾客直接进厨房，所有"从外面来的东西"都要先检查。pydantic 就是那个站在门口的保安：检查你的 ID（类型）、确认你在名单上（字段范围）、不让你带刀进来（额外字段）。

Like a restaurant not letting customers into the kitchen — everything from outside gets inspected first. Pydantic is the bouncer: checks your ID (types), confirms you're on the list (field constraints), and won't let you bring weapons in (extra fields).
