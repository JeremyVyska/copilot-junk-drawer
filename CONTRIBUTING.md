# Contributing to Copilot Junk Drawer

Thanks for considering adding your tool to the Junk Drawer! This repo is for powerful, focused utilities that don't warrant their own repository.

## ✅ Is Your Tool a Good Fit?

Your tool belongs here if it:
- ✅ Solves a real problem elegantly
- ✅ Is self-contained (minimal cross-dependencies)
- ✅ Is production-ready (not experimental)
- ✅ Has clear documentation
- ❌ Doesn't need semantic versioning
- ❌ Doesn't need independent CI/CD pipeline

## 📝 How to Contribute

### 1. Create Your Tool Folder

```powershell
# Create folder with descriptive lowercase-with-hyphens name
mkdir your-tool-name
cd your-tool-name
```

### 2. Structure Your Tool

Required files:
- `README.md` - Comprehensive documentation (see structure below)
- Tool code/scripts
- `package.json` / `requirements.txt` / equivalent (if applicable)

Optional:
- Examples folder
- Test folder
- License file (if different from repo)

### 3. Write Your README

Use this structure:

```markdown
# Tool Name

**One-line hook that sells the tool**

## Purpose / What This Is

2-3 paragraphs explaining:
- What problem it solves
- How it works (high-level)
- Who it's for

## Prerequisites

### Required
- Tool/language version
- Third-party services (APIs, databases)

### Optional
- Nice-to-have tools

## Installation

Step-by-step setup instructions.

## Usage

### Step 1: ...
Clear examples with code blocks.

### Step 2: ...

## What You'll Get

Describe outputs, files generated, etc.

## Stack

**Stack:** List languages, tools, frameworks

## License / Credits

If applicable.
```

### 4. Test Locally

```powershell
# From repo root
node .github/scripts/generate-readme.js

# Review the generated README
git diff README.md
```

### 5. Add Curated Content (Optional, Recommended)

For a polished presentation, add your tool to `.github/scripts/generate-readme.js`:

```javascript
const manualMappings = {
  'your-tool-name': {
    name: 'your-tool-name',
    title: 'Your Tool Name',
    subtitle: 'Compelling one-liner',
    description: '2-3 sentences explaining value and approach.',
    features: [
      'Key feature or capability',
      'Another impressive aspect',
      'Quantifiable result or stat',
      'Integration or compatibility'
    ],
    stack: 'Languages, frameworks, services',
    emoji: '🚀' // Pick a relevant emoji
  }
};
```

### 6. Submit Pull Request

1. Fork the repository
2. Create a feature branch: `git checkout -b add-my-tool`
3. Commit your changes: `git commit -am "Add [tool-name]"`
4. Push to the branch: `git push origin add-my-tool`
5. Submit a pull request

## 📋 PR Checklist

- [ ] Tool folder has descriptive lowercase-with-hyphens name
- [ ] Comprehensive README.md included
- [ ] All prerequisites clearly documented
- [ ] Usage examples provided
- [ ] Dependencies declared (package.json, requirements.txt, etc.)
- [ ] Tool is self-contained
- [ ] Tested locally with `node .github/scripts/generate-readme.js`
- [ ] (Optional) Curated entry added to generate-readme.js

## 🎨 Style Guidelines

- **Emojis**: Use sparingly, only in headings or curated mappings
- **Tone**: Professional but approachable
- **Code blocks**: Always specify language for syntax highlighting
- **Examples**: Show realistic, practical use cases
- **Prerequisites**: Be specific about versions when it matters

## 🔒 Security

- **Never** commit API keys, tokens, or credentials
- Use environment variables for secrets
- Document authentication requirements clearly
- If tool handles sensitive data, document security practices

## 📜 Licensing

- Repo is MIT licensed
- Your tool can have additional/different license (document in your README)  
- Clearly credit any third-party code or libraries

## ❓ Questions?

Open an issue with the `question` label and we'll help you out!

---

**Remember**: The best additions to the Junk Drawer are tools that are too useful to scatter across gists, but don't need the overhead of a full repository. Make them discoverable, documented, and delightful! ✨
