# Test README Generation Locally

Before pushing changes, you can test the README generation locally:

## Quick Test

```powershell
# From repo root
node .github/scripts/generate-readme.js
```

This will regenerate `README.md` based on current tools.

## What It Does

1. **Scans** top-level folders for `README.md` files
2. **Extracts** key info: title, description, features, tech stack
3. **Picks** relevant emoji based on folder name
4. **Generates** complete README with:
   - All tools auto-listed
   - Consistent formatting
   - Automatic emoji selection
   - Direct links to each tool's docs

## Adding a New Tool

1. Create new folder: `my-awesome-tool/`
2. Add `my-awesome-tool/README.md` with:
   - Clear title (`# My Awesome Tool`)
   - Short description paragraph
   - Key features list (bullets)
   - Optional: `**Stack:** Node.js, Python` line
3. Run local test: `node .github/scripts/generate-readme.js`
4. Review updated `README.md`
5. Commit and push — GitHub Actions will auto-update on future changes

## Emoji Selection

The script picks emojis based on folder name keywords:
- `agentic/assessment/analyzer` → 🤖📊🔬
- `time/log/monitor` → ⏱️📝📡
- `api/webhook/scraper` → 🔌🪝🕷️
- `deploy/pipeline/migration` → 🚀🔁🔄
- Default → 🔧

Override by adding emoji to your tool's README title.
