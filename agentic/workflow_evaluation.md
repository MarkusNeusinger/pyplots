# Workflow Orchestrator Evaluation

Evaluation of composable workflow orchestrators across 3 model tiers.

## Test Task

**Prompt:** "Add a GET /api/v1/plots/statistics/summary endpoint that returns a JSON response with: total_specifications (count of all spec directories in plots/), implementations_by_library (dict mapping each library to count of implementations), most_recent_spec (ID of the spec directory with the latest mtime), and generated_at (current UTC timestamp as ISO string). Create a new file api/routers/summary.py with the endpoint using FastAPI's APIRouter, register it in api/main.py, and add a pytest test in tests/test_summary_endpoint.py that validates the response schema and status code."

**Why this task:** Non-trivial because it requires reading the codebase structure, understanding the plots/ directory layout, creating a new router file, registering it, and adding tests. Likely to trigger linting/test failures for the test phase retry loop.

---

## Results

### Model: large (opus)

#### 1. plan_build.py

| Metric | Value |
|--------|-------|
| Start | |
| End | |
| Duration | |
| Plan Phase | |
| Build Phase | |
| Run ID | |
| Spec File | |
| Exit Code | |
| Notes | |

#### 2. plan_build_test.py

| Metric | Value |
|--------|-------|
| Start | |
| End | |
| Duration | |
| Plan Phase | |
| Build Phase | |
| Test Phase | |
| Test Retries | |
| Tests Passed | |
| Tests Failed | |
| Run ID | |
| Exit Code | |
| Notes | |

#### 3. plan_build_test_review.py

| Metric | Value |
|--------|-------|
| Start | |
| End | |
| Duration | |
| Plan Phase | |
| Build Phase | |
| Test Phase | |
| Review Phase | |
| Test Retries | |
| Review Retries | |
| Blockers Found | |
| Run ID | |
| Exit Code | |
| Notes | |

---

### Model: medium (sonnet)

#### 4. plan_build.py

| Metric | Value |
|--------|-------|
| Start | |
| End | |
| Duration | |
| Exit Code | |
| Notes | |

#### 5. plan_build_test.py

| Metric | Value |
|--------|-------|
| Start | |
| End | |
| Duration | |
| Test Retries | |
| Exit Code | |
| Notes | |

#### 6. plan_build_test_review.py

| Metric | Value |
|--------|-------|
| Start | |
| End | |
| Duration | |
| Test Retries | |
| Review Retries | |
| Exit Code | |
| Notes | |

---

### Model: small (haiku)

#### 7. plan_build.py

| Metric | Value |
|--------|-------|
| Start | |
| End | |
| Duration | |
| Exit Code | |
| Notes | |

#### 8. plan_build_test.py

| Metric | Value |
|--------|-------|
| Start | |
| End | |
| Duration | |
| Test Retries | |
| Exit Code | |
| Notes | |

#### 9. plan_build_test_review.py

| Metric | Value |
|--------|-------|
| Start | |
| End | |
| Duration | |
| Test Retries | |
| Review Retries | |
| Exit Code | |
| Notes | |

---

## Comparison Matrix

| # | Orchestrator | Model | Duration | Exit | Plan | Build | Test | Review | Retries | Notes |
|---|-------------|-------|----------|------|------|-------|------|--------|---------|-------|
| 1 | plan_build | large | | | | | - | - | - | |
| 2 | plan_build_test | large | | | | | | - | | |
| 3 | plan_build_test_review | large | | | | | | | | |
| 4 | plan_build | medium | | | | | - | - | - | |
| 5 | plan_build_test | medium | | | | | | - | | |
| 6 | plan_build_test_review | medium | | | | | | | | |
| 7 | plan_build | small | | | | | - | - | - | |
| 8 | plan_build_test | small | | | | | | - | | |
| 9 | plan_build_test_review | small | | | | | | | | |

## Observations

### Speed Comparison
- large vs medium:
- large vs small:
- medium vs small:

### Quality Comparison
- large:
- medium:
- small:

### Retry Behavior
- Test auto-fix effectiveness:
- Review blocker resolution:

### Prompt Optimization Suggestions
-
