# Feature Assessment & Synthesis Framework

A two-stage conversational AI framework for transforming rough feature requests into well-defined, implementation-ready specifications through iterative Q&A.

## Overview

This framework provides two AI agent prompts that work together to refine feature descriptions:

1. **Ingestion Prompt** (`framework-ingestion-prompt.md`): Iteratively assesses feature completeness and asks clarifying questions using an inference-first approach
2. **Synthesis Prompt** (`framework-summarize-prompt.md`): Synthesizes all gathered information into polished, structured output ready for development

## Key Capabilities

### ✨ Inference-First Questioning
Instead of asking "What's the business value?", the agent proposes: *"Based on your description of automating payment matching, I'm inferring this saves 30-60 minutes per day for finance staff. Is this correct?"*

This dramatically reduces back-and-forth by making educated guesses the user can simply confirm or refine.

### 🔄 Iterative Refinement Loop
- **Previously Collected Answers** array tracks all clarifications across multiple rounds
- Agent never re-asks answered questions
- Completeness score improves with each iteration
- Focus automatically shifts to next most critical gaps

### 📊 Structured Output
Both prompts emit strict JSON for programmatic consumption in automation workflows (Power Automate, Zapier, n8n, etc.)

### 🎯 Product Knowledge Cross-Check
Automatically detects when feature requests overlap with existing product capabilities and asks for differentiation

## Workflow

```
User submits rough feature request
         ↓
[Ingestion Prompt - Round 1]
  - Assesses completeness (e.g., 30%)
  - Identifies top 3 critical gaps
  - Proposes inferences with confirmation questions
         ↓
User confirms/corrects inferences
         ↓
[Ingestion Prompt - Round 2]
  - Reassesses with accumulated answers (e.g., 60%)
  - Moves to next most critical gaps
  - Continues inference-first approach
         ↓
...iterate until completeness ≥ 85%...
         ↓
[Synthesis Prompt]
  - Transforms description + all Q&A into polished spec
  - Generates release notes, acceptance criteria, dev notes
  - Returns structured JSON for work tracking system
         ↓
Feature ready for development
```

## Files in This Framework

- **`framework-ingestion-prompt.md`**: Assessment & questioning agent prompt
- **`framework-summarize-prompt.md`**: Synthesis & output generation agent prompt
- **`README-framework.md`**: This file - usage guide and customization instructions
- **`QUICKSTART-EXAMPLE.md`**: Concrete walkthrough with "TaskFlow Pro" example  
  **⭐ Includes detailed Power Automate flow implementation (based on production system)**
- **`CUSTOMIZATION-COMPARISON.md`**: Side-by-side comparison showing what was abstracted from the original BrightCom version

## Customization Guide

These prompts are intentionally generic. Here's how to adapt them for your product:

### 1. Define Your Input Format

**Location:** Both files, "Understanding the Input" section

Replace the example fields with your actual intake process:

```markdown
Feature Title: [Title]
Feature Description: [Original description text]
---
Your Custom Fields Here:
Priority: [1-10]
Impact: [High/Medium/Low]
Module: [Which module this affects]
----
Requested By: [email]
```

### 2. Add Product-Specific Knowledge

**Location:** `framework-ingestion-prompt.md`, "Product Knowledge Cross-Check" section

Replace the generic examples with YOUR product's existing features that requests often duplicate:

**Example for a CRM system:**

```markdown
### Common Features to Check Against:

**Contact Management:**
- Contact blocking (sales, marketing, all)
- Duplicate detection and merging
- Contact segmentation and tags
- Activity history tracking

**Sales Process:**
- Opportunity stages and pipelines
- Quote/proposal generation
- Approval workflows
- Revenue forecasting

... (add more for your product) ...
```

This enables the agent to detect when users are requesting features you already have.

### 3. Customize Technical Guidance

**Location:** `framework-summarize-prompt.md`, "developer_notes" examples

Update the technical components to match your stack:

**Example for a React/Node.js app:**

```markdown
**Components Needed:**
- **React Component:** Customer sync UI
- **API Endpoint:** POST /api/sync/customer-vendor
- **Service Layer:** CustomerVendorSyncService
- **Database:** Add vendor_link column to customers table

**Key Considerations:**
- Use React hooks for real-time updates
- Implement optimistic UI updates
- Add error boundary for sync failures
- Use SWR or React Query for cache invalidation
```

### 4. Adjust Estimation Guidelines

**Location:** `framework-summarize-prompt.md`, "Estimating Development Hours" section

Calibrate the complexity bands based on your typical feature sizes:

```markdown
**Estimation Guidelines (for Your Product):**

- **Trivial** (UI text change, config toggle): 1-2 hours
- **Simple** (1 screen change, simple backend logic): 4-8 hours
- **Medium** (multiple screens, business logic, API): 16-32 hours
- **Complex** (new module, external integration, data migration): 40-80 hours
- **Epic** (major subsystem, multiple integrations): 80-200 hours
```

### 5. Add Localization (Optional)

