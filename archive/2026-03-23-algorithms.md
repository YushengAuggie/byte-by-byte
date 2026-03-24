💻 **算法 Day 8 (4 min read) / Algorithms Day 8**
**#36 Valid Sudoku (Medium) — Arrays & Hashing**

🔗 [LeetCode #36: Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) 🟡 Medium
📹 [NeetCode Solution](https://neetcode.io/problems/valid-sudoku)

---

**🌎 Real-World Analogy / 现实类比**

想象你是数独比赛的裁判。你不需要解出整个数独，只需要检查当前填入的数字是否违规 — 同一行、同一列、同一个 3×3 宫格内有没有重复数字。

---

**题目 / Problem**

判断一个 9×9 的数独棋盘是否有效。只需验证已填入的数字是否合法：
- 每行不能有重复数字
- 每列不能有重复数字
- 每个 3×3 宫格不能有重复数字

```
Input:
[["5","3",".",".","7",".",".",".","."]
 ["6",".",".","1","9","5",".",".","."]
 [".","9","8",".",".",".",".","6","."]
 ["8",".",".",".","6",".",".",".","3"]
 ["4",".",".","8",".","3",".",".","1"]
 ["7",".",".",".","2",".",".",".","6"]
 [".","6",".",".",".",".","2","8","."]
 [".",".",".","4","1","9",".",".","5"]
 [".",".",".",".","8",".",".","7","9"]]
Output: True
```

---

**核心洞察 / Key Insight**

用 3 组 HashSet 追踪已见数字：
- `rows[i]` — 第 i 行已有的数字
- `cols[j]` — 第 j 列已有的数字
- `boxes[i//3][j//3]` — 第 (i//3, j//3) 宫格已有的数字

关键：`(i // 3, j // 3)` 把 9×9 映射到 3×3 宫格索引！

```
行列 → 宫格映射:
(0,0)→(0,0)  (0,3)→(0,1)  (0,6)→(0,2)
(3,0)→(1,0)  (3,3)→(1,1)  (3,6)→(1,2)
(6,0)→(2,0)  (6,3)→(2,1)  (6,6)→(2,2)
```

---

**Python 解法 / Solution**

```python
from collections import defaultdict

def isValidSudoku(board):
    rows = defaultdict(set)    # rows[i] = set of nums in row i
    cols = defaultdict(set)    # cols[j] = set of nums in col j
    boxes = defaultdict(set)   # boxes[(i//3, j//3)] = set of nums in box

    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num == '.':
                continue

            box_key = (i // 3, j // 3)

            if num in rows[i] or num in cols[j] or num in boxes[box_key]:
                return False  # Duplicate found!

            rows[i].add(num)
            cols[j].add(num)
            boxes[box_key].add(num)

    return True
```

**Trace (first few cells):**
- (0,0)="5": rows[0]={5}, cols[0]={5}, boxes[(0,0)]={5} ✅
- (0,1)="3": rows[0]={5,3}, cols[1]={3}, boxes[(0,0)]={5,3} ✅
- (0,4)="7": rows[0]={5,3,7}, cols[4]={7}, boxes[(0,1)]={7} ✅
- ...遍历完所有非空格，无冲突 → True ✅

---

**⏱️ Complexity**
- Time: O(81) = O(1) — 固定 9×9 棋盘
- Space: O(81) = O(1) — 最多存 81 个数字

---

**举一反三 / Pattern Recognition**

HashSet 验证唯一性 — "seen before?" 模式：
- 🟢 [LeetCode #217: Contains Duplicate](https://leetcode.com/problems/contains-duplicate/)
- 🟡 [LeetCode #49: Group Anagrams](https://leetcode.com/problems/group-anagrams/)
- 🔴 [LeetCode #37: Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) (回溯法)

---

📚 **深入学习 / Learn More:**
• 📹 [NeetCode Solution Video](https://neetcode.io/problems/valid-sudoku)
• [NeetCode Roadmap: Arrays & Hashing](https://neetcode.io/roadmap)
• [LeetCode #37: Sudoku Solver](https://leetcode.com/problems/sudoku-solver/) — 进阶：从验证到求解

🧒 **ELI5:** Checking a Sudoku board is like being a hall monitor — you walk down each row, each column, and peek into each 3×3 room, making sure nobody snuck in twice!
