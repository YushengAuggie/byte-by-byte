# 💻 算法 / Algorithms — Day 98
**#17 Letter Combinations of a Phone Number** | 🟡 Medium | Backtracking (8/9)

---

🧩 **回溯模式 (8/9)** — building on the template from Day 88

今天是回溯 block 的第 8 题（共 9 题）。模版一样，变化在于：**每一步的 choices 不是固定集合，而是由当前输入字符决定**。

---

## 问题 / Problem

🔗 [LeetCode #17](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | 📹 [NeetCode](https://neetcode.io/problems/phone-number-letter-combinations)

给定数字字符串（如 `"23"`），返回手机九宫格上所有可能的字母组合。

```
2 → abc
3 → def
"23" → ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

**生活类比：** 想象老式 T9 手机打字——每按一个数字键，可能对应多个字母。你想列出所有可能的拼写组合。

---

## 映射到回溯模版 / Pattern Mapping

```python
# 通用模版
def backtrack(path, choices):
    if IS_COMPLETE(path):      # len(path) == len(digits)
        result.append(path[:])
        return
    for choice in choices:     # phone_map[digits[len(path)]]
        path.append(choice)
        backtrack(path, NEXT_CHOICES)  # 自动由下一个 digit 决定
        path.pop()
```

**与前几题的区别 / What's Different:**
| 题目 | choices 来源 | 关键约束 |
|------|------------|---------|
| Subsets #78 | 固定数组索引 | 不重复 |
| Permutations #46 | 剩余未用元素 | 全选 |
| **Phone #17** | **phone_map[digit]** | **每层不同选项集** |

---

## Python 解法 / Solution

```python
from typing import List

def letterCombinations(digits: str) -> List[str]:
    if not digits:
        return []
    
    phone_map = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
    }
    
    result = []
    
    def backtrack(index: int, path: list):
        # Base case: path length == digits length
        if index == len(digits):
            result.append("".join(path))
            return
        
        # Choices: letters for current digit
        for letter in phone_map[digits[index]]:
            path.append(letter)
            backtrack(index + 1, path)  # next digit
            path.pop()  # undo
    
    backtrack(0, [])
    return result

# Trace for "23":
# backtrack(0, []) → choices: a,b,c
#   backtrack(1, [a]) → choices: d,e,f
#     backtrack(2, [a,d]) → DONE → "ad"
#     backtrack(2, [a,e]) → DONE → "ae"
#     backtrack(2, [a,f]) → DONE → "af"
#   backtrack(1, [b]) → "bd","be","bf"
#   backtrack(1, [c]) → "cd","ce","cf"
```

**复杂度 / Complexity:**
- Time: O(4^n × n) — 最多4个字母/digit，n是长度，×n是join操作
- Space: O(n) — 递归深度

---

## 举一反三 / Connect to Pattern Block

```
回溯 Block 进度 (8/9):
✅ #78 Subsets        → 组合，start 递增
✅ #39 Combination Sum → 可重复用，start 不变
✅ #46 Permutations   → 全排列，used[] 标记
✅ #90 Subsets II     → 去重 subsets，排序+skip
✅ #40 Combination Sum II → 去重 combinations
✅ #79 Word Search    → 2D grid + visited
✅ #131 Palindrome Partition → 剪枝 + 回文检查
🎯 #17 Phone Number   → **每层不同 choices（今天）**
⏳ #51 N-Queens       → 最难，二维约束
```

**Phone #17 的独特点：** `choices` 不是常量，而是 `phone_map[digits[index]]` — 每层 choices 都不同，但回溯框架完全不变。

---

## 📚 References
- https://leetcode.com/problems/letter-combinations-of-a-phone-number/
- https://neetcode.io/roadmap
- https://en.wikipedia.org/wiki/E.161 (Phone keypad layout history)

## 🧒 ELI5
想象你要猜一个密码，第一位可能是 a、b、c（数字 2），第二位可能是 d、e、f（数字 3）。你就把所有组合都试一遍：ad、ae、af、bd、be、bf……这就是回溯——系统地把所有路径都走一遍。
