# Implementation Plan — Daily Knowledge Digest

## 🎯 Project Summary
Automated daily knowledge delivery system: 5 bilingual (CN/EN) messages via Telegram + 1 combined email, every day at 8:00 AM PT. Content covers system design, algorithms, behavioral skills, frontend, and AI — designed as a general learning resource (not interview-specific branding).

---

## ✅ Checklist

### Phase 1: Repo & Branding
- [x] Create GitHub repo
- [x] Write SPEC.md
- [x] Write README.md
- [ ] **Pick final repo name** (brainstormed: `morning-bytes`, `dev-espresso`, `byte-by-byte`, etc.)
- [ ] **Rename GitHub repo** to chosen name
- [ ] **Update README.md** — rebrand language from "interview prep" to "daily learning"
- [ ] **Update SPEC.md** — match new branding
- [ ] **Update cron job names** — remove "Interview Prep" wording
- [ ] Update local workspace directory name to match

### Phase 2: Content Databases
- [x] `content/neetcode-150.json` — 150 problems, NeetCode order, pattern-grouped
- [x] `content/system-design.json` — 40 topics, progressive difficulty
- [x] `content/behavioral.json` — 40 questions, senior/staff level
- [x] `content/frontend.json` — 50 topics, CSS → React → Next.js → TypeScript
- [x] `content/ai-topics.json` — 30 AI concept topics
- [x] `state.json` — progress tracking
- [ ] **Review content databases for completeness** — spot check a few entries in each
- [ ] **Verify NeetCode 150 matches official list** — cross-check with neetcode.io

### Phase 3: Cron Jobs (Telegram Delivery)
- [x] Cron 1: System Design — 8:00 AM PT daily
- [x] Cron 2: LeetCode — 8:01 AM PT daily
- [x] Cron 3: Behavioral — 8:02 AM PT daily
- [x] Cron 4: Frontend — 8:03 AM PT daily
- [x] Cron 5: AI Update — 8:04 AM PT daily
- [x] All jobs: isolated session, announce to Telegram, model=sonnet
- [x] All jobs: save to archive/, update state.json, git commit+push
- [ ] **Test run all 5 jobs manually** — verify output quality before first live morning
- [ ] **Verify state.json updates correctly** after test runs
- [ ] **Verify archive/ files are created** with correct naming
- [ ] **Verify git commit+push works** from cron context
- [ ] **Check Telegram message formatting** — ensure no truncation, markdown renders properly
- [ ] **Handle concurrency** — jobs run 1 min apart, but verify no state.json race conditions

### Phase 4: Email Delivery
- [ ] **Check if `gog` CLI is installed and configured** for Gmail
- [ ] If gog works: add email sending to each cron job (or a 6th aggregator job)
- [ ] If gog doesn't work: set up alternative (IMAP/SMTP skill, or gog OAuth setup)
- [ ] **Design email format** — combined daily digest, all 5 sections in one email
- [ ] **Option A:** 6th cron job at 8:05 AM that reads today's 5 archive files and sends combined email
- [ ] **Option B:** Each cron job appends, last one (AI) sends the email
- [ ] **Decision:** Go with Option A (cleaner, single responsibility)
- [ ] **Create cron job 6: Daily Email Digest** — 8:10 AM PT (gives 5 jobs time to finish)
- [ ] **Test email delivery** to Auggie1024.d@gmail.com

### Phase 5: Quality & Polish
- [ ] **Run Day 1 manually** and review all 5 outputs for quality
- [ ] Verify bilingual format is consistent (Chinese first, English second)
- [ ] Verify system design has ASCII diagrams
- [ ] Verify LeetCode has working Python code + visual trace
- [ ] Verify behavioral has bad/good answer comparison
- [ ] Verify frontend has "guess the output" interactive element
- [ ] Verify AI update alternates between news and concept days
- [ ] **Adjust prompts** based on Day 1 review if needed
- [ ] **Confirm cross-day references work** — Day 2+ should reference Day 1 concepts when relevant

