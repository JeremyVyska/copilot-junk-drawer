# Developer AI-Quality Analysis — Reusable Template

## What This Is

A static code analysis process for any developer to quantify the impact of AI-assisted development on **code quality** — not just volume. The output is a side-by-side comparison across testing, documentation, design patterns, and security, backed by real measurements from real codebases.

This process was originally built for Jeremy Vyska (Microsoft MVP, Business Central developer) and produced findings like **252 test procedures vs. 1**, a **57x increase in structured documentation**, and a **0 → 48 improvement in secure credential handling** — all in a post-agent codebase built *faster* than the pre-agent one.

This analysis is the rebuttal to "sure, you wrote more — but is it any good?"

---

## Phase 0: Interview (START HERE)

The agent must work through these questions before touching any code. The answers determine whether a comparison is even possible, which repo strategy to use, and how to frame the output honestly.

Ask these questions one at a time and wait for answers.

---

### Part A: Do You Have a Valid Comparison Pair?

This analysis requires two codebases that meet three criteria:
1. **Same language** — quality metrics are language-specific (test decorators, doc comment syntax, etc.)
2. **Same type of work** — comparing a CLI tool to an enterprise app will produce noise, not signal
3. **Meaningfully different eras** — one must be predominantly pre-agent, one predominantly post-agent

**Question A1:** Do you have two separate products/repos where one was built *before* you used AI agents and one was built *after* (or substantially reworked after)?

- If **yes** → go to Part B (Two Separate Repos)
- If **no** → go to Part C (Single Repo / Git History Strategy)

---

### Part B: Two Separate Repos

**B1.** What are the names/locations of the two repos?
*(Include clone URL or local path for each)*

**B2.** Which one is the pre-agent product? Briefly describe it:
- What does it do?
- Approximate age / when it was mostly built
- Is it in production / actively maintained?

**B3.** Which one is the post-agent product? Briefly describe it:
- What does it do?
- When did development start relative to your AI adoption?
- Is it in production / actively maintained?

**B4.** Are they the *same kind* of thing? (Same language, same domain, same type of project — e.g., both web APIs, both desktop apps, both library packages)
*(If they are very different in purpose, the comparison will require careful framing — note the differences and address them in the narrative)*

**B5.** Is one significantly larger or older than the other?
*(Size difference is fine — we normalize metrics per 1,000 lines and by percentage. Age difference may mean the older one had more time to accumulate debt. Note it.)*

**Proceed to Part D.**

---

### Part C: Single Repo / Git History Strategy

If you don't have two separate products, you can compare two checkpoints in the same repo's history. This is a valid but more complex approach.

**C1.** What repo will be analyzed?
*(URL or local path)*

**C2.** Can you identify a commit or tag that represents the "pre-agent state" of the codebase?
- An ideal checkpoint is **before** you started using AI tools, or at minimum a point where the codebase was built entirely manually
- Examples: a release tag, a date-based commit like `git log --before="2024-09-01" -1 --format="%H"`, a specific version tag

**C3.** Is the codebase's *purpose or scope* roughly the same at both checkpoints, or did the AI period add entirely new subsystems?
*(If major new features were added post-agent, the comparison will show both quality improvement AND scope expansion — both are valid findings, just label them clearly)*

**C4.** Do you have local access to the repo, or do you need to clone it?

> **Git History Approach — What the Agent Will Do:**
> 1. Clone the repo (if not local)
> 2. Check out the pre-agent commit → run static inventory → save results
> 3. Check out the current HEAD (or post-agent tag) → run static inventory → save results
> 4. Restore HEAD to current state
> 5. Produce the comparison

**Proceed to Part D.**

---

### Part D: Language and Platform

**D1.** What primary language is the codebase written in?
*(The inventory script will use language-specific patterns — see the Language Pattern Reference at the end of this template)*

Common options: `al` | `csharp` | `typescript` | `javascript` | `python` | `java` | `go` | `ruby` | `rust` | `other`

**D2.** Are there multiple languages in the same repo? (e.g., TypeScript frontend + Python backend)
*(If yes, specify which language is the primary focus of the comparison)*

