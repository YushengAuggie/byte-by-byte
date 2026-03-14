# 🧠 byte-by-byte

> *A little bit every day. A lot over time.*

**15 minutes of tech knowledge, delivered to your morning. Automated, bilingual (Chinese/English), and designed to compound.**

I built this because I wanted to stay sharp without spending hours grinding LeetCode. 15 minutes. Every morning. Compounding. After 30 days, you've covered 30 algorithm patterns, 30 system designs, and 30 frontend concepts — all without blocking your calendar.

---

## 📋 What You Get

| # | Section | Time | What |
|---|---------|------|------|
| 🏗️ | System Design | 3-4 min | Architecture patterns, tradeoffs, real-world systems |
| 💻 | Algorithms | 3-4 min | NeetCode 150, Python, pattern-focused |
| 🗣️ | Soft Skills | 2-3 min | Communication, leadership, decision-making |
| 🎨 | Frontend | 2-3 min | CSS → JS → React → Next.js → TypeScript |
| 🤖 | AI | 2-3 min | Latest news + core concepts explained |

**~15 min daily** • **Bilingual 中/EN** • **Progressive difficulty** • **Automated delivery**

### 🌏 Why Bilingual?

Every lesson is written in both Chinese and English — not translated, but **natively bilingual**. You learn the concepts *and* the technical vocabulary in both languages. No other daily learning system does this.

---

## 📖 Sample: What Day 1 Looks Like

<details>
<summary>💻 Algorithms Day 1 — #217 Contains Duplicate (click to expand)</summary>

> 你负责给活动签到。来了100个人，你需要确认有没有人用同一张票进场两次。
>
> *You're checking tickets at an event. 100 people arrive — you need to detect if anyone uses the same ticket twice.*
>
> **方案A（笨方法）**：每来一个人，翻遍之前所有人的名单。100×100=10,000次。
>
> **方案B（聪明方法）**：准备一本空白通讯录。每来一个人，查一下——没有就登记，有就报警！
>
> 方案B 用的就是今天的核心数据结构：**哈希集合 (Hash Set)**。

```python
def containsDuplicate(nums: list[int]) -> bool:
    seen = set()              # Our "notebook" — starts empty
    for num in nums:
        if num in seen:       # Already stamped this ticket?
            return True       # Duplicate found!
        seen.add(num)         # First time — stamp and record
    return False              # No duplicates
```

> **Step-by-step trace** with `[1, 2, 3, 1]`:
> ```
> Step 1: num=1, seen={} → not found → seen={1}
> Step 2: num=2, seen={1} → not found → seen={1,2}
> Step 3: num=3, seen={1,2} → not found → seen={1,2,3}
> Step 4: num=1, seen={1,2,3} → FOUND! ✅ return True
> ```

[Full sample with complexity analysis, pattern recognition, and related problems →](samples/day1-algorithms.md)

</details>

<details>
<summary>🏗️ System Design Day 1 — Client-Server Model (click to expand)</summary>

[Full sample →](samples/day1-system-design.md)

</details>

<details>
<summary>🎨 Frontend Day 1 — CSS Box Model (click to expand)</summary>

> 猜猜这段代码输出什么？/ Guess: how wide is this div?
> ```css
> .box { width: 200px; padding: 20px; border: 5px solid black; }
> ```
> Answer: **250px**, not 200px! `width` only sets the content area.

[Full sample with diagrams and mini challenge →](samples/day1-frontend.md)

</details>

More samples: [Soft Skills](samples/day1-soft-skills.md) • [AI News](samples/day1-ai.md)

---

## ✨ Philosophy

- **Teach, don't lecture** — real-world analogies, "guess the output" challenges, step-by-step traces
- **Pattern recognition** — we don't just solve problems, we teach *patterns* so you can solve any problem
- **Build on itself** — each day references what you've learned before
- **Stay current** — AI section alternates fresh news with foundational concepts
- **Quality-checked** — every lesson goes through self-review + automated QA

