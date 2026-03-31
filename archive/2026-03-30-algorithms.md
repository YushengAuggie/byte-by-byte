# 💻 算法 Day 14 / Algorithms Day 14 — #42 Trapping Rain Water (Hard) — Two Pointers
## 📊 进度 / Progress
📊 Day 14/150 · NeetCode: 13/150 · SysDesign: 12/40 · Behavioral: 12/40 · Frontend: 12/50 · AI: 5/30
🔥 2-day streak!

---

## 🧩 双指针 (5/5) — 基于之前的模版继续加深 / Building on the template

前面几题（回文 / Two Sum II / 3Sum / 最大装水）都是“左右夹逼”去找**某个条件满足的配对/组合**。
今天这题更像“左右夹逼 + 维护边界”，不是找 pair，而是用左右两侧的“墙高”去决定当前位置能存多少水。

In prior problems (palindrome, Two Sum II, 3Sum, Container With Most Water), two pointers “squeeze from both ends” to find a pair/tuple. Here, we still squeeze from both ends, but we maintain **boundaries** (leftMax/rightMax) to compute trapped water.

### 🔗 Links
- LeetCode: https://leetcode.com/problems/trapping-rain-water/ 🟥
- NeetCode (Two Pointers / Trapping Rain Water): https://neetcode.io/problems/trapping-rain-water

---

## 🌍 现实类比 / Real-world analogy

把高度数组想成一排楼/挡板，下雨后水会积在“低洼处”，但能积多少取决于**左右两边更矮的那堵墙**：
- 左边最高墙是 leftMax
- 右边最高墙是 rightMax
- 当前能存水 = min(leftMax, rightMax) - height[i]

Think of bars as walls. Water at position i is limited by the **shorter** of the tallest wall to its left and right.

---

## 🧠 关键洞察 / Key insight

不用为每个位置都去找“左边最高、右边最高”（那会是 O(n^2)），
我们可以用双指针从两端向中间走：
- 若 leftMax < rightMax，说明左侧是瓶颈，left 位置的水量已经确定
- 否则右侧是瓶颈，right 位置的水量已经确定

We can decide water deterministically from the side with the smaller boundary.

---

## ✅ Python 解法（带 trace）/ Python solution (with trace)

```python
from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        left_max = right_max = 0
        water = 0

        while left < right:
            if height[left] < height[right]:
                # Left side is the limiting boundary
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    water += left_max - height[left]
                left += 1
            else:
                # Right side is the limiting boundary
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    water += right_max - height[right]
                right -= 1

        return water
```

### 🔍 Trace（以经典例子）/ Trace (classic example)
height = [0,1,0,2,1,0,1,3,2,1,2,1]

- 初始 left=0 right=11 leftMax=0 rightMax=0 water=0
- 当 height[left] < height[right]，处理 left 并更新 leftMax / 累加水
- 反之处理 right 并更新 rightMax / 累加水

最终 water=6。

---

## ⏱️ 复杂度 / Complexity
- Time: O(n)
- Space: O(1)

---

## 🔁 举一反三（同一模式 block）/ Pattern connections

同一 Two Pointers block 的演进：
1) #125 Valid Palindrome：左右夹逼，跳过无效字符
2) #167 Two Sum II：左右夹逼，按和大小移动指针
3) #15 3Sum：外层固定 + 内层双指针去重
4) #11 Container With Most Water：左右夹逼，但移动较短边
5) #42 Trapping Rain Water：左右夹逼 + 维护 leftMax/rightMax

你会发现：
- “移动哪边”一直是核心决策
- #11/#42 都在问“由较短边决定上限”，只是 #11 求最大面积，#42 求累计体积

Across the block, the recurring question is: **which pointer move is safe without missing optimal answers?**

---

## 🧒 ELI5
把两边最高的墙记下来。哪边矮，就先算哪边：因为水位被矮墙卡住，另一边再高也没用。

Record the tallest wall on each side. Work from the shorter side because it limits the water level.

---

## 📚 References
- LeetCode editorial: https://leetcode.com/problems/trapping-rain-water/editorial/
- NeetCode explanation: https://neetcode.io/problems/trapping-rain-water
- CP-Algorithms (two pointers concept background): https://cp-algorithms.com/ 


