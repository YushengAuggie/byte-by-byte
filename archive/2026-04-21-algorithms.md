# 💻 算法 / Algorithms — Day 28
## #739 Daily Temperatures (Medium) — Stack Pattern (5/7)

> **模式 / Pattern:** 单调栈 (Monotonic Stack) | **阶段 / Phase:** Growth | **预计阅读 / Read time:** 4 min

---

🧩 **单调栈 (Monotonic Stack) — 5/7** — building on the template from Day 23 (Valid Parentheses), Day 24 (Min Stack), Day 26 (Evaluate Reverse Polish Notation)

今天是单调栈模式的第5题。前面我们用栈做了括号匹配、最小值追踪、表达式求值。今天进入**单调栈最经典的用法：找下一个更大元素 (next greater element)**。

Today is the 5th problem in the stack block. We've used stacks for parentheses, min tracking, and expression evaluation. Now we hit the **most classic monotonic stack use case: finding the next greater element**.

---

### 🔗 Links
- 🔗 [LeetCode #739](https://leetcode.com/problems/daily-temperatures/) 🟡 Medium
- 📹 [NeetCode Video](https://www.neetcode.io/problems/daily-temperatures)

---

### 🌍 Real-World Analogy / 现实类比

你站在一排人群中，每个人都想知道：**后面什么时候会出现比我更高的人？**  
暴力解法：每个人回头一个个数。  
聪明解法：维护一个"等待队列"——还没找到更高者的人先排队，一旦出现更高的，通知所有比他矮的人。

You're in a queue; each person wants to know: **when will someone taller appear behind me?**  
Brute force: each person looks back one by one.  
Smart: maintain a "waiting list" — those who haven't found someone taller yet wait in stack. When a taller person appears, notify everyone shorter.

---

### 📋 Problem

```
Input:  temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
Output: [1,  1,  4,  2,  1,  1,  0,  0]
```

For each day, find how many days until a warmer temperature. If none, return 0.

---

### 🗺️ Mapping to Pattern Template

```python
# Template (from Day 22 intro):
# stack = []
# for i, num in enumerate(arr):
#     while stack and arr[stack[-1]] < num:
#         idx = stack.pop()
#         result[idx] = num  # next greater
#     stack.append(i)

# Daily Temperatures — direct application:
# arr = temperatures
# result[idx] = i - idx  (distance, not value)
```

**这题 vs 模板的区别 / Difference from template:**
- Template records the "next greater value" → this problem records the **distance** (i - idx)
- Everything else is identical: maintain decreasing stack of indices

---

### ✅ Solution with Trace

```python
def dailyTemperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    result = [0] * n
    stack = []  # stack of indices, temperatures[stack top] is always decreasing
    
    for i, temp in enumerate(temperatures):
        # Pop all indices where we found a warmer day
        while stack and temperatures[stack[-1]] < temp:
            prev_idx = stack.pop()
            result[prev_idx] = i - prev_idx  # days to wait
        stack.append(i)
    
    # Remaining indices in stack → no warmer day found, result stays 0
    return result
```

**逐步追踪 / Step-by-step trace:**
```
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
index:          [0,  1,  2,  3,  4,  5,  6,  7 ]

i=0, temp=73: stack=[] → push 0.      stack=[0]
i=1, temp=74: 74>73(idx0)→result[0]=1; push 1.  stack=[1]
i=2, temp=75: 75>74(idx1)→result[1]=1; push 2.  stack=[2]
i=3, temp=71: 71<75 → just push 3.    stack=[2,3]
i=4, temp=69: 69<71 → just push 4.    stack=[2,3,4]
i=5, temp=72: 72>69(idx4)→result[4]=1
              72>71(idx3)→result[3]=2
              72<75 → stop, push 5.   stack=[2,5]
i=6, temp=76: 76>72(idx5)→result[5]=1
              76>75(idx2)→result[2]=4; push 6.   stack=[6]
i=7, temp=73: 73<76 → push 7.         stack=[6,7]

result = [1, 1, 4, 2, 1, 1, 0, 0] ✓
```

**⏱️ Complexity:** Time O(n) — each element pushed/popped at most once. Space O(n).

---

### 🔄 举一反三 / Pattern Variations in This Block

| Problem | Stack Usage | What Changes |
|---------|------------|--------------|
| #20 Valid Parentheses (1/7) | matching brackets | pop on match |
| #155 Min Stack (2/7) | dual stack for min | track minimum |
| #150 Eval RPN (3/7) | operator/operand | pop two, compute |
| **#739 Daily Temps (5/7)** | **monotonic decreasing** | **next greater** |
| #853 Car Fleet (6/7) | monotonic | merge fleets |
| #84 Histogram (7/7) | monotonic | area calculation |

**核心变体 / Core variation to recognize:**  
"Next greater/smaller" → **monotonic stack** (today's pattern)  
"Matching/balanced" → **bracket stack** (Day 23)  
"Evaluate expression" → **operand/operator stack** (Day 26)

---

### 📚 References
- [LeetCode Discussion — Best Explanation](https://leetcode.com/problems/daily-temperatures/solutions/109832/java-easy-ac-solution-with-stack/)
- [NeetCode — Monotonic Stack Explained](https://neetcode.io/courses/dsa-for-beginners/29)
- [Visualgo — Stack Visualization](https://visualgo.net/en/list)

---

### 🧒 ELI5

想象你在排队买票，每个人记录"我前面什么时候会有空位（比我快的人离开）"。我们维护一个"还在等的人"的列表，按顺序排。一旦有人离开（温度更高），就告诉所有等得比他久的人"你等了几天"。这样每个人最多进出列表一次，比一个个回头数快多了！

Imagine everyone in line tracking "when will someone faster than me appear?" We keep a list of people still waiting in order. When someone faster shows up, we notify everyone slower. Each person enters/leaves the list at most once — way faster than checking one by one!
