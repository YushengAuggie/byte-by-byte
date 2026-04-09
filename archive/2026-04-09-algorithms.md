💻 **算法 / Algorithms** — #76 Minimum Window Substring (Hard) — Sliding Window

🧩 **滑动窗口模式 (5/6)** — building on the template from Day 19
这个题目是滑动窗口的终极形态。与之前的题目不同，这里我们需要在窗口内包含目标字符串 `t` 的所有字符，并且要求**最短**的窗口。
This is the ultimate form of the sliding window. Unlike previous problems, we need to include all characters of the target string `t` in the window, and we want the **shortest** window.

🔗 [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/) | 🔴 Hard | 📹 [NeetCode](https://www.youtube.com/watch?v=jSto0O4PIzM)

**现实类比 / Real-world Analogy**
想象你在寻宝，你需要收集一套特定的宝石（字符串 `t`）。你沿着一条路（字符串 `s`）走，把路上的宝石都捡起来（右指针扩张）。一旦你集齐了所有需要的宝石，你就开始扔掉最早捡到的没用的宝石（左指针收缩），直到你不能再扔为止，这时候你手里的宝石就是最短的有效集合。
Imagine you are treasure hunting and need a specific set of gems (string `t`). You walk along a path (string `s`), picking up gems (right pointer expands). Once you have all the required gems, you start dropping the earliest useless ones (left pointer shrinks) until you can't drop any more. The gems you hold at that moment form the shortest valid set.

**映射到模式 / Map to Pattern**
- **Expand (Right Pointer):** 将字符加入窗口频率字典。如果该字符是 `t` 中需要的，并且频率达到了要求，则 `have` 计数器加一。
- **Shrink (Left Pointer):** 当 `have == need` 时，说明当前窗口有效。记录当前窗口大小和位置，然后尝试收缩：移除左指针字符，如果该字符是 `t` 中需要的且频率低于要求，则 `have` 减一。左指针右移。

**Python Solution**
```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if t == "": return ""

        countT, window = {}, {}
        for c in t:
            countT[c] = 1 + countT.get(c, 0)

        have, need = 0, len(countT)
        res, resLen = [-1, -1], float("infinity")
        l = 0

        for r in range(len(s)):
            c = s[r]
            window[c] = 1 + window.get(c, 0)

            if c in countT and window[c] == countT[c]:
                have += 1

            while have == need:
                # update our result
                if (r - l + 1) < resLen:
                    res = [l, r]
                    resLen = (r - l + 1)
                
                # pop from the left of our window
                window[s[l]] -= 1
                if s[l] in countT and window[s[l]] < countT[s[l]]:
                    have -= 1
                l += 1
                
        l, r = res
        return s[l:r+1] if resLen != float("infinity") else ""
```

**复杂度 / Complexity**
- Time: O(N + M) where N is len(s) and M is len(t). Each character is visited at most twice.
- Space: O(1) if we consider the character set is fixed (e.g., 26 letters or 128 ASCII characters).

**举一反三 / Connect to other problems**
- 这是滑动窗口求**最短**子串的经典题。对比 #3 Longest Substring Without Repeating Characters，那是求**最长**，所以是在不满足条件时收缩；而本题是求最短，是在**满足**条件时收缩。

**📚 References**
- [NeetCode 76. Minimum Window Substring](https://neetcode.io/problems/minimum-window-with-characters)
- [LeetCode Discuss: Sliding Window template](https://leetcode.com/problems/find-all-anagrams-in-a-string/discuss/92007/Sliding-Window-algorithm-template-to-solve-all-the-Leetcode-substring-search-problem.)

**🧒 ELI5**
一直往右走，直到集齐了所有需要的卡片。然后看看能不能把最左边没用的卡片扔掉，让手里的卡片越少越好。
Keep walking right until you collect all the needed cards. Then see if you can throw away useless cards from the left to make your hand as small as possible.
