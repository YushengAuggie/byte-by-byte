📊 NeetCode: 23/150 · SysDesign: 22/40 · Behavioral: 22/40 · Frontend: 22/50 · AI: 11/30
🔥 1-day streak!

💻 **算法 / Algorithms** — #22 Generate Parentheses (Medium) — Stack

🧩 **Stack (4/7)** — building on the template from Day 1
今天这题和“括号匹配 / Valid Parentheses”同属一类：**用栈表示“当前还没闭合的结构”**。不同点是：
- Valid Parentheses 是“验证”
- Generate Parentheses 是“生成所有合法结果”

Today is in the same family as Valid Parentheses: use a stack to represent “currently open structures”. Difference:
- Valid Parentheses = verify
- Generate Parentheses = generate all valid sequences

🔗 LeetCode: https://leetcode.com/problems/generate-parentheses/ 🟡
📹 NeetCode: https://www.youtube.com/watch?v=s9fokUqJ76A

---

## 1) 现实类比 / Real-world analogy
把它想成写代码时的“自动补全括号”功能：你打了 `(`，编辑器知道你欠一个 `)`；但为了不出错，任何时候都不能让 `)` 的数量超过 `(`。

Think of an editor auto-completing parentheses: every `(` creates a debt of `)`; you can never close more than you opened.

---

## 2) 问题重述 / Restate
给定 n 对括号，生成所有长度 2n 的字符串，使得任意前缀里 `(` 数量 ≥ `)` 数量，且最终 `(` == `)`。

Given n pairs, generate all length-2n strings such that for every prefix, opens ≥ closes, and total opens == closes.

---

## 3) 映射到模式 / Map to the pattern
这里的“栈”不一定真的要存字符（也可以只用计数），关键是它代表：
- `stack` 里有多少个“还没关掉的左括号”

So the “stack” conceptually is the number of unmatched `(`.

生成规则（约束驱动）：
- 还能放 `(`：当 `open < n`
- 还能放 `)`：当 `close < open`（否则会出现非法前缀）

---

## 4) Python 解法（回溯 + 栈含义）/ Python solution (Backtracking)
```python
from typing import List

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res: List[str] = []

        def dfs(open_cnt: int, close_cnt: int, path: List[str]) -> None:
            # open_cnt: number of '(' used
            # close_cnt: number of ')' used
            # stack size == open_cnt - close_cnt (unmatched opens)
            if open_cnt == n and close_cnt == n:
                res.append(''.join(path))
                return

            # Option 1: add '(' if we still can
            if open_cnt < n:
                path.append('(')
                dfs(open_cnt + 1, close_cnt, path)
                path.pop()

            # Option 2: add ')' only if it won't break validity
            if close_cnt < open_cnt:
                path.append(')')
                dfs(open_cnt, close_cnt + 1, path)
                path.pop()

        dfs(0, 0, [])
        return res
```

### 小 trace / Mini trace (n=3)
- start: open=0 close=0 path=""
- add "(": open=1 close=0 path="("
- add "(": open=2 close=0 path="(("
- add ")": open=2 close=1 path="(()"  ✅（因为 close < open）
- ...

核心：任何时刻都保证 `close_cnt <= open_cnt`，这等价于“栈从不变成负数”。

Key: maintain `close_cnt <= open_cnt` always (stack never negative).

---

## 5) 复杂度 / Complexity
- 时间：输出规模主导，结果数是第 n 个 Catalan 数 `C_n`，大约 `O(C_n * n)`（每个字符串长度 2n）
- 空间：递归深度 `O(n)` + 输出

Time is output-dominated: ~`O(C_n * n)`. Space `O(n)` (excluding output).

---

## 6) 举一反三（同一模式块）/ Transfer (same pattern block)
- #20 Valid Parentheses：栈匹配（验证）
- #150 Evaluate RPN：栈求值（表达式）
- #739 Daily Temperatures：单调栈（找下一个更大元素）
- #84 Largest Rectangle：单调栈（结算区间）

同一个“Stack”家族里，核心都是：**把“未完成的东西”压栈，遇到触发条件就出栈结算**。

Across the Stack family, the idea is: push unfinished work, pop when a condition resolves it.

---

## 🧒 ELI5
你在搭积木：
- 放 `(` 就像搭一层楼
- 放 `)` 就像关掉一层楼
规则是：你不能先关楼再建楼，所以 `)` 只能在已经有没关的 `(` 时出现。

Like building floors: you can’t close a floor that wasn’t opened.

---

## 📚 References
- https://leetcode.com/problems/generate-parentheses/
- https://neetcode.io/problems/generate-parentheses
- https://en.wikipedia.org/wiki/Catalan_number
