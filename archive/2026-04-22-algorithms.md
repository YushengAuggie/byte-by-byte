💻 **算法 / Algorithms** — #853 Car Fleet (Medium) — Stack

🧩 **单调栈模式 (6/7)** — building on the template from Day X

**场景 / Real-world analogy:**
想象你在高速公路上开车，前面有一辆慢车。你不能超车，只能减速跟在它后面，你们就成了一个“车队”。有多少个这样的车队能到达终点？
Imagine driving on a highway behind a slow car. You can't pass it, so you slow down and follow it, forming a "fleet." How many such fleets will reach the destination?

**问题 / Problem:**
有 `n` 辆车在单车道上行驶，目标是 `target`。每辆车有初始位置 `position[i]` 和速度 `speed[i]`。如果一辆车追上前面的车，它必须降速并与前车组成一个车队（视为一个整体）。求到达终点时的车队数量。
There are `n` cars driving on a single-lane road to a `target`. Each car has an initial `position[i]` and `speed[i]`. If a car catches up to the one ahead, it must slow down and form a fleet (treated as one entity). Find the number of car fleets arriving at the target.

**映射到模板 / Map to pattern template:**
- **排序 (Sort):** 首先按位置降序排序（离终点近的在前面）。/ Sort by position descending (closest to target first).
- **时间 (Time):** 计算每辆车到达终点所需的时间 `(target - pos) / speed`。/ Calculate time to reach target for each car.
- **单调栈 (Monotonic Stack):** 维护到达时间。如果后面的车（栈顶）比前面的车（栈顶的下一个）时间**短或等于**，说明它能追上，形成车队（弹出后面的车）。/ Maintain arrival times. If a car behind (top of stack) takes **less or equal** time than the car ahead (next in stack), it catches up, forming a fleet (pop the car behind).

**Python 代码 / Python Solution:**
```python
def carFleet(target: int, position: List[int], speed: List[int]) -> int:
    # 1. 组合并按位置降序排序 / Combine and sort by position descending
    cars = sorted(zip(position, speed), reverse=True)
    stack = []
    
    # 2. 遍历每辆车 / Iterate through each car
    for pos, spd in cars:
        # 计算到达时间 / Calculate arrival time
        time = (target - pos) / spd
        stack.append(time)
        
        # 3. 如果当前车（后车）的时间 <= 前车的时间，说明追上了，合并车队
        # If current car (behind) time <= car ahead time, it catches up, merge fleet
        if len(stack) >= 2 and stack[-1] <= stack[-2]:
            stack.pop() # 弹出当前车（后车），保留前车的时间 / Pop current car, keep car ahead's time
            
    return len(stack) # 栈中剩余的元素个数就是车队数量 / Remaining elements are the number of fleets
```

**复杂度 / Complexity:**
- **时间 / Time:** `O(N log N)` (排序 / Sorting), `O(N)` (遍历 / Traversal). Total: `O(N log N)`.
- **空间 / Space:** `O(N)` (栈和排序数组 / Stack and sorted array).

**举一反三 / Connect to other problems:**
- #739 Daily Temperatures: 寻找下一个更大的元素（单调递减栈）。/ Find next greater element (monotonic decreasing stack).
- #84 Largest Rectangle in Histogram: 寻找左右边界（单调递增栈）。/ Find left and right boundaries (monotonic increasing stack).

**📚 参考文献 / References:**
- [LeetCode #853 Car Fleet](https://leetcode.com/problems/car-fleet/)
- [NeetCode Video](https://www.youtube.com/watch?v=Pr6T-3yB9RM)

**🧒 ELI5 (Explain Like I'm 5):**
把车排成一排，离终点近的在最前面。算算每辆车自己开到终点要多久。如果后面的车算出来的时间比前面的短，说明它开得快，会追上前面的车，然后只能跟着前面的车慢慢开（变成一个车队）。我们用一个栈来记录每个车队的时间，最后栈里有几个时间，就有几个车队！
Line up the cars, closest to the finish line first. Calculate how long each car takes to reach the finish line on its own. If a car behind has a shorter time than the car ahead, it means it's faster, will catch up, and then must follow slowly (forming a fleet). We use a stack to record the time of each fleet. The number of times left in the stack is the number of fleets!