**D3.** What test framework(s) are used, if any?
*(e.g., Jest, pytest, xUnit, JUnit, Go test — used to identify test files and test function patterns)*

**D4.** Does the project use any of the following documentation patterns?**
- [ ] XMLDoc / JSDoc / TSDoc (inline `///` or `/** */` style comments)
- [ ] Docstrings (`"""` in Python, `//!` in Rust)
- [ ] Markdown docs in the repo (`*.md` files, `/docs` folder)
- [ ] Auto-generated API docs (OpenAPI, Typedoc, etc. — check for config files)
- [ ] CHANGELOG or ARCHITECTURE files

---

### Part E: Framing and Audience

**E1.** What is the most important thing you want to demonstrate with this analysis?
*(e.g., "I want to show my team that AI doesn't mean cutting corners", "I want evidence for a conference talk", "I'm just curious for myself")*

**E2.** Who is the audience?
- [ ] Personal reflection
- [ ] Engineering team / peers (technical)
- [ ] Management / business stakeholders (non-technical)
- [ ] Blog post or conference talk
- [ ] Social media highlight

**E3.** Are there any honest caveats to acknowledge?
*(e.g., "The post-agent product is newer so had less tech debt to start with", "I had more time during the post-agent period", "The requirements were simpler for the post-agent project")*
*(Document these — honest caveats strengthen the analysis rather than weaken it)*

---

## Phase 1: Repository Setup

Based on the interview answers, set up the local comparison pair.

### Two Separate Repos:
```powershell
# Clone both if not already local
git clone <pre-agent-repo-url> ./pre-agent-repo
git clone <post-agent-repo-url> ./post-agent-repo
```

### Single Repo / Git History:
```powershell
git clone <repo-url> ./repo-to-analyze
cd ./repo-to-analyze

# Find the pre-agent checkpoint commit
# Option A: by date
$preCommit = git log --before="<pre-agent-cutoff-date>" -1 --format="%H"
# Option B: by tag
$preCommit = git rev-list -1 <pre-agent-tag>

# Save current HEAD
$currentHead = git rev-parse HEAD
Write-Output "Current HEAD: $currentHead"
Write-Output "Pre-agent checkpoint: $preCommit"
```

---

## Phase 2: Static Inventory

Create `measure-quality.ps1` (or adapt from the reference script below). This script:
1. Scans each codebase for the quality indicators matching the interview's language/framework
2. Outputs a `quality-metrics.json` file

### Reference Script Structure

```powershell
# measure-quality.ps1
param(
    [string]$PrePath,
    [string]$PostPath,
    [string]$Language = "auto",   # auto-detect or specify
    [string]$OutputFile = "quality-metrics.json"
)

function Get-Metric($root, $lang) {
    # File discovery (see Language Pattern Reference for $testPattern, $srcPattern)
    $srcFiles  = Get-ChildItem $root -Recurse -Filter $srcPattern  | Where-Object { not in .git }
    $testFiles = Get-ChildItem $root -Recurse -Filter $testPattern | Where-Object { not in .git }
    $docFiles  = Get-ChildItem $root -Recurse -Include "*.md","CHANGELOG","ARCHITECTURE*","README*" | ...
    $mockFiles = Get-ChildItem $root -Recurse | Where-Object { $_.Name -match 'mock|Mock|stub|Stub|fake|Fake' }

    $srcLines  = $srcFiles  | Get-Content -ErrorAction SilentlyContinue
    $testLines = $testFiles | Get-Content -ErrorAction SilentlyContinue
    $allLines  = $srcLines + $testLines

    return [PSCustomObject]@{
        src_files      = $srcFiles.Count
        test_files     = $testFiles.Count
        doc_files      = $docFiles.Count
        mock_files     = $mockFiles.Count
        src_lines      = $srcLines.Count
        test_lines     = $testLines.Count
        # Comment lines: language-specific pattern (see reference)
        comment_lines  = @($allLines | Where-Object { $_ -match $commentPattern }).Count
        # XMLDoc/docstring lines: language-specific
        xmldoc_lines   = @($allLines | Where-Object { $_ -match $docstringPattern }).Count
        # Test procedures: language-specific decorator/naming pattern
        test_procs     = @($testLines | Where-Object { $_ -match $testProcPattern }).Count
        # Interface/abstract objects: language-specific
        interfaces     = @($srcLines | Where-Object { $_ -match $interfacePattern }).Count
        # Error handling: language-specific
        error_calls    = @($srcLines | Where-Object { $_ -match $errorPattern }).Count
        # Secure credential patterns: language-specific
        secure_cred    = @($srcLines | Where-Object { $_ -match $credPattern }).Count
    }
}
```

