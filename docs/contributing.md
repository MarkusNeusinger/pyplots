# Contributing to pyplots

## Overview

pyplots is a specification-driven platform where **AI generates all plot implementations**. As a contributor, your main focus is on **specifications** (what to visualize) rather than code (how to implement).

---

## Three Ways to Contribute

| Action | When to Use | From pyplots.ai |
|--------|-------------|-----------------|
| **[Suggest Spec](#suggest-a-new-plot-type)** | Propose a new plot type | Click "suggest spec" in catalog |
| **[Report Spec Issue](#report-a-spec-issue)** | Problem with a specification | Click "report issue" on spec page |
| **[Report Impl Issue](#report-an-impl-issue)** | Problem with a library implementation | Click "report issue" on impl page |

All contributions go through GitHub Issues with AI-powered validation and processing.

---

## Suggest a New Plot Type

1. **Create a GitHub Issue** with a descriptive title (e.g., "Radar Chart with Multiple Series")
   - Do NOT include spec-id in the title
2. **Add the `spec-request` label**
3. **Wait for automation**:
   - `spec-create.yml` analyzes your request
   - Assigns a unique spec-id
   - Creates a PR with `specification.md` and `specification.yaml`
4. **Review the generated spec** (PR comments)
5. **Maintainer adds `approved` label** to the Issue (not the PR)
6. **Spec merges to main** with `spec-ready` label

---

## Report a Spec Issue

Found a problem with a specification (affects all libraries)?

1. **From pyplots.ai**: Navigate to the spec page (e.g., `/scatter-basic`) and click "report issue"
2. **From GitHub**: Create issue using the [Report Specification Issue](https://github.com/MarkusNeusinger/pyplots/issues/new?template=report-spec-issue.yml) template
3. **Choose a category**: Visual, Data, Functional, or Other (optional)
4. **Describe the issue**

AI validates your report and adds structured analysis. Maintainers review and approve fixes.

---

## Report an Impl Issue

Found a problem with a specific library implementation?

1. **From pyplots.ai**: Navigate to the impl page (e.g., `/scatter-basic/matplotlib`) and click "report issue"
2. **From GitHub**: Create issue using the [Report Implementation Issue](https://github.com/MarkusNeusinger/pyplots/issues/new?template=report-impl-issue.yml) template
3. **Enter the library name** (matplotlib, seaborn, etc.)
4. **Choose a category**: Visual, Data, Functional, or Other (optional)
5. **Describe the issue**

AI validates your report and adds structured analysis. Maintainers review and approve fixes.

---

## Trigger Implementation Generation

After a spec has the `spec-ready` label:

**Single Library:**
- Add `generate:{library}` label to the issue (e.g., `generate:matplotlib`)

**All Libraries:**
```bash
gh workflow run bulk-generate.yml -f specification_id=<spec-id> -f library=all
```

---

## What NOT to Do

| Don't | Why |
|-------|-----|
| Manually create `plots/` directories | Let `spec-create.yml` handle it |
| Write `specification.md` files directly | Let AI generate from your Issue |
| Include `[spec-id]` in issue titles | Spec-id is auto-assigned |
| Add `approved` label to PRs | Add it to Issues instead |
| Run `gh pr merge` on implementation PRs | Let `impl-merge.yml` handle it |
| Create `metadata/*.yaml` manually | Created automatically on merge |

---

## Why This Workflow?

Manual intervention causes:
- Missing quality scores in metadata
- Missing preview images in GCS
- Issues staying open when complete
- Broken database sync

**Trust the automation.** It handles: code generation, quality review, repair attempts, image promotion, and database sync.

---

## Labels Reference

See [workflows/overview.md](./workflows/overview.md) for the complete label system.

---

## Questions?

- Check existing [Issues](https://github.com/MarkusNeusinger/pyplots/issues) for similar requests
- Review the [workflows overview](./workflows/overview.md) for automation details
