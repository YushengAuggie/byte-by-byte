# 💻 算法 / Algorithms — Day 88 · #78 Subsets (Medium) [Backtracking]

🧩 **回溯模式 (1/9)** — Saturday: Full backtracking guide in today's deep dive

---

**今日题目 / Today's Problem:** LeetCode #78 — Subsets

**模式 / Pattern:** Backtracking — 选择 → 递归 → 撤销

🔗 [LeetCode #78](https://leetcode.com/problems/subsets/) | 📹 [NeetCode](https://www.youtube.com/watch?v=REOH22Xwdkk)

---

## 核心解法 / Core Solution

```python
def subsets(nums: list[int]) -> list[list[int]]:
    result = []

    def backtrack(start: int, path: list[int]):
        result.append(path[:])  # collect at every node
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

**Time:** O(n · 2ⁿ) | **Space:** O(n)

**关键点 / Key Points:**
- 每个节点都是合法子集，在每次调用时都收集结果
- `start` 参数防止重复，确保只向右扩展
- `path[:]` 浅复制必须有，否则最终结果都是空列表

---

*For the complete backtracking deep dive covering all 5 problem types (Subsets, Combination Sum, Permutations, Subsets II, N-Queens), see today's deep dive archive.*
