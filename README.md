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

### 🎤 [talk-eval-kit](talk-eval-kit)

**Local-first toolkit for turning talk recordings into coaching-ready transcripts, metrics, and rhetorical analysis**

End-to-end analysis kit that transcribes recorded talks, computes quantitative delivery metrics, extracts key passages, and runs a psychology-informed rhetorical pass to support high-quality speaker coaching.

**Key Features:**
- Word-level timestamped transcription via faster-whisper
- Delivery metrics: pace, fillers, pauses, and engagement markers
- Config-driven deep passage extraction around thesis and landmarks
- Psychological-design analysis (Cialdini, peak-end, CTA, efficacy framing)

**Stack:** Python, faster-whisper, ffmpeg (optional), local AI workflows

[📖 Full Documentation](./talk-eval-kit/README.md)

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

### 🎯 [work-ingestion](work-ingestion)

**AI-powered framework for transforming rough feature requests into implementation-ready specifications**

Two-stage conversational AI system using inference-first questioning to refine vague ideas into polished specs. Iteratively assesses completeness, asks smart clarifying questions, and synthesizes structured output for development teams.

**Key Features:**
- Inference-first questioning (AI proposes answers to confirm/refine)
- Iterative refinement with completeness tracking (never re-asks)
- Production-validated: 100+ features/month at BrightCom
- Includes full Power Automate + Azure OpenAI implementation guide

**Stack:** AI prompts (GPT-4/Claude), Power Automate, Azure DevOps, Teams

[📖 Full Documentation](./work-ingestion/README.md)

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
