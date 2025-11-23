# 📋 Rule Versioning System

## Overview

The pyplots automation system relies on **rules** for two critical operations:
1. **Code Generation**: How AI generates plot implementations from specs
2. **Quality Evaluation**: How AI evaluates if generated plots meet quality standards

These rules are the "algorithms" of the system and must be:
- **Versioned**: Track changes over time
- **Testable**: Compare different versions scientifically
- **Rollback-able**: Revert to previous versions if needed
- **Auditable**: Know which rule version generated each plot

**Key Principle**: Rules are code. They need the same engineering rigor as any other code: version control, testing, and systematic rollout.

---

## Why Rule Versioning is Critical

### The Problem Without Versioning

```
❌ Without Rule Versioning:
- Prompt changed → All plots regenerated → Can't compare before/after
- Quality criteria updated → No way to test impact
- Something breaks → Don't know what changed
- Improvements made → Can't prove they're better
- Manual tweaks → Lost in chat history
```

### The Solution With Versioning

```
✅ With Rule Versioning:
- Every rule change has a version number (v1.0.0, v2.0.0, etc.)
- A/B testing: Generate plots with both versions, compare objectively
- Full audit trail: Know which rule version generated each plot
- Safe rollback: Issues with v2.0.0? Rollback to v1.5.2 instantly
- Scientific improvement: Prove new rules are better before deploying
```

---

## File Format: Why Markdown?

Rules are stored as **Markdown files** (not YAML, JSON, or code) because:

| Benefit | Explanation |
|---------|-------------|
| **Human-readable** | Easy to review and discuss in PRs |
| **LLM-friendly** | Well-structured, easy for AI to parse and understand |
| **Git-diffable** | See exactly what changed between versions |
| **Commentable** | Add inline explanations and rationale |
| **Flexible** | Support various structures (checklists, examples, prose) |
| **Tool-agnostic** | No special parser needed, just read and use |
| **Version-controllable** | Standard git workflows apply |

**Example Comparison**:

```markdown
# Markdown (✅ Chosen)
## Quality Criteria

### Axes Labeling
- **Requirement**: Both X and Y axes must have clear labels
- **Rationale**: Without labels, users can't understand the data
- **Check**: Verify `ax.get_xlabel()` and `ax.get_ylabel()` are not empty
- **Weight**: Critical (1.0)
```

```yaml
# YAML (❌ Not chosen - less expressive)
quality_criteria:
  axes_labeling:
    requirement: "Both X and Y axes must have clear labels"
    weight: 1.0
```

```python
# Python (❌ Not chosen - requires execution)
@quality_check(weight=1.0, critical=True)
def check_axes_labeled(fig):
    """Both X and Y axes must have clear labels"""
    pass
```

---

## Directory Structure

```
pyplots/
├── rules/
│   ├── README.md                          # Entry point, explains system
│   │
│   ├── templates/                         # Templates for creating new rules
│   │   ├── generation-rules-template.md   # Template for code generation
│   │   ├── quality-criteria-template.md   # Template for quality checks
│   │   └── evaluation-prompt-template.md  # Template for LLM prompts
│   │
│   ├── generation/                        # Code generation rules
│   │   ├── v1.0.0/                        # Stable version 1.0.0
│   │   │   ├── metadata.yaml              # Version info (date, author, status)
│   │   │   ├── code-generation-rules.md   # How to generate code
│   │   │   ├── quality-criteria.md        # Quality checks for generation
│   │   │   └── self-review-checklist.md   # Self-review loop criteria
│   │   │
│   │   ├── v1.1.0/                        # Minor update
│   │   │   └── ...
│   │   │
│   │   ├── v2.0.0/                        # Major update
│   │   │   └── ...
│   │   │
│   │   └── v2.1.0-draft/                  # Work in progress (not active)
│   │       └── ...
│   │
│   ├── evaluation/                        # Quality evaluation rules
│   │   ├── v1.0.0/
│   │   │   ├── metadata.yaml
│   │   │   ├── scoring-rubric.md          # How to score plots (0-100)
│   │   │   ├── llm-evaluation-prompt.md   # Prompt for Claude/Gemini/GPT
│   │   │   └── criteria-weights.md        # Importance of each criterion
│   │   │
│   │   └── v2.0.0/
│   │       └── ...
│   │
│   └── versions.yaml                      # Index of all versions
```

---

## Versioning Strategy: Semantic Versioning

Rules follow **Semantic Versioning** (semver): `vMAJOR.MINOR.PATCH`

### Version Number Meaning

```
v2.3.1
│ │ │
│ │ └─ PATCH: Bug fixes, clarifications (backward compatible)
│ │            Example: Fix typo, clarify wording
│ │
│ └─── MINOR: New features, improvements (backward compatible)
│             Example: Add new quality criterion, improve prompt
│
└───── MAJOR: Breaking changes (not backward compatible)
              Example: Change scoring scale, remove criteria
```

