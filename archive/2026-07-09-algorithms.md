# 算法 / Algorithms — Day 86 (LeetCode #355)

## 💻 算法 / Algorithms — #355 Design Twitter (Medium) — Heap / Priority Queue

🧩 **堆/优先队列模式 (6/7)** — building on the template from the pattern start

这是第 6 题，模式的最后一道 Medium 难度。下一题（#295 Find Median from Data Stream）将是 Hard 收官。

*This is problem 6/7 in the Heap/Priority Queue block. We're applying the same top-K pattern in a social media context.*

---

🔗 [LeetCode #355](https://leetcode.com/problems/design-twitter/) 🟡 Medium
📹 [NeetCode Video](https://neetcode.io/problems/design-twitter-feed)

---

### 🌍 真实场景类比

想象你在构建 Twitter/X 的"首页时间线"功能：
- 每个用户关注了多人
- 每条关注的 Feed 都是时间有序的推文列表
- 首页需要合并所有关注者的推文，按时间倒序显示 **最新 10 条**

这正是"合并 K 个有序序列取前 K 个"的堆经典应用场景。

*Building a social media feed = merging K sorted timelines and extracting the top-10 most recent posts.*

---

### 🧩 模式映射

回顾堆模板：
```python
import heapq
heap = []
for item in stream:
    heapq.heappush(heap, item)
    if len(heap) > k:
        heapq.heappop(heap)
```

本题变体：**不是单一数据流，而是 K 个独立的有序列表（每个被关注者的推文列表）**

变化点：
- 之前（#703, #1046, #973, #621）：单一流或固定集合 → 维护大小 K 的堆
- 今天（#355）：K 个独立列表的合并 → **最大堆 + 按时间戳倒序合并**

---

### 🐍 Python 解法（带注释）

```python
import heapq
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.count = 0                    # Global timestamp (decreasing for max-heap trick)
        self.tweets = defaultdict(list)   # userId -> list of [-count, tweetId]
        self.followMap = defaultdict(set) # userId -> set of followeeIds

    def postTweet(self, userId: int, tweetId: int) -> None:
        # Use negative count so Python's min-heap acts as max-heap by time
        self.tweets[userId].append([-self.count, tweetId])
        self.count += 1

    def getNewsFeed(self, userId: int) -> list[int]:
        # Merge tweets from user + all followees
        minHeap = []
        
        # Include self
        self.followMap[userId].add(userId)
        
        for followeeId in self.followMap[userId]:
            if followeeId in self.tweets:
                # Start with the most recent tweet (last in list)
                idx = len(self.tweets[followeeId]) - 1
                count, tweetId = self.tweets[followeeId][idx]
                # Push: [timestamp, tweetId, followeeId, tweet_index]
                heapq.heappush(minHeap, [count, tweetId, followeeId, idx - 1])
        
        result = []
        while minHeap and len(result) < 10:
            count, tweetId, followeeId, idx = heapq.heappop(minHeap)
            result.append(tweetId)
            
            # If this followee has more tweets, push their next most recent
            if idx >= 0:
                count, tweetId = self.tweets[followeeId][idx]
                heapq.heappush(minHeap, [count, tweetId, followeeId, idx - 1])
        
        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        self.followMap[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.followMap[followerId]:
            self.followMap[followerId].discard(followeeId)
```

---

### 🔍 执行跟踪

```
postTweet(1, 5)  → tweets[1] = [[-0, 5]]
postTweet(1, 3)  → tweets[1] = [[-0, 5], [-1, 3]]
follow(1, 2)     → followMap[1] = {2}
postTweet(2, 101)→ tweets[2] = [[-2, 101]]

getNewsFeed(1):
  followees = {1, 2}
  Initial heap: [[-1, 3, 1, 0], [-2, 101, 2, -1]]
  
  Pop [-1, 3, 1, 0]:  result=[3], push [-0, 5, 1, -1]
  Pop [-0, 5, 1, -1]: result=[3, 5], no more from user 1
  Pop [-2, 101, 2, -1]: result=[3, 5, 101], no more from user 2
  
  → 等等，注意 -0 < -1 < -2，所以堆顺序是：
  正确：tweet(count=2) 最新 → 负数 -2 最小 → 先出堆
  Result: [101, 3, 5]  (最新的先出)
```

**复杂度:**
- `postTweet`: O(1)
- `getNewsFeed`: O(N log K) — N 条推文，K 个被关注者
- `follow/unfollow`: O(1)

---

### 🔁 举一反三 — 本 Pattern 对比

| 题目 | 核心变化 | 堆操作 |
|------|----------|--------|
| #703 Kth Largest in Stream | 单流，动态插入 | 大小 K 的 min-heap |
| #1046 Last Stone Weight | 每次取最大两个 | max-heap |
| #973 K Closest Points | 距离作 key | 大小 K 的 max-heap |
| #621 Task Scheduler | 贪心，最高频先调度 | max-heap by count |
| **#355 Design Twitter** | **K 个有序列表合并** | **多指针 + min-heap** |
| #295 Find Median (Next!) | 动态中位数 | 两个 heap 配合 |

**关键洞察：** 当问题从"一个流"变成"多个有序列表合并"时，堆里要存的不只是值，还要存"这个值来自哪个列表的哪个位置"（指针）。

*Key insight: When merging K sorted lists, store (value, list_id, pointer) in the heap, not just the value.*

---

### 📚 References

- [LeetCode #355 - Design Twitter](https://leetcode.com/problems/design-twitter/)
- [NeetCode - Design Twitter Solution](https://neetcode.io/problems/design-twitter-feed)
- [Merge K Sorted Lists Pattern](https://leetcode.com/problems/merge-k-sorted-lists/)

### 🧒 ELI5

想象你订阅了 5 个 YouTube 频道，每个频道都有视频列表（最新在最后）。你想看最新的 10 条视频。
方法：在每个频道的"最新一条"上贴便利贴，每次从便利贴里挑最新的一条看，然后把那个频道的下一条贴上便利贴，重复 10 次。
这就是"多指针 + 最小堆"。

*You subscribed to 5 YouTube channels. Each has a sorted video list. To get the 10 newest: put a bookmark on each channel's latest video, always pick the newest bookmark, then advance that channel's bookmark. Repeat 10 times. That's the multi-pointer heap.*
