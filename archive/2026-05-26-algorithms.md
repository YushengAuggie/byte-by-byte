# 💻 算法 / Algorithms — Day 43
**Topic:** #146 LRU Cache (Medium) — Linked List Pattern
**Date:** 2026-05-26 | **Phase:** Expert

---

## 💻 算法 / Algorithms — #146 LRU Cache (Medium)
**⏱️ 预计阅读时间 / Estimated reading time: 4 min**

---

### 🧩 链表技巧模式 (9/11) — 延续 Day 41 开始的模式

🧩 **Linked List Pattern (9/11)** — building on the template from Day 41

前 8 题我们用快慢指针处理环检测、找中点、合并等问题。今天的 LRU Cache 是这个 pattern 的"Boss 关"——它需要把**链表 + 哈希表**结合起来，实现 O(1) 的所有操作。

The first 8 problems used fast-slow pointers for cycle detection, finding midpoints, and merging. LRU Cache is the "boss fight" — it combines **linked list + hash map** to achieve O(1) for all operations.

---

### 🔗 Links
- [LeetCode #146 LRU Cache](https://leetcode.com/problems/lru-cache/) 🟡 Medium
- [NeetCode Video Solution](https://neetcode.io/problems/lru-cache)

---

### 现实类比 / Real-World Analogy

你的浏览器最多显示 10 个最近访问的标签历史。每次访问一个网站，如果它已在列表中就把它移到最前；如果列表满了，删掉最久没访问的那个。

Your browser's "recent tabs" keeps the last N sites. When you visit a site already in the list, bump it to the front. When the list is full, evict the least recently used one.

---

### 问题分析 / Problem

```
LRUCache(capacity):
- get(key): return value if exists, else -1. Mark key as recently used.
- put(key, value): insert/update. If capacity exceeded, evict LRU key.

All operations must be O(1).
```

**关键洞察：**为什么要用双向链表 + 哈希表？
- 哈希表：O(1) 查找 key → node
- 双向链表：O(1) 移动节点到头部、删除尾节点
- 单向链表不行 → 删除节点需要找前驱，O(n)

---

### 与模式模板的关系 / Mapping to Pattern

```
快慢指针模板 → LRU 变体：

快慢指针用于遍历/找位置
LRU 用双向链表 + dummy head/tail 做 O(1) 插删

核心技巧相同：用额外的指针结构突破链表的 O(n) 限制
```

---

### Python Solution (带 trace)

```python
class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}  # key -> Node

        # Dummy head (most recent) & tail (least recent)
        # head <-> ... <-> tail
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Remove node from its current position."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node):
        """Insert node right after head (most recent)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_front(node)  # mark as recently used
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._insert_front(node)

        if len(self.cache) > self.cap:
            # Evict LRU: node right before tail
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]  # don't forget to remove from dict!

class Node:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None

# Trace: capacity=2
# put(1,1): head <-> [1,1] <-> tail
# put(2,2): head <-> [2,2] <-> [1,1] <-> tail
# get(1):   head <-> [1,1] <-> [2,2] <-> tail  (1 moved to front)
# put(3,3): capacity exceeded, evict LRU=2
#           head <-> [3,3] <-> [1,1] <-> tail
# get(2) -> -1 (evicted!)
```

**复杂度 / Complexity:**
- Time: O(1) — 所有操作
- Space: O(capacity)

---

### 举一反三 / Pattern Connections

在同一个 Linked List block 中：
- **#141 Linked List Cycle**: fast/slow pointer 找环入口
- **#19 Remove Nth From End**: fast/slow pointer 找倒数第 N 个
- **#146 LRU Cache**: 双向链表 + 哈希表，O(1) 插删

下一步（block 剩余 2 题）：
- **#23 Merge K Sorted Lists**: 用堆合并，不是纯链表题
- **#25 Reverse Nodes in K-Group**: 分组反转，递归/迭代

---

### 📚 References
- [LeetCode #146](https://leetcode.com/problems/lru-cache/)
- [NeetCode LRU Cache Explanation](https://neetcode.io/problems/lru-cache)
- [Python OrderedDict LRU (built-in shortcut)](https://docs.python.org/3/library/collections.html#collections.OrderedDict)

### 🧒 ELI5
想象你有一个最多放 3 本书的桌子。每次你看一本书，就把它放到桌子最左边（最新）。桌子满了要放新书？把最右边的（最久没看的）扔掉。链表就是这张桌子，哈希表让你能瞬间找到任何书在哪里。
