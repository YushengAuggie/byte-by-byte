# 💻 算法 / Algorithms — Day 19
**Topic:** Permutation in String (#567)
**Date:** 2026-04-07

---

💻 **算法 / Algorithms** — #567 Permutation in String (Medium)

🧩 **滑动窗口模式 (4/6)** — building on the template from Day 15

今天的问题是滑动窗口的经典变体：**固定大小窗口**。与寻找“最长/最短”子串不同，这里的窗口大小是固定的（等于目标字符串的长度）。

*Today's problem is a classic variation: **Fixed-Size Window**. Unlike finding the "longest/shortest" substring, the window size here is strictly fixed to the length of the target string.*

🔗 [LeetCode #567](https://leetcode.com/problems/permutation-in-string/) | 🟡 Medium | 📹 [NeetCode Video](https://www.youtube.com/watch?v=UbyhOgBN834)

---

### 🌍 现实场景 / Real-World Analogy

想象你在玩拼字游戏（Scrabble）。你手里有字母 `a, b`，你想在黑板上的长字符串 `eidbaooo` 中寻找是否有一段连续的字母正好能用你手里的字母拼出来（顺序无所谓，只要字母和数量对得上）。这就是寻找“排列”（Permutation）。

*Imagine playing Scrabble. You have letters `a, b`. You want to see if there's a contiguous sequence in the string `eidbaooo` that can be formed using exactly your letters (order doesn't matter, just the counts). That's finding a permutation.*

---

### 🧠 映射到模版 / Map to Pattern Template

排列（Permutation）的本质是：**字符出现的频率完全相同**。
我们维护一个大小恒定为 `len(s1)` 的滑动窗口，在 `s2` 上滑动。每次向右滑动一步：
1. **Expand**: 右边新进来的字符，频率 +1
2. **Shrink**: 左边出去的字符，频率 -1（因为窗口大小固定，所以进一个必须出一个）
3. **Check**: 如果窗口内的字符频率和 `s1` 完全一致，就找到了！

*A permutation means **exact same character frequencies**. We maintain a sliding window of strictly size `len(s1)` over `s2`. For each step right: add the new char, remove the old char from the left, and check if frequencies match.*

---

### 💻 Python 实现 / Python Solution

```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False
            
        # 1. Initialize frequency maps
        s1_count = [0] * 26
        window_count = [0] * 26
        
        for i in range(len(s1)):
            s1_count[ord(s1[i]) - ord('a')] += 1
            window_count[ord(s2[i]) - ord('a')] += 1
            
        # 2. Check the first window
        if s1_count == window_count:
            return True
            
        # 3. Slide the fixed-size window
        left = 0
        for right in range(len(s1), len(s2)):
            # Expand window: add right char
            window_count[ord(s2[right]) - ord('a')] += 1
            
            # Shrink window: remove left char
            window_count[ord(s2[left]) - ord('a')] -= 1
            left += 1
            
            # Check if current window matches
            if s1_count == window_count:
                return True
                
        return False
```

**复杂度 / Complexity:**
- **Time:** $O(N)$ where $N$ is the length of `s2`. Comparing two arrays of size 26 takes $O(1)$ time.
- **Space:** $O(1)$ because the frequency arrays are always size 26, regardless of string length.

---

### 🔄 举一反三 / Connect to Pattern

这道题和 #438 Find All Anagrams in a String 完全一样！Anagram（字母异位词）和 Permutation（排列）在这个语境下是同一个意思。掌握了这个固定窗口频率匹配的技巧，那道题可以直接秒杀。

*This is identical to #438 Find All Anagrams in a String! Anagram and Permutation mean the exact same thing here. Master this fixed-window frequency matching, and you get two problems for the price of one.*

---

### 📚 参考资料 / References
1. [NeetCode: Permutation in String](https://neetcode.io/problems/permutation-in-string)
2. [Sliding Window Pattern — LeetCode Discuss](https://leetcode.com/discuss/study-guide/177204/half-blood-prince-sliding-window)
3. [Python ord() function — W3Schools](https://www.w3schools.com/python/ref_func_ord.asp)

---

### 🧒 ELI5

你要在一条长长的火车上找两节特定的车厢（比如一节红的，一节蓝的，挨在一起）。你拿一个刚好能罩住两节车厢的框，从车头开始往后套。每次往后挪一节，看看框里的颜色对不对。因为框的大小不变，所以每次挪动，前面进来一节，后面就出去一节。

*You're looking for two specific train cars (one red, one blue, next to each other) on a long train. You take a frame that fits exactly two cars and slide it from the front. Each time you move it, one new car enters the frame, and one old car leaves. You just check if the colors inside the frame match what you want!*