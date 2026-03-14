# 💻 Algorithms · Day 1
**LeetCode #217 — Contains Duplicate**
**模式：数组 & 哈希 / Pattern: Arrays & Hashing · 难度：简单 / Easy**

🔗 https://leetcode.com/problems/contains-duplicate/

---

## 🌅 先来个生活比喻 / Start with a real-world analogy

你负责给活动签到。来了100个人，你需要确认有没有人用同一张票进场两次。

怎么做最快？

**方案A（笨方法）**：每来一个人，翻遍之前所有人的名单，看有没有重复。100人要比较100×100=10,000次。

**方案B（聪明方法）**：准备一本空白通讯录。每来一个人，查一下通讯录里有没有这个名字——没有就登记，有就报警！翻通讯录只需要1秒钟，不管里面有多少人。

*You're checking tickets at an event. 100 people arrive — you need to detect if anyone uses the same ticket twice.*

*Method A (brute force): For each person, check against everyone before them. 100×100 = 10,000 comparisons.*

*Method B (smart): Keep an empty notebook. For each person, check the notebook — if not there, write them down; if already there, sound the alarm! Notebook lookup is instant regardless of size.*

方案B 用的就是今天的核心数据结构：**哈希集合 (Hash Set)**。

*Method B uses today's key data structure: a **Hash Set**.*

---

## 📋 题目 / Problem

给你一个整数数组 `nums`，如果任何值在数组中**出现至少两次**，返回 `true`；如果每个元素各不相同，返回 `false`。

*Given an integer array `nums`, return `true` if any value appears **at least twice**, and `false` if every element is distinct.*

```
Input:  [1, 2, 3, 1]  →  Output: True  ✓  (1 出现了两次)
Input:  [1, 2, 3, 4]  →  Output: False ✓  (全部唯一)
Input:  [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]  →  Output: True ✓
```

---

## 💡 思路 / The Insight

**核心问题**：怎么"记住"我已经见过哪些数字？

*The core question: how do we "remember" which numbers we've already seen?*

用 Python 的 `set`。集合有一个魔法：**O(1) 时间判断元素是否存在**。

不管集合里有1个元素还是100万个，`x in my_set` 都是瞬间完成的。

*Use Python's `set`. Sets have a superpower: **O(1) membership lookup**. Whether the set has 1 element or 1 million, `x in my_set` is instant.*

---

## 🐍 代码 / The Code

```python
def containsDuplicate(nums: list[int]) -> bool:
    seen = set()              # Our "notebook" — starts empty
    
    for num in nums:
        if num in seen:       # Already stamped this ticket?
            return True       # Duplicate found! Sound the alarm.
        seen.add(num)         # First time seeing it — stamp and record
    
    return False              # Made it through, no duplicates
```

就这样。7行。这就是最优解。

*That's it. 7 lines. This is the optimal solution.*

---

## 🔍 逐步追踪 / Step-by-Step Trace

输入 `[1, 2, 3, 1]`，我们一步一步看：

*Input `[1, 2, 3, 1]`, let's trace through:*

```
初始状态 / Initial state:
  seen = {}  (empty set)

步骤 1 / Step 1: num = 1
  1 in {} ?  → No
  seen.add(1)
  seen = {1}

步骤 2 / Step 2: num = 2
  2 in {1} ?  → No
  seen.add(2)
  seen = {1, 2}

步骤 3 / Step 3: num = 3
  3 in {1, 2} ?  → No
  seen.add(3)
  seen = {1, 2, 3}

步骤 4 / Step 4: num = 1
  1 in {1, 2, 3} ?  → YES! ✅
  return True  ← 立刻返回，不用再看了
                 Return immediately, no need to continue
```

**关键细节**：一发现重复就立刻 `return True`，不需要遍历完整个数组。最好情况下，数组第一第二个元素就相同，我们只需要2次操作。

*Key detail: we return `True` the instant we find a duplicate. In the best case (first two elements match), we only do 2 operations.*

---

## ⏱️ 复杂度分析 / Complexity Analysis

```
时间复杂度 Time:  O(n)
  — 最多遍历一遍数组
  — At most one pass through the array

空间复杂度 Space: O(n)
  — 最坏情况：所有元素唯一，set 里存了 n 个元素
  — Worst case: all unique, set holds n elements
```

**对比暴力解法 vs 哈希解法 / Brute force vs Hash set:**

```
数组大小 / Array size    暴力 O(n²)      哈希 O(n)
        100               10,000           100
      10,000          100,000,000        10,000
   1,000,000    1,000,000,000,000     1,000,000

                              ↑ 这就是为什么算法重要
                                This is why algorithms matter
```

---

## 🎁 一行解法彩蛋 / Bonus One-liner

如果你想让面试官眼前一亮（但一定要能解释清楚）：

*If you want to impress (but only if you can explain it):*

```python
def containsDuplicate(nums: list[int]) -> bool:
    return len(nums) != len(set(nums))
```

**原理**：`set` 会自动去重。如果 `set(nums)` 的长度比 `nums` 短，说明有元素被去掉了——即存在重复。

*Logic: `set()` removes duplicates. If the set is shorter than the original list, something was removed — meaning a duplicate existed.*

⚠️ **缺点**：这会遍历整个数组，无法提前退出。面试中先给出 for 循环版本，再提这个作为优化讨论。

*Downside: this always scans the entire array — no early exit. In interviews, start with the for-loop version, then mention this as a trade-off.*

---

## 🧩 模式识别 / Pattern Recognition

学会识别"什么时候用 set"：

*Learn to recognize "when to use a set":*

```
题目说：
"是否存在重复"     → Set ✓
"是否见过某个值"   → Set ✓
"找到第一个重复"   → Set ✓
"两数之和"         → Dict (需要存值和索引) ✓
"字母出现次数"     → Dict/Counter ✓
```

*When the problem asks:*
- *"Does a duplicate exist?" → Set*
- *"Have we seen this value?" → Set*
- *"Two Sum" → Dict (need to store value + index)*
- *"Count character frequency" → Dict/Counter*

---

## 🚀 相关题目 / Related Problems

掌握了今天的模式，这些题你能直接上手：

*With today's pattern, you can tackle these directly:*
- #1 Two Sum (用 dict 代替 set，存值→索引映射)
- #128 Longest Consecutive Sequence (set 的进阶用法)
- #349 Intersection of Two Arrays (两个 set 求交集)

---

## 💡 今日总结 / Today's Takeaway

```python
# 当你需要"我见过这个吗？"→ 用 set
# When you need "Have I seen this?" → use a set

seen = set()
if x in seen:    # O(1) — 瞬间 / instant
    ...
seen.add(x)      # O(1) — 瞬间 / instant
```

**面试Tips**：先说思路（"我用一个 set 来追踪已见过的数字"），再写代码，最后分析复杂度。不要上来就闷头写。

*Interview tip: verbalize your approach first ("I'll use a set to track seen numbers"), then code, then analyze complexity. Never code in silence.*

---
*⏱️ 阅读时间 ~4分钟 / Read time ~4 min*
