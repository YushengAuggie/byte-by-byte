# 💻 算法 / Algorithms — #981 Time Based Key-Value Store (Medium)

> Day 38 · Mastery Phase · ~4 min read
> 🧩 **二分搜索模式 (6/7)** — 在上一题 Search in Rotated Sorted Array 基础上进阶

---

## 🧩 模式回顾 / Pattern Recap (6/7)

Building on the template from earlier in this block:

```python
# 通用二分模板 / Universal Binary Search Template
left, right = 0, len(arr) - 1
while left <= right:
    mid = (left + right) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: left = mid + 1
    else: right = mid - 1
```

**今天的变体 / Today's Variation:** 不是在连续数组中搜索，而是在**时间戳列表**中找"最大的 ≤ target 的值"（upper bound 变体）。核心洞察不变：排除一半搜索空间。

*Not searching a plain array — searching a list of timestamps for the largest value ≤ target. Same core insight: eliminate half the search space each time.*

---

## 题目 / Problem

🔗 [LeetCode #981](https://leetcode.com/problems/time-based-key-value-store/) 🟡 Medium · 📹 [NeetCode](https://neetcode.io/problems/time-based-key-value-store)

设计一个时间版本的 key-value 存储，支持：
- `set(key, value, timestamp)` — 存储 key 在某时间戳的值
- `get(key, timestamp)` — 获取 key 在 ≤ timestamp 的**最新**值

*Design a time-versioned key-value store supporting `set(key, value, timestamp)` and `get(key, timestamp)` which returns the value at the largest timestamp ≤ the given timestamp.*

---

## 现实类比 / Real-World Analogy

Git 的版本历史！`git log` 给你所有提交（按时间排序），`git checkout` 让你回到"某时间点之前最新的"那次提交。这道题就是实现这个机制。

*Git version history! `git log` gives you all commits (sorted by time), and `git checkout` lets you restore the most recent commit before a given time. This problem implements exactly that.*

---

## 解题思路 / Approach

1. 用 `defaultdict(list)` 存储每个 key 的 `(timestamp, value)` 列表
2. `set` 时直接 append（题目保证时间戳递增，所以自然有序）
3. `get` 时对时间戳列表做**二分搜索**，找最大的 ≤ target 的时间戳

*Use `defaultdict(list)` to store `(timestamp, value)` pairs per key. `set` simply appends (timestamps are guaranteed increasing = naturally sorted). `get` binary searches the timestamp list for the largest timestamp ≤ target.*

---

## Python 解法 / Solution

```python
from collections import defaultdict
import bisect

class TimeMap:
    def __init__(self):
        # key -> list of (timestamp, value), sorted by timestamp
        self.store = defaultdict(list)
    
    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))
    
    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        
        values = self.store[key]  # [(ts1, val1), (ts2, val2), ...]
        
        # Binary search: find rightmost timestamp <= target
        # bisect_right on timestamps
        left, right = 0, len(values) - 1
        result = ""
        
        while left <= right:
            mid = (left + right) // 2
            if values[mid][0] <= timestamp:
                result = values[mid][1]  # candidate — try to find closer
                left = mid + 1           # go right (want larger timestamp ≤ target)
            else:
                right = mid - 1          # too large, go left
        
        return result

# Trace example:
# set("foo", "bar", 1)  → store["foo"] = [(1, "bar")]
# set("foo", "bar2", 4) → store["foo"] = [(1, "bar"), (4, "bar2")]
# get("foo", 4) → binary search [1,4] for ≤4 → ts=4 ✓ → "bar2"
# get("foo", 3) → binary search [1,4] for ≤3 → ts=1 ✓ → "bar"
# get("foo", 0) → ts=1 > 0, right=-1 → result stays "" → ""
```

**时间/空间复杂度：**
- `set`: O(1) 均摊
- `get`: O(log n) — n 为该 key 的版本数
- Space: O(n) — n 为总 set 调用次数

---

## 模板映射 / Template Mapping

```
标准模板中:            这道题中:
arr[mid] == target  →  values[mid][0] == timestamp (exact match)
arr[mid] < target   →  values[mid][0] <= timestamp → result = value; left = mid + 1
arr[mid] > target   →  values[mid][0] > timestamp  → right = mid - 1
```

**关键变化：** 不是找精确值，而是找"最右边满足条件的"。用 `result` 变量记录候选答案，继续向右搜索。

*Key difference: not finding exact match but the rightmost satisfying condition. Use a `result` variable to track the best candidate, keep searching right.*

---

## 举一反三 / Pattern Connection

这个 block 中的 6 道题都是二分的不同变体：

| 题目 | 变体 |
|------|------|
| #704 Binary Search | 基础：精确查找 |
| #74 Search a 2D Matrix | 把矩阵当 1D 数组 |
| #875 Koko Eating Bananas | 二分答案（不是数组） |
| #153 Find Min in Rotated | 找边界点 |
| #33 Search in Rotated | 判断哪半段有序 |
| **#981 Time Based KV** | **找最右满足条件的值** |
| #4 Median of Two Sorted | 下次见 😈 |

---

## 📚 参考资料 / References

- [LeetCode #981](https://leetcode.com/problems/time-based-key-value-store/)
- [NeetCode Video Solution](https://neetcode.io/problems/time-based-key-value-store)
- [Python bisect module docs](https://docs.python.org/3/library/bisect.html)

---

## 🧒 ELI5

想象一本日记本，每页都有日期和内容。你想找"4月3日或之前最新的那页日记"。笨方法是从头翻到第4月3日。聪明方法是先翻到中间——如果中间那页是4月10日，说明太新了，往前翻；如果是3月20日，可以用它但继续往后翻找更新的。每次都排除一半，很快就找到了！

*Imagine a diary with dated pages. You want "the most recent entry on or before April 3rd." Dumb way: read every page. Smart way: open to the middle — if it's April 10th, it's too new so go earlier; if it's March 20th, it's a candidate but keep looking later. Eliminate half each time — that's binary search!*
