# Workflow Overview

## How pyplots Automation Works

pyplots uses GitHub Actions to automate the entire plot lifecycle: from specification creation to implementation generation, quality review, and deployment.

---

## The Two Main Pipelines

### 1. Specification Pipeline

```
Issue + [spec-request] label
       |
       v
spec-create.yml
  |-- Creates branch: specification/{spec-id}
  |-- Generates: specification.md + specification.yaml
  |-- Creates PR --> main
  |-- Posts analysis comment
       |
       v (maintainer adds [approved] label to Issue)
       |
spec-create.yml (merge job)
  |-- Merges PR to main
  |-- Adds [spec-ready] label
  |-- Triggers sync-postgres.yml
```

### 2. Implementation Pipeline

```
Issue + [generate:{library}] label  OR  workflow_dispatch
       |
       v
impl-generate.yml
  |-- Creates branch: implementation/{spec-id}/{library}
  |-- AI generates code
  |-- Creates metadata/{library}.yaml (initial)
  |-- Tests execution
  |-- Uploads preview to GCS staging
  |-- Creates PR --> main
       |
       v
impl-review.yml
  |-- AI evaluates code + image
  |-- Posts review comment with score
  |-- Updates metadata/{library}.yaml (quality_score, review feedback)
  |-- Adds [quality:XX] label
       |
       |-- Score >= 90 --> [ai-approved] --> impl-merge.yml
       |                                        |-- Squash merge
       |                                        |-- Promotes GCS: staging --> production
       |                                        |-- Triggers sync-postgres.yml
       |
       |-- Score < 90 --> [ai-rejected] --> impl-repair.yml (max 3 attempts)
                                               |-- Reads AI feedback
                                               |-- Fixes implementation
                                               |-- Re-triggers impl-review.yml
```

---

## Label System

### Specification Labels (on Issues)

| Label | Meaning | Set By |
|-------|---------|--------|
| `spec-request` | New specification request | User |
| `spec-update` | Update existing specification | User |
| `spec-ready` | Specification merged, ready for implementations | Workflow |

### Implementation Labels (on Issues)

| Label | Meaning | Set By |
|-------|---------|--------|
| `generate:{library}` | Trigger generation for library | User |
| `impl:{library}:pending` | Generation in progress | Workflow |
| `impl:{library}:done` | Implementation merged to main | Workflow |
| `impl:{library}:failed` | Max retries exhausted | Workflow |

### PR Labels (on Pull Requests)

| Label | Meaning | Set By |
|-------|---------|--------|
| `ai-approved` | Quality check passed (score >= 90, or >= 50 after 3 attempts) | Workflow |
| `ai-rejected` | Quality check failed, triggers repair | Workflow |
| `ai-attempt-1/2/3` | Retry counter | Workflow |
| `quality:XX` | Quality score (e.g., quality:92) | Workflow |
| `quality-poor` | Score < 50, needs fundamental fixes | Workflow |

### Approval Labels

| Label | Meaning | Set By |
|-------|---------|--------|
| `approved` | Human approved specification | Maintainer |
| `rejected` | Human rejected | Maintainer |

---

## Quality Workflow

- **Score >= 90**: Immediately approved and merged
- **Score < 90**: Repair loop (up to 3 attempts)
- **After 3 attempts**:
  - Score >= 50: Merge anyway
  - Score < 50: Close PR, mark as failed

---

## Key Principles

1. **Decoupled**: Each library runs independently (no single point of failure)
2. **Partial OK**: 6/9 implementations done = fine
3. **No merge conflicts**: Per-library metadata files
4. **Auto-sync**: Database updated on every merge to main
5. **GCS flow**: staging --> production only after merge

---

## Workflow Files

Located in `.github/workflows/`:

| Workflow | Purpose |
|----------|---------|
| `spec-create.yml` | Creates new specifications |
| `spec-update.yml` | Updates existing specifications |
| `impl-generate.yml` | Generates single implementation |
| `impl-review.yml` | AI quality review |
| `impl-repair.yml` | Fixes rejected implementations |
| `impl-merge.yml` | Merges approved PRs |
| `bulk-generate.yml` | Batch implementation generation |
| `sync-postgres.yml` | Syncs plots/ to database |

---

## Bulk Operations

```bash
# All libraries for one spec:
gh workflow run bulk-generate.yml -f specification_id=scatter-basic -f library=all

# One library across all specs:
gh workflow run bulk-generate.yml -f specification_id=all -f library=matplotlib
```

**Concurrency limit**: Max 3 parallel implementations globally.
