# Report Issues

Report issues with existing plot specifications or implementations.

## Overview

Found a problem with an existing plot? The report system helps you:
1. Submit structured issue reports
2. Get AI-powered analysis and validation
3. Queue issues for maintainer review and fix

Reports are validated by AI and structured for efficient review.

---

## How to Report

### From pyplots.ai (Recommended)

1. Navigate to the plot page (e.g., `pyplots.ai/scatter-basic`)
2. Click **"report issue"** in the breadcrumb bar (top right)
3. Complete the form on GitHub
4. Wait for AI validation

**Spec issues:** Report from the overview page (e.g., `/scatter-basic`)
**Impl issues:** Report from the detail page (e.g., `/scatter-basic/matplotlib`)

The form will be pre-filled with the spec ID and library based on your current page.

### From GitHub

1. Go to [New Issue](https://github.com/MarkusNeusinger/pyplots/issues/new/choose)
2. Select **"Report Issue"** template
3. Fill in the spec ID, target, library, category, and description
4. Submit

---

## Issue Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **Visual** | Design/display issues | Overlapping labels, ugly colors, hard to read |
| **Data** | Data quality issues | Unrealistic values, inappropriate context |
| **Functional** | Doesn't work as expected | QR code not scannable, broken interactivity |
| **Other** | Other issues | Unclear spec, missing features |

---

## Labels

### Report Type

| Label | Purpose |
|-------|---------|
| `report:spec` | Issue with the specification (affects all libraries) |
| `report:impl` | Issue with a specific implementation |
| `report:impl:{library}` | Specific library affected (e.g., `report:impl:matplotlib`) |

### Categories

| Label | Purpose |
|-------|---------|
| `category:visual` | Design/visual issues |
| `category:data` | Data quality issues |
| `category:functional` | Non-functional elements |
| `category:other` | Other issues |

### Status

| Label | Purpose |
|-------|---------|
| `report-pending` | Report submitted, awaiting AI validation |
| `report-validated` | AI validated, ready for maintainer review |
| `approved` | Maintainer approved, ready for fix (future) |

---

## Workflow

```
User submits report
        │
        ▼ (report-pending label auto-added)
        │
report-validate.yml runs:
  ├── Validates spec/impl exists
  ├── Reads specification and metadata
  ├── AI analyzes the issue
  ├── Posts structured analysis comment
  └── Updates labels (report-validated + category + target)
        │
        ▼
Issue ready for maintainer review
        │
        ▼
Maintainer adds "approved" label
        │
        ▼
(Fix workflow - future implementation)
```

---

## Tips for Good Reports

1. **Be specific:** Describe exactly what's wrong
2. **Include context:** What did you expect vs. what happened?
3. **Use screenshots:** Especially for visual issues
4. **Check the spec:** Make sure the spec ID is correct
5. **One issue per report:** Don't combine multiple issues

---

## Related

- [Workflow Overview](overview.md)
- [Contributing](../contributing.md)
