# 💻 算法 Day 14 / Algorithms Day 14
## #42 Trapping Rain Water (Hard) — Two Pointers

🧩 **Two Pointers (5/5)** — building on the template from earlier days in this block

- 🔗 LeetCode: https://leetcode.com/problems/trapping-rain-water/  🔴
- 📹 NeetCode: https://www.youtube.com/watch?v=ZI2z5pq0TqA
- **Pattern / 模式:** Two Pointers（双指针）

---

## 🌧️ 现实类比 / Real-world analogy

把城市的屋顶想成一排高度不同的墙。下雨后，低洼处会积水，但能积多少取决于它左边最高的墙和右边最高的墙：

> **water[i] = min(maxLeft, maxRight) - height[i]**（如果为正）

Think of bars as walls. The water above a bar is limited by the shorter of the tallest wall on its left and the tallest wall on its right.

---

## 🧠 问题重述 / Problem

给定数组 `height` 表示柱子高度，每根柱子宽度为 1，计算下雨后能接多少雨水。

Given `height`, compute total trapped water.

---

## 🧩 如何映射到双指针模板 / Map to the Two Pointers template

之前的双指针块（
#125 回文、#167 两数之和II、#15 三数之和、#11 盛最多水的容器
）里，左右指针“夹逼”的核心是：

- **每一步都能确定一侧的最优/可行性**，因此可以移动那一侧，整体 O(n)

这题的“变化点”是：
- 我们不再追求 pair/sum，而是维护 **leftMax / rightMax**，并在每一步“结算”一侧的水量。

Key twist vs earlier problems: instead of comparing sums/areas, we compare `leftMax` and `rightMax`. The side with the smaller max can be finalized because its limiting wall is known.

---

## ✅ 双指针解法 / Two pointers solution

### 核心思路 / Key idea

- `l, r` 从两端向中间走
- 维护 `leftMax = max(height[0..l])`，`rightMax = max(height[r..end])`
- **如果 `leftMax < rightMax`**：左边的水位上限已确定（被 leftMax 限制），可以计算 `l` 位置的水并 `l += 1`
- 否则：对称处理右边

---

### Python 代码 / Python code

```python
from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        left_max, right_max = 0, 0
        water = 0

        while l < r:
            if height[l] < height[r]:
                # left side is bounded by left_max
                if height[l] >= left_max:
                    left_max = height[l]
                else:
                    water += left_max - height[l]
                l += 1
            else:
                # right side is bounded by right_max
                if height[r] >= right_max:
                    right_max = height[r]
                else:
                    water += right_max - height[r]
                r -= 1

        return water
```

---

## 🔍 手动走一遍 / Quick trace

例子：`[0,1,0,2,1,0,1,3,2,1,2,1]`

- 开始 `l=0, r=11, left_max=0, right_max=0, water=0`
- 右边较高（1 vs 1 走 else），更新 `right_max=1`，`r=10`
- 当左边较小（0 < 2）：左侧可结算，`left_max=0`，`l=1`
- `height[2]=0` 时，`left_max=1`，水 += 1-0 = 1
- ... 最终累计 `water=6`

Why it works: the side with the smaller boundary max is the limiting factor, so we can safely finalize water there without knowing the exact interior structure.

---

## ⏱️ 复杂度 / Complexity

- Time: **O(n)** (each pointer moves at most n steps)
- Space: **O(1)**

---

## 举一反三 / Transfer within this pattern block

- #11 Container With Most Water：移动“短板”来寻找更可能变大的面积
- #15 3Sum：固定一个数 + 双指针夹逼
- #125 Valid Palindrome：两端检查并向内收缩

共同点：
- **每一步移动都基于一个可证明的单调性/界限**，避免 O(n^2)

---

## 📚 References
- LeetCode editorial: https://leetcode.com/problems/trapping-rain-water/editorial/
- NeetCode explanation (video): https://www.youtube.com/watch?v=ZI2z5pq0TqA
- GeeksforGeeks (two-pointer approach): https://www.geeksforgeeks.org/trapping-rain-water/

## 🧒 ELI5

想象你在一排积木之间倒水。某一格能装多少水，只取决于它左边最高的积木和右边最高的积木里较矮的那个。双指针就是从两边往中间走，随时记住“目前看到的最高积木”，然后一格一格把水算出来。

Imagine filling water between blocks. A spot’s water level is capped by the shorter of the tallest block on its left and right. Two pointers walk inward, tracking those tallest blocks and adding water as you go.