### Core Metrics to Collect

Regardless of language, collect these eight dimensions:

| Dimension | What It Measures | Why It Matters |
|-----------|-----------------|----------------|
| Test files | Files dedicated to testing | Level of test investment |
| Test lines % | Test lines / total AL lines | Depth of test coverage relative to product size |
| Test procedures | Individual `[Test]` / `def test_` / `it()` blocks | Number of discrete behavioral assertions |
| Mock files | Files implementing test doubles | Testability of design — mocks require dependency injection |
| Comment density | Comment lines / total lines % | Code self-documentation habit |
| XMLDoc/docstring lines | Structured doc comments (`///`, `"""`, `/** */`) | IDE-navigable, maintainable documentation |
| Doc file ratio | .md files / source files | External documentation culture |
| Secure credential patterns | IsolatedStorage, SecretText, vault, os.environ, etc. | Security design built-in vs. retrofitted |

---

## Phase 3: Analysis and Normalization

Raw counts are not enough — the two codebases may differ in size. Normalize everything.

### Normalized Metrics to Compute

```javascript
// For each metric that is a raw count, compute:
const testRatio = testLines / (testLines + srcLines) * 100      // %
const commentPct = commentLines / allLines * 100                 // %
const xmldocPer1k = xmldocLines / srcLines * 1000               // per 1,000 src lines
const testProcPer1k = testProcs / srcLines * 1000               // per 1,000 src lines
const errorPer1k = errorCalls / srcLines * 1000                 // per 1,000 src lines
const docFileRatio = docFiles / srcFiles * 100                  // %
const mockPerTestFile = mockFiles / Math.max(testFiles, 1)      // ratio
```

### Multiplier Table

Build a multiplier table comparing post to pre for each normalized metric:

```
testRatioMultiplier    = post.testRatio / pre.testRatio
commentPctMultiplier   = post.commentPct / pre.commentPct
testProcPer1kMultiplier = post.testProcPer1k / pre.testProcPer1k
...
```

Where pre = 0, use "∞" or "N/A (none before)".

---

## Phase 4: Narrative — `quality-compare.md`

Write the narrative following this structure. All placeholders in `[brackets]` are filled from interview answers and analysis data.

### Opening

The most natural objection to [X]x productivity increase is: *"Sure, you wrote more — but is it any good?"*

It's a fair question. Frame the comparison pair. Acknowledge size/age differences honestly. State what will be measured.

### Section 1: The Two Codebases

Brief description of each (anonymized or named, per audience preference):
- **[Pre-Agent Label]** — [what it does, when built, production status, size in files/lines]
- **[Post-Agent Label]** — [what it does, when built, production status, size in files/lines]

State clearly: *"This comparison is about quality density, not raw size."*

If using git history strategy: explain that both snapshots are from the same codebase, taken [X months] apart.

### Section 2: Raw Inventory Table

Insert the raw metrics table. Both columns side by side. Bold the post-agent values where they are substantially better.

### Section 3: Dimension by Dimension

One subsection per quality dimension. For each:
1. Show the numbers
2. Explain what the gap means in practice
3. Connect it to *why* AI assistance changes this — lower marginal cost, not better judgment

Structure each as:
```
### [Dimension Name]
[Normalized metric table for this dimension, pre vs post]
[2-3 sentences of interpretation]
> Pull-quote callout of the key finding
```

### Section 4: The Mechanism

This is the argument, not just the data. Explain:
- Manual dev: quality work (tests, docs, error handling) competes with feature work for finite hours
- Agent dev: agent performs quality work alongside feature work — the marginal cost collapsed
- Result: decisions that used to be "deferred until later" now happen as a matter of course

