# Algorithms — Day 75: #40 Combination Sum II (Medium) — Backtracking

🧩 **回溯模式 (5/9)** — building on the template from Day 72 (Subsets II, Day 88/89 for Subsets/Combination Sum)

今天是 Backtracking 模式块的第 5 题。对比 #39 Combination Sum，今天多了一个关键约束：**候选数组有重复项，且每个元素只能用一次**。  
*Today is problem 5/9 in the Backtracking block. Versus #39, the key difference: **candidates have duplicates and each element can only be used once**.*

---

## 🔗 Links
- 🔗 [LeetCode #40](https://leetcode.com/problems/combination-sum-ii/) 🟡 Medium
- 📹 [NeetCode Video](https://neetcode.io/problems/combination-target-sum-ii)

---

## 现实类比 / Real-World Analogy

你有一堆零钱（可能有重复面值），想凑出一个精确金额，但每枚硬币只能用一次，且结果不能重复。

*You have a pile of coins (with possible duplicates) and want to make exact change — but each coin can only be used once, and duplicate combinations aren't allowed.*

---

## 问题 / Problem

```
Input: candidates = [10,1,2,7,6,1,5], target = 8
Output: [[1,1,6],[1,2,5],[1,7],[2,6]]

Constraint: Each number in candidates may only be used once.
Duplicates in candidates → but output must have no duplicate combinations.
```

---

## 与模版的映射 / Mapping to Template

```python
def backtrack(path, choices):          # Template structure
    if IS_COMPLETE(path): ...          # sum(path) == target
    for choice in choices:
        if IS_VALID(choice): ...       # sum + choice <= target, skip dups
        path.append(choice)
        backtrack(path, NEXT_CHOICES)  # start+1 (not start!) — no reuse
        path.pop()
```

**与 #39 的关键差异 / Key diff from #39 Combination Sum:**
- #39: `candidates` has no dups, each can be reused → recurse with `start` (same index)
- #40: `candidates` has dups, each used once → recurse with `start+1`, AND skip dup siblings

---

## Python 解法 + 注释 / Solution + Trace

```python
def combinationSum2(candidates, target):
    candidates.sort()  # CRITICAL: sort to group duplicates together
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])  # found valid combination
            return
        for i in range(start, len(candidates)):
            # Skip duplicates at same tree level
            # "i > start" means: skip if same value as prev sibling
            # (i == start is fine — first occurrence at this level)
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            if candidates[i] > remaining:
                break  # sorted → no point going further
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])  # i+1: no reuse
            path.pop()

    backtrack(0, [], target)
    return result

# Trace for candidates=[1,1,2,5,6,7,10], target=8:
# Level 0: try 1 → [1]
#   Level 1: try 1(second) → [1,1]
#     Level 2: try 2 → [1,1,2], rem=4... try 5 → [1,1,5], rem=1... no
#              try 6 → [1,1,6], rem=0 ✅ FOUND [1,1,6]
#   Level 1: try 2 → [1,2]... eventually [1,2,5] ✅
#   Level 1: try 6 → [1,6], rem=1... [1,7] ✅
# Level 0: try 1(second) — SKIP (i>start and candidates[i]==candidates[i-1])
# Level 0: try 2 → [2]... [2,6] ✅
```

**Complexity:**
- Time: O(2^n) — each element in or out
- Space: O(n) — recursion depth (target / min_candidate)

---

## 与同模式块的对比 / Comparison Within Block

| 题目 | 重复元素？ | 可重用？ | 递归调用 | 去重方式 |
|------|----------|---------|---------|--------|
| #78 Subsets | No | No | `i+1` | N/A |
| #39 Combo Sum | No | **Yes** | `i` (same) | N/A |
| #46 Perms | No | No | exclude visited | N/A |
| #90 Subsets II | **Yes** | No | `i+1` | skip `candidates[i]==candidates[i-1]` |
| **#40 Combo Sum II** | **Yes** | No | `i+1` | skip `candidates[i]==candidates[i-1]` |

**规律 / Pattern:** 只要有重复元素 → 先排序 → 同层跳过相同值。

---

## 举一反三 / Connect to Block

- **下一题 #79 Word Search** — 2D 棋盘上的 backtracking，不是数字，而是路径
- **#131 Palindrome Partitioning** — 不是"数字求和"而是"字符串划分"，但框架完全一样
- **核心变化模式：** 约束变了（不重用、不重复），但 选择→递归→撤销 三步不变

---

## 📝 Quiz
```json
{"question":"In #40 Combination Sum II, why do we check `i > start` before skipping duplicate candidates?","options":["A) To allow the first occurrence at each recursion level","B) To ensure the list is sorted","C) To prevent index out of bounds","D) To handle negative numbers"],"correct_index":0}
```

---

## 📚 References
- https://leetcode.com/problems/combination-sum-ii/
- https://neetcode.io/problems/combination-target-sum-ii
- https://leetcode.com/explore/featured/card/recursion-ii/472/backtracking/

## 🧒 ELI5
想象你在一堆糖果里挑糖，有两颗一样的草莓糖。你先把糖按口味排好，然后每次挑糖时，如果上一颗已经跳过同口味的了，这颗也跳过（不然会装出重复的袋子）。每颗糖只能装一次，装完不够再加，超了就换下一种口味。

*Imagine picking candy from a bag, some duplicates. Sort the bag first. When at the same "level" of choosing, if you already skipped a strawberry candy, skip all subsequent strawberry candies too — otherwise you'd get duplicate bags. Each candy goes in once; if over the budget, stop trying heavier candies.*
