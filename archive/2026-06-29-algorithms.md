# 💻 算法 / Algorithms — Day 77
## #211 Design Add and Search Words Data Structure (Medium)

> ⏱️ 阅读时间约 4 分钟 / ~4 min read

🧩 **前缀树模式 (2/3)** — 基于 Day 74 的 Trie 模板继续深化
Building on the Trie template from Day 74 (#208 Implement Trie)

---

### 🔗 Links

- 🔗 [LeetCode #211](https://leetcode.com/problems/design-add-and-search-words-data-structure/) 🟡 Medium
- 📹 [NeetCode Video](https://neetcode.io/problems/design-word-search-data-structure)
- 🧩 **Trie Pattern Block:** #208 Implement Trie → **#211 This Problem** → #212 Word Search II (Hard)

---

### 🌍 现实类比 / Real-World Analogy

你在写一个 grep 工具，支持 `.` 通配符：`se.rch` 能匹配 `search` 也能匹配 `seerch`。字典里有几十万个单词，怎么做到 O(L) 匹配？

You're building grep with `.` wildcard: `se.rch` matches `search` or `seerch`. With 500K words in the dictionary, how do you match in O(L)?

---

### 🧩 与模板的关系 / How It Maps to the Template

上次的模板（#208）：`insert` + `startsWith` + `search`（精确匹配）
今天的变化（#211）：`search` 支持 `.` 通配符 → 需要**DFS 回溯**

Day 74's template: exact `insert` + `search`  
Today's twist: `search("b.d")` must try ALL children when `.` is hit → **DFS backtracking**

```
模板核心变化 / Key Template Diff:

精确匹配 / Exact:     node = node.children[ch]   (直接跳 / direct jump)
通配匹配 / Wildcard:  for child in node.children.values():  (遍历全部 / try all)
                          dfs(child, i+1)
```

---

### 💻 Python 解法 + 追踪 / Solution with Trace

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        # Same as Day 74's insert template — unchanged
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        # THE KEY CHANGE: DFS when we hit '.'
        def dfs(node: TrieNode, i: int) -> bool:
            if i == len(word):
                return node.is_end
            ch = word[i]
            if ch == '.':
                # Try ALL children — backtracking
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False
            else:
                # Exact match — O(1) lookup
                if ch not in node.children:
                    return False
                return dfs(node.children[ch], i + 1)

        return dfs(self.root, 0)
```

**追踪 / Trace:** 插入 "bad", "dad", "mad"，搜索 ".ad"
```
root
 ├─ b → a → d (is_end=True)
 ├─ d → a → d (is_end=True)
 └─ m → a → d (is_end=True)

search(".ad"):
  i=0, ch='.': try b, d, m
    → dfs(b_node, 1): ch='a' → match → dfs(a_node, 2): ch='d' → match → is_end=True ✅
```

---

### 📊 复杂度 / Complexity

| | 时间 / Time | 空间 / Space |
|---|---|---|
| addWord | O(L) | O(L) |
| search (no wildcard) | O(L) | O(L) recursion |
| search (all wildcards) | O(N) worst — traverses all nodes | O(L) stack |

**实际中 / In practice:** most queries have few `.` → fast in practice, but O(N) worst case is real for `"..."` queries.

---

### 举一反三 / Pattern Family

| 题目 | 关系 | 难点 |
|---|---|---|
| #208 Implement Trie | 基础模板 / Base template | 精确匹配 exact match |
| **#211 This** | 通配符变体 / Wildcard variant | `.` triggers DFS |
| #212 Word Search II (Hard) | 2D 版本 / 2D grid version | Trie prunes DFS on grid |

**核心洞察 / Insight:** 每次 Trie 遇到"模糊"条件（通配符/近似匹配），精确查找就变成 DFS。理解这个跳跃就理解了 Trie 的全部变种。

Whenever a Trie query becomes "fuzzy," exact lookup becomes DFS. Master this transition and you understand all Trie variants.

---

### 📚 References

- [LeetCode #211 editorial](https://leetcode.com/problems/design-add-and-search-words-data-structure/editorial/)
- [NeetCode Trie playlist](https://neetcode.io/roadmap)

---

### 🧒 ELI5

普通 Trie 就像走一条有标记的路，每个字母是一个路标，走到终点就找到了。今天加了通配符 `.`，就像路标模糊了——你得把所有支路都试一遍（DFS），只要有一条路能走通就算找到。代价是通配符越多，要走的路越多。

Normal Trie: follow one road per letter. With `.` wildcard: the sign is blurry — you try every branch (DFS) until one succeeds. More wildcards = more roads to explore.