### Section 5: Honest Caveats

Address the confounders identified in the interview. Keep it short — one paragraph. Honest acknowledgment of limitations strengthens credibility.

### Conclusion

Restate the headline numbers. End with the mechanism insight.

---

## Phase 5: Charts — `generate-quality-charts.py`

Produce two charts saved to `charts/`.

### Chart 1: Code Composition Pies — `quality-composition.png`

A 2×2 grid of pie charts:
- Top row: Test lines as % of all code — pre vs post
- Bottom row: Comment density (XMLDoc vs plain comment vs uncommented) — pre vs post

Use consistent colors matching the main productivity chart set:
- Pre-agent: `#EF5350` (red)
- Post-agent: `#26A69A` (teal)
- Remainder/neutral: `#ECEFF1` (light grey)

### Chart 2: Quality Attributes Bar — `quality-attributes.png`

Horizontal grouped bar chart with one row per quality dimension. Normalize each row to max=100. Annotate with actual values to the right of bars. This makes all dimensions visually comparable even when they have different units.

Dimensions to include (any with a zero pre-agent value will visually emphasize the "didn't exist before" story):
- Doc files per 100 source files
- Comment density (% of all code lines)
- XMLDoc/docstring density (% of source lines)
- Test lines (% of total code)
- Test procedures per 1,000 source lines
- Error handling per 1,000 source lines
- Mock files (count)
- Interface/abstract objects (count)
- Secure credential patterns (count)

---

## Language Pattern Reference

Use these patterns in the `measure-quality.ps1` script. Replace the generic placeholders with the values for the interview's language.

| Language | Source filter | Test file pattern | Test proc pattern | Comment pattern | XMLDoc/docstring pattern | Interface pattern | Error pattern | Secure cred pattern |
|----------|--------------|-------------------|-------------------|-----------------|--------------------------|-------------------|---------------|---------------------|
| **AL (Business Central)** | `*.al` | `-Test\` directory or `Test` in filename | `\[Test\]` | `^\s*//` | `^\s*///` | `^interface\s` | `\bError\s*\(` | `IsolatedStorage\.\|SecretText\b` |
| **C#** | `*.cs` | `*Test*.cs`, `*Tests*.cs`, or `Tests/` directory | `\[Test\]\|\[Fact\]\|\[Theory\]` | `^\s*//` | `^\s*///` | `^\s*(public\|internal)\s+interface\s` | `\bthrow\b\|\bcatch\b` | `SecretClient\|KeyVaultSecret\|Environment\.GetEnvironmentVariable\|IConfiguration` |
| **TypeScript/JavaScript** | `*.ts`, `*.js` | `*.test.ts`, `*.spec.ts`, `__tests__/` | `\bit\s*(\|\bdescribe\s*(\|\btest\s*(` | `^\s*//` | `^\s*\*\|^\s*/\*\*` | `^\s*(export\s+)?interface\s` | `\bthrow\b\|\bcatch\b` | `process\.env\|dotenv\|secretsmanager\|KeyVaultSecret` |
| **Python** | `*.py` | `test_*.py`, `*_test.py`, `tests/` directory | `^\s*def test_` | `^\s*#` | `^\s*"""` | `^\s*class.*Protocol\|ABC\|abstractmethod` | `\braise\b\|\bexcept\b` | `os\.environ\|getenv\|boto3.*secrets\|SecretManagerServiceClient` |
| **Java** | `*.java` | `*Test.java`, `src/test/` directory | `@Test` | `^\s*//` | `^\s*\*\|^\s*/\*\*` | `^\s*(public\|private)?\s*interface\s` | `\bthrow\b\|\bcatch\b` | `SecretManagerServiceClient\|Vault\|@Value.*secret` |
| **Go** | `*.go` | `*_test.go` | `^\s*func Test` | `^\s*//` | `^\s*//` (Go uses plain `//` for all docs) | `^\s*type.*interface\s*{` | `\berr\b.*!=.*nil\|if err` | `os\.Getenv\|viper\|secretmanager` |
| **Ruby** | `*.rb` | `*_spec.rb`, `*_test.rb`, `spec/`, `test/` | `^\s*it\s\|^\s*def test_` | `^\s*#` | `^\s*#` | `^\s*module\|^\s*include` | `\braise\b\|\brescue\b` | `ENV\[\|Vault\|Rails\.application\.credentials` |
| **Rust** | `*.rs` | `#[cfg(test)]` block or `tests/` | `#\[test\]` | `^\s*//[^/!]` | `^\s*///\|^\s*//!` | `^\s*(pub\s+)?trait\s` | `\bunwrap\|\bexpect\|\bResult\b` | `std::env::var\|dotenvy\|SecretManager` |

