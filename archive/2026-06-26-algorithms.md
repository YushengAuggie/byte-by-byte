# 💻 算法 / Algorithms — Day 62
## 🧩 前缀树模式 (2/3) — building on the Trie template from Day 61

**#211 Design Add and Search Words Data Structure** 🟡 Medium

🔗 [LeetCode](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | 📹 [NeetCode](https://neetcode.io/problems/design-word-search-data-structure)

---

## 🧩 Trie 模式回顾 (2/3)

这是 Tries 模式块的第 2 题（共 3 题）。上节课 #208 我们实现了标准 Trie（精确匹配）。今天的变化：支持 **通配符 `.`**，它可以匹配任意一个字符。

*This is problem 2/3 in the Tries block. Day 61's #208 was exact-match Trie. Today's twist: support **wildcard `.`** that matches any single character.*

**模板延伸 / Template extension:**
- Insert: 完全相同，直接复用
- Search: 遇到 `.` 时，需要对当前节点的**所有子节点**做递归搜索（DFS）

---

## 🌍 真实场景 / Real-world Analogy

你有一个联系人应用，用户可以搜索 `J.hn`（忘记是 John 还是 John-ish？）。`.` 代表"我不确定这个字母是什么"。Trie 需要在那个位置尝试所有可能。

*You have a contacts app. User types `J.hn` — they forgot if it's John or Jahn. `.` means "I'm not sure about this character." The Trie needs to try all possibilities at that position.*

---

## 💡 解题思路 / Solution Walkthrough

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end = False

class WordDictionary:

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        # Standard Trie insert — identical to template
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        # NEW: handle '.' wildcard via DFS
        def dfs(node, i):
            if i == len(word):
                return node.is_end
            
            ch = word[i]
            if ch == '.':
                # Try ALL children — this is the key difference from #208
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False
            else:
                # Normal character — standard Trie traversal
                if ch not in node.children:
                    return False
                return dfs(node.children[ch], i + 1)
        
        return dfs(self.root, 0)
```

### 执行跟踪 / Execution Trace
```
addWord("bad"), addWord("dad"), addWord("mad")

搜索 ".ad":
  dfs(root, 0), ch = '.'
    → try 'b': dfs(b_node, 1), ch='a' → dfs(a_node, 2), ch='d' → is_end=True ✓
```

---

## ⏱️ 复杂度 / Complexity
- **addWord:** O(L) time, O(L) space — 与模板相同
- **search (无通配符):** O(L) time — 与模板相同
- **search (含 `.`):** O(N × L) worst case — 每个 `.` 都要尝试所有子节点
  - N = 节点总数, L = 单词长度

---

## 🔗 举一反三 / Pattern Connections

| 题目 | 核心变化 | 难点 |
|------|----------|------|
| #208 Implement Trie | 精确匹配 | 基础模板 |
| **#211 本题** | `.` 通配符 | DFS 递归 |
| #212 Word Search II (下题) | 2D 网格 + 前缀剪枝 | Trie + Backtracking |

下节课 #212 是这个模式的终极 Boss：在二维字符网格里找所有存在于词典中的单词——把 Trie 和回溯结合起来。

*Next problem #212 is the pattern boss: find all dictionary words in a 2D character grid — combine Trie with backtracking.*

---

## 📊 Quiz
**问题:** `WordDictionary` 搜索 `"..."` (三个点) 时，最坏情况下会访问多少节点？
- A) 3 个
- B) 整棵树所有节点
- C) 只有叶子节点
- D) 与单词长度无关

<details><summary>显示答案 / Show Answer</summary>
**B — 整棵树所有节点 / All nodes in the tree**

三个 `.` 意味着每一层都要尝试所有子节点 → 完整 DFS 遍历整棵树。这是 Trie 通配符搜索的最坏情况。实际系统中通常限制通配符数量或深度。

*Three `.` characters mean every level tries all children → full DFS of the entire tree. This is the worst case. Real systems typically limit the number of wildcards.*
</details>

---

## 📚 References
- [LeetCode #211 Discussion](https://leetcode.com/problems/design-add-and-search-words-data-structure/discuss/)
- [NeetCode Trie Playlist](https://neetcode.io/roadmap)
- [Trie Data Structure (Visualgo)](https://visualgo.net/en/trie)

## 🧒 ELI5
普通的 Trie 像查字典——你一个字母一个字母往下找。今天的题加了个 `.` 通配符，就像"百搭牌"——遇到它就得把所有可能的字母都试一遍，用的是深度优先搜索（DFS）。

*A normal Trie is like looking up a word in a dictionary — one letter at a time. Today's problem adds `.` as a wildcard "wild card" — when you hit it, try every possible letter using DFS.*
