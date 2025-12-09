# Plot Specification Guide

## Overview

Plot specifications are **library-agnostic descriptions** of what a plot should show. They live in `plots/{spec-id}/spec.md`.

**Key Principle**: A spec describes **WHAT** to visualize, not **HOW** to implement it.

---

## File Location

Each spec lives in its own directory:
```
plots/{spec-id}/
├── spec.md              ← Specification file
├── metadata.yaml        ← Tags, generation info
└── implementations/     ← Library code
```

---

## Spec Format

```markdown
# {spec-id}: {Title}

## Description

{2-4 sentences: What does this plot show? When should you use it?}

## Applications

- {Realistic scenario 1 with domain context}
- {Realistic scenario 2}
- {Realistic scenario 3}

## Data

- `{column}` ({type}) - {what it represents}
- `{column}` ({type}) - {what it represents}
- Size: {recommended data size}
- Example: {dataset reference or description}

## Notes

- {Optional implementation hints or special requirements}
```

---

## Sections

### Title
Format: `# {spec-id}: {Human-Readable Title}`

Example: `# scatter-basic: Basic Scatter Plot`

### Description
2-4 sentences (prose text) explaining:
- What the plot visualizes
- When to use it
- What makes it useful

### Applications
3-4 realistic scenarios with domain context (finance, science, marketing, etc.)

### Data
Simple list format:
- Required columns with types (numeric, categorical, datetime)
- Recommended data size
- Example dataset reference

### Notes (Optional)
Implementation hints, visual preferences, or special requirements.

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
4. **AI generates spec file** in `plots/{spec-id}/spec.md`
5. **AI generates implementations** for all 9 libraries
6. **Quality check** runs automatically
7. **Auto-merge** if quality passes

---

## Writing Good Specs

### DO
- Be specific about data requirements
- Use realistic applications with domain context
- Keep description concise (2-4 sentences)

### DON'T
- Include library-specific details
- Add quality criteria (handled by central prompts)
- Over-specify styling (AI decides based on style guide)

---

*See `prompts/templates/spec.md` for the full template.*
