# 📋 pyplots Rules System

## Overview

This directory contains **versioned rules** for automated plot generation and quality evaluation. These rules define how AI generates code and evaluates quality.

**Think of rules as "algorithms" for the AI system** - they need the same rigor as code: versioning, testing, and careful deployment.

---

## Quick Start

### Using Rules

```bash
# See what rules exist
cat rules/versions.yaml

# Read generation rules
cat rules/generation/v1.0.0-draft/code-generation-rules.md

# Read quality criteria
cat rules/generation/v1.0.0-draft/quality-criteria.md
```

### Creating a New Version

```bash
# 1. Copy existing version
cp -r rules/generation/v1.0.0-draft rules/generation/v1.1.0-draft

# 2. Edit rules
vim rules/generation/v1.1.0-draft/code-generation-rules.md

# 3. Update metadata
vim rules/generation/v1.1.0-draft/metadata.yaml

# 4. Test (see docs/concepts/ab-testing-rules.md)
python automation/testing/compare_rules.py --versions v1.0.0,v1.1.0

# 5. Promote to stable
mv rules/generation/v1.1.0-draft rules/generation/v1.1.0

# 6. Update active version
vim rules/versions.yaml
```

---

## Directory Structure

```
rules/
├── README.md                    # This file
├── versions.yaml                # Index of all versions
│
├── templates/                   # Templates for creating new rules
│   ├── generation-rules-template.md
│   ├── quality-criteria-template.md
│   └── evaluation-prompt-template.md
│
├── generation/                  # Code generation rules
│   ├── v1.0.0-draft/           # Initial version (work in progress)
│   │   ├── metadata.yaml       # Version info
│   │   ├── code-generation-rules.md
│   │   ├── quality-criteria.md
│   │   └── self-review-checklist.md
│   │
│   └── v2.0.0/                 # Future versions...
│       └── ...
│
└── evaluation/                  # Quality evaluation rules (future)
    └── v1.0.0/
        ├── metadata.yaml
        ├── scoring-rubric.md
        └── llm-evaluation-prompt.md
```

---

## File Formats

### Metadata (YAML)

Each version has a `metadata.yaml` with version info:

```yaml
version: "1.0.0"
type: "generation"
status: "draft"  # or "active", "deprecated", "archived"
created: "2025-01-23"
author: "Claude"
description: "Initial generation ruleset"
```

### Rules (Markdown)

Rules are written in **Markdown** because it's:
- ✅ Human-readable
- ✅ LLM-friendly
- ✅ Git-diffable
- ✅ Easy to comment and explain

---

## Version States

| State | Meaning | Can Edit? | Can Use? |
|-------|---------|-----------|----------|
| **draft** | Work in progress | ✅ Yes | ⚠️ Testing only |
| **active** | Production version | ❌ No (create new version) | ✅ Yes |
| **deprecated** | Superseded by newer version | ❌ No | ⚠️ Not recommended |
| **archived** | Historical record | ❌ No | ❌ No |

---

## Semantic Versioning

Rules use semantic versioning: `vMAJOR.MINOR.PATCH`

- **MAJOR** (v2.0.0): Breaking changes (e.g., change scoring scale)
- **MINOR** (v1.1.0): New features (e.g., add quality criterion)
- **PATCH** (v1.0.1): Bug fixes (e.g., clarify wording)

---

## Current Versions

See [versions.yaml](./versions.yaml) for the complete list.

**Active Versions** (as of last update):
- Generation: `v1.0.0-draft` (initial draft, not yet production-ready)
- Evaluation: _Not yet created_

---

## Workflow

### 1. Using Existing Rules

When generating plots, always specify which rule version to use:

```python
# Example (conceptual)
from pyplots.generation import generate_plot

plot = generate_plot(
    spec="specs/scatter-basic-001.md",
    library="matplotlib",
    rule_version="v1.0.0"  # Explicit version
)
```

### 2. Testing New Rules

Before activating a new version, test it:

```bash
# A/B test new vs current
python automation/testing/ab_test_runner.py \
  --baseline v1.0.0 \
  --candidate v2.0.0 \
  --specs scatter-basic-001,heatmap-corr-002 \
  --output comparison-report.html
```

See [docs/concepts/ab-testing-rules.md](../docs/concepts/ab-testing-rules.md) for detailed strategies.

### 3. Activating New Rules

After successful testing:

