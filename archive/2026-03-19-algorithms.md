💻 **算法 Day 6 / Algorithms Day 6 — #271 Encode and Decode Strings (Medium) — Arrays & Hashing**
🔗 https://leetcode.com/problems/encode-and-decode-strings/

---

**现实类比 / Real-World Analogy**

你要把一堆购物清单放进一个信封里寄出去。问题是：收件人怎么知道哪里是一个清单的结束、另一个的开始？

笨办法：用逗号分隔 → 但如果清单内容本身有逗号呢？
聪明办法：每个清单前面写上它的长度 → `"5#Hello3#Bye"` → 无歧义！

---

**题目 / Problem Statement**

设计一个算法，将字符串列表编码为单个字符串，再解码回原始列表。
Design an algorithm to encode a list of strings into a single string, and decode it back.

```
Input:  ["Hello", "World"]
Encode: "5#Hello5#World"
Decode: ["Hello", "World"]
```

编码后的字符串可以包含任何字符（包括 `#`、空字符串等），必须无歧义。

---

**追踪过程 / Trace Through**

编码 `["Hi", "", "a#b"]`：

```
"Hi"  → len=2  → "2#Hi"
""    → len=0  → "0#"
"a#b" → len=3  → "3#a#b"

encoded = "2#Hi0#3#a#b"
```

解码 `"2#Hi0#3#a#b"`：

```
i=0: find '#' at index 1 → length=2 → read "Hi" → i=4
i=4: find '#' at index 5 → length=0 → read "" → i=6
i=6: find '#' at index 7 → length=3 → read "a#b" → i=11
Done! → ["Hi", "", "a#b"] ✅
```

注意 `"a#b"` 内部的 `#` 不会造成混淆，因为我们是按**长度**读取的，不是按分隔符！

---

**Python 解法 / Python Solution**

```python
class Codec:
    def encode(self, strs: list[str]) -> str:
        # Format: "length#string" for each string
        result = []
        for s in strs:
            result.append(f"{len(s)}#{s}")
        return "".join(result)

    def decode(self, s: str) -> list[str]:
        result = []
        i = 0
        while i < len(s):
            # Find the '#' delimiter
            j = s.index('#', i)
            # Characters before '#' are the length
            length = int(s[i:j])
            # Read exactly 'length' characters after '#'
            result.append(s[j + 1 : j + 1 + length])
            # Move pointer past the string
            i = j + 1 + length
        return result
```

---

**复杂度 / Complexity**

- **时间 Time:** O(n) — n 是所有字符串总长度
- **空间 Space:** O(1) — 不算输出空间（编码和解码都是线性扫描）

---

**边界情况 / Edge Cases**

```python
codec = Codec()

# Empty list
codec.decode(codec.encode([])) == []  # ✅

# List with empty string
codec.decode(codec.encode([""])) == [""]  # ✅ "0#" → [""]

# Strings containing '#'
codec.decode(codec.encode(["a#b", "#"])) == ["a#b", "#"]  # ✅

# Very long string
codec.decode(codec.encode(["a" * 10000])) == ["a" * 10000]  # ✅
```

---

**举一反三 / Pattern Recognition**

**模式：长度前缀编码（Length-Prefixed Encoding）**

这和网络协议（TCP、HTTP/2）、序列化格式（Protocol Buffers）用的是同一个思路：先告诉你"接下来有多少字节"，然后精确读取。

为什么不用特殊分隔符（如 `|` 或 `\0`）？
→ 字符串可能包含任何字符！长度前缀永远不会歧义。

**相关题目：**
- #443 String Compression（类似的编码思维）
- 序列化/反序列化（#297 Serialize and Deserialize Binary Tree）

---

*Day 6 / 150 — Arrays & Hashing 系列*
*昨天 Day 4：Group Anagrams | 明天 Day 7：Product of Array Except Self*
