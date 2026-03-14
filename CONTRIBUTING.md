# Contributing to byte-by-byte

Thanks for your interest in contributing! byte-by-byte is a community project and we welcome help in many forms — from fixing typos to building entirely new sections.

---

## 🤝 Ways to Contribute

| Type | How |
|------|-----|
| 📝 Content improvements | Fix errors, sharpen explanations in `samples/` or `archive/` |
| ➕ Add problems/topics | Extend `content/*.json` databases |
| 🌐 Translations | Add languages beyond Chinese/English |
| 🐛 Bug reports | Open an issue with expected vs actual output |
| 💡 Topic suggestions | Open an issue tagged `content-request` |
| 🔧 Infrastructure | Improve scripts, add GitHub Actions, new delivery methods |

---

## 📝 Adding New Content Sections

### Adding a New Topic to Existing Databases

Each category has a JSON database in `content/`:

| File | Category | Format |
|------|----------|--------|
| `content/neetcode-150.json` | Algorithms | See below |
| `content/system-design.json` | System Design | `{ "id", "title", "difficulty", "category" }` |
| `content/behavioral.json` | Soft Skills | `{ "id", "question", "category", "level" }` |
| `content/frontend.json` | Frontend | `{ "id", "topic", "week", "category" }` |
| `content/ai-topics.json` | AI | `{ "id", "topic", "type", "difficulty" }` |

**Algorithm entry format:**
```json
{
  "id": 217,
  "title": "Contains Duplicate",
  "difficulty": "Easy",
  "pattern": "Arrays & Hashing",
  "neetcode_url": "https://neetcode.io/problems/duplicate-integer"
}
```

### Adding a Whole New Section

If you want to add a new daily section (e.g., DevOps, Database Design):

1. Create `content/<new-section>.json` with the topic list
2. Add a prompt in `cron/daily-prompt.md` for the new section
3. Update `scripts/generate.sh` to pick a topic from the new file
4. Update `scripts/generate-index.py` `SECTION_META` dict
5. Open a PR — tag it `new-section`

---

## 💡 Submitting Topic Suggestions

Have an algorithm problem, system design case study, or frontend concept you want covered?

**Open a GitHub Issue** with:

```
Title: [Topic Request] <your topic>

Category: [algorithms / system-design / soft-skills / frontend / ai]
Topic: <what you want covered>
Why this topic?: <why it's worth including>
Difficulty: [beginner / intermediate / advanced]
References: <any good resources you found>
```

We aim to respond to topic requests within 1 week.

---

## 🔀 PR Template for Content Contributions

When opening a Pull Request, please include:

```markdown
## What's changed
<!-- Brief description of the change -->

## Category
- [ ] algorithms
- [ ] system-design
- [ ] soft-skills
- [ ] frontend
- [ ] ai
- [ ] infrastructure / scripts

## Checklist
- [ ] Content is bilingual (Chinese + English)
- [ ] Code examples are correct (traced through manually)
- [ ] Follows existing format (see samples/ for reference)
- [ ] No sensitive info or credentials included
- [ ] `python3 scripts/generate-index.py` runs without errors (if touching scripts)

## Testing
<!-- How did you verify this works? -->
```

---

## 📏 Content Quality Bar

All content must meet these standards before merging:

### ✅ Required
- **Bilingual** — Chinese first, English second (not just a translation — written for both audiences)
- **Accurate** — code traces verified, answers correct
- **Analogy-first** — start with a real-world scenario before technical details
- **Appropriately scoped** — each section should take 2–4 minutes to read

### 🎯 Encouraged
- "Guess the output" challenges for algorithms and frontend
- ASCII diagrams for system design
- Step-by-step traces (like the ticket-stamping trace in Day 1)
- "Today's pattern" callout at the end
- Connections to previous days

### ❌ Not acceptable
- English-only content
- Copy-paste from LeetCode editorial without transformation
- Overly abstract explanations with no concrete example
- Content that requires more than 4 minutes to read

---

## 🔍 How the QA System Works

Every generated piece of content passes through an automated QA review before delivery. Understanding this helps you write content that passes.

### QA Prompts

The QA system lives in `cron/qa-prompt.md`. It checks generated content against:

1. **Accuracy** — Are code examples syntactically correct? Do they trace correctly?
2. **Bilingual completeness** — Is every concept explained in both languages?
3. **Analogy quality** — Is the real-world analogy clear and relevant?
4. **Scope** — Is the content appropriately sized (not too long, not too short)?
5. **Format** — Does it follow the established template structure?

### QA Reports

After each generation run, a QA report is saved to `archive/<date>-qa-report.md`. You can check these to see what kinds of issues get flagged.

### For Contributors

When submitting content PRs:
- Read through a QA report to understand common failure modes
- Self-review against the checklist above before submitting
- If your PR is a content fix, reference the original QA report issue

---

## 🤲 Code of Conduct

This project follows a simple code of conduct: **be kind, be helpful, we're all here to learn**.

Specifically:
- Critique the content, not the contributor
- Questions from beginners are welcome — we were all there once
- If you spot an error, assume good faith and open an issue or PR
- Language-related feedback (Chinese or English) is always appreciated

Unacceptable: harassment, discrimination, or bad-faith criticism. Violations will result in being blocked from the project.

---

## 🚀 Getting Started

```bash
# 1. Fork + clone
git clone https://github.com/YOUR_USERNAME/byte-by-byte.git
cd byte-by-byte

# 2. Create a branch
git checkout -b improve-algorithms-day5

# 3. Make your changes

# 4. Test scripts if you touched them
python3 scripts/generate-index.py

# 5. Push and open a PR
git push origin improve-algorithms-day5
```

---

*Questions? Open an issue — we're happy to help you get started.* 🧠
