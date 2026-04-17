# 💻 算法 / Algorithms — Day 23
## #150 Evaluate Reverse Polish Notation (Medium) — Stack Pattern

---

🧩 **Stack 模式 (3/7)** — 基于 Day 21 (Valid Parentheses) 和 Day 24 (Min Stack) 的模版

上次 Min Stack 用栈**存最小值**，这次用栈**做运算**——同样的工具，不同的用途。
*Last time (Min Stack) we used the stack to track minimums; this time we use it to evaluate — same tool, different job.*

---

### 🔗 Links

- 🔗 [LeetCode #150](https://leetcode.com/problems/evaluate-reverse-polish-notation/) 🟡 Medium
- 📹 [NeetCode Video](https://www.youtube.com/watch?v=iu0082c4HDE)

---

### 🌍 现实类比 / Real-World Analogy

逆波兰表达式（RPN）是计算器的内部语言。当你在科学计算器上按 `3 4 + 2 *`，计算器内部其实就是在用栈处理 RPN。Forth 语言、PostScript 都基于 RPN。
*RPN is the internal language of calculators. When you press `3 4 + 2 *` on a scientific calculator, it's processing RPN with a stack internally. Forth, PostScript are all RPN-based.*

---

### 🧩 问题 / Problem

给你一个字符串数组，表示逆波兰表达式：
*Given a string array representing a Reverse Polish Notation expression:*

```
Input: ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) * 3) = 9

Input: ["4","13","5","/","+"]
Output: 6
Explanation: (4 + (13 / 5)) = 6
```

**规则 / Rules:** 遇到数字 → 入栈；遇到运算符 → 弹出两个数计算 → 结果入栈。
*Rule: number → push; operator → pop two, compute, push result.*

---

### 🗺️ 映射到模版 / Map to Template

**通用栈模版：** 遍历 → 条件判断 → push 或 pop
**这道题的变化：** 不是找"下一个更大元素"，而是把数字当操作数，遇到运算符就出栈计算

```
stack = []
for token in tokens:
    if token is NUMBER:
        stack.append(int(token))     # push
    else:
        b = stack.pop()              # 注意顺序！b是后弹出的
        a = stack.pop()              # a是先弹出的（先入栈的）
        result = apply(a, op, b)
        stack.append(result)         # push result back
return stack[0]
```

**关键陷阱 / Key Trap:** 弹出顺序！`a - b` 中，a 是先入栈的（先到达），所以：
先 pop b（后到），再 pop a（先到），计算 `a op b`。
*Pop order matters! For `a - b`: a was pushed first, so pop b first, then a.*

---

### 🐍 Python 解法 / Solution

```python
def evalRPN(tokens: list[str]) -> int:
    stack = []
    ops = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b)  # truncate toward zero (not //!)
    }
    
    for token in tokens:
        if token in ops:
            b = stack.pop()   # second operand (pushed last)
            a = stack.pop()   # first operand (pushed first)
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    
    return stack[0]

# Trace: ["2","1","+","3","*"]
# "2" → stack: [2]
# "1" → stack: [2, 1]
# "+" → pop 1,2 → 2+1=3 → stack: [3]
# "3" → stack: [3, 3]
# "*" → pop 3,3 → 3*3=9 → stack: [9]
# return 9 ✓
```

**注意 `/` 的处理！**
Python `//` 向负无穷截断：`-7 // 2 = -4`
题目要求向零截断：`-7 / 2 = -3`
所以用 `int(a / b)`，不用 `a // b`！
*Python `//` truncates toward negative infinity, but the problem wants truncation toward zero. Use `int(a/b)` not `a//b`!*

---

### 📊 复杂度 / Complexity

- **时间 Time:** O(n) — 每个 token 处理一次
- **空间 Space:** O(n) — 栈最大存 n/2 个数字

---

### 🔄 举一反三 / Pattern Block: Stack (3/7)

| 题目 | 栈的用途 | 关键变化 |
|------|---------|---------|
| #20 Valid Parentheses | 匹配括号 | 用栈检查匹配 |
| #155 Min Stack | 追踪最小值 | 额外辅助栈 |
| **#150 RPN** ← 今天 | **操作数暂存** | **pop 顺序陷阱** |
| #22 Generate Parentheses | 生成有效括号 | DFS + 栈思维 |
| #739 Daily Temperatures | 单调栈 | 找下一个更大 |

---

### 📚 References

1. [LeetCode #150 — Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/)
2. [NeetCode — Stack Playlist](https://www.youtube.com/watch?v=iu0082c4HDE)
3. [Wikipedia — Reverse Polish Notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation)

---

### 🧒 ELI5

想象你在排队买东西，每次看到数字就记下来（放进口袋）。看到加减乘除号，就从口袋里掏出最后两个数字算完再放回去。最后口袋里只剩一个数，就是答案！
*Imagine a queue: see a number → put in pocket. See an operator → take out last 2 numbers, compute, put result back. When done, one number left in pocket = answer!*
