# Implementation Plan — byte-by-byte

> *A little bit every day. A lot over time.*

## 🎯 Project Summary
Automated daily tech knowledge system: 5 bilingual (CN/EN) messages via Telegram + 1 combined email, every day at 8:00 AM PT. Covers system design, algorithms, soft skills, frontend, and AI.

---

## ✅ Checklist

### Phase 1: Repo & Branding ✅
- [x] Create GitHub repo
- [x] Write SPEC.md
- [x] Write README.md with tagline
- [x] Pick final repo name → `byte-by-byte`
- [x] Rename GitHub repo → github.com/YushengAuggie/byte-by-byte
- [x] Update README.md — rebranded to daily learning
- [x] Update SPEC.md — match new branding
- [x] Update cron job names — now "byte-by-byte 1/5" etc.
- [x] Update local workspace directory → `byte-by-byte/`
- [x] Update all cron job paths from `daily-interview-prep` → `byte-by-byte`

### Phase 2: Content Databases ✅
- [x] `content/neetcode-150.json` — 150 problems, NeetCode order, pattern-grouped
- [x] `content/system-design.json` — 40 topics, progressive difficulty
- [x] `content/behavioral.json` — 40 questions, senior/staff level
- [x] `content/frontend.json` — 50 topics, CSS → React → Next.js → TypeScript
- [x] `content/ai-topics.json` — 30 AI concept topics
- [x] `state.json` — progress tracking
- [ ] **Verify NeetCode 150 matches official list** — cross-check with neetcode.io

### Phase 3: Cron Jobs (Telegram Delivery) ✅
- [x] Cron 1: System Design — 8:00 AM PT daily
- [x] Cron 2: Algorithms — 8:01 AM PT daily
- [x] Cron 3: Soft Skills — 8:02 AM PT daily
- [x] Cron 4: Frontend — 8:03 AM PT daily
- [x] Cron 5: AI — 8:04 AM PT daily
- [x] All jobs: isolated session, announce to Telegram, model=sonnet
- [x] All jobs: save to archive/, update state.json, git commit+push
- [ ] **Test run all 5 jobs manually** — verify output quality
- [ ] **Verify state.json updates correctly** after test runs
- [ ] **Verify archive/ files are created** with correct naming
- [ ] **Verify git commit+push works** from cron context
- [ ] **Check Telegram message formatting** — no truncation, markdown renders
- [ ] **Confirm no state.json race conditions** — jobs 1 min apart, should be fine

### Phase 4: Email Delivery ⬜
- [ ] **Check if `gog` CLI is configured** for Gmail sending
- [ ] If gog works: create 6th cron job as email aggregator
- [ ] If not: set up alternative (IMAP/SMTP skill, or gog OAuth)
- [ ] **Create cron job 6: Daily Email Digest** — 8:10 AM PT
  - Reads today's 5 archive files, combines into one email
  - Sends to Auggie1024.d@gmail.com
- [ ] **Test email delivery**

### Phase 5: Quality & Polish ⬜
- [ ] **Run Day 1 and review all 5 outputs**
- [ ] Verify bilingual format (Chinese first, English second)
- [ ] Verify system design has ASCII diagrams
- [ ] Verify algorithms has working Python code + visual trace
- [ ] Verify soft skills has bad/good comparison
- [ ] Verify frontend has "guess the output" element
- [ ] Verify AI alternates between news and concept days
- [ ] **Adjust prompts** based on Day 1 review
- [ ] **Confirm cross-day references** — Day 2+ references earlier concepts

### Phase 6: Public Polish ⬜
- [ ] Add "How to set up your own" section in README
- [ ] Add LICENSE file (MIT)
- [ ] Remove personal info (email, Telegram ID) from committed files
- [ ] Add `.gitignore` (state.json? temp files?)
- [ ] Add sample output in `samples/` directory
- [ ] Consider GitHub Actions alternative for non-OpenClaw users

### Phase 7: Ongoing Maintenance ⬜
- [ ] Monitor first week for issues
- [ ] Set up error alerting on cron failure
- [ ] Plan content extensions before exhaustion:
  - NeetCode 150: ~150 days → add LeetCode 75 hard mode?
  - System Design: ~40 days → add deep-dive repeats
  - Frontend: ~50 days → add advanced topics
  - Soft Skills: ~40 days → add scenario variations
- [ ] Consider user feedback mechanism (reply to rate quality)

---

## 📐 Architecture

```
┌──────────────────────────────────────────┐
│            OpenClaw Gateway               │
│                                           │
│  Cron Scheduler (5+1 jobs)                │
│  ┌───────────┐  8:00  🏗️ System Design   │
│  │ state.json │  8:01  💻 Algorithms      │
│  │  (shared)  │  8:02  🗣️ Soft Skills    │
│  └───────────┘  8:03  🎨 Frontend         │
│       ↕         8:04  🤖 AI              │
│  ┌───────────┐  8:10  📧 Email Digest     │
│  │  content/  │                           │
│  │  *.json    │                           │
│  └───────────┘                           │
│        ↓                                  │
│  ┌───────────┐  ┌───────────┐            │
│  │  Telegram  │  │   Email   │            │
│  │  (5 msgs)  │  │ (1 digest)│            │
│  └───────────┘  └───────────┘            │
│        ↓                                  │
│  ┌───────────┐                           │
│  │  archive/  │  → git commit + push     │
│  │ YYYY-MM-DD │                           │
│  └───────────┘                           │
└──────────────────────────────────────────┘
```

## ⚠️ Known Risks

| Risk | Mitigation |
|------|-----------|
| state.json race condition | Jobs staggered 1 min apart. Monitor first week. |
| Telegram message too long | Prompted for 3-4 min reads. Add truncation if needed. |
| Git push fails from cron | Content still delivered. Fix manually if needed. |
| Email not set up yet | Phase 4 — verify gog/IMAP before creating email cron. |
| Content quality varies | Review Day 1, iterate on prompts. |
| Content exhaustion | Shortest is soft skills (40 days). Plan extensions. |

## 📅 Timeline

| Phase | Status | ETA |
|-------|--------|-----|
| Phase 1: Repo & Branding | ✅ Complete | Done |
| Phase 2: Content Databases | ✅ Complete | Done |
| Phase 3: Cron Jobs | ✅ Created, first run tomorrow 8 AM | Tomorrow |
| Phase 4: Email Delivery | ⬜ Not started | Tomorrow |
| Phase 5: Quality & Polish | ⬜ After Day 1 | Tomorrow |
| Phase 6: Public Polish | ⬜ Not started | This weekend |
| Phase 7: Ongoing | ⬜ Continuous | Ongoing |

## 🔑 Key Decisions Remaining

1. **Email approach** — confirm gog works, or use alternative
2. **License** — MIT for public sharing
3. **state.json** — gitignore or keep public?