### Examples

**v1.0.0 → v1.0.1** (Patch)
```diff
## Quality Criteria
- Axes must be labeled with column names
+ Axes must be labeled with descriptive names (column names by default)
```
*Clarification only, doesn't change behavior*

**v1.0.0 → v1.1.0** (Minor)
```diff
## Quality Criteria
- Axes must be labeled
- Grid must be visible
+ Font sizes must be readable (minimum 10pt)
```
*New criterion added, old ones still valid*

**v1.0.0 → v2.0.0** (Major)
```diff
## Scoring Scale
- Old: Score 0-10
+ New: Score 0-100
```
*Breaking change: old scores not comparable to new*

---

## Metadata Format

Every rule version has a `metadata.yaml` file:

```yaml
# rules/generation/v1.0.0/metadata.yaml
version: "1.0.0"
type: "generation"  # or "evaluation"
status: "active"    # active, draft, deprecated, archived
created: "2025-01-23"
author: "Claude"
description: "Initial code generation ruleset"

supersedes: null    # Previous version (null for first version)
superseded_by: null # Next version (null if still active)

compatibility:
  python_versions: ["3.10", "3.11", "3.12", "3.13"]
  libraries:
    matplotlib: "3.8.0+"
    seaborn: "0.13.0+"
    plotly: "5.18.0+"

changelog:
  - "Initial release"
  - "Based on documentation from docs/workflow.md"
  - "Extracted quality criteria from docs/architecture/specs-guide.md"

references:
  - "docs/workflow.md"
  - "docs/architecture/specs-guide.md"
  - "GitHub Issue #XXX: Initial rule definition"
```

---

## Rule File Structure

### 1. Code Generation Rules

**File**: `rules/generation/v1.0.0/code-generation-rules.md`

**Structure**:
```markdown
# Code Generation Rules v1.0.0

## Metadata
- Version: 1.0.0
- Type: Generation
- Status: Active
- Last Updated: 2025-01-23

## Purpose
Define how AI generates plot implementation code from specifications.

## Input
- Spec Markdown file (specs/{spec-id}.md)
- Target library (matplotlib, seaborn, plotly)
- Variant (default, style, version-specific)

## Output
- Python file with create_plot() function
- Type-annotated, documented, tested

## Generation Process

### Step 1: Analyze Spec
- Read spec requirements
- Identify required vs optional parameters
- Understand expected output

### Step 2: Library Selection
- **matplotlib**: Always implement
- **seaborn**: If plot type suitable (heatmap, scatter, etc.)
- **plotly**: If interactivity beneficial

### Step 3: Code Generation
[Detailed generation rules...]

### Step 4: Self-Review
[Self-review checklist...]

## Code Style Requirements
[Style guidelines...]

## Examples
[Concrete examples...]
```

### 2. Quality Criteria

**File**: `rules/generation/v1.0.0/quality-criteria.md`

**Structure**:
```markdown
# Quality Criteria v1.0.0

## Visual Quality

### Criterion: Axes Labeled
- **ID**: `axes_labeled`
- **Requirement**: X and Y axes must have descriptive labels
- **Check**: Both `ax.get_xlabel()` and `ax.get_ylabel()` return non-empty strings
- **Weight**: 1.0 (critical)
- **Failure Impact**: Major - plot is unusable without labels

### Criterion: Grid Visibility
- **ID**: `grid_visible`
- **Requirement**: Grid should be visible but subtle (alpha ≤ 0.5)
- **Check**: Grid is enabled and transparency is appropriate
- **Weight**: 0.5 (nice-to-have)
- **Failure Impact**: Minor - aesthetic issue only

[More criteria...]

## Code Quality

### Criterion: Type Hints
[...]

### Criterion: Docstring
[...]

## Performance

### Criterion: Execution Time
[...]
```

### 3. LLM Evaluation Prompt

**File**: `rules/evaluation/v1.0.0/llm-evaluation-prompt.md`

**Structure**:
```markdown
# LLM Evaluation Prompt v1.0.0

## System Prompt

You are a data visualization quality expert. Your task is to evaluate if a generated plot meets the specified quality criteria.

## Input Format

You will receive:
1. **Spec Markdown**: The original plot specification
2. **Preview Image**: PNG of the generated plot
3. **Quality Criteria**: List of criteria from the spec

## Evaluation Process

### Step 1: Load Criteria
Read the quality criteria from the spec:
```
## Quality Criteria
- [ ] Criterion 1
- [ ] Criterion 2
...
```

### Step 2: Visual Inspection
[Detailed instructions...]

### Step 3: Scoring
[Scoring guidelines...]

## Output Format

```json
{
  "score": 0-100,
  "criteria_met": ["id1", "id2"],
  "criteria_failed": ["id3"],
  "feedback": "Detailed explanation...",
  "suggestions": ["Suggestion 1", "Suggestion 2"]
}
```

[More detailed instructions...]
```

