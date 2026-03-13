# Developer AI-Productivity Analysis — Reusable Template

## What This Is

A complete, data-driven process for any developer to quantify the impact of AI-assisted development on their own productivity. The output is a full narrative story, pattern analysis, and a set of publication-ready charts — all grounded in real commit data from your own repositories.

This process was originally built for Jeremy Vyska (Microsoft MVP, Business Central developer) and produced findings like a **3x commit velocity increase**, **12.5x lines-added multiplier**, and a clear platform diversification story. Yours will be different — and equally real.

---

## Phase 0: Interview (START HERE)

Before running any code, the agent must interview the requestor to gather the context that replaces all hardcoded values. Ask these questions one at a time and wait for answers. Record the responses — they drive every phase that follows.

### Identity & Context

1. **What's your name and role?**
   *(Used in narrative header and chart titles)*

2. **What kind of work do you primarily do?**
   *(e.g., "backend web dev", "mobile", "ERP/business apps", "data engineering", "fullstack" — used to frame the narrative)*

3. **Do you work at a company, freelance, or primarily on open source?**
   *(Helps frame the ADO/private vs GitHub/public split)*

### Repository Platforms

4. **Which platforms host your code?** *(Select all that apply)*
   - [ ] Azure DevOps (ADO)
   - [ ] GitHub (personal account)
   - [ ] GitHub (organization accounts — list names)
   - [ ] GitLab
   - [ ] Bitbucket
   - [ ] Other

5. **For each platform selected:**
   - What is the organization/tenant URL or name?
   - Are there specific projects/namespaces that contain your work vs. others?
   - Should we include ALL repos or filter by name pattern? (e.g., "only repos starting with XYZ")

6. **Are you authenticated on the CLI for each platform?**
   *(Check: `gh auth status` for GitHub; `az account show` + `az account get-access-token` for ADO; etc.)*

### AI Agent Timeline

7. **When did you start using AI coding agents in a meaningful way?**
   *(e.g., "Around September 2025", "Early 2024", "Just started last month")*
   
8. **When would you say those tools became a real part of your workflow — not just occasional, but genuinely changing HOW you work?**
   *(This is the "inflection point" — will be marked on all timeline charts)*

9. **Is there a "before" period you want as a baseline? Ideally 3–6 months of pre-agent work.**
   *(e.g., "Jan–Jun 2025 before I got serious with Copilot")*

10. **What's the "after" period — the mature agent-assisted era?**
    *(e.g., "Sep 2025 to today", "the last 6 months")*

