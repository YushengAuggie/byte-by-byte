# 📚 Daily Interview Prep

Automated daily interview preparation system — bilingual (Chinese/English).

## 📋 Sections

| # | Section | Time | Topics |
|---|---------|------|--------|
| 🏗️ | System Design | 3-4 min | 40 topics, fundamentals → advanced |
| 💻 | LeetCode | 3-4 min | NeetCode 150, Python, pattern-focused |
| 🗣️ | Behavioral | 2-3 min | 40 questions, senior/staff level |
| 🎨 | Frontend | 2-3 min | 50 topics, CSS → React → Next.js |
| 🤖 | AI Update | 2-3 min | News + 30 concept topics |

**Total: ~15 min daily read**

## 🚀 Delivery

- **Time:** 8:00 AM PT daily
- **Channels:** 5 Telegram messages + 1 combined email
- **Engine:** OpenClaw cron job

## 📊 Progress

### LeetCode (NeetCode 150)
- [ ] Arrays & Hashing (9 problems)
- [ ] Two Pointers (5 problems)
- [ ] Sliding Window (6 problems)
- [ ] Stack (7 problems)
- [ ] Binary Search (7 problems)
- [ ] Linked List (11 problems)
- [ ] Trees (15 problems)
- [ ] Tries (3 problems)
- [ ] Heap / Priority Queue (7 problems)
- [ ] Backtracking (9 problems)
- [ ] Graphs (13 problems)
- [ ] Advanced Graphs (6 problems)
- [ ] 1-D Dynamic Programming (12 problems)
- [ ] 2-D Dynamic Programming (11 problems)
- [ ] Greedy (8 problems)
- [ ] Intervals (6 problems)
- [ ] Math & Geometry (8 problems)
- [ ] Bit Manipulation (7 problems)

### System Design
- [ ] Fundamentals (14 topics)
- [ ] Building Blocks (1 topic)
- [ ] System Design Problems (22 topics)
- [ ] Expert (1 topic)

### Frontend
- [ ] CSS Fundamentals (9 topics)
- [ ] JavaScript Deep Dive (10 topics)
- [ ] React Core (9 topics)
- [ ] Next.js (6 topics)
- [ ] TypeScript (3 topics)
- [ ] Testing (2 topics)
- [ ] Performance (3 topics)
- [ ] Advanced (7 topics)

## 🗂️ Structure

```
content/
├── neetcode-150.json      # 150 LeetCode problems (NeetCode order)
├── system-design.json     # 40 system design topics
├── behavioral.json        # 40 behavioral questions
├── frontend.json          # 50 frontend topics
└── ai-topics.json         # 30 AI concept topics
archive/                   # Daily content saved as YYYY-MM-DD.md
state.json                 # Progress tracking
SPEC.md                    # Full specification
```

## 🔧 Manual Run

Content is generated and delivered by the OpenClaw cron job. See `SPEC.md` for details.
