# 💻 算法 / Algorithms — Day 78
**#212 Word Search II** | 🔴 Hard | **Pattern: Tries (3/3)**

🔗 [LeetCode #212](https://leetcode.com/problems/word-search-ii/) | 📹 [NeetCode Solution](https://neetcode.io/problems/word-search-ii)

---

## 🧩 前缀树模式 (3/3) — 本系列最终章

```
Trie Block 总览:
  Day 74: #208 Implement Trie (Medium)          ← 建模板
  Day 76: #211 Add and Search Words (Medium)     ← 加通配符 .
  Day 78: #212 Word Search II (Hard)             ← TODAY: Trie + DFS
```

这是 Trie 系列的终极 Boss！把 Trie 嵌入 DFS 回溯，实现在矩阵里同时搜索多个单词。

---

## 真实类比 / Real-world Analogy

想象你有一张巨大的字母瓷砖地图，要在地图上找到所有词典里的单词。暴力方法：对每个单词跑一遍 DFS。聪明方法：**把词典压进 Trie，DFS 时同时在 Trie 上走** —— 一旦没有前缀匹配，立刻剪枝，不用继续搜下去。

You have a grid of letter tiles. Find all words from a dictionary that can be formed by following adjacent cells. Brute force: run DFS for every word. Smart: **load the dictionary into a Trie, walk Trie + grid simultaneously** — prune immediately when no prefix matches.

---

## 题目 / Problem

```
board = [
  ['o','a','a','n'],
  ['e','t','a','e'],
  ['i','h','k','r'],
  ['i','f','l','v']
]
words = ["oath","pea","eat","rain"]
Output: ["eat","oath"]
```

---

## 模式映射 / Pattern Mapping

| 单独用 DFS | Trie + DFS |
|-----------|-----------|
| 对每个单词 DFS：O(W × M×N×4^L) | 所有单词共享一次 DFS：O(M×N×4^L) |
| 无法早期剪枝 | 只要 Trie 没有当前前缀，立刻停止 |
| words=10000 时超时 | words=10000 依然可行 |

**核心洞察**：Trie 把"前缀共享"的优势带入了搜索过程。

---

## Python 解法 + 逐步追踪 / Solution + Trace

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # store full word at end node (not just True)

class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        # Step 1: Build Trie from word list
        root = TrieNode()
        for w in words:
            node = root
            for ch in w:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.word = w  # mark end

        rows, cols = len(board), len(board[0])
        result = set()

        def dfs(r, c, node):
            ch = board[r][c]
            if ch not in node.children:
                return  # prune: no prefix match in Trie

            next_node = node.children[ch]

            if next_node.word:
                result.add(next_node.word)
                next_node.word = None  # avoid duplicates

            # Mark visited by overwriting (cheaper than a visited set)
            board[r][c] = '#'

            for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                    dfs(nr, nc, next_node)

            board[r][c] = ch  # restore

            # Optimization: prune empty Trie nodes (key insight!)
            if not next_node.children:
                del node.children[ch]

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)

        return list(result)
```

**追踪示例 / Trace:**
```
从 (1,2)='a' 开始，找 "eat":
  root → 'e'? 不在 board[1][2]='a' 的邻居里...
  
从 (1,1)='t' 开始，找 "eat":
  root 里有 'e'? (1,0)='e' 是邻居
  → dfs(1,0,'e') → Trie node 'e'
    → 邻居 (0,0)='o'? Trie 下一步是 'a', 不匹配
    → 邻居 (1,1)='t'? Trie 下一步是 'a', 不匹配
    → 邻居 (2,0)='i'? 不匹配
  
从 (0,1)='a' 开始:
  root 里有 'e'? (1,1)='t' 邻居... 找到 e→a→t 路径!
  → found "eat" ✓
```

**复杂度 / Complexity:**
- Time: O(M×N×4^L) where L = max word length (Trie 剪枝大幅减少实际路径)
- Space: O(N×L) for Trie — N words × avg length L

---

## 关键优化 / Key Optimizations

### 1. 存完整单词，不存布尔值
```python
node.word = w  # better than node.is_end = True
```
找到时直接加入结果，不需要重建单词。

### 2. 原地标记已访问
```python
board[r][c] = '#'  # overwrite, not a separate visited set
...
board[r][c] = ch   # restore after DFS
```
省去 O(M×N) 的 visited 数组。

### 3. 修剪空 Trie 节点（最关键优化！）
```python
if not next_node.children:
    del node.children[ch]
```
找到单词后，从 Trie 里删除叶节点。随着更多单词被找到，Trie 越来越小，后续 DFS 剪枝更激进。

---

## 举一反三 / Pattern Connections

| 题目 | 和 Word Search II 的关系 |
|------|------------------------|
| #208 Implement Trie | Word Search II 的核心数据结构 |
| #211 Add and Search Words | 同样 Trie + DFS，但 '.' 通配符换成了矩阵的4方向 |
| #79 Word Search I | Word Search II 的简化版：单词 → 多单词 |
| Boggle Game | Word Search II 的现实应用 |

---

## 📚 References

- 🔗 [LeetCode #212](https://leetcode.com/problems/word-search-ii/)
- 🔗 [NeetCode Video Explanation](https://neetcode.io/problems/word-search-ii)
- 🔗 [Trie + DFS Pattern Guide](https://leetcode.com/discuss/general-discussion/1125813/trie-question-patterns)

---

## 🧒 ELI5

想象玩一个字母找词游戏：一张字母格子地图，找出所有词典里能走出来的单词。

笨方法：拿着词典，每个词在地图上走一遍。10000 个词 = 走 10000 遍。

聪明方法：**先把词典变成一棵"前缀树"（Trie）**。比如 "eat", "east", "easy" 都从 'e'→'a' 开始，在树上共享这两步。

然后在地图上 DFS，同时在 Trie 上走。一走进地图某格，就问 Trie："这条路有单词吗？" 没有前缀匹配→直接放弃，不用继续往下走。

就像迷宫里，你走到一扇门，门上写"此路绝对没有出口"，你就不用进去了！
