# Day 99 — Algorithms: #51 N-Queens (Hard) — Backtracking

## 💻 算法 / Algorithms — #51 N-Queens (Hard)

🧩 **回溯模式 (9/9)** — The grand finale of this block! 构建在模版上的终极挑战

---

### 模式回顾 / Pattern Review
这是回溯块的第9题，也是最后一题。回顾一下模版：

This is the 9th and final problem in the backtracking block. Quick template recap:

```python
def backtrack(path, choices):
    if IS_COMPLETE(path):
        result.append(path[:])
        return
    for choice in choices:
        if IS_VALID(choice):
            path.append(choice)
            backtrack(path, NEXT_CHOICES)
            path.pop()  # undo
```

---

### 真实类比 / Real-World Analogy

想象你要在8×8国际象棋棋盘上放8个皇后，每个皇后可以攻击同行、同列、同对角线的所有格子。你每行放一个，一旦发现冲突就回退，换个位置。

Imagine placing 8 queens on a chessboard so no queen can attack another — same row, column, or diagonal is invalid. Place one per row; if conflict detected, backtrack and try next column.

---

### 问题 / Problem

[🔗 LeetCode #51](https://leetcode.com/problems/n-queens/) 🔴 Hard | [📹 NeetCode](https://neetcode.io/problems/n-queens)

Given an integer `n`, return all distinct solutions to the n-queens puzzle. Each solution contains a distinct board configuration.

---

### 如何映射到模版 / Mapping to Template

| 模版概念 | N-Queens 对应 |
|---|---|
| `path` | 每行皇后所在的列号 `[col0, col1, ...]` |
| `IS_COMPLETE` | `len(path) == n` |
| `choices` | 列号 `0..n-1` |
| `IS_VALID` | 没有列冲突、没有对角线冲突 |
| `NEXT_CHOICES` | 下一行的列号 |

**关键洞察：每行只放一个皇后**，所以行冲突自动不存在。只需检查列和对角线。

Key insight: we place exactly one queen per row, so row conflicts are impossible. Only check column and diagonal.

---

### Python 解法 / Solution

```python
def solveNQueens(n: int) -> list[list[str]]:
    result = []
    # Track which cols and diagonals are occupied
    cols = set()
    pos_diag = set()  # (row + col) same for each positive diagonal
    neg_diag = set()  # (row - col) same for each negative diagonal
    
    board = [['.' for _ in range(n)] for _ in range(n)]
    
    def backtrack(row: int) -> None:
        if row == n:
            # Convert board to required format
            result.append([''.join(r) for r in board])
            return
        
        for col in range(n):
            # IS_VALID check
            if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                continue
            
            # CHOOSE
            cols.add(col)
            pos_diag.add(row + col)
            neg_diag.add(row - col)
            board[row][col] = 'Q'
            
            # RECURSE
            backtrack(row + 1)
            
            # UNDO (backtrack)
            cols.remove(col)
            pos_diag.remove(row + col)
            neg_diag.remove(row - col)
            board[row][col] = '.'
    
    backtrack(0)
    return result

# Trace n=4:
# row=0: try col=1 → valid → board[0][1]='Q'
#   row=1: try col=3 → valid (no col conflict, diag: 1+1≠3+0, 1-1≠3-1... check) 
#   → board[1][3]='Q'
#     row=2: try col=0 → valid → board[2][0]='Q'
#       row=3: try col=2 → valid → board[3][2]='Q' → SOLUTION ✅
```

**时间复杂度:** O(n!) — n choices for row 0, n-1 for row 1, etc.
**空间复杂度:** O(n²) for board storage

---

### 关键优化：对角线的数学 / Diagonal Math

对角线碰撞的判断是这道题最巧妙的地方：

The diagonal trick is the key insight:
- **正对角线（↗）**: `row + col` is constant along the same diagonal
- **负对角线（↙）**: `row - col` is constant along the same diagonal

```
row=0, col=2: pos_diag = 2, neg_diag = -2
row=1, col=1: pos_diag = 2 ← SAME! They're on the same diagonal
row=1, col=3: pos_diag = 4, neg_diag = -2 ← neg_diag conflict with (0,2)!
```

---

### 举一反三：整个回溯块回顾 / Block Retrospective

| 问题 | 关键变体 | 剪枝策略 |
|---|---|---|
| #78 Subsets | No duplicates, no constraints | None needed |
| #39 Combination Sum | Reuse elements allowed | Skip if `target < 0` |
| #46 Permutations | Order matters, no repeats | Use `visited` set |
| #90 Subsets II | **Duplicates** in input | Sort + skip same element at same level |
| #40 Combination Sum II | Each element once, deduplicate | Sort + skip |
| #79 Word Search | 2D grid, mark visited | Mark cell, unmark on backtrack |
| #131 Palindrome Partitioning | Check palindrome validity | Precompute palindrome table |
| #17 Phone Numbers | Map digits to letters | None needed |
| **#51 N-Queens** | **Constraint satisfaction** | **Set-based O(1) validity** |

**核心洞察：剪枝越早，速度越快。** N-Queens 用 O(1) set lookup 代替 O(n) board scan。

Core insight: prune early, prune fast. N-Queens uses O(1) set lookup instead of O(n) board scan.

---

### 📝 Quiz
```json
{"question":"In N-Queens, what condition do two queens on (r1,c1) and (r2,c2) share if they're on the same positive diagonal?","options":["r1+c1 == r2+c2","r1-c1 == r2-c2","r1*c1 == r2*c2","abs(r1-r2) == abs(c1-c2) and r1==r2"],"correct_index":0}
```

---

### 📚 References
- https://leetcode.com/problems/n-queens/
- https://neetcode.io/problems/n-queens
- https://en.wikipedia.org/wiki/Eight_queens_puzzle

### 🧒 ELI5
在棋盘上放皇后，皇后会攻击同行同列同斜线。每行放一个，放不了就退回来换列，直到每行都有一个安全的皇后为止。就像解数独：尝试 → 发现冲突 → 擦掉 → 换一个。

Place queens on a chessboard where each queen attacks its row, column, and diagonals. Place one per row, backtrack when stuck, until every row has a safe queen. Like solving a Sudoku: try → find conflict → erase → try next.
