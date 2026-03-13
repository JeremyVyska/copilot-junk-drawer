# Clockify Narrative Generator - Quick Start

## 1. Install dependencies
```powershell
npm install
```

## 2. Extract your data
```powershell
# Last 7 days
node extract-week.js

# Or use npm scripts
npm run extract
```

## 3. Generate narratives with AI

Open your AI agent (Claude Code, ChatGPT, etc.) and provide it with the `NARRATIVE_AGENT_INSTRUCTIONS.md` file, then ask:

> "Generate the weekly narrative for the latest export in weekly-exports/"

The agent will:
- Launch parallel day agents
- Write individual day narratives
- Combine them into a weekly summary

## 4. Review your narrative

Open `weekly-exports/YYYY-MM-DD_narrative.md` to see your week summarized!

---

## Automation Example (PowerShell)

Save this as `generate-narrative.ps1`:

```powershell
# Extract data
Write-Host "Extracting Clockify data..." -ForegroundColor Cyan
node extract-week.js

# Find latest week file
$latestWeek = Get-ChildItem weekly-exports/*_week.json | Sort-Object Name -Descending | Select-Object -First 1

if ($latestWeek) {
    Write-Host "Latest export: $($latestWeek.Name)" -ForegroundColor Green
    Write-Host "`nNow ask your AI agent to:" -ForegroundColor Yellow
    Write-Host "  'Generate the weekly narrative for $($latestWeek.BaseName).json'" -ForegroundColor White
} else {
    Write-Host "No exports found. Run 'node extract-week.js' first." -ForegroundColor Red
}
```

Run with:
```powershell
.\generate-narrative.ps1
```
