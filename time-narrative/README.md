# Clockify AutoTrack Narrative Generator

**Transform raw Clockify AutoTrack data into human-readable weekly narratives using AI agents.**

## Purpose

This package extracts time-tracking data from Clockify's AutoTracker SQLite database and uses AI agents to generate narrative summaries of your work weeks. Instead of raw application logs, you get context-rich stories about what you worked on, when, and how.

### What it does

1. **Extracts** activity data from Clockify's local database
2. **Buckets** entries into 30-minute time slots
3. **Launches** parallel AI agents (one per day) to interpret the data
4. **Generates** markdown narratives with semantic activity labels
5. **Produces** a weekly summary combining all days

### Example output

```markdown
## Thursday, 2026-02-20

### Morning

**09:00 – 09:30** | *BC AL Development* | 24m 16s active
> Deep focus session on Business Central AL extensions. Primary work in
> BRCCore workspace implementing inventory module features. Terminal shows
> Claude Code task 'Fix Compile Errors' running alongside VS Code.

**09:30 – 10:00** | *Azure DevOps + BC AL Dev* | 28m 3s active
> Split time between reviewing work items in Azure DevOps (Feature 23707)
> and continuing AL development. Quick context switches to Teams for
> stand-up meeting coordination.
```

## Prerequisites

### Required

- **Node.js** (v18 or later)
- **Clockify Desktop App** with AutoTracker enabled
  - Download: https://clockify.me/downloads
  - AutoTracker must be running and collecting data
- **Claude Code** or another AI agent system that supports subagent invocation
  - The narrative generation requires AI agents with file read/write capabilities

### Optional

- Git (for version control of your narratives)
- PowerShell or Bash (for automation scripts)

## Installation

1. **Clone or download** this package to your preferred location

2. **Install dependencies**:
   ```powershell
   cd package
   npm install
   ```

3. **Verify Clockify database location**:
   - Windows: `%LOCALAPPDATA%\Clockify\ClockifyDB_v2.db`
   - macOS: `~/Library/Application Support/Clockify/ClockifyDB_v2.db`
   - Linux: `~/.config/Clockify/ClockifyDB_v2.db`

   If your database is in a different location, edit `extract-week.js` line 15:
   ```javascript
   const DB_SRC = path.join(process.env.LOCALAPPDATA, 'Clockify', 'ClockifyDB_v2.db');
   ```

## Usage

### Step 1: Extract the data

Run the extraction script to pull data from Clockify:

```powershell
# Extract last 7 days (default)
node extract-week.js

# Extract custom date range
node extract-week.js --from 2026-02-10 --to 2026-02-16

# Extract last 14 days
node extract-week.js --days 14
```

This creates:
- `weekly-exports/YYYY-MM-DD_week.json` (full week data)
- `weekly-exports/YYYY-MM-DD_daydata.json` (per-day data for parallel processing)

### Step 2: Generate narratives

Using Claude Code or your AI agent system:

1. Open the `NARRATIVE_AGENT_INSTRUCTIONS.md` file
2. Provide it to your AI agent (Claude Code, GPT with function calling, etc.)
3. Ask the agent to "generate the weekly narrative for the latest export"

The agent will:
- Launch parallel day agents (one per day)
- Each writes a `YYYY-MM-DD_day.md` file
- Combine them into `YYYY-MM-DD_narrative.md`

## Customization

### Semantic interpretation rules

Edit the semantic rules table in `NARRATIVE_AGENT_INSTRUCTIONS.md` to match your workflow:

```markdown
| `app = "Visual Studio Code"`, title contains `.al` or `BusinessCentral` | BC AL Development |
| `app = "Microsoft Edge"`, `url` contains `dev.azure.com` | Azure DevOps work |
```

**Common customizations:**

- Add your IDE/editor patterns (JetBrains, Sublime, Vim)
- Add your project workspace names
- Add your web tools (Jira, Linear, Notion, Figma)
- Add your communication tools (Slack, Discord, Teams)
- Adjust idle thresholds (default: < 2 minutes active = idle)

### Privacy filters

The instructions include privacy-aware rules:

- Personal browsing is labeled generically ("personal browsing")
- You can add custom filters for sensitive projects or sites

### Time slot size

Default is 30-minute buckets. To change, edit `extract-week.js` function `slotKey()`:

```javascript
function slotKey(isoStr) {
  const d = new Date(isoStr.replace(' ', 'T'));
  const mm = d.getMinutes() < 30 ? '00' : '30';  // Change this logic
  // ...
}
```

## File Structure

```
package/
├── README.md                           # This file
├── package.json                        # Node dependencies
├── extract-week.js                     # Data extraction script
├── NARRATIVE_AGENT_INSTRUCTIONS.md     # AI agent instructions
└── weekly-exports/                     # Generated files (created on first run)
    ├── YYYY-MM-DD_week.json           # Full week data
    ├── YYYY-MM-DD_daydata.json        # Per-day data
    ├── YYYY-MM-DD_day.md              # AI-generated day narratives
    └── YYYY-MM-DD_narrative.md        # Final weekly narrative
```

## Troubleshooting

### "Database file not found"

- Verify Clockify Desktop is installed
- Check the database path in `extract-week.js`
- Ensure AutoTracker has collected some data

### "No entries found"

- Check that AutoTracker is enabled in Clockify settings
- Verify the date range includes days when you worked
- Look at `ClockifyDB_copy.db` with a SQLite viewer to inspect raw data

### AI agent doesn't generate narratives

- Ensure your AI agent supports file read/write operations
- Verify the agent can launch subagents/tasks
- Check that `weekly-exports/` contains the JSON data files
- Try running a day agent manually first to test

### Narratives are too generic

- Customize the semantic rules to match your specific apps and workflows
- Add project-specific patterns (workspace names, URL patterns)
- Increase context in rules (e.g., capture work item IDs from URLs)

## Tips

- **Run weekly**: Extract and narrate on Fridays for weekly review
- **Version control**: Commit narratives to git for long-term tracking
- **Automate**: Create a PowerShell/bash script to extract + trigger AI generation
- **Review patterns**: Over time, identify peak productivity hours and context-switching costs
- **Privacy**: Narratives stay local unless you explicitly share them

## Architecture

```
┌─────────────────────┐
│  Clockify Desktop   │
│   (AutoTracker)     │
└──────────┬──────────┘
           │ SQLite DB
           ▼
┌─────────────────────┐
│  extract-week.js    │ ← You run this
│   (Node script)     │
└──────────┬──────────┘
           │ JSON exports
           ▼
┌─────────────────────┐
│  Overseer Agent     │
│  (reads weekly.json)│
└──────────┬──────────┘
           │ Launches parallel
           ▼
   ┌───────┴───────┐
   │ Day Agents    │ (one per day, concurrent)
   │ (read daydata)│
   └───────┬───────┘
           │ Write _day.md files
           ▼
┌─────────────────────┐
│  Overseer Agent     │
│  (stitches days)    │
└──────────┬──────────┘
           │
           ▼
    narrative.md (final output)
```

## License

Unlicensed - use freely for personal or commercial purposes.

## Contributing

This is a personal workflow tool. Fork and adapt to your needs!

Suggested improvements:
- Support for other time-tracking tools (RescueTime, ActivityWatch)
- Web UI for browsing narratives
- Integration with journaling tools (Obsidian, Notion)
- Automatic weekly email summaries
- Time allocation charts and visualizations
