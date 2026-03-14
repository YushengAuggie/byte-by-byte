# 🧠 byte-by-byte

> *A little bit every day. A lot over time.*

15 minutes of tech knowledge, delivered to your morning. One byte won't change your life — but 100 of them will.

## 📋 What You Get

| # | Section | Time | What |
|---|---------|------|------|
| 🏗️ | System Design | 3-4 min | Architecture patterns, tradeoffs, real-world systems |
| 💻 | Algorithms | 3-4 min | NeetCode 150 problems, Python, pattern-focused |
| 🗣️ | Soft Skills | 2-3 min | Communication, leadership, decision-making |
| 🎨 | Frontend | 2-3 min | CSS → JS → React → Next.js → TypeScript |
| 🤖 | AI | 2-3 min | Latest news + core concepts explained |

**~15 min daily read** • **Bilingual (Chinese/English)** • **Progressive difficulty**

## ✨ Philosophy

- **Teach, don't lecture** — real-world analogies, visual traces, "guess the output" challenges
- **Pattern recognition** — connect today's lesson to previous ones
- **Build on itself** — each day references what you've learned before
- **Stay current** — AI section alternates fresh news with foundational concepts

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
- [ ] Fundamentals (14)
- [ ] Building Blocks (1)
- [ ] System Design Problems (22)
- [ ] Expert (1)

### Frontend (50 topics)
- [ ] CSS Fundamentals (9)
- [ ] JavaScript Deep Dive (10)
- [ ] React Core (9)
- [ ] Next.js (6)
- [ ] TypeScript (3)
- [ ] Testing, Performance, Advanced (8)

## 🗂️ Structure

```
content/
├── neetcode-150.json      # 150 algorithm problems (NeetCode order)
├── system-design.json     # 40 system design topics
├── behavioral.json        # 40 soft skills topics
├── frontend.json          # 50 frontend topics
└── ai-topics.json         # 30 AI concept topics
archive/                   # Daily content saved as YYYY-MM-DD-*.md
state.json                 # Progress tracking
SPEC.md                    # Full specification
```

## 🚀 How It Works

Automated via [OpenClaw](https://openclaw.ai) cron jobs. 5 isolated sessions generate content daily and deliver via Telegram + email.

**Want to use this yourself?** Fork the repo, customize the content JSONs, and set up your own delivery mechanism (OpenClaw cron, GitHub Actions, or any scheduler).

## 📝 License

MIT — use it, fork it, learn from it.
