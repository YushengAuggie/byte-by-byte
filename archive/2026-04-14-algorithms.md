# 💻 算法 / Algorithms — Day 23
**题目 / Problem:** #20 Valid Parentheses (Easy)
**模式 / Pattern:** Stack — 第 1/7 题

---

## 🧩 新模式 / New Pattern: 单调栈 (Stack)

📍 本组共 7 题 / This block: 7 problems

**什么时候用 / When to use:**
括号匹配、下一个更大/更小元素、表达式求值、需要"记住历史"的线性扫描
Parentheses matching, next greater/smaller element, expression evaluation, any linear scan where you need to "remember history"

**识别信号 / Signals:**
keywords: `next greater element`, `valid parentheses`, `evaluate expression`, `monotonic`, "最近的"/"nearest"

**通用模版 / Template:**
```python
stack = []
for i, num in enumerate(arr):
    while stack and arr[stack[-1]] < num:
        idx = stack.pop()
        result[idx] = num  # process: num is the "next greater"
    stack.append(i)
# remaining in stack have no next greater element
```

**核心洞察 / Key Insight:**
栈维护单调递减序列——遇到更大的就弹出结算。这是"懒处理"的精髓：把问题推迟到你有足够信息时再解决。
The stack maintains a monotonically decreasing sequence — pop and "settle" when you find something bigger. This is the essence of lazy evaluation: defer processing until you have enough information.

---

## 今日问题 / Today's Problem

🔗 [LeetCode #20](https://leetcode.com/problems/valid-parentheses/) 🟢 Easy
📹 [NeetCode Solution](https://neetcode.io/problems/validate-parentheses)

### 🌎 真实类比 / Real-World Analogy

想象你在审查代码，看到了 `{[(`。你脑子里是不是会"压栈"，等待对应的 `)]}` 才放心？这就是栈的直觉！

Imagine reviewing code and seeing `{[(`. Your brain automatically "pushes" these onto a mental stack, waiting for the matching `}])` before relaxing. That's exactly what a stack does!

### 📋 问题 / Problem

给定一个字符串，仅包含 `(`, `)`, `{`, `}`, `[`, `]`，判断括号是否合法匹配。
Given a string of brackets, determine if it's valid (every open bracket has a matching close in the right order).

```
Input: s = "()[]{}"  → Output: true
Input: s = "([)]"   → Output: false
Input: s = "{[]}"   → Output: true
```

### 🗺️ 映射到模版 / Map to Template

这题是栈模式最纯粹的应用——不需要"单调"，只需要"匹配"：
This is the purest stack application — not monotonic, just matching:

1. 遇到开括号 `(`, `[`, `{` → **压栈 push**
2. 遇到闭括号 → 检查栈顶是否是对应的开括号
3. 最后栈必须为空

### ✅ Python 解法 / Python Solution

```python
def isValid(s: str) -> bool:
    stack = []
    # map each closing bracket to its opening counterpart
    close_to_open = {")": "(", "]": "[", "}": "{"}

    for char in s:
        if char in close_to_open:
            # closing bracket: check stack top
            if not stack or stack[-1] != close_to_open[char]:
                return False
            stack.pop()
        else:
            # opening bracket: push onto stack
            stack.append(char)

    return len(stack) == 0  # valid only if nothing left unmatched
```

**执行轨迹 / Trace:** `s = "{[]}"`
```
char='{'  → push    stack=['{']
char='['  → push    stack=['{','[']
char=']'  → top='[' matches ']' ✅ → pop  stack=['{']
char='}'  → top='{' matches '}' ✅ → pop  stack=[]
→ stack empty → True ✅
```

**执行轨迹 / Trace:** `s = "([)]"`
```
char='('  → push    stack=['(']
char='['  → push    stack=['(','[']
char=')'  → top='[' ≠ '(' ❌ → return False
```

### ⏱️ 复杂度 / Complexity

- **Time:** O(n) — 每个字符只处理一次 / each character processed once
- **Space:** O(n) — 最坏情况全是开括号 / worst case all opening brackets

### 🔗 举一反三 / Pattern Connections

本组 7 题都用栈，但复杂度递增 / All 7 problems in this block use stacks, increasing in complexity:

| # | 题目 | 栈的用法 |
|---|------|----------|
| 20 | Valid Parentheses ← 今天 | 匹配配对 |
| 155 | Min Stack | 维护辅助栈记录最小值 |
| 150 | Evaluate RPN | 数字压栈，遇算符弹出运算 |
| 22 | Generate Parentheses | 回溯 + 栈思维 |
| 739 | Daily Temperatures | 单调栈找下一个更大 |
| 853 | Car Fleet | 单调栈思维 |
| 84 | Largest Rectangle | 单调栈 hard 题 |

---

## 📚 References

- https://leetcode.com/problems/valid-parentheses/editorial/
- https://neetcode.io/problems/validate-parentheses
- https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/

---

## 🧒 ELI5

就像检查你的鞋带是否对称打结：每次遇到一个"开始"就记在本子上，遇到"结束"就检查本子上最新的是不是对应的。如果对，就划掉；如果不对或本子空了，就乱了！

It's like checking if your shoelaces are tied symmetrically. Every time you see a "start" mark, write it in your notebook. When you see an "end", check if the latest note matches. If yes, cross it off. If not — it's all tangled!

---

## 📝 Quiz

```json
{"question":"What does the stack contain after processing '([{' in Valid Parentheses?","options":["['(','[','{']","['{','[','(']","Empty — all balanced","[')','[','{']"],"correct_index":0}
```