### Auto-Detection Logic

If the interview didn't specify a language, detect it:

```powershell
function Detect-Language($root) {
    $counts = @{
        al         = (Get-ChildItem $root -Recurse -Filter "*.al"   | Measure-Object).Count
        csharp     = (Get-ChildItem $root -Recurse -Filter "*.cs"   | Measure-Object).Count
        typescript = (Get-ChildItem $root -Recurse -Filter "*.ts"   | Measure-Object).Count
        javascript = (Get-ChildItem $root -Recurse -Filter "*.js"   | Measure-Object).Count
        python     = (Get-ChildItem $root -Recurse -Filter "*.py"   | Measure-Object).Count
        java       = (Get-ChildItem $root -Recurse -Filter "*.java" | Measure-Object).Count
        go         = (Get-ChildItem $root -Recurse -Filter "*.go"   | Measure-Object).Count
        ruby       = (Get-ChildItem $root -Recurse -Filter "*.rb"   | Measure-Object).Count
        rust       = (Get-ChildItem $root -Recurse -Filter "*.rs"   | Measure-Object).Count
    }
    return ($counts.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 1).Key
}
```

---

## Output File Summary

| File | Description |
|------|-------------|
| `quality-metrics.json` | Raw metric counts for both codebases |
| `quality-compare.md` | Narrative quality analysis document |
| `charts/quality-composition.png` | Pie charts — test % and comment % before/after |
| `charts/quality-attributes.png` | Horizontal bar comparison across 9 quality dimensions |
| `measure-quality.ps1` | Static inventory script |
| `generate-quality-charts.py` | Chart generation script |

---

## Important Limitations to Acknowledge

Always document these in the `quality-compare.md` output:

- **Static analysis only** — measures the presence of tests, comments, and patterns, not their correctness or completeness. A test file with 252 procedures could still have gaps. A comment could be wrong.
- **Size matters for some metrics** — a larger codebase has more surface area requiring documentation. Per-unit normalization corrects for raw size, but a newer/smaller product may have proportionally more documentation simply because it had less legacy to carry.
- **What code doesn't capture** — code reviews, design discussions, pull request quality, deployment reliability. These matter enormously and are not measured here.
- **Confounders** — address anything from interview Part E3. State them plainly; don't hide them.
- **Language limitations** — some languages have richer doc-comment tooling than others. A Go codebase using `//` for all docs looks the same as uncommented code to a naive `///` detector — adjust patterns accordingly.

---

## Notes on the Git History Strategy

When using a single repo compared across a git checkpoint:

1. **Always restore HEAD** after taking the pre-agent snapshot inventory. Never leave the repo checked out to the old commit for the user.
2. **Note any files that exist in post but not pre** — this is scope expansion, which is also part of the quality story (new subsystems don't exist until the AI era made them feasible to build).
3. **Be careful with renamed files** — a file that was `UserService.cs` pre-agent and `IUserService.cs` + `UserServiceImpl.cs` post-agent represents a genuine quality improvement (extraction of an interface) that static file counts alone will partially miss. Look for these in the diff narrative.
4. **Git stash** any uncommitted changes before checking out the old commit:
   ```powershell
   git stash
   git checkout $preCommit
   # ... run inventory ...
   git checkout $currentHead
   git stash pop
   ```

---

*This template was built from the quality analysis of Jeremy Vyska's BRCConnect (pre-agent) and AppSource-BRCRisk (post-agent) Business Central AL products, March 2026. BRCRisk was built faster than BRCConnect and has 252× more test procedures, 57× more structured documentation, and complete secure credential handling where BRCConnect has none.*
