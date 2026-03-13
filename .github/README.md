# 📚 README Auto-Generation System

Your Junk Drawer repo now has **automatic README generation** that updates whenever you add new tools!

## 🎯 How It Works

### GitHub Actions Workflow

When you push new folders to the repo, GitHub Actions automatically:

1. **Detects** folders with README.md files
2. **Generates** updated main README with all tools listed
3. **Commits** and pushes the changes back

**Workflow file:** [`.github/workflows/update-readme.yml`](.github/workflows/update-readme.yml)

### The Generator Script

**Location:** `.github/scripts/generate-readme.js`

**Two modes:**

1. **Curated Mode** (recommended for polished tools)
   - Hand-crafted descriptions in `manualMappings` object
   - Full control over subtitle, description, features, stack, emoji

2. **Auto-Parse Mode** (fallback for new tools)
   - Automatically extracts title and basic info from README
   - Works immediately without manual configuration

## ✨ Adding a New Tool

### Option A: Quick & Automatic

1. Create folder: `awesome-tool/`
2. Add `awesome-tool/README.md`
3. Push to GitHub
4. Done! GitHub Actions auto-updates main README

The tool will be listed with:
- Folder name
- Extracted title
- Auto-picked emoji
- Link to full docs

### Option B: Polished & Curated (Recommended)

1. Create your tool folder and README
2. Test locally: `node .github/scripts/generate-readme.js`
3. If output isn't perfect, add curated entry to `generate-readme.js`:

```javascript
const manualMappings = {
  'your-tool-name': {
    name: 'your-tool-name',
    title: 'Tool Title',
    subtitle: 'One-line hook that sells the tool',
    description: 'Paragraph explaining what it does and why it matters.',
    features: [
      'Key feature 1',
      'Key feature 2',
      'Key feature 3',
      'Impressive stat or finding'
    ],
    stack: 'Node.js, Python, etc.',
    emoji: '🚀'
  }
};
```

4. Test again locally
5. Commit and push

## 🧪 Local Testing

**Always test before pushing:**

```powershell
# From repo root
node .github/scripts/generate-readme.js

# Check the output
git diff README.md

# If it looks good, commit
git add README.md .github/
git commit -m "Add new tool"
git push
```

## 🔧 Customization Options

### Emoji Selection

Auto-picked based on folder name keywords, or specify in `manualMappings`:

| Keywords | Emoji |
|----------|-------|
| agentic, assessment, analyzer | 🤖📊🔬 |
| time, log, monitor | ⏱️📝📡 |
| api, webhook, scraper | 🔌🪝🕷️ |
| deploy, pipeline, migration | 🚀🔁🔄 |

### Ignored Folders

Edit `IGNORE_FOLDERS` in `generate-readme.js`:

```javascript
const IGNORE_FOLDERS = ['.github', '.git', 'node_modules', '.vscode'];
```

### Template Sections

The Philosophy, Quick Start, Contributing, License sections are static.
Edit them in the `generateReadme()` function.

## 🎬 Workflow Triggers

The GitHub Action runs when:
- ✅ Pushing to `main` or `master`
- ✅ Manual trigger via Actions tab
- ❌ Changes to README.md only (prevents loops)
- ❌ Changes to `.github/**` only

## 🛑 Troubleshooting

**Q: Action isn't running?**
- Check Actions tab for errors
- Verify workflow file is in `.github/workflows/`
- Ensure repo has Actions enabled (Settings → Actions)

**Q: README not updating?**
- Check if new folder has a `README.md`
- Look for errors in Actions logs
- Test locally to see if script works

**Q: Permissions error when pushing?**
- Workflow needs `contents: write` permission (already configured)
- Check repo Settings → Actions → Workflow permissions

**Q: Don't want auto-updates?**
- Delete `.github/workflows/update-readme.yml`
- Or disable workflow in Actions tab

## 🎨 Philosophy

**Curated > Automated**

While the script can auto-parse READMEs, hand-crafted descriptions in `manualMappings` ensure:
- Professional, consistent tone
- Highlight the most impressive features
- Tell a compelling story

For your two amazing tools, I've already added polished curated entries. Follow the same pattern for future additions!

---

**Made with ❤️ and a touch of automation**
