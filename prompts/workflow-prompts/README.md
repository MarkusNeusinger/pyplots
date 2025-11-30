# Workflow Prompts

Centralized prompt templates for GitHub Actions workflows.

## Usage in Workflows

These prompts use `${VARIABLE}` placeholders that must be substituted before use:

```yaml
- name: Generate prompt
  id: prompt
  run: |
    cat prompts/workflow-prompts/generate-implementation.md | \
      sed "s/\${LIBRARY}/${{ inputs.library }}/g" | \
      sed "s/\${SPEC_ID}/${{ inputs.spec_id }}/g" | \
      sed "s/\${ATTEMPT}/${{ inputs.attempt }}/g" > /tmp/prompt.md
```

## Available Prompts

| File | Purpose | Variables |
|------|---------|-----------|
| `generate-implementation.md` | Initial code generation | LIBRARY, SPEC_ID, ATTEMPT, MAIN_ISSUE_NUMBER, SUB_ISSUE_NUMBER, PREVIOUS_ATTEMPTS_CONTEXT |
| `improve-from-feedback.md` | Code improvement after rejection | LIBRARY, SPEC_ID, ATTEMPT, PLOT_FILE, CURRENT_CODE, SPEC_CONTENT, LIBRARY_RULES, ALL_ATTEMPTS, LATEST_FEEDBACK |
| `ai-quality-review.md` | Quality evaluation | LIBRARY, SPEC_ID, ATTEMPT, PR_NUMBER, SUB_ISSUE_NUMBER |

## Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `${LIBRARY}` | Target library | `matplotlib` |
| `${SPEC_ID}` | Specification ID | `scatter-basic` |
| `${ATTEMPT}` | Current attempt number | `1`, `2`, `3` |
| `${PR_NUMBER}` | Pull request number | `42` |
| `${SUB_ISSUE_NUMBER}` | Library-specific sub-issue | `100` |
| `${MAIN_ISSUE_NUMBER}` | Parent issue number | `99` |
| `${PLOT_FILE}` | Path to implementation file | `plots/matplotlib/scatter/scatter-basic/default.py` |
| `${CURRENT_CODE}` | Current implementation code | Python source |
| `${SPEC_CONTENT}` | Spec file contents | Markdown |
| `${LIBRARY_RULES}` | Library-specific rules | Markdown |
| `${ALL_ATTEMPTS}` | Previous attempt history | Markdown |
| `${LATEST_FEEDBACK}` | Most recent AI feedback | Markdown |
| `${PREVIOUS_ATTEMPTS_CONTEXT}` | Context about previous attempts | String |

## Why External Prompts?

1. **Testability** - Prompts can be validated independently
2. **Consistency** - Same prompt used across runs
3. **Maintainability** - Single place to update instructions
4. **Version Control** - Git history tracks all changes
5. **Readability** - Workflows focus on flow, not content
