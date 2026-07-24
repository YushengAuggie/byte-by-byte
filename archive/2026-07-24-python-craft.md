# Day 99 — Python Craft: dataclasses vs pydantic vs attrs — When to Use Each

## 🎨 Python Craft — dataclasses vs pydantic vs attrs

**场景：你在做一个 dashboard API，需要定义一个 User 数据模型。用哪个？**
**Scenario: You're building a dashboard API and need to define a User data model. Which one?**

---

### 真实代码对比 / Code Comparison

同一个 `User` 模型，三种方式：

```python
# ── 1. dataclasses (stdlib, Python 3.7+) ──────────────────
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class UserDC:
    name: str
    age: int
    email: Optional[str] = None
    tags: list[str] = field(default_factory=list)

# ✅ Works: UserDC(name="Alice", age=30)
# ❌ No validation: UserDC(name="Alice", age="thirty") → no error!


# ── 2. pydantic (v2, external package) ────────────────────
from pydantic import BaseModel, EmailStr, field_validator

class UserPydantic(BaseModel):
    name: str
    age: int
    email: Optional[EmailStr] = None
    tags: list[str] = []

    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError("age must be positive")
        return v

# ✅ Validation: UserPydantic(name="Alice", age=-1) → ValidationError!
# ✅ JSON: user.model_dump(), UserPydantic.model_validate(json_data)


# ── 3. attrs (external package, older) ────────────────────
import attr

@attr.s(auto_attribs=True)
class UserAttrs:
    name: str
    age: int = attr.ib(validator=attr.validators.instance_of(int))
    email: Optional[str] = None
    tags: list[str] = attr.Factory(list)

# ✅ Validation via validators
# ✅ Slots, frozen, hash customization
```

---

### 猜输出 / Quiz: What's the Behavior?

```python
from dataclasses import dataclass

@dataclass
class Config:
    host: str
    port: int = 8080

c = Config(host="localhost", port="9000")  # Note: port is a string!
print(type(c.port))  # A) int  B) str  C) ValueError  D) TypeError
```

**答案 / Answer: B) `str`** — dataclasses don't validate types! Annotations are hints only.

---

### 决策框架 / Decision Framework

```
你需要什么？
│
├── 只是数据容器，无需验证，不依赖外部包
│   → dataclasses ✅ (stdlib, zero cost)
│
├── API 输入/输出、配置解析、需要验证
│   → pydantic ✅ (FastAPI的标配, JSON schema, 自动docs)
│
├── 大量自定义 (slots, frozen, hash, 复杂validator)
│   → attrs ✅ (最灵活，但学习曲线更陡)
│
└── 不可变值对象 (NamedTuple-like)
    → dataclass(frozen=True) or NamedTuple
```

---

### ❌ 常见错误 / Common Mistakes

```python
# ❌ Bad: mutable default in dataclass
@dataclass
class Bad:
    tags: list = []  # ValueError: mutable default!

# ✅ Good: use field(default_factory=...)
@dataclass
class Good:
    tags: list = field(default_factory=list)


# ❌ Bad: using dataclasses for API request bodies
@app.post("/user")
async def create_user(user: UserDC):  # No type coercion from JSON!
    ...

# ✅ Good: pydantic for FastAPI
@app.post("/user")
async def create_user(user: UserPydantic):  # Auto-parses + validates
    ...
```

---

### 实际选择指南 / Practical Guide

| 场景 | 推荐 |
|---|---|
| FastAPI 请求/响应体 | pydantic (FastAPI内置) |
| 配置解析 (.env, yaml) | pydantic-settings |
| 内部 DTO，不需要验证 | dataclasses |
| 复杂领域对象，需要 slots/frozen | attrs |
| 简单值对象 | dataclass(frozen=True) |
| ORM models (SQLAlchemy) | SQLAlchemy models (有自己的系统) |

---

### 📝 Quiz
```json
{"question":"You're building a FastAPI endpoint that accepts JSON request bodies with type coercion and validation. Which Python data modeling library is the natural choice?","options":["dataclasses (stdlib)","attrs","pydantic","NamedTuple"],"correct_index":2}
```

---

### 📚 References
- https://docs.python.org/3/library/dataclasses.html — Python dataclasses docs
- https://docs.pydantic.dev/latest/ — Pydantic v2 docs
- https://www.attrs.org/en/stable/ — attrs docs
- https://realpython.com/python-data-classes/ — Real Python comparison

### 🧒 ELI5
三个数据容器工具，从简到强：dataclass 是轻量级便利贴，pydantic 是有验证功能的表单，attrs 是可配置的专业工具箱。大多数时候用前两个就够了。

Three data container tools, simple to powerful: dataclasses are lightweight sticky notes, pydantic is a form with validation, attrs is a professional configurable toolkit. Most projects only need the first two.
