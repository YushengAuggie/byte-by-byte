# 💻 算法 Day 4 / Algorithms Day 4 — #49 Group Anagrams (Medium) — Arrays & Hashing

> **基础阶段 Foundation Phase** | 预计阅读时间 ~3-4 分钟

---

## 现实类比 / Real-World Analogy

想象你在邮局分拣包裹。每个包裹上写的是打乱顺序的地址，比如 "acts", "cats", "tacs" 其实都是同一个地方（字母相同，顺序不同）。你的任务是把所有"相同地址"的包裹放到同一个箱子里。

怎么判断两个地址"本质相同"？把字母排个序，如果排序后一样，就是同一个地址！

At the post office, sorting packages with scrambled addresses: "acts", "cats", "tacs" all go to the same place. Your job: group them together. The trick? Sort the letters — if they match after sorting, they're anagrams!

---

## 题目 / Problem Statement

**给定一个字符串数组，将所有字母异位词（anagram）分组在一起。**

Given an array of strings, group the anagrams together.

```
输入 Input:  ["eat","tea","tan","ate","nat","bat"]
输出 Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
```

字母异位词 = 由相同字母以不同顺序构成的单词
Anagram = words with the same letters in different order

---

## 思路解析 / Step-by-Step Walkthrough

**关键洞察 Key Insight：**
两个字符串互为 anagram，当且仅当它们排序后相同。
Two strings are anagrams if and only if their sorted versions are identical.

所以我们用排序后的字符串作为**哈希表的 key**，把所有 anagram 归到同一个桶（bucket）里。

### 追踪过程 / Trace Through the Example

输入：`["eat","tea","tan","ate","nat","bat"]`

| 当前单词 Word | 排序后 Sorted Key | 哈希表状态 HashMap State |
|------------|----------------|----------------------|
| "eat" | "aet" | {"aet": ["eat"]} |
| "tea" | "aet" | {"aet": ["eat","tea"]} |
| "tan" | "ant" | {"aet": ["eat","tea"], "ant": ["tan"]} |
| "ate" | "aet" | {"aet": ["eat","tea","ate"], "ant": ["tan"]} |
| "nat" | "ant" | {"aet": ["eat","tea","ate"], "ant": ["tan","nat"]} |
| "bat" | "abt" | {"aet": [...], "ant": [...], "abt": ["bat"]} |

最终取哈希表的所有 values → `[["eat","tea","ate"], ["tan","nat"], ["bat"]]`

---

## Python 解法 / Python Solution

```python
from collections import defaultdict

def groupAnagrams(strs: list[str]) -> list[list[str]]:
    # Use a defaultdict so we can append without checking if key exists
    # 用 defaultdict，省去手动判断 key 是否存在的麻烦
    anagram_map = defaultdict(list)
    
    for word in strs:
        # Sort the word's characters to create the canonical key
        # 对字母排序，得到这组 anagram 的"标准形式"
        # e.g., "eat" -> sorted("eat") -> ['a','e','t'] -> "aet"
        key = "".join(sorted(word))
        
        # Append this word to the bucket for its key
        # 把当前单词放入对应的桶
        anagram_map[key].append(word)
    
    # Return all the groups (values of the map)
    # 返回所有分组
    return list(anagram_map.values())
```

### 手动验证 / Manual Verification

让我们用 `["eat","tea","tan","ate","nat","bat"]` 逐步跑代码：

1. `word = "eat"` → `sorted("eat")` = `['a','e','t']` → `key = "aet"` → `anagram_map = {"aet": ["eat"]}`
2. `word = "tea"` → `sorted("tea")` = `['a','e','t']` → `key = "aet"` → `anagram_map = {"aet": ["eat","tea"]}`
3. `word = "tan"` → `sorted("tan")` = `['a','n','t']` → `key = "ant"` → `anagram_map = {"aet": [...], "ant": ["tan"]}`
4. `word = "ate"` → `sorted("ate")` = `['a','e','t']` → `key = "aet"` → `anagram_map = {"aet": ["eat","tea","ate"], "ant": ["tan"]}`
5. `word = "nat"` → `sorted("nat")` = `['a','n','t']` → `key = "ant"` → `anagram_map = {"aet": [...], "ant": ["tan","nat"]}`
6. `word = "bat"` → `sorted("bat")` = `['a','b','t']` → `key = "abt"` → `anagram_map = {"aet": [...], "ant": [...], "abt": ["bat"]}`

最终返回 `[["eat","tea","ate"], ["tan","nat"], ["bat"]]` ✅ 与题目期望输出一致！

---

## 时间/空间复杂度 / Complexity Analysis

**时间复杂度 Time Complexity: O(n × k log k)**
- n = 字符串数量（number of strings）
- k = 最长字符串的长度（max string length）
- 对每个字符串排序 = O(k log k)，总共 n 个字符串

**空间复杂度 Space Complexity: O(n × k)**
- 哈希表存储所有字符串的副本
- 最坏情况：所有字符串都不是 anagram，每个单独一个桶

---

## 边界情况 / Edge Cases

```python
# 空数组 Empty input
groupAnagrams([])  # → []

# 单个字符串 Single string
groupAnagrams(["a"])  # → [["a"]]

# 所有字符串都是 anagram All are anagrams
groupAnagrams(["abc","bca","cab"])  # → [["abc","bca","cab"]]

# 没有 anagram 对 No anagram pairs
groupAnagrams(["abc","def","ghi"])  # → [["abc"],["def"],["ghi"]]
```

---

## 举一反三 / Pattern Recognition

**这道题的模式：用排序/哈希创建"规范形式"（Canonical Form）**

当你需要"把等价的东西归类"时，找到一个好的 key 是关键。

**同类变体 / Follow-up Variations:**

1. **#242 Valid Anagram（Day 2 做过！）** — 判断两个字符串是否互为 anagram，现在你应该更理解为什么用哈希表了

2. **用字符计数作 key（优化版）** — 不排序，而是统计 26 个字母的频率，构成一个 tuple 作 key。时间复杂度降到 O(n × k)：
   ```python
   key = tuple(Counter(word).values())  # 不推荐，顺序不固定
   # 更好的方式：
   count = [0] * 26
   for c in word:
       count[ord(c) - ord('a')] += 1
   key = tuple(count)  # e.g., "eat" -> (1,0,0,0,1,0,...,1,...) [a=1,e=1,t=1]
   ```

3. **思考扩展：** 如果字符串包含 Unicode 字符怎么办？用 `Counter` 而非固定 26 位数组

---

*Day 4 / 100 — Arrays & Hashing 系列*
*昨天 Day 3：Two Sum | 明天 Day 5：Top K Frequent Elements*