11. **Were there any transition months between those two periods that you'd consider a "learning curve" or "skill-building" phase?**
    *(These become the transition/bridge period in the analysis — don't exclude them, they tell the learning curve story)*

### Narrative Context

12. **What AI tools are you using?** *(e.g., GitHub Copilot, Claude/Claude Code, Cursor, ChatGPT, etc.)*
    *(Mentioned in the narrative introduction)*

13. **Is there any context about your workload shift that we should know?**
    *(e.g., "I started a new job", "took on more clients", "started giving conference talks", "launched an open source project")*
    *(Important: we want to acknowledge confounders honestly in the narrative)*

14. **Who is the intended audience for the output?**
    - [ ] Personal reflection / private use
    - [ ] Blog post (developer/community audience)
    - [ ] Conference talk (technical audience)
    - [ ] Business conversation (manager/client ROI framing)
    - [ ] Social media post (short form highlight)

---

## Phase 1 & 2: Data Collection

### What to Collect

Collect **all commit activity** across the identified repositories for the **entire date range** (baseline start → today). Do not pre-exclude transition months — collect everything and let the analysis phase assign period labels.

**For each commit, capture:**
- Commit date (for time-slotting into year → month → week)
- Number of files changed (where available without cloning)
- Lines added / deleted (where available via API — GitHub `stats/code_frequency` endpoint, log-scale weekly)

**Note on line stats:**
- GitHub: use `GET /repos/{owner}/{repo}/stats/code_frequency` — weekly line adds/deletes for last 52 weeks. This is an aggregate, not per-commit.
- ADO: the commits list API returns `changeCounts` (Add/Edit/Delete/Rename file counts) without requiring git clone. Line counts are not available without cloning.
- Be transparent in the output about which platforms have line stats and which have file-operation counts only.

### Output Format: `full-inventory.json`

Use a single inventory file covering the complete date range:

```json
{
  "YYYY": {
    "MM": {
      "weekN": {
        "platform_key": {
          "RepoName": {
            "commits": 0,
            "files_changed": 0,
            "lines_added": 0,
            "lines_deleted": 0,
            "net_lines": 0
          }
        }
      }
    }
  }
}
```

Where `platform_key` reflects the actual platforms used (e.g., `"ado"`, `"github"`, `"gitlab"`).

### Period Labels (from interview answers)

After collection, define these constants for all downstream phases:

```
PRE_AGENT_START  = [answer to Q9 start date]
PRE_AGENT_END    = [answer to Q9 end date]
TRANSITION_START = [answer to Q11 start, or null if none]
TRANSITION_END   = [answer to Q11 end, or null if none]
POST_AGENT_START = [answer to Q10 start date]
POST_AGENT_END   = today
INFLECTION_DATE  = [answer to Q8 — the "pedal to the metal" date]
```

---

## Phase 3: Summary Aggregation

Create `summarize-inventory.js` (or equivalent) that reads `full-inventory.json` and outputs `development-summary.json`.

### Monthly aggregates must include:
- `total_commits`
- `total_files`
- `lines_added`, `lines_deleted`, `total_lines_net`
- `repos_active` (unique repos with commits > 0)
- `per_platform_commits` (object keyed by platform_key)
- `weekly_average_commits`
- `period_label`: `"pre_agent"` | `"transition"` | `"post_agent"` (assigned from phase constants above)

### Period totals:
- Aggregate each period separately
- Compute `productivity_multipliers` comparing post-agent to pre-agent averages

---

## Phase 4: Pattern Analysis

Create `analyze-patterns.js` that reads `full-inventory.json` and `development-summary.json` and outputs `pattern-analysis.json`.

### Required analysis:

#### 4a. Platform Distribution
For each period (pre, transition, post):
- Commit count and % by platform
- File count and % by platform
- Net lines by platform

#### 4b. Repository Categories
The interviewer should define categories based on how the person describes their work. Generic starting categories:
- `professional_work` — paid client/employer work (often private repos)
- `tooling_automation` — scripts, CI/CD, dev tools
- `ai_intelligence` — AI tool integrations, experiments, MCP servers
- `community_content` — conference talks, tutorials, demos, blog code
- `open_source` — public libraries, contributions
- `personal_creative` — personal projects, learning experiments

For each category: commits, files, lines by period, list of active repos.

#### 4c. Monthly Velocity
Chronological list with commits, files, lines_net, platform breakdown, repos_active.

#### 4d. Velocity Patterns
- Peak month (commits, files)
- Pre/post averages and multiplier
- Most active repo per platform per period
- Burst vs sustained months (burst = >1.5x period average)

#### 4e. Repo Activity Matrix
All repos with activity: pre_commits, post_commits, transition_commits, categories.
Sort by total commits descending.

#### 4f. New Repos (Post-Agent Only)
Repos with 0 pre-agent commits but >0 post-agent commits. These tell the "agent enabled me to START these" story — scope expansion, not just speed.

#### 4g. Commit Depth
`files_changed / commits` per month — did commits get larger (deeper changes) or more frequent (more focused pushes)?

#### 4h. Platform Share Trend
Per-platform % of monthly commits over time — shows whether domain expansion happened gradually or as a step change.

---

## Phase 5: Narrative Story Creation

Write `productivity-narrative.md` following this arc, substituting all actual numbers from the analysis.

### Narrative Sections

#### Introduction
Open with the most striking multiplier number. Frame what the story is about. Include the person's name, role, and context (from interview). Acknowledge any confounders honestly.

#### Chapter 1: The Baseline
- Describe the pre-agent period using actual monthly data
- What was the rhythm? What repos were most active?
- Platform distribution at baseline
- Framing: "competent, sustainable, bounded by human throughput"

#### Chapter 2: First Experiments
- The earliest months with any agent activity
- Data will likely show modest changes — be honest about the learning curve
- What repos started appearing? Any new platforms?

#### Chapter 3: The Transition Period
- Use actual data from transition months (if defined) — do NOT skip these
- Growing proficiency shows in the data — look for the slope starting to change
- If no formal transition period was defined, look for the month the trend first breaks above baseline average

#### Chapter 4: The Inflection Point
- The INFLECTION_DATE month and surrounding context
- Contrast sharply with baseline
- What changed? Platform share, repo diversity, commit depth

#### Chapter 5: Sustained Excellence
- Walk through post-agent months with actual numbers
- Identify the peak month and explain its significance
- Note the scope expansion (new repos, new platforms)
- The "commits got more focused, not just more frequent" insight from commit depth

#### Conclusion
- What the multipliers actually mean (not just faster — different level of operation)
- Acknowledge the learning curve: it took X months to materialize
- The scope/domain expansion story (GitHub share trend, new repos)
- Key metrics summary table

### Tone Guidelines
- Data-driven but human
- Honest about the learning curve
- Specific with numbers — no vague claims
- Acknowledge confounders (job changes, extra time, etc.) if mentioned in interview

---

## Phase 6: Visual Charts

Create `generate-charts.py` producing the following PNGs in a `charts/` subdirectory.

Use consistent colors:
- Pre-agent: `#E57373` (salmon-red)
- Transition: `#FFB74D` (amber)
- Post-agent: `#4DB6AC` (teal)
- Neutral/cumulative: `#5C85D6` (blue)
- All charts: `dpi=150`, `tight_layout()`

### Required Charts

| # | Filename | Type | Description |
|---|----------|------|-------------|
| 1 | `commits-over-time.png` | Line + shaded regions | Monthly commits with period shading, pre-agent avg reference line, inflection point marker |
| 2 | `lines-over-time.png` | Bar chart | Net lines per month, colored by period |
| 3 | `platform-distribution.png` | Side-by-side pies | Commits by platform, pre vs post |
| 4 | `category-breakdown.png` | Grouped horizontal bars | Commits by repo category, pre vs post |
| 5 | `before-after-comparison.png` | Side-by-side bars | Total commits / files / lines with multiplier annotations |
| 6 | `repo-activity-matrix.png` | Heatmap | Top 20 repos × periods, log scale |
| 7 | `active-repos-over-time.png` | Area/line | Unique active repos per month |
| 8 | `cumulative-commits.png` | Line w/ inflection marker | Running total — the slope change is the key visual |
| 9 | `github-share-trend.png` | Line + area | Platform % of commits over time with period averages |
| 10 | `files-per-commit.png` | Bar | Commit depth per month — did commits get bigger or more frequent? |

---

## Output File Summary

| File | Description |
|------|-------------|
| `full-inventory.json` | Raw week×repo data for the full date range |
| `development-summary.json` | Monthly aggregated summary with period labels |
| `pattern-analysis.json` | Platform splits, categories, velocity, matrix, etc. |
| `productivity-narrative.md` | 1,500–2,500 word narrative story |
| `charts/*.png` | 10 publication-ready charts |
| `collect-data.ps1` | Data collection script (parameterized) |
| `summarize-inventory.js` | Aggregation script |
| `analyze-patterns.js` | Pattern analysis script |
| `generate-charts.py` | Chart generation script |

---

## Notes on Honesty & Limitations

Always document these in the output:

- **Line stat coverage**: GitHub stats API covers last 52 weeks only. Older periods may show 0 lines even if commits exist — note this clearly.
- **ADO line stats**: Not available without cloning. File operation counts (add/edit/delete/rename) are available.
- **Confounders**: If the person mentioned role changes, new clients, available time changes — acknowledge these in the narrative. The goal is insight, not marketing.
- **What commits don't capture**: Code review, planning, architecture thinking, documentation in non-tracked formats. Commits are a proxy, not the whole picture.

---

*This template was built from a real analysis of Jeremy Vyska's development history, Jan 2025–Mar 2026. The process is repeatable for any developer with commit history on GitHub and/or Azure DevOps.*