---

## Version Index

**File**: `rules/versions.yaml`

Maintains an index of all rule versions:

```yaml
# rules/versions.yaml
active_versions:
  generation: "1.0.0"
  evaluation: "1.0.0"

versions:
  generation:
    - version: "1.0.0"
      status: "active"
      path: "generation/v1.0.0/"
      created: "2025-01-23"
      description: "Initial generation ruleset"

    - version: "1.1.0"
      status: "deprecated"
      path: "generation/v1.1.0/"
      created: "2025-02-01"
      description: "Improved quality criteria"
      superseded_by: "2.0.0"

    - version: "2.0.0"
      status: "active"
      path: "generation/v2.0.0/"
      created: "2025-02-15"
      description: "Major update: new scoring system"

    - version: "2.1.0-draft"
      status: "draft"
      path: "generation/v2.1.0-draft/"
      created: "2025-03-01"
      description: "Testing improved self-review"

  evaluation:
    - version: "1.0.0"
      status: "active"
      path: "evaluation/v1.0.0/"
      created: "2025-01-23"
      description: "Initial evaluation ruleset"
```

---

## Git Workflow

### Creating a New Rule Version

```bash
# 1. Create new version directory
mkdir -p rules/generation/v2.0.0

# 2. Copy from previous version
cp -r rules/generation/v1.0.0/* rules/generation/v2.0.0/

# 3. Update metadata
vim rules/generation/v2.0.0/metadata.yaml
# Change version to "2.0.0"
# Update changelog

# 4. Make changes to rule files
vim rules/generation/v2.0.0/code-generation-rules.md

# 5. Commit with semantic message
git add rules/generation/v2.0.0/
git commit -m "feat(rules): add generation rules v2.0.0

- Improved quality criteria for colorblind safety
- Added font size validation
- Refined self-review checklist

Breaking change: New scoring rubric (0-100 scale)
Supersedes: v1.0.0"

# 6. Update active version
vim rules/versions.yaml
# Set active_versions.generation = "2.0.0"

git add rules/versions.yaml
git commit -m "chore(rules): activate generation rules v2.0.0"
```

### Viewing Version History

```bash
# See all changes to a specific rule file
git log rules/generation/v1.0.0/code-generation-rules.md

# Compare two versions
git diff v1.0.0:rules/generation/v1.0.0/quality-criteria.md \
         v2.0.0:rules/generation/v2.0.0/quality-criteria.md

# See when version was created
git log --follow rules/generation/v2.0.0/metadata.yaml
```

---

## Testing Rule Versions

See detailed A/B testing strategies in [docs/concepts/ab-testing-rules.md](../concepts/ab-testing-rules.md).

### Quick Comparison

```bash
# Generate plots with both rule versions
python automation/testing/compare_rules.py \
  --versions v1.0.0,v2.0.0 \
  --specs scatter-basic-001,heatmap-corr-002 \
  --output comparison-report.html

# Report includes:
# - Side-by-side image comparisons
# - Quality score distributions
# - Pass/fail rates
# - Generation time comparisons
```

---

## Integration with Existing System

### Database Schema (Future)

When automation is implemented, track which rule version generated each plot:

```sql
ALTER TABLE implementations
  ADD COLUMN generation_ruleset_version VARCHAR,
  ADD COLUMN evaluation_ruleset_version VARCHAR;

-- Example query: Find all plots generated with v1.0.0
SELECT * FROM implementations
WHERE generation_ruleset_version = 'v1.0.0';

-- Example: Performance comparison
SELECT
  generation_ruleset_version,
  AVG(quality_score) as avg_score,
  COUNT(*) as total_plots
FROM implementations
GROUP BY generation_ruleset_version;
```

### API Endpoints (Future)

```python
# GET /rules/versions
# List all available rule versions

# GET /rules/generation/{version}
# Get specific generation ruleset

# GET /rules/active
# Get currently active versions

# POST /rules/generate-with-version
# Generate plot using specific rule version (for testing)
```

### GitHub Actions Integration (Future)

```yaml
# .github/workflows/ab-test-rules.yml
on:
  pull_request:
    paths:
      - 'rules/**'

jobs:
  test-new-rules:
    runs-on: ubuntu-latest
    steps:
      - name: Detect rule version change
        # Extract old and new version

      - name: Run A/B test
        run: |
          python automation/testing/ab_test_runner.py \
            --baseline $OLD_VERSION \
            --candidate $NEW_VERSION \
            --test-specs standard_test_set.txt

      - name: Post results to PR
        # Comment with comparison report
```

