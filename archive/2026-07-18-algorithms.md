# 🧮 Word Search (LeetCode #79) — Backtracking Deep Dive

> **Note:** This is a Saturday. The full content for this topic is in the [Saturday Deep Dive](./2026-07-18-deepdive.md). This file is a reference stub.

## Quick Summary

**Problem:** Given an `m×n` board of characters, determine if a given word exists — formed from sequentially adjacent cells (horizontal or vertical), where each cell may only be used once.

**Pattern:** Backtracking — mark cell as visited (`'#'`), recurse, restore.

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])
    def dfs(r, c, idx):
        if idx == len(word): return True
        if r < 0 or r >= rows or c < 0 or c >= cols: return False
        if board[r][c] != word[idx]: return False
        temp, board[r][c] = board[r][c], '#'
        found = (dfs(r+1,c,idx+1) or dfs(r-1,c,idx+1) or
                 dfs(r,c+1,idx+1) or dfs(r,c-1,idx+1))
        board[r][c] = temp
        return found
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0): return True
    return False
```

**Complexity:** Time `O(m×n×4^L)`, Space `O(L)` (call stack)

🔗 [LeetCode #79](https://leetcode.com/problems/word-search/)
📹 [NeetCode](https://www.youtube.com/watch?v=pfiQ_PS1g8E)

**Block progress:** 6/9 in Backtracking block. Next: Palindrome Partitioning (#131).
