#!/usr/bin/env node

/**
 * Auto-generate README.md based on discovered tools
 * Scans for top-level directories with README.md files and extracts key info
 */

const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.join(__dirname, '../../');
const README_PATH = path.join(REPO_ROOT, 'README.md');

// Folders to ignore
const IGNORE_FOLDERS = ['.github', '.git', 'node_modules', '.vscode'];

/**
 * Scan repository for tool folders (must contain README.md)
 */
function discoverTools() {
  const entries = fs.readdirSync(REPO_ROOT, { withFileTypes: true });
  const tools = [];

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    if (IGNORE_FOLDERS.includes(entry.name)) continue;

    const readmePath = path.join(REPO_ROOT, entry.name, 'README.md');
    if (!fs.existsSync(readmePath)) continue;

    const readmeContent = fs.readFileSync(readmePath, 'utf-8');
    const toolInfo = parseToolReadme(entry.name, readmeContent);
    tools.push(toolInfo);
  }

  return tools.sort((a, b) => a.name.localeCompare(b.name));
}

/**
 * Extract key information from a tool's README
 * Uses manual mappings for known tools, falls back to parsing for new ones
 * 
 * To add curated content for a new tool, add an entry to manualMappings below.
 * This gives you full control over how the tool is presented in the main README.
 */
function parseToolReadme(folderName, content) {
  // Manual mappings for existing tools (curated content)
  // ADD NEW TOOLS HERE for polished, hand-crafted descriptions
  const manualMappings = {
    'agentic-assessment': {
      name: 'agentic-assessment',
      title: 'AI-Assisted Development Impact Analysis',
      subtitle: 'Data-driven framework for quantifying AI coding assistant impact on productivity and code quality',
      description: 'Complete analysis framework using git commit history to answer: "What measurable difference do AI coding agents make?" Includes productivity analysis (commits, velocity, scope) and quality analysis (testing, docs, security patterns).',
      features: [
        'Productivity analysis from GitHub/Azure DevOps commit history',
        'Code quality density comparisons (testing, docs, security)',
        'Publication-ready charts and statistical multipliers',
        'Real findings: 3x commits, 12.5x lines, 252x test coverage'
      ],
      stack: 'PowerShell, Python (matplotlib), Node.js, GitHub CLI, Azure CLI',
      emoji: '📊'
    },
    'time-narrative': {
      name: 'time-narrative',
      title: 'Clockify AutoTrack Narrative Generator',
      subtitle: 'Transform raw Clockify time-tracking data into AI-generated weekly narratives',
      description: 'Extracts activity data from Clockify SQLite database, buckets into 30-minute slots, and uses parallel AI agents to generate human-readable markdown narratives of your work week.',
      features: [
        'SQLite extraction from Clockify AutoTracker database',
        '30-minute time slot bucketing with activity aggregation',
        'Parallel AI agent processing (one per day)',
        'Markdown narratives with semantic activity labels'
      ],
      stack: 'Node.js, SQLite, Claude Code/AI agents',
      emoji: '⏱️'
    }
  };

  // Check if we have curated content for this tool
  if (manualMappings[folderName]) {
    return manualMappings[folderName];
  }

  // Fallback: parse README for new tools
  const titleMatch = content.match(/^#\s+(.+)$/m);
  const title = titleMatch ? titleMatch[1].replace(/[📦🎯⏱️🔧🛠️⚡🎨🔥✨💡🚀📊🎭🔬🧪🤖]/g, '').trim() : folderName;
  
  let subtitle = '';
  const afterTitle = content.split(/^#\s+.+$/m)[1] || '';
  const boldMatches = afterTitle.matchAll(/\*\*([^*]{20,})\*\*/g);
  for (const match of boldMatches) {
    subtitle = match[1].trim();
    break;
  }

  const emoji = pickEmoji(folderName, content);

  return {
    name: folderName,
    title,
    subtitle,
    description: '',
    features: [],
    stack: '',
    emoji
  };
}

/**
 * Pick a relevant emoji based on folder name/content
 */
function pickEmoji(folderName, content) {
  const emojiMap = {
    'agentic': '🤖',
    'assessment': '📊',
    'time': '⏱️',
    'narrative': '📖',
    'test': '🧪',
    'deploy': '🚀',
    'api': '🔌',
    'auth': '🔐',
    'config': '⚙️',
    'monitor': '📡',
    'log': '📝',
    'database': '🗄️',
    'cache': '⚡',
    'queue': '📬',
    'webhook': '🪝',
    'parser': '🔍',
    'generator': '⚙️',
    'analyzer': '🔬',
    'report': '📈',
    'cli': '💻',
    'scraper': '🕷️',
    'migration': '🔄',
    'pipeline': '🔁'
  };

  for (const [keyword, emoji] of Object.entries(emojiMap)) {
    if (folderName.includes(keyword) || content.toLowerCase().includes(keyword)) {
      return emoji;
    }
  }

  return '🔧'; // Default
}

/**
 * Generate the complete README markdown
 */
function generateReadme(tools) {
  const toolSections = tools.map(tool => {
    let section = `### ${tool.emoji} [${tool.name}](${tool.name})\n\n`;
    
    if (tool.subtitle) {
      section += `**${tool.subtitle}**\n\n`;
    }
    
    if (tool.description) {
      section += `${tool.description}\n\n`;
    }
    
    if (tool.features.length > 0) {
      section += `**Key Features:**\n`;
      tool.features.forEach(f => {
        section += `- ${f}\n`;
      });
      section += '\n';
    }
    
    if (tool.stack) {
      section += `**Stack:** ${tool.stack}\n\n`;
    }
    
    section += `[📖 Full Documentation](./${tool.name}/README.md)`;
    
    return section;
  }).join('\n\n---\n\n');

  return `# 🗄️ Copilot Junk Drawer

**The junk drawer every developer needs** — a collection of powerful, focused tools that don't quite warrant their own repo, but are too useful to scatter across random gists.

You know that drawer in your kitchen with batteries, twist ties, and that one perfect screwdriver? This is that, but for development automation.

---

## 📦 What's Inside

${toolSections}

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
- Dedicated \`README.md\` with installation & usage
- All necessary code and dependencies
- Example outputs or templates

Navigate to the tool folder and follow its README.

---

## 🤝 Contributing

Got a powerful utility that doesn't warrant a full repo? Add it here:

1. Create a new folder with a descriptive lowercase-with-hyphens name
2. Include a comprehensive \`README.md\` following the pattern above
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
`;
}

/**
 * Main execution
 */
function main() {
  console.log('🔍 Discovering tools...');
  const tools = discoverTools();
  
  console.log(`✅ Found ${tools.length} tool(s):`);
  tools.forEach(t => console.log(`   ${t.emoji} ${t.name}`));

  console.log('\n📝 Generating README...');
  const readme = generateReadme(tools);

  fs.writeFileSync(README_PATH, readme, 'utf-8');
  console.log('✨ README.md updated successfully!');
}

main();
