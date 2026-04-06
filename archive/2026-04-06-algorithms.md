💻 **算法 Day 17 / Algorithms Day 17** — #424 Longest Repeating Character Replacement (Medium) — Sliding Window

🧩 **滑动窗口模式 (3/6)** — building on the template from Day 16

今天我们将继续使用滑动窗口模式。这道题的特别之处在于，窗口的“有效性”不是由简单的总和决定的，而是由“窗口内最多出现的字符”和“允许替换的次数”共同决定的。
*Today we continue with the Sliding Window pattern. The twist here is that the window's "validity" isn't determined by a simple sum, but by the "most frequent character in the window" combined with the "allowed replacements".*

### 🔗 题目链接 / Links
- 🔗 [LeetCode #424](https://leetcode.com/problems/longest-repeating-character-replacement/)
- 🟡 Medium
- 📹 [NeetCode Video](https://www.youtube.com/watch?v=gqXU1UyA8pk)

### 💡 现实场景 / Real-world Analogy
想象你在玩拼字游戏，你有一排字母，并且你有 `k` 张“万能牌”（可以变成任何字母）。你想弄出最长的一段完全相同的字母。你会怎么做？你会找一段本身就有很多相同字母的区域，然后把里面少数不同的字母用万能牌替换掉。
*Imagine playing Scrabble. You have a row of letters and `k` "wildcards" (can be any letter). You want to make the longest contiguous sequence of the same letter. What do you do? You find a section that already has a lot of the same letter, and use your wildcards to replace the few different ones.*

### 🧠 映射到模版 / Map to Pattern Template
- **窗口扩张 (Expand)**: 右指针 `right` 向右移动，将新字符加入计数器。
- **违规条件 (Condition Violated)**: `窗口长度 - 窗口内出现次数最多的字符的数量 > k`。这意味着即使把所有其他字符都替换掉，替换次数 `k` 也不够用了。
- **窗口收缩 (Shrink)**: 左指针 `left` 向右移动，将移出窗口的字符从计数器中减去。

### 💻 Python 实现 / Python Solution
```python
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}
        res = 0
        left = 0
        maxf = 0 # Track the count of the most frequent character
        
        for right in range(len(s)):
            # Expand window
            count[s[right]] = 1 + count.get(s[right], 0)
            # Optimization: we only care about the historical max frequency
            maxf = max(maxf, count[s[right]])
            
            # Condition violated: replacements needed > k
            while (right - left + 1) - maxf > k:
                # Shrink window
                count[s[left]] -= 1
                left += 1
                
            res = max(res, right - left + 1)
            
        return res
```

### ⏱️ 复杂度 / Complexity
- **Time**: $O(N)$。右指针遍历一次字符串，左指针最多遍历一次。
- **Space**: $O(26) = O(1)$。哈希表最多存储 26 个大写英文字母。

### 🔄 举一反三 / Connect to Pattern
这道题与 #3 Longest Substring Without Repeating Characters 类似，都是在窗口不满足条件时移动左指针。区别在于 #3 的条件是“有重复字符”，而本题的条件是“需要替换的字符超过了 k”。

### 📚 延伸阅读 / References
- [NeetCode: Sliding Window](https://neetcode.io/courses/advanced-algorithms/0)

### 🧒 ELI5 (Explain Like I'm 5)
你想用积木搭一座纯色的塔，但你只有 `k` 块可以变色的魔法积木。你圈出一堆积木（窗口），数数里面哪种颜色最多。如果总积木数减去最多颜色的积木数，比你的魔法积木 `k` 还要多，说明魔法不够用了，你就得把圈子左边的积木扔出去，直到魔法够用为止。