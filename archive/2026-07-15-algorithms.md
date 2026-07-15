# 算法 / Algorithms — Day 91
**Date:** 2026-07-15 | **Phase:** Expert | **Pattern:** Backtracking (3/9)

---

## 💻 算法 / Algorithms
**#46 Permutations (Medium) 🟡**

🧩 **回溯模式 (3/9)** — building on the template from earlier in this block

上次：#78 Subsets（选不选）、#39 Combination Sum（可重复选）  
今天：#46 Permutations — **有序，每个元素只用一次，顺序不同算不同结果**

Previous: #78 Subsets (include/exclude), #39 Combination Sum (can reuse)  
Today: #46 Permutations — **ordered, each element used exactly once, order matters**

---

### 🔗 链接 / Links

- 🔗 [LeetCode #46](https://leetcode.com/problems/permutations/) 🟡 Medium
- 📹 [NeetCode 视频](https://neetcode.io/problems/permutations)

---

### 真实类比 / Real-World Analogy

想象 3 个人（A, B, C）坐一排座位。有多少种排法？  
3! = 6 种：ABC, ACB, BAC, BCA, CAB, CBA  
**Permutations = 全排列**，每次选一个新人坐下，再从剩余的里选。

Imagine 3 people (A, B, C) sitting in a row. How many arrangements?  
3! = 6: ABC, ACB, BAC, BCA, CAB, CBA  
**Permutations = all orderings**, pick one at a time from the remaining.

---

### 问题 / Problem

```
Input:  nums = [1, 2, 3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

---

### 模版对比：Permutations vs Subsets / Template Comparison

```python
# Subsets (Day 88): choices = remaining elements after index
# 顺序不重要，[1,2] == [2,1]，用 start index 避免重复

def subsets(nums):
    result, path = [], []
    def bt(start):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            bt(i + 1)  # start from NEXT index
            path.pop()
    bt(0)
    return result

# Permutations: choices = ALL unused elements
# 顺序重要，[1,2] != [2,1]，用 visited set 追踪用过的

def permutations(nums):
    result, path = [], []
    used = set()
    
    def bt():
        if len(path) == len(nums):  # 用完所有元素 = 一个完整排列
            result.append(path[:])
            return
        for num in nums:            # 从所有 nums 里选
            if num in used:
                continue            # 跳过已用的
            used.add(num)
            path.append(num)
            bt()                    # 递归，不传 start（顺序重要！）
            path.pop()
            used.remove(num)        # 撤销
    
    bt()
    return result

# 测试 / Test
print(permutations([1, 2, 3]))
# [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

---

### 执行追踪 / Execution Trace

```
nums = [1, 2, 3]

bt(), path=[], used={}
├─ choose 1: path=[1], used={1}
│  ├─ choose 2: path=[1,2], used={1,2}
│  │  └─ choose 3: path=[1,2,3] ✅ append → pop 3
│  ├─ choose 3: path=[1,3], used={1,3}
│  │  └─ choose 2: path=[1,3,2] ✅ append → pop 2
│  └─ pop 1
├─ choose 2: path=[2], used={2}
│  ├─ choose 1: path=[2,1] → choose 3 → [2,1,3] ✅
│  └─ choose 3: path=[2,3] → choose 1 → [2,3,1] ✅
└─ choose 3: ... → [3,1,2] ✅, [3,2,1] ✅
```

---

### 关键洞察：Subsets vs Permutations 核心区别

| | Subsets | Permutations |
|--|---------|-------------|
| 顺序重要？ | ❌ [1,2]==[2,1] | ✅ [1,2]!=[2,1] |
| 避免重复方式 | `start` index | `used` set |
| 递归参数 | `bt(start+1)` | `bt()` (无参数) |
| 结果数量 | 2^n | n! |
| 终止条件 | 每层都收集 | `len(path)==len(nums)` |

---

### 复杂度 / Complexity

- **Time:** O(n × n!) — n! 个排列，每个花 O(n) 复制
- **Space:** O(n) 递归栈深度 + O(n × n!) 输出

---

### 举一反三 / Pattern Variations in This Block

```
本 block 的回溯变体 / Variations in this Backtracking block:

#78  Subsets        → 选/不选，bt(start+1)
#39  Combination Sum → 可重复，bt(start)（不后移）
#46  Permutations   → 全排列，used set，bt() 无参
#90  Subsets II     → 有重复，排序+跳过同层重复 (coming soon)
#40  Combo Sum II   → 同上，但不重复使用 (coming soon)
#79  Word Search    → 2D backtrack (coming soon)
```

---

### 📚 References

- [LeetCode #46 Official Solution](https://leetcode.com/problems/permutations/editorial/)
- [NeetCode Backtracking Playlist](https://neetcode.io/roadmap)
- [Backtracking Template — Labuladong](https://labuladong.online/algo/essential-technique/backtrack-framework/)

### 🧒 ELI5

全排列就像给 3 朋友拍合照：第一个位置有 3 人选，第二个位置剩 2 人，第三个位置剩 1 人。  
3×2×1 = 6 张不同的照片。回溯就是：试一个人站第一位，拍完所有后续组合，再换下一个人试。

Permutations are like taking photos with 3 friends in a row: 3 choices for spot 1, 2 for spot 2, 1 for spot 3.  
3×2×1 = 6 different photos. Backtracking: try each person in spot 1, exhaust all combos, then swap and try again.
