# 🗄️ Copilot Junk Drawer

**The junk drawer every developer needs** — a collection of powerful, focused tools that don't quite warrant their own repo, but are too useful to scatter across random gists.

You know that drawer in your kitchen with batteries, twist ties, and that one perfect screwdriver? This is that, but for development automation.

---

## 📦 What's Inside

### 📊 [agentic-assessment](agentic-assessment)

**Data-driven framework for quantifying AI coding assistant impact on productivity and code quality**

Complete analysis framework using git commit history to answer: "What measurable difference do AI coding agents make?" Includes productivity analysis (commits, velocity, scope) and quality analysis (testing, docs, security patterns).

**Key Features:**
- Productivity analysis from GitHub/Azure DevOps commit history
- Code quality density comparisons (testing, docs, security)
- Publication-ready charts and statistical multipliers
- Real findings: 3x commits, 12.5x lines, 252x test coverage

**Stack:** PowerShell, Python (matplotlib), Node.js, GitHub CLI, Azure CLI

[📖 Full Documentation](./agentic-assessment/README.md)

---

### ⏱️ [time-narrative](time-narrative)

**Transform raw Clockify time-tracking data into AI-generated weekly narratives**

Extracts activity data from Clockify SQLite database, buckets into 30-minute slots, and uses parallel AI agents to generate human-readable markdown narratives of your work week.

**Key Features:**
- SQLite extraction from Clockify AutoTracker database
- 30-minute time slot bucketing with activity aggregation
- Parallel AI agent processing (one per day)
- Markdown narratives with semantic activity labels

**Stack:** Node.js, SQLite, Claude Code/AI agents

[📖 Full Documentation](./time-narrative/README.md)

---

## 🎨 Philosophy

This repo follows the **Junk Drawer Principle**:

> A tool should live in its own repo when it needs independent versioning, CI/CD, or community. Otherwise, it lives here with friends.

**Criteria for inclusion:**
- ✅ Solves a real problem elegantly
- ✅ Self-contained (minimal cross-dependencies)
- ✅ Well-documented with clear README
- ✅ Production-ready, not experimental
- ❌ Doesn't need semantic versioning
- ❌ Doesn't need independent deployment pipeline

---

## 🚀 Quick Start

Each tool is self-contained in its own folder with:
- Dedicated `README.md` with installation & usage
- All necessary code and dependencies
- Example outputs or templates

Navigate to the tool folder and follow its README.

---

## 🤝 Contributing

Got a powerful utility that doesn't warrant a full repo? Add it here:

1. Create a new folder with a descriptive lowercase-with-hyphens name
2. Include a comprehensive `README.md` following the pattern above
3. Make sure it's self-contained (dependencies declared, tooling documented)
4. Submit a PR

The README will be automatically updated to include your contribution.

---

## 📜 License

MIT License — see [LICENSE](./LICENSE) for details.

Each tool may have additional licensing requirements for dependencies. Check individual README files.

---

## 👤 Author

**Jeremy Vyska**  
Microsoft MVP | Business Central Expert | AI Enthusiast

*Because sometimes the best repos are the ones that hold all the pieces that don't fit anywhere else.*

![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FJeremyVyska%2Fcopilot-junk-drawer&label=VISITORS&countColor=%23263759&style=flat-square)