---

## Migration Path

### Phase 1: Documentation (Current)
- ✅ Document rule versioning system
- ✅ Create templates
- ✅ Create v1.0.0-draft (initial rules)
- Status: **You are here**

### Phase 2: Manual Process (Next)
- Manually use rule files when generating plots
- Track versions in git commit messages
- Manual A/B comparisons
- Learn what works

### Phase 3: Semi-Automated
- Scripts to generate with specific rule versions
- Comparison tools
- Database tracking

### Phase 4: Fully Automated
- GitHub Actions integration
- Automatic A/B testing
- Canary releases
- Monitoring and rollback

---

## Best Practices

### DO ✅

**1. Document Changes**
Every version should have clear changelog in metadata.yaml

**2. Test Before Activating**
Always A/B test new version against current before making it active

**3. Keep Old Versions**
Don't delete old rule versions - they're part of the audit trail

**4. Semantic Versioning**
Use semver correctly (major = breaking, minor = features, patch = fixes)

**5. Reference Context**
Link to GitHub Issues, PRs, or discussions that motivated the change

### DON'T ❌

**1. Edit Active Versions**
Don't modify an active version - create a new version instead

**2. Skip Testing**
Never activate a new version without comparing against current

**3. Vague Descriptions**
"Improved quality" is not useful - be specific about what changed

**4. Mix Concerns**
Don't change both generation AND evaluation rules in one version

---

## Examples

### Example 1: Adding a New Quality Criterion

**Situation**: We notice many plots have unreadable font sizes

**Solution**: Add font size validation to generation rules

**Version**: v1.0.0 → v1.1.0 (minor, backward compatible)

**Changes**:
```diff
# rules/generation/v1.1.0/quality-criteria.md

## Visual Quality

+### Criterion: Font Size Readable
+- **ID**: `font_size_readable`
+- **Requirement**: All text must be readable (minimum 10pt)
+- **Check**: Verify axis labels, title, and legend fonts ≥ 10pt
+- **Weight**: 0.8
+- **Failure Impact**: Medium - readability issue
```

**Testing**:
```bash
# Generate 10 plots with v1.0.0 and v1.1.0
# Compare font sizes in generated images
# Confirm v1.1.0 produces larger, more readable text
```

### Example 2: Changing Scoring Scale

**Situation**: 0-10 scale not granular enough

**Solution**: Switch to 0-100 scale

**Version**: v1.0.0 → v2.0.0 (major, breaking change)

**Changes**:
```diff
# rules/evaluation/v2.0.0/scoring-rubric.md

## Scoring Scale

-Score range: 0-10
+Score range: 0-100

-Pass threshold: ≥ 8
+Pass threshold: ≥ 85
```

**Migration**:
- Regenerate all plots with new version
- Cannot compare v1.x scores with v2.x scores
- Update database schema if needed

---

## FAQ

### Q: When should I create a new rule version?

**A**: Create a new version when you want to:
- Change how code is generated
- Add/remove/modify quality criteria
- Update evaluation prompts
- Change scoring thresholds
- Improve self-review process

**Don't create a new version for**:
- Typo fixes in docs (just edit)
- Code implementation changes (that's different)
- UI changes (not related to rules)

### Q: How do I know if a change is major vs minor?

**A**: Ask: "Can I compare results from old and new versions?"
- YES → Minor version (backward compatible)
- NO → Major version (breaking change)

**Examples**:
- Add new criterion → Minor (old criteria still valid)
- Remove criterion → Major (results not comparable)
- Change scoring scale → Major (different meaning)
- Improve prompt wording → Minor (same intent)

### Q: What if I want to experiment with rules?

**A**: Create a draft version with `-draft` suffix:
```
rules/generation/v2.1.0-draft/
```
- Mark status as "draft" in metadata
- Not listed as active in versions.yaml
- Can be modified freely
- Promote to stable when ready

### Q: How do I rollback to a previous version?

**A**: Update `rules/versions.yaml`:
```yaml
active_versions:
  generation: "1.0.0"  # Was: "2.0.0"
```
Commit and push. System will use old version immediately.

### Q: Can I have different versions for different plots?

**A**: Not in the current design - one active version per rule type.
For plot-specific rules, consider variants instead of versions.

---

## Related Documentation

- [A/B Testing Strategies](../concepts/ab-testing-rules.md)
- [Claude Skill for Plot Generation](../concepts/claude-skill-plot-generation.md)
- [Repository Structure](./repository-structure.md)
- [Automation Workflows](./automation-workflows.md)
- [Specs Guide](./specs-guide.md)

---

*"Rules are code. Version them like code."*