```yaml
# Edit rules/versions.yaml
active_versions:
  generation: "v2.0.0"  # Changed from v1.0.0

# Commit
git add rules/versions.yaml
git commit -m "chore(rules): activate generation rules v2.0.0"
```

---

## Best Practices

### DO ✅

- **Version everything**: Every change gets a new version
- **Test before activating**: Use A/B testing to validate improvements
- **Document changes**: Clear changelog in metadata.yaml
- **Keep old versions**: Don't delete, they're audit trail
- **Be specific**: "Improved colorblind safety" > "Made it better"

### DON'T ❌

- **Edit active versions**: Create new version instead
- **Skip testing**: Never activate without comparison
- **Vague descriptions**: Be specific about what changed
- **Mix concerns**: Don't change generation AND evaluation in one version

---

## Examples

### Example 1: View Current Rules

```bash
# What's currently active?
cat rules/versions.yaml

# Read generation rules
cat rules/generation/v1.0.0-draft/code-generation-rules.md

# Check metadata
cat rules/generation/v1.0.0-draft/metadata.yaml
```

### Example 2: Create New Version

```bash
# Start from current version
cp -r rules/generation/v1.0.0-draft rules/generation/v1.1.0-draft

# Make your changes
vim rules/generation/v1.1.0-draft/quality-criteria.md

# Update metadata
cat > rules/generation/v1.1.0-draft/metadata.yaml <<EOF
version: "1.1.0"
status: "draft"
description: "Added font size validation"
supersedes: "v1.0.0"
EOF

# Test it
# (see ab-testing documentation)

# Promote to active when ready
mv rules/generation/v1.1.0-draft rules/generation/v1.1.0
```

---

## Rule Types

### Generation Rules

**Purpose**: Define how AI generates plot code

**Files**:
- `code-generation-rules.md`: How to structure code
- `quality-criteria.md`: What makes good code
- `self-review-checklist.md`: How AI reviews its own code

### Evaluation Rules

**Purpose**: Define how AI evaluates plot quality

**Files**:
- `scoring-rubric.md`: 0-100 scale definition
- `llm-evaluation-prompt.md`: Instructions for Claude/Gemini/GPT
- `criteria-weights.md`: Importance of each criterion

---

## Integration Points

### With Automation

```yaml
# .github/workflows/generate-plot.yml
- name: Generate with specific rule version
  run: |
    python automation/generate.py \
      --spec scatter-basic-001 \
      --library matplotlib \
      --rule-version v1.0.0
```

### With Database

```sql
-- Track which rules generated which plots
SELECT
  spec_id,
  generation_ruleset_version,
  AVG(quality_score) as avg_score
FROM implementations
GROUP BY spec_id, generation_ruleset_version;
```

### With Claude Skills

```python
# Skill automatically loads appropriate rules
result = invoke_skill(
    skill="plot-generation",
    inputs={
        "rule_version": "v1.0.0",  # Which rules to use
        ...
    }
)
```

---

## FAQ

### Q: When should I create a new version?

**A**: When you want to change:
- How code is generated
- Quality criteria or scoring
- Self-review process
- Evaluation prompts

**Don't create new version for**:
- Typo fixes (just edit and commit)
- Code implementation changes (that's separate)

### Q: Can I test draft versions?

**A**: Yes! Draft versions are for testing. Use them to experiment before committing to a stable version.

### Q: How do I rollback?

**A**: Just update `versions.yaml` to point to the previous version:

```yaml
active_versions:
  generation: "v1.0.0"  # Rolled back from v2.0.0
```

### Q: Can different plots use different rule versions?

**A**: Not in the current design. There's one active version per rule type. All new generations use that version.

---

## Related Documentation

- [Rule Versioning Architecture](../docs/architecture/rule-versioning.md) - Full system design
- [A/B Testing Strategies](../docs/concepts/ab-testing-rules.md) - How to test new versions
- [Claude Skill](../docs/concepts/claude-skill-plot-generation.md) - Plot generation skill
- [Repository Structure](../docs/architecture/repository-structure.md) - Where rules fit in

---

## Status

**Current State**: Documentation phase
- ✅ Architecture documented
- ✅ Directory structure created
- ✅ Templates available
- ✅ Initial draft rules (v1.0.0-draft)
- ⏳ Automation not yet implemented
- ⏳ A/B testing framework not yet built

**Next Steps**:
1. Review draft rules
2. Refine based on actual spec generation
3. Build automation to use rules
4. Implement A/B testing
5. Promote v1.0.0-draft → v1.0.0 when ready

---

*"Rules are code. Version them like code."*
