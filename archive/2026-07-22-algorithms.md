# 💻 算法 / Algorithms — Day 97
**#131 Palindrome Partitioning · Medium · Backtracking**

🧩 **回溯模式 (7/9)** — building on the template from Day 88 (Subsets)

今天是回溯 block 第 7 题。模板还是那个，但今天的变化是：**剪枝条件变成了回文检测**。

---

## 问题
🔗 [LeetCode #131](https://leetcode.com/problems/palindrome-partitioning/) 🟡 Medium
📹 [NeetCode Solution](https://neetcode.io/problems/palindrome-partitioning)

给定字符串 `s`，将其分割为若干子串，使每个子串都是回文串。返回所有可能的分割方式。

**Example:**
```
Input: s = "aab"
Output: [["a","a","b"],["aa","b"]]
```

---

## 真实世界类比
想象你在切披萨，每一刀只能在"对称"的位置切——如果一段饼是回文的才允许那一刀。你要找出所有合法的切法。

---

## 模板映射

```python
def backtrack(path, choices):
    if IS_COMPLETE(path):      # 分割到末尾
        result.append(path[:])
        return
    for choice in choices:     # 枚举每个切割点
        if IS_VALID(choice):   # 子串是回文？
            path.append(choice)
            backtrack(path, NEXT_CHOICES)
            path.pop()         # 撤销
```

**今天的关键变化**：
- `IS_COMPLETE` = `start == len(s)` (遍历完整个字符串)
- `IS_VALID` = `is_palindrome(s[start:end])` ← 核心剪枝！
- `NEXT_CHOICES` = `range(start+1, len(s)+1)` (下一个起点到末尾)

---

## Python 解法 + Trace

```python
def partition(s: str) -> list[list[str]]:
    result = []
    n = len(s)

    def is_palindrome(sub: str) -> bool:
        return sub == sub[::-1]

    def backtrack(start: int, path: list[str]):
        # IS_COMPLETE: 分割到字符串末尾
        if start == n:
            result.append(path[:])
            return

        for end in range(start + 1, n + 1):
            substring = s[start:end]
            # IS_VALID: 只有回文才继续递归
            if is_palindrome(substring):
                path.append(substring)
                backtrack(end, path)   # 递归，起点向后移
                path.pop()             # 撤销（回溯）

    backtrack(0, [])
    return result

# Trace for s = "aab"
# backtrack(0, [])
#   end=1: "a" ✅ → path=["a"]
#     end=2: "a" ✅ → path=["a","a"]
#       end=3: "b" ✅ → path=["a","a","b"] → COMPLETE ✅
#     end=3: "ab" ❌ palindrome? No → skip
#   end=2: "aa" ✅ → path=["aa"]
#     end=3: "b" ✅ → path=["aa","b"] → COMPLETE ✅
#   end=3: "aab" ❌ palindrome? No → skip
# Result: [["a","a","b"], ["aa","b"]]
```

**时间复杂度**: O(n · 2^n) — 每个字符可以是切割点或不切割
**空间复杂度**: O(n) 递归栈深度

---

## 优化：DP 预处理回文

```python
def partition_optimized(s: str) -> list[list[str]]:
    n = len(s)
    # dp[i][j] = True if s[i..j] is palindrome
    dp = [[False] * n for _ in range(n)]

    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or dp[i+1][j-1]):
                dp[i][j] = True

    result = []
    def backtrack(start, path):
        if start == n:
            result.append(path[:])
            return
        for end in range(start, n):
            if dp[start][end]:  # O(1) lookup instead of O(n) check
                path.append(s[start:end+1])
                backtrack(end + 1, path)
                path.pop()

    backtrack(0, [])
    return result
# Time: O(n * 2^n) worst case, but palindrome check is O(1)
```

---

## 与 Block 其他题的联系 (举一反三)

| 题目 | 剪枝条件 | 区别 |
|------|----------|------|
| #78 Subsets | 无剪枝，全取 | 最基础 |
| #39 Combination Sum | `sum <= target` | 剪枝是数值 |
| #79 Word Search (Day 96) | 越界/已访问 | 2D + visited |
| **#131 Palindrome** (今天) | `is_palindrome` | 剪枝是字符串属性 |
| #51 N-Queens (下下题) | 行/列/对角线冲突 | 二维约束 |

**模式总结**：回溯的精华不在"回溯本身"，在**剪枝条件**。剪枝越好，性能越好。

---

## 📚 References
- [LeetCode #131](https://leetcode.com/problems/palindrome-partitioning/)
- [NeetCode explanation](https://neetcode.io/problems/palindrome-partitioning)
- [Backtracking guide - Leetcode patterns](https://leetcode.com/explore/learn/card/recursion-ii/472/backtracking/2654/)

## 🧒 ELI5
像拼图：你有一串字母，每次找一段对称的切下来，然后继续处理剩下的。如果某段不对称就跳过那个切法。把所有合法的切法都找出来。
