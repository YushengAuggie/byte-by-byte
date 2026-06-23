# 💻 算法 / Algorithms — Day 61

**#208 Implement Trie (Medium)** — 🟡 Medium

---

## 🧩 新模式 / New Pattern: 前缀树模式 (Trie Pattern)

📍 本模块共 3 道题 / This block: 3 problems

**#208 Implement Trie** ← TODAY
**#211 Design Add and Search Words** (Medium)
**#212 Word Search II** (Hard)

**什么时候用 / When to use:** 前缀搜索、自动补全、词典匹配

**识别信号 / Signals:** prefix search, autocomplete, word dictionary, "starts with", matching patterns across words

**通用模版 / Template:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end = False  # marks end of a word

def insert(root, word):
    node = root
    for ch in word:
        if ch not in node.children:
            node.children[ch] = TrieNode()
        node = node.children[ch]
    node.is_end = True
```

**核心洞察 / Key Insight:** 共享前缀 → 节省空间 + O(L) 查询（L = 词长），不需要 O(N) 扫描所有词

---

## 🔗 Links

- LeetCode: https://leetcode.com/problems/implement-trie-prefix-tree/
- NeetCode: https://neetcode.io/problems/implement-prefix-tree

---

## 🌍 现实类比 / Real-World Analogy

想象一棵「词语树」：
- 根节点是空的
- 每一层是字符串的第 N 个字符
- 所有以「app」开头的词共享同一条「a→p→p」的路径

这就是你手机键盘自动补全的底层结构！

Imagine a "word tree" where words sharing a prefix share the same path from the root. Your phone's autocomplete literally uses a trie underneath.

---

## 🐍 Python 解法 + 追踪 / Solution + Trace

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # maps char -> TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True  # mark word end

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end  # must be full word

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True  # prefix exists, don't need is_end
```

**Trace for insert("app"), search("app"), startsWith("ap"):**
```
insert("app"):
  root → 'a' → 'p' → 'p' (is_end=True)

search("app"):
  root → 'a' ✓ → 'p' ✓ → 'p' ✓, is_end=True → True

search("ap"):
  root → 'a' ✓ → 'p' ✓, is_end=False → False

startsWith("ap"):
  root → 'a' ✓ → 'p' ✓ → return True (don't care about is_end)
```

**复杂度 / Complexity:**
- Time: O(L) per operation (L = word length)
- Space: O(N × L) where N = number of words

---

## 🔄 举一反三 / Pattern Connections

这只是 Trie 模块的**第 1/3** 题——打好基础：

- **#211 (下一题):** 支持 `.` 通配符 → DFS 遍历所有子节点
- **#212 (终极题):** 在 2D 棋盘上搜索单词列表 → Trie 剪枝优化暴力 DFS

关键变化点：
1. 只是**实现**数据结构 → 下题是**变形搜索** → 最后是**组合应用**
2. 每次都用同一个 TrieNode 模板，只改搜索逻辑

---

## 📚 References

- https://leetcode.com/problems/implement-trie-prefix-tree/
- https://en.wikipedia.org/wiki/Trie
- https://neetcode.io/courses/dsa-for-beginners/26

## 🧒 ELI5

Trie 就像一棵字母树：每层是一个字母，想找「apple」就沿着 a→p→p→l→e 走下去。
比每次扫描整个词典快多了！

A Trie is like a letter tree: each level is one character, so finding "apple" means walking a→p→p→l→e. Way faster than scanning the whole dictionary each time!
