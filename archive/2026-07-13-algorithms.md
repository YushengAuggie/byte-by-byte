# Algorithms — Day 89: #39 Combination Sum (Medium) — Backtracking

## 💻 算法 / Algorithms
**#39 Combination Sum — Medium 🟡**
🧩 **回溯模式 (2/9)** — building on the template from Day 88 (Subsets)

[🔗 LeetCode #39](https://leetcode.com/problems/combination-sum/) | [📹 NeetCode Solution](https://neetcode.io/problems/combination-target-sum)

---

### 这道题是模板的哪种变体？/ How Does This Vary from the Subsets Template?

上次 Subsets (#78) 是枚举**所有可能的选择子集**，没有约束。
这次 Combination Sum 加了一个约束：**子集元素之和 = target**，而且**元素可以重复使用**。

*Last time (Subsets #78), we enumerated all possible subsets with no constraint. This time, there's a constraint: **subset must sum to target**, and **elements can be reused** (unlimited times).*

**两个关键变化 / Two Key Differences:**
1. **停止条件变了**: `sum == target` (不再是遍历到末尾)
2. **剪枝新增**: `sum > target` 时直接 return
3. **重复使用**: 递归时起点不后移 (`start` 而非 `start + 1`)

---

### 真实场景 / Real-World Analogy

想象你在收银台，手里有 `[2, 3, 6, 7]` 面值的硬币（可以重复用），需要凑出恰好 7 元。
回溯法就是把所有"试着凑"的过程系统化：选一枚，继续凑，凑不上去就退回来换一枚。

*Imagine you have coins of denominations `[2, 3, 6, 7]` (unlimited supply) and need to make exactly $7. Backtracking systematically tries every combination: pick one, keep going, backtrack when over.*

---

### 模板对比 / Mapping to Template

```python
# 通用模版回顾 / General Template Recap
def backtrack(path, choices):
    if IS_COMPLETE(path):       # ← 这里变了: sum(path) == target
        result.append(path[:])
        return
    for choice in choices:
        if IS_VALID(choice):    # ← 这里加了: sum(path) + choice <= target
            path.append(choice)
            backtrack(path, NEXT_CHOICES)  # ← 这里变了: 起点不后移
            path.pop()
```

---

### Python Solution (with trace)

```python
def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    result = []
    candidates.sort()  # sort for early termination (pruning)

    def backtrack(start: int, path: list[int], remaining: int):
        # Base case: found valid combination
        if remaining == 0:
            result.append(path[:])  # shallow copy of current path
            return

        for i in range(start, len(candidates)):
            num = candidates[i]

            # Pruning: since sorted, if this candidate exceeds remaining,
            # all subsequent ones will too — stop early
            if num > remaining:
                break

            path.append(num)
            backtrack(i, path, remaining - num)  # i not i+1: allow reuse!
            path.pop()  # undo choice

    backtrack(0, [], target)
    return result

# Trace: candidates=[2,3,6,7], target=7
# backtrack(0, [], 7)
#   pick 2 → backtrack(0, [2], 5)
#     pick 2 → backtrack(0, [2,2], 3)
#       pick 2 → backtrack(0, [2,2,2], 1)
#         pick 2 → remaining -1 < 0, break
#         pick 3 → remaining -2 < 0, break
#       pop 2 → [2,2]
#       pick 3 → backtrack(1, [2,2,3], 0) → ✅ append [2,2,3]
#       pop 3 → [2,2]
#     pop 2 → [2]
#     pick 3 → backtrack(1, [2,3], 2)
#       pick 3 → remaining -1 < 0, break
#     ...
#   pick 7 → backtrack(3, [7], 0) → ✅ append [7]
```

---

### Complexity
- **Time: O(n^(T/M))** where T = target, M = min candidate value — branching factor
- **Space: O(T/M)** — max recursion depth is target/minimum (for deepest combination)
- Pruning via `sort + break` drastically reduces actual nodes visited

---

### 举一反三 / Connect to Pattern Block

| 题目 | 变化点 | 关键差异 |
|---|---|---|
| #78 Subsets | 无约束，所有子集 | 每步都加入结果 |
| **#39 Combination Sum** | 目标和，可重复 | `remaining==0` 才加；`i` 不后移 |
| #46 Permutations (下一题) | 全排列，顺序重要 | 用 `visited` 数组，每次从头遍历 |
| #40 Combination Sum II | 有重复元素，每个只用一次 | 跳过重复：`if i > start and nums[i] == nums[i-1]: continue` |
| #90 Subsets II | Subsets + 重复元素 | 同样跳过重复逻辑 |

**关键规律 / Key Rule:**
- 不需要排列顺序 (combination) → `for i in range(start, n)` 保证不重复
- 需要排列顺序 (permutation) → `for i in range(0, n)` + visited array

---

### 📚 References
- [LeetCode #39 Combination Sum](https://leetcode.com/problems/combination-sum/)
- [NeetCode Video — Combination Sum](https://neetcode.io/problems/combination-target-sum)
- [Backtracking Explained — Back To Back SWE](https://www.youtube.com/watch?v=nMnEkBgJbHw)

### 🧒 ELI5
想象你在玩拼图，每块拼图可以反复用。你的目标是拼出"高度为7"的塔。你一块一块地叠，叠过头了就退一步换一块。这就是回溯——系统地试，不对就退，直到找到所有答案。

*Imagine building a tower of height 7 using blocks of various sizes (reusable). You stack blocks one by one; if too tall, remove the last block and try a different one. That's backtracking — systematic trial and undo.*
