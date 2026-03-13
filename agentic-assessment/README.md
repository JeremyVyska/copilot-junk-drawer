# AI-Assisted Development Impact Analysis

A complete, data-driven framework for quantifying the impact of AI coding assistants on both **productivity** and **code quality**. Built from real analysis of Microsoft MVP Jeremy Vyska's development work, these templates are fully reusable for any developer with commit history.

## What This Is

Two complementary analysis templates that together answer the question: *"What measurable difference do AI coding agents make?"*

### 1. Productivity Analysis ([productivity-analysis-template.md](productivity-analysis-template.md))

Measures **volume and velocity** — commits, files, lines of code, and scope expansion over time.

- Uses git commit history from GitHub, Azure DevOps, or both
- Compares pre-agent and post-agent periods with actual statistical multipliers
- Produces a narrative story backed by 10 publication-ready charts
- **Jeremy's findings**: 3x commit velocity, 12.5x lines-added multiplier, clear platform diversification

### 2. Quality Analysis ([quality-analysis-template.md](quality-analysis-template.md))

Measures **code quality density** — testing, documentation, design patterns, security.

- Uses static code analysis to compare two codebases (or git checkpoints)
- Normalizes all metrics per 1,000 lines to account for size differences
- Produces side-by-side comparison tables and quality attribute charts
- **Jeremy's findings**: 252x test procedures, 57x structured documentation, 0→48 secure credential patterns — all in a codebase built *faster*

## Prerequisites

### Required Tools

Both templates require:
- **Git** — for repository access
- **PowerShell** — for data collection scripts (cross-platform: pwsh)
- **Python 3.x** with matplotlib — for chart generation
- **Node.js** — for JSON processing scripts (productivity analysis)

### Additional for Productivity Analysis

- **GitHub CLI** (`gh`) — if analyzing GitHub repos
  - Install: `winget install GitHub.cli`
  - Authenticate: `gh auth login`
- **Azure CLI** (`az`) — if analyzing Azure DevOps repos
  - Install: `winget install Microsoft.AzureCLI`
  - Authenticate: `az login` + `az account set --subscription <id>`

### Verify Prerequisites

```powershell
# Check all tools
git --version
pwsh --version
python --version
node --version
gh auth status        # if using GitHub
az account show       # if using Azure DevOps

# Install Python dependencies
pip install matplotlib pandas
```

## Which Template Should I Use?

| Use Case | Template | Time Required |
|----------|----------|---------------|
| "Did AI make me faster?" | Productivity | 2-4 hours |
| "Did AI make me write better code?" | Quality | 1-2 hours |
| "I need the complete story for a blog/talk" | Both | 4-6 hours |
| "I want quick personal insight" | Productivity only | 2 hours |

**Best practice**: Run productivity analysis first. Its findings will strengthen the quality analysis narrative ("I wrote 3x more commits AND they had 57x more documentation").

## What You'll Get

### Productivity Analysis Outputs

- **Data files**:
  - `full-inventory.json` — raw weekly commit data
  - `development-summary.json` — monthly aggregates with period labels
  - `pattern-analysis.json` — platform splits, categories, velocity patterns
- **Narrative**: `productivity-narrative.md` — 1,500–2,500 word data-driven story
- **Charts** (10 PNGs in `charts/`):
  - Commits over time with inflection point
  - Lines of code over time
  - Platform distribution (before/after)
  - Repo category breakdown
  - Before/after comparison bars with multipliers
  - Repo activity heatmap
  - Active repos trend
  - Cumulative commits (slope change visualization)
  - Platform share trend
  - Commit depth (files per commit)

### Quality Analysis Outputs

- **Data file**: `quality-metrics.json` — raw and normalized metrics for both codebases
- **Narrative**: `quality-compare.md` — dimension-by-dimension comparison with honest caveats
- **Charts** (2 PNGs in `charts/`):
  - Code composition pies (test %, comment density)
  - Quality attributes bar chart (9 dimensions normalized)

## Quick Start

### Step 1: Choose Your Template

Open the template file in your editor and read Phase 0 (Interview).

### Step 2: Answer the Interview Questions

The agent (or you manually) must work through all interview questions. These answers replace all hardcoded values and determine the analysis strategy.

### Step 3: Run the Phases

Each template has 4-6 phases that build sequentially:
1. **Interview** → capture context
2. **Data Collection** → clone repos, run git commands, call APIs
3. **Aggregation/Analysis** → process raw data into patterns
4. **Narrative** → write the story
5. **Charts** → visualize the findings

### Step 4: Review and Publish

All outputs are publication-ready. Review for any sensitive information (repo names, internal project details) and adjust framing for your audience.

## Honest Limitations

Both templates emphasize transparency:

- **Commits are a proxy, not the whole picture** — code reviews, architecture discussions, and planning time aren't captured
- **Correlation ≠ causation** — job changes, available time, and project type all influence outcomes
- **Static analysis has blind spots** — quality metrics measure presence, not correctness
- **Confounders matter** — both templates explicitly document caveats in the output

The goal is **insight**, not marketing. Honest acknowledgment of limitations strengthens credibility.

## Example Use Cases

- **Personal reflection** — "How has my workflow actually changed?"
- **Team conversation** — "Should we invest in AI tooling?"
- **Conference talk** — Data-backed story with visuals
- **Blog post** — Thought leadership with real numbers
- **Manager discussion** — ROI evidence for tooling budget

## Support and Customization

These templates are designed to be adapted. Common customizations:
- **Add new quality dimensions** — memory safety patterns, accessibility checks, internationalization
- **Different chart styles** — adjust colors, layout, or add export formats (SVG, PDF)
- **Multi-language analysis** — extend the quality template's language pattern table
- **Additional platforms** — add GitLab, Bitbucket, or custom git servers to productivity collection

## Credits

Created by **Jeremy Vyska** (Microsoft MVP, Business Central Developer) from analysis of his own development work, January 2025–March 2026. Built with assistance from Claude (Anthropic) and refined through real-world application.

## License

These templates are freely usable. Attribution appreciated but not required.

---

**Ready to start?** Open [productivity-analysis-template.md](productivity-analysis-template.md) or [quality-analysis-template.md](quality-analysis-template.md) and begin at Phase 0.
