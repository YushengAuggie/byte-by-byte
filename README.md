# 🧠 byte-by-byte

> *A little bit every day. A lot over time. / 每天一点，积少成多*

[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Tests](https://github.com/YushengAuggie/byte-by-byte/actions/workflows/test.yml/badge.svg)](https://github.com/YushengAuggie/byte-by-byte/actions)
[![GitHub Stars](https://img.shields.io/github/stars/YushengAuggie/byte-by-byte?style=flat&color=yellow)](https://github.com/YushengAuggie/byte-by-byte/stargazers)
[![Daily Updates](https://img.shields.io/badge/updates-daily-brightgreen)](https://yushengauggie.github.io/byte-by-byte/archive.html)
[![Bilingual](https://img.shields.io/badge/language-中%2FEN-blue)](https://yushengauggie.github.io/byte-by-byte/)
[![RSS](https://img.shields.io/badge/RSS-subscribe-orange)](https://yushengauggie.github.io/byte-by-byte/feed.xml)

**5 topics. 15 minutes. Every day. Bilingual (Chinese/English). Designed to compound.**

I built this because I wanted to grow as an engineer without blocking my calendar. 15 minutes a day adds up — after 30 days, you've covered 30 algorithm patterns, 30 system design concepts, and 30 frontend skills.

🌐 [**Website**](https://yushengauggie.github.io/byte-by-byte/) • 📡 [**RSS Feed**](https://yushengauggie.github.io/byte-by-byte/feed.xml) • 📖 [**Browse Archive**](https://yushengauggie.github.io/byte-by-byte/archive.html)

---

## 📋 What You Get

| # | Section | Time | What |
|---|---------|------|------|
| 🏗️ | System Design | 3-4 min | Architecture patterns, tradeoffs, real-world systems |
| 💻 | Algorithms | 3-4 min | 150 problems, Python, pattern-focused |
| 🗣️ | Soft Skills | 2-3 min | STAR framework, senior/staff-level scenarios |
| 🎨 | Frontend | 2-3 min | CSS → JS → React → Next.js → TypeScript |
| 🤖 | AI | 2-3 min | Latest news + core concepts with runnable code |

**~15 min daily** • **Bilingual 中/EN** • **Progressive difficulty** • **Telegram + Email delivery**

### 🌏 Why Bilingual?

Every lesson is written in both Chinese and English — not translated, but **natively bilingual**. You learn the concepts *and* the technical vocabulary in both languages. No other daily learning system does this.

---

## ✨ Features

### 📚 Learning Engine
- **Spaced repetition** — Every 5th day is a review quiz on past material
- **Difficulty phases** — Foundation (Day 1-10) → Growth (11-30) → Mastery (31-50) → Expert (51+)
- **Exhaustion alerts** — Warns when content sections are running low
- **Cross-day references** — Each day builds on what came before

### 💬 Interactive Delivery
- **Progress tracking** — `📊 Day 12/150 · 🔥 12-day streak!` header every day
- **Quiz polls** — Telegram polls after Algorithms (complexity quiz) and Frontend (output quiz)
- **Weekend format** — Saturday deep-dives, Sunday week-in-review
- **Reading time estimates** — Every section shows estimated minutes
- **Direct links** — Problem links + difficulty badges 🟢🟡🔴 + video solutions

### ✍️ Content Quality
- **Self-review gate** — Content is generated, verified, fixed, THEN sent (never sends unchecked content)
- **QA reviewer** — Second automated pass 15 minutes later catches anything that slipped through
- **📚 Learn More** — Every section ends with 3 curated links (docs, blogs, videos, papers)
- **ELI5** — Every section ends with a one-sentence "explain like I'm 5"
- **Runnable AI code** — Concept days include ≤15 line copy-paste Python snippets
- **Retry logic** — 3x exponential backoff for delivery failures

### 🌐 Sharing & Growth
- **Email subscribers** — Anyone can [subscribe via Google Form](https://forms.gle/UJw1YPmzsA4mKRHK6) — auto-delivered daily
- **GitHub Pages site** — Beautiful dark-mode landing page
- **RSS feed** — Subscribe at `docs/feed.xml`
- **Archive browser** — Browsable HTML for every past day
- **Open Graph cards** — Rich previews when sharing links

### 🧪 Testing
- **61 automated checks** — JSON, schema, syntax, personal info leaks, integration tests
- **Pre-commit hook** — Every commit runs the full test suite; commit fails if tests fail
- **GitHub Actions CI** — Same tests run on every push

---

## 📊 Current Progress

<!-- AUTO-UPDATED by commit.sh — do not edit this section manually -->

| Field | Value |
|-------|-------|
| **Current Day** | Day 2 |
| **Last Sent** | 2026-03-15 |
| **Algorithms** | 2 / 150 (NeetCode 150) |
| **System Design** | 2 / 40 |
| **Frontend** | 2 / 50 |
| **Soft Skills** | 2 / 40 |
| **AI Topics** | 1 / 30 |

---

## 📖 Sample: What a Day Looks Like

<details>
<summary>💻 Algorithms — #217 Contains Duplicate (click to expand)</summary>

> 你负责给活动签到。来了100个人，你需要确认有没有人用同一张票进场两次。
>
> *You're checking tickets at an event. 100 people arrive — you need to detect if anyone uses the same ticket twice.*

```python
def containsDuplicate(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

> **Step-by-step trace** with `[1, 2, 3, 1]`:
> ```
> Step 1: num=1, seen={} → not found → seen={1}
> Step 2: num=2, seen={1} → not found → seen={1,2}
> Step 3: num=3, seen={1,2} → not found → seen={1,2,3}
> Step 4: num=1, seen={1,2,3} → FOUND! ✅ return True
> ```
>
> 📚 **Learn More:** [NeetCode Video](https://neetcode.io/problems/contains-duplicate) • [LeetCode](https://leetcode.com/problems/contains-duplicate/)
>
> 🧒 ELI5: It's like checking if any kid in class has the same birthday — just keep a list and check each new one.

[Full sample →](samples/day1-algorithms.md)

</details>

<details>
<summary>🏗️ System Design — Client-Server Model (click to expand)</summary>

[Full sample →](samples/day1-system-design.md)

</details>

<details>
<summary>🎨 Frontend — CSS Box Model (click to expand)</summary>

> 猜猜这段代码输出什么？/ Guess: how wide is this div?
> ```css
> .box { width: 200px; padding: 20px; border: 5px solid black; }
> ```
> Answer: **250px**, not 200px! `width` only sets the content area.
>
> 📚 **Learn More:** [MDN: Box Model](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model) • [CSS-Tricks Guide](https://css-tricks.com/the-css-box-model/)
>
> 🧒 ELI5: It's like measuring a picture frame — the width you set is just the photo, not the frame around it.

[Full sample →](samples/day1-frontend.md)

</details>

More samples: [Soft Skills](samples/day1-soft-skills.md) • [AI](samples/day1-ai.md)

---

## 🗓️ Difficulty Progression

| Phase | Days | Level | Example |
|-------|------|-------|---------|
| 🌱 Foundation | 1–10 | Easy/Intro | Contains Duplicate, Client-Server Model, CSS Box Model |
| 📈 Growth | 11–30 | Easy + Medium | Sliding Window, Caching + CDN, React State |
| 🏔️ Mastery | 31–50 | Medium | Graphs, Sharding + CAP, TypeScript Generics |
| 🚀 Expert | 51+ | Medium-Hard | DP, Distributed Consensus, Performance Optimization |

**Review days** on Day 5, 10, 15, 20... — quiz yourself on the past 4 days.

---

## 🚀 Getting Started

### Option 1: Subscribe to email (easiest)

[**Subscribe here**](https://forms.gle/UJw1YPmzsA4mKRHK6) — one beautiful HTML email with all 5 sections, delivered daily. Free.

### Option 2: Browse online

Visit the [website](https://yushengauggie.github.io/byte-by-byte/) or [archive](https://yushengauggie.github.io/byte-by-byte/archive.html).

### Option 3: RSS

Subscribe to [`docs/feed.xml`](https://yushengauggie.github.io/byte-by-byte/feed.xml) in your favorite reader.

### Option 4: Self-host with Telegram + Email

Requires [OpenClaw](https://openclaw.ai):

```bash
git clone https://github.com/YushengAuggie/byte-by-byte.git
cd byte-by-byte
cp config.env.example config.env
vim config.env  # Add your Telegram ID, email, paths
./scripts/setup.sh
```

5 Telegram messages + 1 HTML email digest, delivered daily at your configured time.

### Option 5: Fork and customize

1. Fork this repo
2. Edit `content/*.json` to change topics
3. Edit `config.env` for your delivery settings
4. Run `./scripts/setup.sh`

---

## 🗂️ Structure

```
byte-by-byte/
├── config.env.example     ← copy to config.env, add your settings
├── state.json             ← progress tracking (auto-updated)
├── content/
│   ├── neetcode-150.json  ← 150 algorithm problems
│   ├── system-design.json ← 40 system design topics
│   ├── behavioral.json    ← 40 soft skills questions
│   ├── frontend.json      ← 50 frontend topics
│   ├── ai-topics.json     ← 30 AI concepts
│   ├── difficulty-map.json← difficulty phases by day
│   └── review-schedule.json← spaced repetition config
├── samples/               ← example outputs
├── archive/               ← daily generated content
├── docs/                  ← GitHub Pages site + RSS feed
├── scripts/
│   ├── generate.sh        ← topic picker + state manager
│   ├── send-email.py      ← HTML email digest sender
│   ├── send-telegram.py   ← Telegram delivery with retry
│   ├── commit.sh          ← git commit + push + update progress
│   ├── setup.sh           ← one-command setup (cron + hooks)
│   ├── test.sh            ← 61-check test suite
│   ├── check-exhaustion.sh← content remaining alerts
│   ├── verify-neetcode.py ← problem list validation
│   ├── generate-index.py  ← archive HTML page generator
│   └── generate-rss.py    ← RSS feed generator
├── cron/
│   ├── daily-prompt.md    ← generation prompt (with review gate)
│   └── qa-prompt.md       ← QA reviewer prompt
├── hooks/
│   └── pre-commit         ← auto-installed by setup.sh
├── .github/workflows/
│   └── test.yml           ← CI: runs test.sh on every push
└── research/              ← inspiration + test reports
```

---

## 📣 Share

If this helps you, share it!

**Twitter / X:**
> byte-by-byte — free daily bilingual tech learning (Chinese + English). 15 min/day: system design, algorithms, soft skills, frontend, AI. Open source 🧠 https://github.com/YushengAuggie/byte-by-byte

**LinkedIn:**
> I've been learning with byte-by-byte — a daily bilingual tech learning system. 5 topics × 15 minutes = compounding growth. Chinese and English. Automated. Open source. https://yushengauggie.github.io/byte-by-byte/

**微信：**
> 分享一个每天学技术的工具：byte-by-byte。每天5个主题：系统设计、算法、软技能、前端、AI。中英双语，15分钟，每天积累，长期复利。开源免费 https://github.com/YushengAuggie/byte-by-byte

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Adding problems to `content/*.json`
- Submitting topic suggestions
- Improving content quality
- How the QA system works

---

## 📝 License

[MIT](LICENSE) — use it, fork it, learn from it.

---

*Built with [OpenClaw](https://openclaw.ai). A little bit every day. A lot over time.* 🧠
