# 🎨 Python Craft — Day 23

**Import System — How Python Finds and Loads Modules**
**Python 导入系统 — 模块是怎么被找到和加载的**

---

## 🌐 真实场景 / Real-World Scenario

你在做一个大型 Python 项目，遇到过这些问题吗？
- `ImportError: No module named 'mypackage'` — 明明安装了！
- 循环导入 (`circular import`) 导致程序崩溃
- 同名模块冲突，不知道 import 了哪个

要解决这些问题，必须理解 Python 的**导入机制**。

Ever hit `ImportError` on something you're sure is installed? Or a circular import that crashes at startup? Understanding Python's import system demystifies all of this.

---

## 🔍 Python 怎么找模块 / How Python Finds Modules

当你写 `import foo`，Python 按顺序查找：

```
1. sys.modules (缓存) → 已经 import 过？直接返回
2. built-in modules  → math, os, sys...
3. frozen modules    → 编译进 Python 解释器的
4. sys.path          → 一个目录列表，逐一搜索
```

**查看 sys.path:**
```python
import sys
print(sys.path)
# ['', '/usr/lib/python3.11', '/usr/local/lib/python3.11/site-packages', ...]
# '' = 当前工作目录
```

---

## ⚙️ Import 的底层步骤 / Under the Hood

```python
import mymodule
```

Python 内部做了这 3 步：

```
1. Find: 用 Finder 定位模块文件
        - PathFinder → 搜索 sys.path
        - 每个 entry 对应一个 sys.path_hooks importer

2. Load: 用 Loader 读取 + 编译 → .pyc 缓存到 __pycache__

3. Bind: 把模块对象放入 sys.modules，绑定到当前命名空间
```

**验证缓存：**
```python
import sys
import json
print(sys.modules['json'])  # <module 'json' from '...json/__init__.py'>
# 第二次 import json 直接从这里返回，不重复加载
```

---

## 🔄 循环导入陷阱 / Circular Import Trap

```
# a.py
from b import func_b

# b.py
from a import func_a  # ❌ CircularImportError!
```

**为什么会崩？**
Python 开始 import a → 发现需要 b → 开始 import b → 发现需要 a → a 还没加载完 → 报错

**解法 / Fix:**
```python
# 方法1: 延迟导入 (lazy import)
def func_b():
    from a import func_a  # 在函数内部 import，避免模块级循环
    return func_a()

# 方法2: 重构 → 提取共同依赖到第三个模块
# a.py 和 b.py 都 import common.py，互不依赖
```

---

## 🛠️ 自定义 Import Hook / Custom Import Hook

```python
import sys

class DebugFinder:
    """Log every import attempt."""
    @classmethod
    def find_module(cls, name, path=None):
        print(f"Importing: {name}")
        return None  # None = let normal import proceed

sys.meta_path.insert(0, DebugFinder())

import json  # prints: Importing: json
import os    # prints: Importing: os
```

用途：
- 懒加载插件系统
- 模块 mock（测试时替换真实模块）
- 权限控制（禁止 import 某些模块）

---

## ❌ vs ✅ 常见错误 / Common Mistakes

**❌ 相对导入用错：**
```python
# 在 mypackage/utils.py 中
import helper  # 可能找到系统 helper，不是你想要的
```

**✅ 用明确的相对导入：**
```python
from . import helper      # 同包
from .models import User  # 同包的子模块
```

**❌ 动态修改 sys.path（hack）：**
```python
sys.path.append('/some/random/path')  # 脆弱、不可移植
```

**✅ 用 `pip install -e .` 或正确的 `pyproject.toml`**

---

## 📚 References

- https://docs.python.org/3/reference/import.html — Official import system docs
- https://realpython.com/python-import/ — Deep dive with examples
- https://peps.python.org/pep-0302/ — PEP 302: New Import Hooks

## 🧒 ELI5

Import 就像去图书馆借书：Python 先查「已借目录」(sys.modules)，没有的话按地图 (sys.path) 逐个书架 (目录) 找，找到了就借出来（加载），并记录在「已借目录」里，下次不用再找。

Importing is like borrowing a library book: check the "already borrowed" catalog (sys.modules) first, then search the shelves in order (sys.path). Once found, it's loaded and cataloged so the next import is instant.