---

## 🗓️ What Your First Month Looks Like

| Week | Algorithms | System Design | Frontend |
|------|-----------|---------------|----------|
| 1 | Arrays & Hashing | How the Internet works, DNS, HTTP, REST | CSS Box Model, Flexbox, Grid |
| 2 | Two Pointers, Sliding Window | Load Balancing, Caching, CDN | Responsive Design, Positioning |
| 3 | Stack, Binary Search | SQL vs NoSQL, Indexing, Replication | JavaScript: Closures, Event Loop |
| 4 | Linked List | Sharding, Consistent Hashing, CAP Theorem | Promises, Prototypes, DOM |

By Day 30: **30 algorithm patterns** • **14 system design concepts** • **18 frontend skills** • **30 soft skills scenarios** • **30 AI updates**

---

## 🚀 Getting Started

### Use the automated delivery (recommended)

Requires [OpenClaw](https://openclaw.ai):

```bash
git clone https://github.com/YushengAuggie/byte-by-byte.git
cd byte-by-byte
# Edit config.env with your paths and Telegram/email targets
vim config.env
# Run setup — creates cron jobs automatically
./scripts/setup.sh
```

You'll get 5 messages every morning at 8 AM. That's it.

### Just read the content

Browse the [`samples/`](samples/) directory or the [`archive/`](archive/) directory (populated daily) for all past content.

### Fork and customize

1. Fork this repo
2. Edit `content/*.json` to change topics or add your own
3. Edit `config.env` for your delivery settings
4. Run `./scripts/setup.sh`

---

## 📊 Progress

### Algorithms (NeetCode 150)
- [ ] Arrays & Hashing (9)
- [ ] Two Pointers (5)
- [ ] Sliding Window (6)
- [ ] Stack (7)
- [ ] Binary Search (7)
- [ ] Linked List (11)
- [ ] Trees (15)
- [ ] Tries (3)
- [ ] Heap / Priority Queue (7)
- [ ] Backtracking (9)
- [ ] Graphs (13)
- [ ] Advanced Graphs (6)
- [ ] 1-D Dynamic Programming (12)
- [ ] 2-D Dynamic Programming (11)
- [ ] Greedy (8)
- [ ] Intervals (6)
- [ ] Math & Geometry (8)
- [ ] Bit Manipulation (7)

### System Design (40 topics)
Fundamentals (14) → Building Blocks → Full Systems (22) → Expert

### Frontend (50 topics)
CSS (9) → JavaScript (10) → React (9) → Next.js (6) → TypeScript (3) → Testing & Performance (8)

---

## 🗂️ Structure

```
byte-by-byte/
├── config.env             ← machine-specific settings (edit this)
├── state.json             ← progress tracking
├── content/
│   ├── neetcode-150.json  ← 150 algorithm problems
│   ├── system-design.json ← 40 system design topics
│   ├── behavioral.json    ← 40 soft skills questions
│   ├── frontend.json      ← 50 frontend topics
│   └── ai-topics.json     ← 30 AI concepts
├── samples/               ← example outputs (see quality before committing)
├── archive/               ← daily generated content
├── scripts/
│   ├── generate.sh        ← topic picker + state manager
│   ├── commit.sh          ← git commit + push
│   └── setup.sh           ← new machine setup
├── cron/
│   ├── daily-prompt.md    ← generation prompt
│   └── qa-prompt.md       ← QA reviewer prompt
└── research/              ← inspiration + test reports
```

## 🤝 Contributing

Contributions welcome! You can help by:
- Adding more problems to `content/*.json`
- Improving existing content in `samples/` or `archive/`
- Translating to additional languages
- Reporting quality issues
- Suggesting new sections

## 📝 License

MIT — use it, fork it, learn from it.

---

*Built with [OpenClaw](https://openclaw.ai). A little bit every day. A lot over time.* 🧠