**Location:** `framework-summarize-prompt.md`, "Optional: Multi-Language Support" section

If you need translations for customer communication, uncomment/configure the localization section:

```json
{
  "description": {
    "markdown": "Primary language (English)",
    "html": "Primary language HTML"
  },
  "description_localized": {
    "es-ES": { "html": "Spanish translation" },
    "fr-FR": { "html": "French translation" },
    "ja-JP": { "html": "Japanese translation" }
  }
}
```

### 6. Integrate with Your Workflow Tool

These prompts emit JSON for automation. Example integrations:

#### Power Automate (Azure DevOps) 

**⭐ See [QUICKSTART-EXAMPLE.md - Building the Power Automate Flow](QUICKSTART-EXAMPLE.md#building-the-power-automate-flow) for a complete step-by-step guide.**

This is based on a production implementation processing 100+ features/month at BrightCom. The flow:
- Triggers from Microsoft Forms submission
- Creates draft Azure DevOps work item
- Runs up to 5 Q&A iterations via Teams adaptive cards
- Automatically accumulates answers and refines context
- Generates final polished spec in multiple formats
- Updates work item with all structured fields

**High-level pattern:**
```
Trigger: Form submission
 ↓
Create work item (draft state)
 ↓
Call OpenAI with ingestion prompt
 ↓
Do Until loop (max 5 iterations):
  - If questions exist:
    → Post adaptive card to Teams (2 questions at a time)
    → Wait for user response
    → Append answers to AccumulatedAnswers array
    → Call OpenAI again with accumulated context
  - If no questions:
    → Exit loop
 ↓
Call OpenAI with synthesis prompt (includes all Q&A)
 ↓
Update work item with polished output (HTML + markdown)
 ↓
Post completion card to Teams
```

#### Zapier (Jira)
```
Trigger: New Jira issue with label "needs-refinement"
 ↓
Action: OpenAI API call (ingestion prompt)
 ↓
Action: Add comment to Jira with questions
 ↓
Trigger: Comment added to issue
 ↓
Loop: Repeat until is_ok = true
 ↓
Action: OpenAI API call (synthesis prompt)
 ↓
Action: Update Jira issue fields with JSON output
 ↓
Action: Remove "needs-refinement" label, add "ready-for-dev"
```

#### n8n (Custom Workflow)
```
Webhook: New feature request
 ↓
OpenAI Node: Ingestion prompt
 ↓
IF Node: is_ok check
 ↓
Slack Node: Post questions to channel
 ↓
Webhook: Answer received
 ↓
Loop until complete
 ↓
OpenAI Node: Synthesis prompt
 ↓
HTTP Request: Post to your API/database
```

## Assessment Criteria Explained

The ingestion prompt checks for these elements (customize as needed):

| Criterion | Required? | What It Checks |
|-----------|-----------|----------------|
| **Business Value** | ✅ Required | Why the feature matters, who benefits, expected outcomes |
| **Acceptance Criteria** | ✅ Required | Testable "done" conditions in Given/When/Then format |
| **Functional Requirements** | ✅ Required | What the feature does, user workflows, data needs |
| **Constraints & Assumptions** | ✅ Required | Technical limits, scope boundaries, what's NOT included |
| **Dependencies** | ⚠️ If Applicable | Other features, external systems, prerequisites |
| **Non-Functional Requirements** | ⚠️ If Applicable | Performance, security, localization, compatibility |
| **Implementation Guidance** | 💡 Nice to Have | Suggested approach, known challenges |

## Inference Examples

The framework's "inference-first" approach is its superpower. Here's how it works:

### ❌ Traditional Open-Ended Question
> "What is the business value of this feature?"

**Problem:** User has to write a detailed explanation from scratch. Slow, often incomplete.

### ✅ Framework Inference Question
> "Based on your description of automating payment matching, I'm inferring this feature is primarily valuable for reducing manual accounting work and improving cash application speed - possibly saving 30-60 minutes per day for AR staff. Is this the core business value, or is there a different benefit you're targeting?"

**Result:** User can just say "Yes, that's right" or "Actually, it's more about reducing errors". Much faster iteration.

## Completeness Scoring

The framework uses a 0-100 scale:

- **0-30**: Critical gaps, needs multiple rounds of Q&A
- **40-60**: Core elements present, details needed
- **70-85**: Nearly complete, minor clarifications
- **85-100**: Ready for synthesis

**Tip:** Set your automation threshold at 85% to trigger the synthesis prompt.

## Output JSON Schema

### Ingestion Prompt Output
```json
{
  "is_ok": boolean,               // Ready for synthesis?
  "completeness_score": number,   // 0-100
  "missing": [                    // Top 3 critical gaps
    {
      "category": string,
      "severity": "critical" | "important" | "nice-to-have",
      "details": string,
      "question_to_ask": string   // Inference-based question
    }
  ],
  "suggestions": string[],        // Up to 3 improvements
  "strengths": string[]           // Up to 3 positive elements
}
```

### Synthesis Prompt Output
```json
{
  "release_title": string,
  "release_description": string,
  "description": {
    "markdown": string,
    "html": string
  },
  "acceptance_criteria": {
    "markdown": string,
    "html": string
  },
  "developer_notes": {
    "markdown": string,
    "html": string
  },
  "estimated_development_hours": number
}
```

## Tips for Success

### 1. Prime the Agent with Product Context
Before using the ingestion prompt, provide context:

```
You are assessing features for [ProductName], a [brief description].
Our users are primarily [user types]. Our tech stack is [technologies].
We compete with [competitors] and differentiate on [unique value].

Here's the feature request to assess:
[paste feature description]
```

### 2. Limit to 3 Questions Per Round
The framework automatically limits to top 3 gaps. Don't override this - it keeps conversations digestible.

### 3. Show Your Inference Work
When customizing example questions, always explain WHY you made that inference. This builds user trust.

### 4. Calibrate Estimates to Your Team
Track actual vs. estimated hours for a few features, then adjust your estimation guidelines.

### 5. Use Product Glossary
If your product has specialized terminology, include a glossary section in the ingestion prompt so the agent uses correct terms.

## Advanced Customization

### Add Custom Assessment Criteria
If your product needs additional checks (e.g., regulatory compliance), add them:

```markdown
### 8. Regulatory Compliance - REQUIRED IF APPLICABLE

**What to look for:**
- HIPAA data handling requirements
- GDPR right to deletion support
- SOC 2 audit trail considerations
- Industry-specific regulations (FINRA, etc.)

**Missing if:** Feature handles sensitive data but no compliance mentioned.
```

### Customize Severity Levels
The default severities are: `critical`, `important`, `nice-to-have`

You could add domain-specific severities:
- `security-critical` for security features
- `compliance-blocker` for regulated industries
- `customer-escalation` for urgent customer requests

### Add Workflow States
If your process has gates, add state tracking:

```json
{
  "workflow_state": "draft" | "in-review" | "approved" | "ready-for-dev",
  "approval_required": boolean,
  "approvers": string[]
}
```

## Example Usage (Python)

```python
import openai
import json

# Round 1: Initial assessment
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": open("framework-ingestion-prompt.md").read()},
        {"role": "user", "content": feature_request}
    ]
)

assessment = json.loads(response.choices[0].message.content)

# If not complete, ask questions
if not assessment["is_ok"]:
    for gap in assessment["missing"]:
        answer = input(gap["question_to_ask"])
        # Add to Previously Collected Answers array
        
# Round N: Final assessment shows is_ok = true
# Now synthesize
synthesis_response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": open("framework-summarize-prompt.md").read()},
        {"role": "user", "content": full_context_with_answers}
    ]
)

final_spec = json.loads(synthesis_response.choices[0].message.content)

# Create work item in tracking system
create_jira_issue(final_spec)
```

## Common Pitfalls

### ❌ Don't Skip Product Knowledge Section
Without this, the agent can't detect feature duplication. Users will request features you already have.

### ❌ Don't Over-Engineer Round 1
Start with 3-5 critical questions. You'll do multiple rounds anyway.

### ❌ Don't Ignore the Completeness Score
Use it as your automation trigger. Don't hard-code a round count.

### ❌ Don't Bypass Inference Step
The inference-first approach is what makes this fast. Don't revert to open-ended questions.

### ❌ Don't Forget JSON Escaping
Ensure your automation properly escapes quotes and newlines in JSON string fields.

## FAQ

**Q: Can I use this with Claude/Gemini instead of GPT-4?**  
A: Yes, the prompts are model-agnostic. Just ensure you use a model with 8K+ context window.

**Q: How do I handle "I don't know" answers?**  
A: The prompts handle this - they'll note the uncertainty and suggest researching that element before development.

**Q: Can I skip the assessment and go straight to synthesis?**  
A: Not recommended. The synthesis prompt expects complete information. You'll get poor results from incomplete requests.

**Q: What if my features are too complex for one work item?**  
A: The ingestion prompt can suggest breaking it into multiple features. Add that to your custom criteria.

**Q: How do I version these prompts?**  
A: Treat them like code. Use Git, semantic versioning, and track changes. Include version in the system message.

**Q: Can I use this for bug reports instead of features?**  
A: Yes, but customize the criteria (replace "business value" with "impact", add "steps to reproduce", etc.)

## License & Attribution

This framework is provided as-is for community use. Feel free to:
- ✅ Use in commercial products
- ✅ Modify for your needs
- ✅ Share with attribution
- ✅ Contribute improvements

No warranty provided. Test thoroughly before production use.

## Support & Contributions

Found this useful? Have improvements? We'd love to hear about it:
- Share examples of your customizations
- Report issues or edge cases
- Suggest new assessment criteria
- Contribute domain-specific examples

## Version History

**1.0.0** (2026-03-25)
- Initial framework release
- Inference-first approach
- Iterative Q&A loop pattern
- Dual markdown/HTML output
- Product knowledge cross-check

---

**Made with ❤️ for product teams who value specification quality**
