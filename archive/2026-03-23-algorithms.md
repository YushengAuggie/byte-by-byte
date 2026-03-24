# 💻 算法 Day 8 / Algorithms Day 8
**题目 / Problem:** #36 Valid Sudoku · 🟡 Medium
**模式 / Pattern:** Arrays & Hashing

🔗 [LeetCode #36](https://leetcode.com/problems/valid-sudoku/) · 📹 [NeetCode Video](https://www.youtube.com/watch?v=TjFXEUCMqI8)

---

## 🌍 真实类比 / Real-World Analogy

想象你是数独游戏的裁判。你不需要**解开**这个数独——只需要检查当前状态是否**合法**（没有行、列、3×3格子里有重复数字）。就像检查停车场：不是找空位，而是确认没有两辆车占同一个格子。

*Imagine you're a Sudoku referee. You don't need to solve the puzzle — just verify the current state is valid (no duplicate numbers in any row, column, or 3×3 box). Like checking a parking lot: not finding empty spots, but confirming no two cars share the same space.*

---

## 🧩 题目 / Problem

给定一个 9×9 的数独棋盘，判断是否有效。规则：  
- 每行数字 1-9 不重复  
- 每列数字 1-9 不重复  
- 每个 3×3 子格数字 1-9 不重复  
- 空格用 `'.'` 表示

*Given a 9×9 Sudoku board, determine if it is valid. Rules: no duplicates in any row, column, or 3×3 box. Empty cells are `'.'`.*

---

## 💡 关键洞察 / Key Insight

**用哈希集合跟踪所见数字。** 同时遍历三种结构：行、列、3×3格。  
**关键公式：** 位于 `(r, c)` 的格子属于哪个 3×3 格？ → `box_id = (r // 3) * 3 + (c // 3)`

*Use hash sets to track seen numbers simultaneously across rows, columns, and 3×3 boxes.*  
*Key formula: which box does cell `(r, c)` belong to? → `box_id = (r // 3) * 3 + (c // 3)`*

```
Box IDs:
┌───────┬───────┬───────┐
│ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │
│ box 0 │ box 1 │ box 2 │
├───────┼───────┼───────┤
│ box 3 │ box 4 │ box 5 │
├───────┼───────┼───────┤
│ box 6 │ box 7 │ box 8 │
└───────┴───────┴───────┘
r=0,c=0: (0//3)*3+(0//3) = 0*3+0 = box 0 ✅
r=1,c=4: (1//3)*3+(4//3) = 0*3+1 = box 1 ✅
r=4,c=7: (4//3)*3+(7//3) = 1*3+2 = box 5 ✅
```

---

## 🐍 Python 解法 / Python Solution

```python
from collections import defaultdict

def isValidSudoku(board):
    # Use sets for each row, col, box
    rows = defaultdict(set)   # rows[r] = set of digits seen in row r
    cols = defaultdict(set)   # cols[c] = set of digits seen in col c
    boxes = defaultdict(set)  # boxes[b] = set of digits seen in box b

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == '.':
                continue  # Skip empty cells

            box_id = (r // 3) * 3 + (c // 3)

            # Check for duplicates
            if val in rows[r] or val in cols[c] or val in boxes[box_id]:
                return False

            # Record this value
            rows[r].add(val)
            cols[c].add(val)
            boxes[box_id].add(val)

    return True
```

---

## 🔍 代码追踪 / Code Trace

Using a small example focusing on the top-left 3×3 box (box 0):

```
board[0] = ["5","3",".",".","7",".",".",".","."]
board[1] = ["6",".",".","1","9","5",".",".","."]
board[2] = [".","9","8",".",".",".",".","6","."]

Processing r=0, c=0: val="5"
  box_id = (0//3)*3 + (0//3) = 0
  "5" not in rows[0]={}, cols[0]={}, boxes[0]={} → OK
  rows[0]={"5"}, cols[0]={"5"}, boxes[0]={"5"}

Processing r=0, c=1: val="3"
  box_id = (0//3)*3 + (1//3) = 0
  "3" not in rows[0]={"5"}, cols[1]={}, boxes[0]={"5"} → OK
  rows[0]={"5","3"}, cols[1]={"3"}, boxes[0]={"5","3"}

Processing r=1, c=0: val="6"
  box_id = (1//3)*3 + (0//3) = 0
  "6" not in rows[1]={}, cols[0]={"5"}, boxes[0]={"5","3"} → OK
  boxes[0]={"5","3","6"}

Processing r=2, c=1: val="9"
  box_id = (2//3)*3 + (1//3) = 0
  "9" not in boxes[0]={"5","3","6"} → OK

Processing r=2, c=2: val="8"
  box_id = 0
  "8" not in boxes[0]={"5","3","6","9"} → OK
  boxes[0]={"5","3","6","9","8"}

Final result: True ✅ (valid board)
```

---

## ⏱️ 复杂度 / Complexity

| | 时间 Time | 空间 Space |
|---|---|---|
| 复杂度 | O(9²) = **O(81) = O(1)** | O(9²) = **O(1)** |
| 说明 | 固定 81 格，常数时间 | 最多存 81 个数字 |

*Board is always 9×9 — technically O(1) since input size is fixed!*

---

## 🔄 举一反三 / Pattern Recognition

掌握"哈希集合去重"模式后，还能解：  
*Once you master "hash set deduplication," apply it to:*

- [#48 Rotate Image](https://leetcode.com/problems/rotate-image/) — in-place matrix transformation
- [#54 Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) — matrix traversal order
- [#289 Game of Life](https://leetcode.com/problems/game-of-life/) — state tracking in grids
- [#73 Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) — flagging with sets

---

## 📚 References

- [LeetCode #36 Valid Sudoku](https://leetcode.com/problems/valid-sudoku/)
- [NeetCode Solution Video](https://www.youtube.com/watch?v=TjFXEUCMqI8)
- [Python defaultdict docs](https://docs.python.org/3/library/collections.html#collections.defaultdict)

## 🧒 ELI5

想象你有9张纸，每张代表一行。遇到数字就写到对应行的纸上。如果那张纸上**已经有了**这个数字，就说明不合法！同样对列和3×3格子也这样检查。

*Imagine 9 sheets of paper, one per row. When you see a number, write it on that row's sheet. If the sheet already has that number — invalid! Do the same for columns and 3×3 boxes.*
