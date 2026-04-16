# 💻 算法 / Algorithms — Day 22: #155 Min Stack (Medium) — Stack

> 📊 Day 24 | Phase: Growth | Pattern: 单调栈模式 (2/7)

---

## 🧩 单调栈模式 (2/7) — 在 Day 23 的模版基础上延伸

Yesterday (#20 Valid Parentheses) introduced the Stack pattern for matching. Today's Min Stack is a **variation**: instead of using a stack for matching, we use **a stack to augment data retrieval** — specifically, tracking the minimum in O(1).

**Pattern recap / 模版回顾:**
```python
# Core stack pattern: push/pop with invariant maintenance
stack = []
# Each element: (value, auxiliary_info)  ← today's twist
```

---

## 🔗 Links

- 🟡 Medium | [LeetCode #155 Min Stack](https://leetcode.com/problems/min-stack/)
- 📹 [NeetCode Solution](https://neetcode.io/problems/minimum-stack)

---

## 现实类比 / Real-World Analogy

想象你在整理一摞文件，每次放一份文件上去，你都想随时知道"这摞里最薄的文件是哪本"——不翻找，O(1) 取出。

Imagine stacking folders on your desk. At any moment you need to instantly know the thinnest folder in the stack — without searching through all of them.

---

## 问题描述 / Problem

设计一个栈，支持 push、pop、top，以及 **O(1) 时间** 获取栈内最小值 `getMin()`。

Design a stack that supports push, pop, top, and **getMin() in O(1) time**.

```
MinStack stack = new MinStack();
stack.push(-2);
stack.push(0);
stack.push(-3);
stack.getMin();  # → -3
stack.pop();
stack.top();     # → 0
stack.getMin();  # → -2
```

---

## 映射到模式 / Map to Pattern

**关键洞察 / Key Insight:** 普通栈只记录值，Min Stack 在每个节点额外记录"到目前为止的最小值"。

Normal stack stores values. Min Stack stores **(value, min_so_far)** pairs — so every element "knows" the minimum at the time it was pushed.

---

## Python 解法 + 执行追踪 / Solution + Trace

```python
class MinStack:
    def __init__(self):
        # Each entry: (value, current_min_at_this_point)
        self.stack = []

    def push(self, val: int) -> None:
        # If stack is empty, min is val itself
        # Otherwise, min is min(val, top element's recorded min)
        current_min = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
```

**执行追踪 / Trace:**
```
push(-2): stack = [(-2, -2)]          # min = -2
push(0):  stack = [(-2,-2), (0,-2)]   # min still -2
push(-3): stack = [(-2,-2),(0,-2),(-3,-3)]  # new min = -3
getMin(): → stack[-1][1] = -3  ✅
pop():    stack = [(-2,-2), (0,-2)]
getMin(): → stack[-1][1] = -2  ✅ (min "restored" automatically!)
```

**神奇之处 / The Magic:** When we pop -3, the min automatically reverts to -2 — because each element carries its own "min context". No extra work needed!

---

## 复杂度 / Complexity

- **Time:** O(1) for all operations — push, pop, top, getMin
- **Space:** O(n) — extra space for storing min alongside each element

---

## 与其他模式变体的对比 / Compare to Block Problems

| Problem | Stack Stores | Key Twist |
|---------|-------------|-----------|
| #20 Valid Parentheses | Opening brackets | Match on close |
| **#155 Min Stack** ← | **(val, min)** pairs | Augment with metadata |
| #150 Eval RPN (next) | Numbers | Pop two, compute, push result |
| #739 Daily Temperatures | Indices | Monotonic decreasing values |

---

## 举一反三 / Pattern Connections

这个"携带辅助信息"的技巧在栈中非常通用：
- **Max Stack** — 同理，存 (val, max_so_far)
- **频率栈** (LFU Cache 变体) — 存 (val, frequency)
- **单调栈** (#739) — 存索引，维护单调性

The "carry auxiliary info" trick generalizes broadly:
- Max Stack → store (val, max_so_far)
- Daily Temperatures → store indices, maintain monotonic property

---

## 📚 References

- https://leetcode.com/problems/min-stack/editorial/
- https://neetcode.io/problems/minimum-stack
- https://www.geeksforgeeks.org/design-a-stack-that-supports-getmin-in-o1-time-and-o1-extra-space/

---

## 🧒 ELI5

每次往盒子里放玩具，你都在玩具上贴一个便利贴，写上"到目前为止，这箱子里最小的玩具是哪个"。想知道最小的？直接看最上面那个玩具的便利贴——不用翻箱子！

Every time you put a toy in the box, write a sticky note on it: "the smallest toy in the box so far is ___." Want to know the minimum? Just read the note on the top toy — no digging needed!