### Phase 6: Repo Polish (for public use)
- [ ] **Update README.md for public audience** — how others can fork/use it
- [ ] Add "How to set up your own" section in README
- [ ] Add LICENSE file (MIT?)
- [ ] Remove any personal info (email, Telegram ID) from committed files
- [ ] `state.json` in `.gitignore`? Or keep it for progress tracking visibility?
- [ ] Add `.gitignore` for any temp files
- [ ] Add sample output in README or a `samples/` directory
- [ ] Consider GitHub Actions alternative for non-OpenClaw users

### Phase 7: Ongoing Maintenance
- [ ] **Monitor first week** of daily sends for issues
- [ ] Set up error alerting if a cron job fails
- [ ] Plan for when NeetCode 150 is exhausted (~150 days) — cycle back or add LeetCode 75?
- [ ] Plan for when system design topics are exhausted (~40 days) — add more or deep-dive repeats?
- [ ] Plan for when frontend topics are exhausted (~50 days)
- [ ] Plan for when behavioral questions are exhausted (~40 days)
- [ ] **Memory maintenance** — periodically review and update content databases
- [ ] Consider adding user feedback mechanism (reply to rate quality)

---

## 📐 Architecture

```
┌─────────────────────────────────────────┐
│           OpenClaw Gateway               │
│                                          │
│  Cron Scheduler (5+1 jobs)               │
│  ┌──────────┐  8:00  System Design      │
│  │ state.json│  8:01  LeetCode           │
│  │ (shared)  │  8:02  Behavioral         │
│  └──────────┘  8:03  Frontend            │
│       ↕        8:04  AI Update           │
│  ┌──────────┐  8:10  Email Digest        │
│  │ content/  │                            │
│  │ *.json    │                            │
│  └──────────┘                            │
│       ↓                                   │
│  ┌──────────┐  ┌──────────┐              │
│  │ Telegram  │  │  Email   │              │
│  │ (5 msgs)  │  │ (1 digest│              │
│  └──────────┘  └──────────┘              │
│       ↓                                   │
│  ┌──────────┐                            │
│  │ archive/  │  → git commit + push      │
│  │ YYYY-MM-DD│                            │
│  └──────────┘                            │
└─────────────────────────────────────────┘
```

## ⚠️ Known Risks

| Risk | Mitigation |
|------|-----------|
| state.json race condition (5 jobs writing) | Jobs staggered 1 min apart, should be fine. Monitor. |
| Telegram message too long | Sonnet is prompted for 3-4 min reads, should fit. Add truncation if needed. |
| Git push fails from cron | Jobs have git push; if it fails, content still delivered. Fix manually. |
| Email not set up yet | Phase 4 — need to verify gog/IMAP before creating email cron. |
| Content quality varies | Review Day 1 output, iterate on prompts. |
| NeetCode 150 exhausted | ~5 months of content. Plan extension before then. |

## 📅 Timeline

| Phase | Status | ETA |
|-------|--------|-----|
| Phase 1: Repo & Branding | 🔄 In progress (need name decision) | Tonight |
| Phase 2: Content Databases | ✅ Done | Done |
| Phase 3: Cron Jobs | ✅ Created, needs testing | Tomorrow 8 AM first live run |
| Phase 4: Email Delivery | ⬜ Not started | Tomorrow |
| Phase 5: Quality & Polish | ⬜ Waiting on Day 1 output | Tomorrow after first run |
| Phase 6: Repo Polish | ⬜ Not started | This weekend |
| Phase 7: Ongoing | ⬜ Continuous | Ongoing |

## 🔑 Key Decisions Needed

1. **Repo name** — pick from brainstorm list or new idea
2. **Email approach** — confirm gog works, or use alternative
3. **License** — MIT for public sharing?
4. **state.json visibility** — gitignore or keep public?
