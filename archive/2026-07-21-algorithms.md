# 算法 / Algorithms — Day 96

**Day 96 | #79 Word Search | Medium | Backtracking (6/9)**

---

## 💻 算法 / Algorithms
### #79 Word Search — 回溯在二维网格上的应用

🧩 **回溯模式 (6/9)** — building on the template from Day 88 (Subsets)

今天是回溯模式第 6 题。前面我们做了：子集、组合求和、全排列……今天把回溯搬到 **2D 网格** 上。本质没变，只是 "choices" 变成了四个方向。

---

### 🔗 Links
- 🔗 [LeetCode #79](https://leetcode.com/problems/word-search/) 🟡 Medium
- 📹 [NeetCode Video](https://neetcode.io/problems/search-for-word)

---

### 🌍 Real-World Analogy
想象你在 Wordle 的升级版 — 一个字母网格里找单词，每个格子只能用一次，可以上下左右走。这就是 Word Search。

Imagine a word-search puzzle you find in newspapers. Given a grid of letters, find if a specific word exists by navigating horizontally or vertically, without reusing any cell.

---

### 📋 Problem
```
Given an m×n grid of characters and a string word,
return true if word exists in the grid.
The word must be constructed from adjacent cells (horizontal/vertical).
Each cell may only be used once.

Example:
board = [["A","B","C","E"],
         ["S","F","C","S"],
         ["A","D","E","E"]]
word = "ABCCED" → True
word = "SEE"    → True
word = "ABCB"   → False
```

---

### 🗺️ 映射到回溯模版 / Map to Pattern Template

```python
def backtrack(path, choices):
    if IS_COMPLETE(path):        # 找到 word 所有字符
        return True
    for choice in choices:       # 4 个方向
        if IS_VALID(choice):     # 在边界内 + 未访问 + 字符匹配
            path.append(choice)  # 标记已访问
            backtrack(...)
            path.pop()           # 撤销标记
```

**关键区别 vs 之前的题 / Key Difference vs Previous Problems:**
- 之前：choices = 数组中的数字
- 今天：choices = 网格中的 4 个方向坐标
- 之前：path = 数字列表
- 今天：path = 已访问的格子（用 visited 标记代替显式 path）

---

### 🐍 Python Solution

```python
def exist(board: list[list[str]], word: str) -> bool:
    ROWS, COLS = len(board), len(board[0])
    
    def backtrack(r, c, idx):
        # Base case: found all characters
        if idx == len(word):
            return True
        
        # Bounds + character match + not visited
        if (r < 0 or r >= ROWS or 
            c < 0 or c >= COLS or
            board[r][c] != word[idx]):
            return False
        
        # Mark visited by temporarily modifying board
        temp = board[r][c]
        board[r][c] = '#'   # Mark as visited
        
        # Explore all 4 directions
        found = (backtrack(r+1, c, idx+1) or
                 backtrack(r-1, c, idx+1) or
                 backtrack(r, c+1, idx+1) or
                 backtrack(r, c-1, idx+1))
        
        board[r][c] = temp  # Undo: restore original character
        return found
    
    # Try starting from every cell
    for r in range(ROWS):
        for c in range(COLS):
            if backtrack(r, c, 0):
                return True
    return False
```

**Trace on "ABCCED":**
```
Start at (0,0)='A' ✓ idx=0
  → (0,1)='B' ✓ idx=1
    → (0,2)='C' ✓ idx=2
      → (1,2)='C' ✓ idx=3
        → (2,2)='E' ✓ idx=4
          → (2,1)='D' ✓ idx=5 → return True ✓
```

---

### ⏱️ Complexity
- **Time:** O(M·N·4^L) where L = len(word)
  - M·N starting positions, each path has ≤ 4^L branches
  - In practice much faster due to early pruning
- **Space:** O(L) — recursion depth = word length

---

### ✂️ 剪枝优化 / Pruning Optimization

```python
# If word is long and starts with rare char, reverse it
# This can reduce search space significantly
from collections import Counter

def exist_optimized(board, word):
    # Count chars in board and word
    board_count = Counter(c for row in board for c in row)
    word_count = Counter(word)
    
    # If word needs more of a char than board has → False
    for c, cnt in word_count.items():
        if board_count[c] < cnt:
            return False
    
    # Optional: reverse word if last char rarer than first
    # (reduces branching factor at start)
    if board_count[word[0]] > board_count[word[-1]]:
        word = word[::-1]
    
    # ... rest of backtrack same as above
```

---

### 🔁 举一反三 / Pattern Connections

| Problem | 和今天的关系 |
|---|---|
| #78 Subsets | 最基础的回溯框架 |
| #39 Combination Sum | 回溯 + 剪枝 (sum > target) |
| #46 Permutations | 回溯 + visited 数组 |
| **#79 Word Search** | **回溯 + 2D 网格 + 原地标记** |
| #131 Palindrome Partitioning | 下一题：回溯 + 字符串分割 |
| #51 N-Queens (Hard) | 回溯 + 约束剪枝的最终 Boss |

**核心规律：** 所有回溯题都是 "选择 → 递归 → 撤销"。变的只是搜索空间的形状。

---

### 📚 References
- [LeetCode #79 Word Search](https://leetcode.com/problems/word-search/)
- [NeetCode Backtracking Playlist](https://neetcode.io/roadmap)
- [Backtracking Explained](https://medium.com/algorithms-and-leetcode/backtracking-e001561b9f28)

### 🧒 ELI5
就像在字母汤里找单词。从每个字母开始，沿着上下左右走，走错了就退回来换个方向，直到找到完整的单词或者所有路都走不通。

---

**Quiz JSON:** `/tmp/bbb-quiz-2.json`
