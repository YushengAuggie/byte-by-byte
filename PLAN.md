# Implementation Plan — byte-by-byte

> *A little bit every day. A lot over time.*

## 🎯 Project Summary
Automated daily tech knowledge system: 5 bilingual (CN/EN) messages via Telegram + 1 combined email, every day at 8:00 AM PT. Covers system design, algorithms, soft skills, frontend, and AI. Self-reviewing with QA pass.

---

## ✅ Checklist

### Phase 1: Repo & Branding ✅
- [x] Create GitHub repo → github.com/YushengAuggie/byte-by-byte
- [x] Write SPEC.md, README.md, PLAN.md
- [x] Tagline: "A little bit every day. A lot over time."
- [x] Rebrand all files/cron jobs (no interview-specific language)

### Phase 2: Content Databases ✅
- [x] `content/neetcode-150.json` — 150 problems, NeetCode order
- [x] `content/system-design.json` — 40 topics, progressive
- [x] `content/behavioral.json` — 40 questions, senior/staff
- [x] `content/frontend.json` — 50 topics, CSS → Next.js
- [x] `content/ai-topics.json` — 30 AI concepts
- [x] `state.json` — progress tracking
- [ ] **Verify NeetCode 150 matches official list**

### Phase 3: Automation Scripts ✅
- [x] `config.env` — machine-specific settings (portable!)
- [x] `scripts/generate.sh` — reads config, picks topics, updates state atomically
- [x] `scripts/commit.sh` — git commit + push with retry
- [x] `scripts/setup.sh` — one-command setup on new machines
- [x] `cron/daily-prompt.md` — prompt stored in repo (not hardcoded in cron)
- [x] `cron/qa-prompt.md` — QA reviewer prompt stored in repo
- [x] `.gitignore` — OS files, temp files

### Phase 4: Cron Jobs ✅
- [x] **1 daily cron job** at 8:00 AM PT (replaces 5 separate jobs)
  - Runs generate.sh → generates 5 sections → self-reviews → sends → archives → commits
- [x] **1 QA cron job** at 8:15 AM PT
  - Reviews all 5 archive files → grades each section → reports issues → logs improvements
- [x] Both: isolated session, announce to Telegram, model=sonnet

### Phase 5: Quality System ✅
- [x] **Self-review** built into daily prompt (checklist before sending)
  - Code accuracy, diagram readability, Chinese fluency, difficulty level, format
- [x] **QA reviewer** as separate cron job
  - Grades each section ✅/⚠️/❌
  - Detailed bug reports for ❌
  - Improvement suggestions for ⚠️
  - Logs to `qa-log.md` for continuous improvement
  - Commits QA report to archive

### Phase 6: Portability ✅
- [x] `config.env` — all machine-specific values in one file
- [x] `scripts/setup.sh` — creates cron jobs from repo config
- [x] Prompts stored in `cron/*.md` — not hardcoded
- [x] New laptop workflow:
  ```
  git clone https://github.com/YushengAuggie/byte-by-byte.git
  cd byte-by-byte
  vim config.env  # update paths
  ./scripts/setup.sh
  ```

### Phase 7: Email Delivery ⬜
- [ ] Check if `gog` CLI is configured for Gmail
- [ ] Create 3rd cron job at 8:20 AM — reads archives, sends combined email
- [ ] Test email to Auggie1024.d@gmail.com

### Phase 8: Public Polish ⬜
- [ ] Add "How to set up your own" section in README
- [ ] Add LICENSE file (MIT)
- [ ] Sanitize personal info from committed files
- [ ] Add sample output in `samples/`
- [ ] Document GitHub Actions alternative

### Phase 9: Ongoing Maintenance ⬜
- [ ] Monitor first week
- [ ] Review QA reports, iterate on prompts
- [ ] Plan content extensions before exhaustion
- [ ] Consider user feedback mechanism

---

## 📁 Repo Structure

```
byte-by-byte/
├── README.md              ← public-facing overview
├── SPEC.md                ← full specification
├── PLAN.md                ← this file (implementation checklist)
├── config.env             ← machine-specific settings
├── .gitignore
├── state.json             ← progress tracking
├── qa-log.md              ← QA improvement log (created after first run)
├── content/
│   ├── neetcode-150.json  ← 150 algorithm problems
│   ├── system-design.json ← 40 system design topics
│   ├── behavioral.json    ← 40 soft skills questions
│   ├── frontend.json      ← 50 frontend topics
│   └── ai-topics.json     ← 30 AI concepts
├── archive/               ← daily content + QA reports
│   ├── YYYY-MM-DD-system-design.md
│   ├── YYYY-MM-DD-algorithms.md
│   ├── YYYY-MM-DD-soft-skills.md
│   ├── YYYY-MM-DD-frontend.md
│   ├── YYYY-MM-DD-ai.md
│   └── YYYY-MM-DD-qa-report.md
├── scripts/
│   ├── generate.sh        ← topic picker + state manager
│   ├── commit.sh          ← git commit + push
│   └── setup.sh           ← new machine setup
└── cron/
    ├── daily-prompt.md    ← generation prompt (stored in repo)
    └── qa-prompt.md       ← QA reviewer prompt (stored in repo)
```

## 📐 Flow

```
8:00 AM ─→ Cron triggers "byte-by-byte daily"
  │
  ├─ Step 1: generate.sh
  │   ├─ Read state.json
  │   ├─ Pick topics from content/*.json
  │   ├─ Write /tmp/bbb-section-{1..5}.txt
  │   └─ Update state.json atomically
  │
  ├─ Step 2: LLM generates 5 sections
  │
  ├─ Step 3: Self-review checklist
  │   └─ Revise if needed
  │
  ├─ Step 4: Send 5 Telegram messages
  │
  ├─ Step 5: Save to archive/
  │
  └─ Step 6: commit.sh → git push

8:15 AM ─→ Cron triggers "byte-by-byte QA"
  │
  ├─ Read today's archive files
  ├─ Grade each section ✅/⚠️/❌
  ├─ Send QA report to Telegram
  ├─ Log issues to qa-log.md
  └─ commit.sh → git push
```

## ⚠️ Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| state.json race | Single cron job, sequential execution |
| Git push fail | commit.sh has pull --rebase retry |
| Code bugs in output | Self-review + QA reviewer double-check |
| Hardcoded paths | config.env + setup.sh |
| Content exhaustion | Shortest: soft skills (40 days). Plan extensions at Day 30. |
| LLM prompt drift | QA logs track issues. Iterate prompts. |

## 📅 Status

| Phase | Status |
|-------|--------|
| Repo & Branding | ✅ Complete |
| Content Databases | ✅ Complete |
| Automation Scripts | ✅ Complete |
| Cron Jobs | ✅ Live (first run tomorrow 8 AM) |
| Quality System | ✅ Self-review + QA reviewer |
| Portability | ✅ config.env + setup.sh |
| Email Delivery | ⬜ Next |
| Public Polish | ⬜ This weekend |
| Ongoing | ⬜ Continuous |
