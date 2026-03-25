# Feature Assessment & Synthesis Framework

**Two-stage conversational AI framework for transforming rough feature requests into implementation-ready specifications through iterative Q&A**

## What This Is

A pair of AI agent prompts that work together to refine vague feature ideas into polished, structured specifications ready for development teams.

### 1. Ingestion Prompt ([framework-ingestion-prompt.md](framework-ingestion-prompt.md))

**Iterative assessment agent** that analyzes feature completeness and asks clarifying questions using an inference-first approach.

- Proposes educated guesses instead of open-ended questions (*"I'm inferring this saves 30-60 minutes per day. Is this correct?"*)
- Tracks accumulated answers across multiple rounds to never re-ask
- Calculates completeness scores and focuses on critical gaps
- Detects overlaps with existing product capabilities
- Emits structured JSON for automation workflows

### 2. Synthesis Prompt ([framework-summarize-prompt.md](framework-summarize-prompt.md))

**Output generation agent** that transforms all gathered information into polished, structured specifications.

- Generates release notes, acceptance criteria, and developer notes
- Creates both markdown (human-readable) and HTML (interactive cards)
- Provides development hour estimates with complexity breakdowns
- Returns strict JSON for programmatic consumption
- Ready for Power Automate, Zapier, n8n, or custom automation

## Key Capabilities

- ✨ **Inference-First Questioning**: AI proposes answers for users to confirm/refine instead of asking blank-slate questions
- 🔄 **Iterative Refinement**: Completeness tracking and automatic focus shifting across multiple rounds
- 📊 **Structured Output**: Strict JSON for automation workflows
- 🎯 **Product Knowledge Cross-Check**: Detects feature request overlaps with existing capabilities
- 🤖 **Automation-Ready**: Designed for Power Automate, Zapier, n8n, and custom workflows

## Quick Start

1. **Submit** a rough feature request to the ingestion prompt
2. **Iterate** through Q&A rounds until completeness ≥ 85%
3. **Synthesize** all accumulated answers through the synthesis prompt
4. **Deliver** polished specification to development team

Full walkthrough: [QUICKSTART-EXAMPLE.md](QUICKSTART-EXAMPLE.md)  
**Includes detailed Power Automate flow implementation based on production system processing 100+ features/month**

## Production Credentials

This framework is abstracted from BrightCom's production implementation:
- **100+ feature requests/month** processed through Microsoft Forms → Power Automate → Azure OpenAI
- **Microsoft Teams** integration for interactive Q&A with adaptive cards
- **Azure DevOps** work item tracking with custom fields
- Real-world validation across 12+ products in healthcare/finance/logistics domains

## Files in This Framework

| File | Purpose |
|------|---------|
| `framework-ingestion-prompt.md` | Assessment & iterative questioning agent prompt |
| `framework-summarize-prompt.md` | Synthesis & output generation agent prompt |
| `QUICKSTART-EXAMPLE.md` | Complete walkthrough + Power Automate flow guide |
| `CUSTOMIZATION-COMPARISON.md` | What was abstracted from original BrightCom version |

## Prerequisites

- AI platform with JSON response format support (Azure OpenAI GPT-4, Claude 3+, etc.)
- Optional: Automation platform (Power Automate, Zapier, n8n) for end-to-end workflow
- Optional: Work tracking system (Azure DevOps, Jira, etc.) for spec delivery

## Stack

**Stack:** AI prompts (platform-agnostic), JSON, Markdown, HTML/Adaptive Cards

**Example Implementation:** Power Automate + Azure OpenAI GPT-4 + Microsoft Forms + Azure DevOps + Teams

## Customization

The prompts are intentionally generic. See [README-framework.md](README-framework.md) for detailed customization guide:

1. Define your input format (custom fields, priority levels, etc.)
2. Add product-specific knowledge (existing features to check against)
3. Customize technical guidance (your stack, architecture patterns)
4. Adjust estimation guidelines (your typical feature complexity bands)

## License

MIT
