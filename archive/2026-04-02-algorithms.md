# 💻 算法 Day 15 / Algorithms Day 15
## #121 Best Time to Buy and Sell Stock (Easy) — Sliding Window
🔗 LeetCode: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/  🟢
📹 NeetCode: https://www.youtube.com/watch?v=1pkOgXD63yU

---

### 🧩 新模式 / New Pattern: 滑动窗口模式 (Sliding Window)
📍 This block: 6 problems

**什么时候用 / When to use:** 连续子数组/子串的最大值、最小值、满足条件的最短/最长

**识别信号 / Signals:** subarray, substring, contiguous, window, maximum/minimum length

**通用模版 / Template:**
```python
left = 0
for right in range(len(arr)):
    window.add(arr[right])  # expand
    while CONDITION_VIOLATED:
        window.remove(arr[left])  # shrink
        left += 1
    result = max(result, right - left + 1)
```

**核心洞察 / Key Insight:** 右指针扩张探索，左指针收缩维护约束 — 每个元素最多进出窗口各一次

---

### 🌍 现实类比 / Real-world Analogy
**中文：**把股价想成每天的“进货价”。你要做的是：先找到历史最低进货价（买入），然后在未来某天卖出（卖出价 - 买入价最大）。

**English:** Think of prices as daily “cost to buy inventory.” You want the lowest cost so far (buy) and the best future selling day to maximize profit.

---

### 🧠 题意拆解 / Problem Restatement
**中文：**给定数组 `prices[i]` 表示第 i 天价格。只能买一次、卖一次（卖在买之后）。求最大利润。

**English:** Given `prices[i]` as day i price. Buy once, sell once (sell after buy). Return max profit.

---

### 🗺️ 映射到滑动窗口 / Map to the Pattern Template
这题看起来不像“窗口里有什么元素集合”，但本质仍是“在线扫描 + 维护一个约束状态”。

- `right` = 今天（卖出日）
- `left` 不需要显式移动；我们维护“到目前为止最低买入价” = `min_price_so_far`
- `result` = 当前最大利润

**关键变化 / Key variation:**
- 不需要 `while` 收缩窗口，因为约束不是“窗口合法性”，而是“买入必须在卖出之前”。

---

### ✅ Python 解法 / Python Solution
```python
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_price = float('inf')
        best = 0

        for price in prices:  # price is the current 'sell' candidate
            # Update the best profit if we sell today
            best = max(best, price - min_price)
            # Update the minimum price seen so far (best 'buy')
            min_price = min(min_price, price)

        return best
```

---

### 🔎 手动 Trace / Walkthrough Trace
以 `prices = [7,1,5,3,6,4]` 为例：

- Day1 price=7: min=7, best=max(0, 7-∞)=0
- Day2 price=1: best=max(0, 1-7)=0, min=1
- Day3 price=5: best=max(0, 5-1)=4, min=1
- Day4 price=3: best=max(4, 3-1)=4, min=1
- Day5 price=6: best=max(4, 6-1)=5, min=1
- Day6 price=4: best=max(5, 4-1)=5, min=1

答案 = 5

---

### ⏱️ 复杂度 / Complexity
- Time: **O(n)**
- Space: **O(1)**

---

### 举一反三 / Connect to Other Problems in This Pattern Block
同一个“右指针扫过去，维护一个状态”的思路，在这个 block 里会逐步升级：

1. **#3 Longest Substring Without Repeating Characters**：窗口里维护“无重复”的约束，需要 `while` 收缩。
2. **#424 Longest Repeating Character Replacement**：维护“窗口内最多字符频次”和允许替换次数。
3. **#76 Minimum Window Substring**：需要精确覆盖目标字符计数，窗口收缩更讲究。
4. **#239 Sliding Window Maximum**：窗口最大值维护通常用单调队列。

**今天这题是最简形态：**窗口里只需要记住“历史最小值”。

---

### 📚 References
- LeetCode Problem: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
- NeetCode Explanation: https://www.youtube.com/watch?v=1pkOgXD63yU
- Sliding Window Technique (general): https://www.geeksforgeeks.org/window-sliding-technique/

---

### 🧒 ELI5
**中文：**每天你看到一个价格，就问自己两件事：
1）如果我以前最便宜的时候买了，今天卖能赚多少？
2）今天会不会比以前更便宜，适合作为新的“最便宜买入日”？
一路走到最后，你就找到能赚最多的一次买卖。

**English:** Each day, ask: (1) if I had bought at the cheapest earlier day, what profit do I get selling today? (2) is today the new cheapest day to buy? Keep the best profit.
