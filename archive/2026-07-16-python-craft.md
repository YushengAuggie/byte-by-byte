# Python Craft — Property-Based Testing with hypothesis

> Day 92 · Expert · Testing · Week 9

---

## 🎨 前端 → Python Craft — 属性基础测试 / Property-Based Testing with `hypothesis`

### 真实场景 / Real Scenario

你在做一个 JSON 序列化库，unit tests 只测了 3 个 case。用户发现：当 key 包含 Unicode 字符（比如 emoji 🎉）时，序列化后反序列化得到的不是原始数据。**普通测试覆盖不到这种 edge case，但 hypothesis 会自动找到它。**

You're building a JSON serialization library. Unit tests cover 3 cases. A user discovers: when a key contains Unicode (like emoji 🎉), serialize → deserialize doesn't round-trip. Regular tests miss this; **hypothesis finds it automatically.**

---

### 什么是属性基础测试 / What Is Property-Based Testing

不是写"给定这个输入，期望这个输出"，而是写**属性**：
"对于**任意**有效输入，这个性质都应该成立。"

Instead of "given THIS input, expect THIS output" — you write **properties**:
"For ANY valid input, this invariant must hold."

```
传统测试 (Example-based):         属性测试 (Property-based):
assert add(2, 3) == 5             For all x, y: add(x, y) == add(y, x)
assert add(0, 0) == 0             For all x: add(x, 0) == x
assert add(-1, 1) == 0            For all x, y, z: add(add(x,y),z) == add(x,add(y,z))
```

`hypothesis` 会自动生成数百个测试用例，并在失败时**缩小到最小复现用例（shrinking）**。

---

### 代码示例 / Code Example

```python
# pip install hypothesis
from hypothesis import given, settings, assume
from hypothesis import strategies as st
from typing import List
import json

# === Example 1: Round-trip property ===
# Property: serialize then deserialize == original
@given(st.dictionaries(
    keys=st.text(min_size=1),    # any non-empty string key
    values=st.one_of(
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(),
        st.booleans(),
        st.none()
    )
))
def test_json_roundtrip(data: dict):
    """Property: JSON roundtrip preserves data"""
    serialized = json.dumps(data)
    deserialized = json.loads(serialized)
    assert deserialized == data  # hypothesis will find any dict that breaks this!

# === Example 2: Sorting properties ===
@given(st.lists(st.integers()))
def test_sort_properties(lst: List[int]):
    """Multiple invariants about sorted output"""
    result = sorted(lst)
    
    # Property 1: same length
    assert len(result) == len(lst)
    
    # Property 2: same elements (just reordered)
    assert sorted(result) == result  # idempotent
    assert set(result) == set(lst)
    
    # Property 3: actually sorted
    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1]

# === Example 3: Stateful testing — finding race conditions ===
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize

class BankAccountMachine(RuleBasedStateMachine):
    """hypothesis generates random sequences of deposits/withdrawals"""
    
    @initialize()
    def create_account(self):
        self.balance = 0
    
    @rule(amount=st.integers(min_value=1, max_value=1000))
    def deposit(self, amount):
        self.balance += amount
        assert self.balance >= 0  # invariant: never negative
    
    @rule(amount=st.integers(min_value=1, max_value=1000))
    def withdraw(self, amount):
        assume(self.balance >= amount)  # precondition
        self.balance -= amount
        assert self.balance >= 0  # invariant: never negative

BankAccountTest = BankAccountMachine.TestCase

# === Example 4: Find the bug hypothesis discovers ===
def buggy_median(lst: List[float]) -> float:
    """Buggy: fails when list has even length and mixed signs"""
    lst = sorted(lst)
    n = len(lst)
    if n % 2 == 0:
        return (lst[n//2] + lst[n//2 - 1]) / 2  # actually correct!
    return lst[n // 2]

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_median_properties(lst):
    median = buggy_median(lst)
    # Property: median must be between min and max
    assert min(lst) <= median <= max(lst)
```

---

### Hypothesis 核心概念 / Core Concepts

```
策略 (Strategies) — 描述怎么生成测试数据:
  st.integers()           # 整数 (含负数、极值、0)
  st.text()               # Unicode 字符串 (含 emoji, 控制字符!)
  st.lists(st.integers()) # 整数列表 (含空列表, 单元素, 大列表)
  st.floats()             # 浮点数 (含 NaN, inf, -0.0!)
  st.builds(MyClass, ...) # 构造自定义对象

收缩 (Shrinking) — 找到最小失败用例:
  hypothesis 发现 [1,2,3,4,5,6,7,8] 失败
  → 自动尝试 [1,2,3,4], [1,2], [1], ...
  → 最终报告: 最小失败用例是 [5, -1]
  这让调试变得极其容易!

数据库 (Database) — 记住曾经失败的用例:
  默认保存到 .hypothesis/
  下次运行时优先测试这些用例 (regression prevention)
```

---

### 何时用 / When to Use

```
✅ 适合属性测试:
  - 数据转换 (序列化/反序列化、编解码)
  - 算法 (排序、搜索、数据结构)
  - 数学运算 (加法交换律、逆运算)
  - 状态机 / 协议

❌ 不太适合:
  - 有外部副作用 (API calls, DB writes) — 用 mock 隔离
  - 业务规则测试 ("用户 ID=5 时返回 Premium") — 用 example-based
  - 性能测试 — hypothesis 不关心速度
```

---

### 生产最佳实践 / Production Tips

```python
# 1. 设置 max_examples 避免 CI 太慢
@settings(max_examples=200)  # default=100
@given(st.text())
def test_something(s): ...

# 2. 固定数据库路径 (reproduce in CI)
# pytest.ini:
# [pytest]
# hypothesis_database = .hypothesis

# 3. 标记已知 bug，先跳过
from hypothesis import HealthCheck
@settings(suppress_health_check=[HealthCheck.too_slow])
```

---

### 📚 References
- https://hypothesis.readthedocs.io/en/latest/
- https://hypothesis.works/articles/
- https://fsharpforfunandprofit.com/posts/property-based-testing/ (concepts, language-agnostic)

### 🧒 ELI5
Normal tests are like asking "does this recipe work with chocolate?" Property-based tests are like: "For ANY flavor, cake must be taller than 2cm and have the same ingredients going in as coming out." hypothesis is a robot that tries 1000 random flavors to break your recipe — and when it finds one that fails, it tells you the simplest failing flavor.
