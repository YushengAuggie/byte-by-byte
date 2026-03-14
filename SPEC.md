# Daily Interview Prep — Specification

## Overview
Daily automated interview preparation system delivering 5 bilingual (Chinese/English) messages via Telegram + 1 combined email at 8:00 AM PT.

## Sections (5 separate Telegram messages)

### 1. 🏗️ System Design (3-4 min read)
- One topic per day, progressive difficulty
- Real-world scenario intro ("You're building Uber's ride matching...")
- ASCII diagrams for architecture
- "为什么这样设计？/ Why this design?" — explain tradeoffs
- "别踩这个坑 / Don't fall into this trap" — common mistakes
- Week 1-2: Fundamentals (load balancing, caching, databases, API design)
- Week 3-4: Mid-level (URL shortener, rate limiter, key-value store)
- Week 5+: Complex (news feed, chat, search engine, video streaming)

### 2. 💻 LeetCode (3-4 min read)
- NeetCode 150, in pattern-grouped order
- Python code with detailed explanations
- Real-world analogy before the algorithm
- Step-by-step walkthrough with concrete example
- Visual trace of how algorithm processes input
- Pattern recognition: connect to similar problems
- Time/Space complexity + follow-up variations
- Progression:
  - Week 1: Arrays + Hashing
  - Week 2: Two Pointers + Sliding Window
  - Week 3: Stack + Binary Search
  - Week 4: Trees + Tries
  - Week 5: Graphs + BFS/DFS
  - Week 6: DP
  - Week 7+: Advanced (intervals, greedy, bit manipulation)

### 3. 🗣️ Behavioral (2-3 min read)
- One question per day, senior/staff level framing
- STAR framework breakdown
- "Bad answer vs Good answer" comparison
- Real scenario templates to adapt
- Categories: leadership, conflict, failure, teamwork, ambiguity, etc.

### 4. 🎨 Frontend (2-3 min read)
- Tips/concepts for becoming full stack
- User has basic understanding but rusty
- Interactive: "猜猜这段代码输出什么？/ What does this code output?"
- Visual concepts with ASCII/emoji diagrams
- Mini challenges at the end
- Progression:
  - Week 1-2: HTML/CSS fundamentals, Flexbox, Grid
  - Week 3-4: JavaScript deep dives (closures, promises, event loop)
  - Week 5-6: React core (hooks, state, lifecycle, rendering)
  - Week 7-8: Next.js, SSR/SSG, routing
  - Week 9+: TypeScript, testing, performance, accessibility

### 5. 🤖 AI Update (2-3 min read)
- Alternates between news days and concept days
- News: fresh AI headlines, new models, papers, launches
- Concepts: transformers, RLHF, RAG, agents, etc.
- "为什么你应该关心 / Why you should care"
- Practical relevance for engineers

## Language
- Bilingual: Chinese first, English second in each section
- Code comments in English

## Delivery
- Telegram: 5 separate messages (one per section)
- Email: 1 combined email to Auggie1024.d@gmail.com
- Daily at 8:00 AM PT via OpenClaw cron

## Data Files to Create

### content/neetcode-150.json
Array of 150 problems in NeetCode order, grouped by pattern:
```json
[
  {
    "id": 1,
    "title": "Contains Duplicate",
    "leetcode_num": 217,
    "pattern": "Arrays & Hashing",
    "difficulty": "Easy",
    "url": "https://leetcode.com/problems/contains-duplicate/"
  }
]
```

### content/system-design.json
Array of ~40 system design topics in progressive order:
```json
[
  {
    "id": 1,
    "title": "Client-Server Model & DNS",
    "category": "Fundamentals",
    "difficulty": "Beginner"
  }
]
```

### content/behavioral.json
Array of ~40 behavioral questions:
```json
[
  {
    "id": 1,
    "question": "Tell me about a time you had to make a technical decision with incomplete information",
    "category": "Decision Making",
    "level": "Senior/Staff"
  }
]
```

### content/frontend.json
Array of ~60 frontend topics in progressive order:
```json
[
  {
    "id": 1,
    "title": "CSS Box Model",
    "category": "CSS Fundamentals",
    "week": 1
  }
]
```

### content/ai-topics.json
Array of ~30 AI concept topics (for non-news days):
```json
[
  {
    "id": 1,
    "title": "How Transformers Work",
    "category": "Foundations"
  }
]
```

### state.json
```json
{
  "currentDay": 0,
  "lastSentDate": null,
  "systemDesignIndex": 0,
  "leetcodeIndex": 0,
  "behavioralIndex": 0,
  "frontendIndex": 0,
  "aiTopicIndex": 0,
  "history": []
}
```

### archive/
Each day's content saved as `YYYY-MM-DD.md`

## README.md
- Overview of the project
- Progress tracker (which problems/topics covered)
- How to run manually
- Cron job reference

## Quality Bar
- Teach like a good teacher with interesting examples
- Real-world analogies before abstract concepts
- Visual traces, ASCII diagrams
- "Guess what this outputs" interactive style for frontend
- Bad vs Good answer comparisons for behavioral
- Each day can reference previous days' knowledge
