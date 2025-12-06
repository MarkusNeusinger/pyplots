# Plot Specification Guide

## Overview

Plot specifications are **library-agnostic descriptions** of what a plot should show. They live in `specs/` as Markdown files.

**Key Principle**: A spec describes **WHAT** to visualize, not **HOW** to implement it.

---

## Spec Format

```markdown
# {spec-id}: {Title}

## Description

{2-4 sentences: What does this plot show? When should you use it?}

## Data

**Required columns:**
- `{column}` (numeric) - {what it represents}
- `{column}` (categorical) - {what it represents}

**Example:**
```python
import pandas as pd
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 3, 5, 4]
})
```

## Tags

{type}, {purpose}, {complexity}

## Use Cases

- {Realistic scenario 1 with domain context}
- {Realistic scenario 2}
- {Realistic scenario 3}
```

---

## Sections

### Title
Format: `# {spec-id}: {Human-Readable Title}`

Example: `# scatter-basic: Basic Scatter Plot`

### Description
2-4 sentences explaining:
- What the plot visualizes
- When to use it
- What makes it useful

### Data
- **Required columns** with types (numeric, categorical, datetime)
- **Example** (optional): Inline data, dataset reference, or omit for AI to generate

### Tags
Comma-separated keywords for discovery:
- Type: scatter, bar, line, pie, histogram, box, area
- Purpose: comparison, distribution, correlation, trend
- Complexity: basic, intermediate, advanced

### Use Cases
3-4 realistic scenarios with domain context (finance, science, marketing, etc.)

---

## Spec ID Naming

Format: `{type}-{variant}` or `{type}-{variant}-{modifier}`

Examples:
- `scatter-basic` - Simple scatter plot
- `scatter-color-groups` - Scatter with color-coded groups
- `bar-grouped-horizontal` - Horizontal grouped bars

Rules:
- Lowercase only
- Hyphens as separators
- Descriptive names (no numbers needed)

---

## Workflow

1. **User creates GitHub Issue** with plot idea
2. **Bot assigns spec ID** and validates request
3. **Maintainer adds `approved` label**
4. **AI generates spec file** in `specs/`
5. **AI generates implementations** for all 9 libraries
6. **Quality check** runs automatically
7. **Auto-merge** if quality passes

---

## Writing Good Specs

### DO
- Be specific about data requirements
- Use realistic use cases with domain context
- Keep description concise (2-4 sentences)

### DON'T
- Include library-specific details
- Add quality criteria (handled by central prompts)
- Over-specify styling (AI decides based on style guide)

---

*See `specs/.template.md` for the full template.*
