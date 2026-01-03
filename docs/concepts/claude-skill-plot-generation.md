# 🎨 Claude Skill: Plot Generation

## Overview

A **Claude Skill** is a specialized, reusable capability that can be invoked by Claude Code or other AI systems. This document proposes a comprehensive skill for automated plot generation that:

- Reads versioned rule files (Markdown)
- Generates implementation code from specs
- Performs self-review and optimization
- Handles multi-attempt feedback loops
- Integrates with the pyplots rule versioning system

## Why a Claude Skill?

### Problems with Ad-Hoc Prompting

❌ **Inconsistent**: Every generation uses slightly different prompts
❌ **Not reusable**: Have to explain the full process each time
❌ **Hard to improve**: Prompt changes lost in chat history
❌ **No versioning**: Can't track what prompts generated which plots
❌ **Manual orchestration**: Human has to manage the feedback loop

### Benefits of a Skill

✅ **Consistent**: Same process every time
✅ **Reusable**: Call the skill, get a plot
✅ **Versionable**: Skill linked to rule versions
✅ **Automated**: Handles feedback loops internally
✅ **Testable**: Can A/B test different skill versions
✅ **Scalable**: Easy to invoke from automation (GitHub Actions, n8n)

---

## Skill Architecture

### High-Level Flow

```
Input: Spec Markdown + Target Library + Rule Version
   ↓
┌──────────────────────────────────────────┐
│  Claude Skill: Plot Generation v1.0.0    │
│                                           │
│  1. Load Rules (from rules/{version}/)   │
│  2. Generate Code                         │
│  3. Self-Review                           │
│  4. Optimize if needed (max 3 attempts)  │
│  5. Return Result                         │
└──────────────────────────────────────────┘
   ↓
Output: Python Code + Metadata + Feedback
```

### Skill Interface

```python
# Conceptual API
from claude_skills import PlotGenerationSkill

skill = PlotGenerationSkill(
    rule_version="v1.0.0",  # Which rules to use
    max_attempts=3           # Maximum optimization loops
)

result = skill.generate(
    spec_markdown="specs/scatter-basic-001.md",
    library="matplotlib",
    variant="default"
)

# result.success → True/False
# result.code → Generated Python code
# result.quality_score → Self-review score
# result.attempt_count → How many tries it took
# result.feedback → Improvement suggestions
```

---

## Skill Inputs

### Required Inputs

```python
{
  "spec_markdown": "# scatter-basic-001: Basic 2D Scatter Plot\n\n...",
  "library": "matplotlib",  # or "seaborn", "plotly", etc.
  "variant": "default",     # or "ggplot_style", "dark_mode", etc.
}
```

### Optional Inputs

```python
{
  "rule_version": "v1.0.0",     # Default: latest active version
  "max_attempts": 3,             # Default: 3
  "strict_mode": False,          # If True, fail if any criterion not met
  "custom_criteria": [],         # Additional quality checks
  "python_version": "3.12",      # Target Python version
  "style_constraints": {         # Additional styling rules
    "color_palette": "colorblind_safe",
    "figure_size": (12, 8)
  }
}
```

---

## Skill Outputs

### Success Case

```python
{
  "success": True,
  "code": "import matplotlib.pyplot as plt\nimport pandas as pd\n\n...",
  "quality_score": 92,
  "attempt_count": 2,
  "criteria_met": [
    "axes_labeled",
    "grid_visible",
    "colorblind_safe"
  ],
  "criteria_failed": [],
  "feedback": {
    "attempt_1": {
      "score": 78,
      "issues": ["X-axis labels overlapping", "Grid too prominent"],
      "improvements": "Rotate labels, reduce grid alpha"
    },
    "attempt_2": {
      "score": 92,
      "issues": [],
      "improvements": "All criteria met, code optimized"
    }
  },
  "metadata": {
    "rule_version": "v1.0.0",
    "generation_time_seconds": 15.3,
    "library": "matplotlib",
    "variant": "default"
  }
}
```

### Failure Case

```python
{
  "success": False,
  "code": None,
  "quality_score": 71,  # Below threshold after 3 attempts
  "attempt_count": 3,
  "criteria_met": ["axes_labeled"],
  "criteria_failed": ["grid_visible", "colorblind_safe"],
  "feedback": {
    "attempt_1": {...},
    "attempt_2": {...},
    "attempt_3": {
      "score": 71,
      "issues": [
        "Colorblind safety check still failing",
        "Unable to find suitable palette that works with data"
      ],
      "recommendations": [
        "Consider using different visualization type",
        "May need manual refinement"
      ]
    }
  },
  "error": "Failed to meet quality threshold after 3 attempts"
}
```

---

## Internal Workflow

### Phase 1: Load Rules

```python
def load_rules(version: str) -> Rules:
    """
    Load generation rules from rules/generation/{version}/

    Returns:
    - code_generation_rules: How to generate code
    - quality_criteria: What makes a good plot
    - self_review_checklist: How to self-evaluate
    """
    base_path = f"rules/generation/{version}/"

    rules = Rules(
        generation=load_markdown(base_path + "code-generation-rules.md"),
        quality=load_markdown(base_path + "quality-criteria.md"),
        self_review=load_markdown(base_path + "self-review-checklist.md"),
        metadata=load_yaml(base_path + "metadata.yaml")
    )

    return rules
```

### Phase 2: Generate Initial Code

```python
def generate_initial_code(
    spec: str,
    library: str,
    rules: Rules
) -> str:
    """
    Generate first version of code based on spec and rules

    Process:
    1. Parse spec to extract requirements
    2. Follow generation rules for code structure
    3. Apply library-specific patterns
    4. Generate complete, executable code
    """
    prompt = f"""
You are generating a plot implementation.

# Spec
{spec}

# Target Library
{library}

# Generation Rules
{rules.generation}

# Task
Generate complete Python code that:
1. Implements the spec requirements
2. Follows all generation rules
3. Is ready to execute

Return only the Python code, no explanations.
"""

    code = call_claude(prompt)
    return code
```

### Phase 3: Self-Review

```python
def self_review(
    code: str,
    spec: str,
    rules: Rules
) -> SelfReviewResult:
    """
    Evaluate generated code against quality criteria

    Returns:
    - score: 0-100
    - issues: List of problems found
    - suggestions: How to improve
    """
    # Execute code to generate plot image
    image_bytes = execute_and_render(code)

    prompt = f"""
You are reviewing a generated plot implementation.

# Spec
{spec}

# Generated Code
```python
{code}
```

# Quality Criteria (from rules)
{rules.quality}

# Self-Review Checklist
{rules.self_review}

# Task
1. Execute the code mentally (or review the logic)
2. Check against each quality criterion
3. Provide a score (0-100) and detailed feedback

Return JSON:
{{
  "score": 0-100,
  "criteria_met": ["id1", "id2"],
  "criteria_failed": ["id3"],
  "issues": ["Issue 1", "Issue 2"],
  "suggestions": ["Suggestion 1", "Suggestion 2"]
}}
"""

    result = call_claude_with_image(prompt, image_bytes)
    return parse_json(result)
```

### Phase 4: Optimization Loop

```python
def optimize_code(
    code: str,
    review_result: SelfReviewResult,
    rules: Rules
) -> str:
    """
    Improve code based on self-review feedback

    Process:
    1. Identify specific issues
    2. Generate targeted fixes
    3. Apply fixes to code
    4. Return improved version
    """
    prompt = f"""
You are optimizing plot code based on review feedback.

# Current Code
```python
{code}
```

# Review Feedback
Score: {review_result.score}/100

Issues:
{'\n'.join(f"- {issue}" for issue in review_result.issues)}

Suggestions:
{'\n'.join(f"- {sug}" for sug in review_result.suggestions)}

# Quality Criteria (still need to meet)
{format_failed_criteria(review_result.criteria_failed, rules.quality)}

# Task
Generate improved code that addresses all issues.
Focus specifically on the failed criteria.

Return only the improved Python code, no explanations.
"""

    improved_code = call_claude(prompt)
    return improved_code
```

### Phase 5: Multi-Attempt Loop

```python
def generate_with_feedback_loop(
    spec: str,
    library: str,
    rules: Rules,
    max_attempts: int = 3,
    pass_threshold: int = 90
) -> GenerationResult:
    """
    Main generation loop with self-correction

    Returns after:
    - Score >= threshold (success)
    - max_attempts reached (failure)
    """
    feedback_history = []

    # Attempt 1: Initial generation
    code = generate_initial_code(spec, library, rules)
    review = self_review(code, spec, rules)
    feedback_history.append(review)

    attempt = 1

    # Attempts 2-3: Optimization loop
    while review.score < pass_threshold and attempt < max_attempts:
        attempt += 1

        code = optimize_code(code, review, rules)
        review = self_review(code, spec, rules)
        feedback_history.append(review)

    # Final result
    success = review.score >= pass_threshold

    return GenerationResult(
        success=success,
        code=code if success else None,
        quality_score=review.score,
        attempt_count=attempt,
        criteria_met=review.criteria_met,
        criteria_failed=review.criteria_failed,
        feedback=feedback_history
    )
```

---

## Skill Definition (Claude Code Format)

```yaml
# skills/plot-generation/skill.yaml
name: plot-generation
version: 1.0.0
description: Generate plot implementations from specifications with automated quality feedback

inputs:
  spec_markdown:
    type: string
    required: true
    description: Plot specification in Markdown format

  library:
    type: string
    required: true
    enum: [matplotlib, seaborn, plotly, bokeh, altair]

  variant:
    type: string
    required: false
    default: "default"

  rule_version:
    type: string
    required: false
    default: "latest"
    description: Which rule version to use (e.g., "v1.0.0")

  max_attempts:
    type: integer
    required: false
    default: 3
    min: 1
    max: 5

capabilities:
  - read_files: true        # Read spec and rule files
  - execute_code: true      # Execute generated code to render plots
  - vision: true            # Analyze generated plot images
  - iterative: true         # Multi-attempt optimization loop

outputs:
  success:
    type: boolean
    description: Whether generation succeeded

  code:
    type: string
    description: Generated Python code (null if failed)

  quality_score:
    type: integer
    description: Final quality score (0-100)

  attempt_count:
    type: integer
    description: Number of attempts needed

  feedback:
    type: object
    description: Detailed feedback from all attempts

workflow:
  - step: load_rules
    action: Read rule files from rules/generation/{rule_version}/

  - step: generate
    action: Create initial code based on spec and rules

  - step: review
    action: Self-evaluate code against quality criteria
    loop:
      max_iterations: ${max_attempts}
      continue_if: quality_score < 90
      next_step: optimize

  - step: optimize
    action: Improve code based on feedback
    next_step: review

  - step: finalize
    action: Return result with code and metadata
```

---

## Invocation Examples

### Example 1: Basic Invocation

```bash
# From command line (hypothetical)
claude-skill plot-generation \
  --spec specs/scatter-basic-001.md \
  --library matplotlib \
  --variant default \
  --output generated-plot.py
```

### Example 2: From Python

```python
# core/generators/claude_generator.py
from claude_skills import invoke_skill

result = invoke_skill(
    skill="plot-generation",
    inputs={
        "spec_markdown": Path("specs/scatter-basic-001.md").read_text(),
        "library": "matplotlib",
        "variant": "default",
        "rule_version": "v1.0.0"
    }
)

if result.success:
    # Save generated code
    Path("plots/matplotlib/scatter/scatter-basic-001/default.py").write_text(result.code)

    # Record metadata
    save_metadata(
        spec_id="scatter-basic-001",
        quality_score=result.quality_score,
        attempt_count=result.attempt_count,
        rule_version="v1.0.0"
    )
else:
    # Log failure
    log_failure(
        spec_id="scatter-basic-001",
        reason=result.error,
        feedback=result.feedback
    )
```

### Example 3: From GitHub Actions

```yaml
# .github/workflows/generate-plot.yml
- name: Generate plot implementation
  id: generate
  run: |
    claude-skill plot-generation \
      --spec ${{ env.SPEC_FILE }} \
      --library ${{ matrix.library }} \
      --rule-version v1.0.0 \
      --output generated.py \
      --json-output result.json

- name: Check if successful
  run: |
    SUCCESS=$(jq -r '.success' result.json)
    SCORE=$(jq -r '.quality_score' result.json)

    if [ "$SUCCESS" = "true" ]; then
      echo "✓ Generation successful (score: $SCORE)"
    else
      echo "✗ Generation failed"
      exit 1
    fi
```

### Example 4: A/B Testing with Different Rule Versions

```python
# automation/testing/ab_with_skills.py
from claude_skills import invoke_skill

def compare_rule_versions(spec_id: str, versions: list[str]):
    """
    Generate plot with multiple rule versions and compare
    """
    results = {}

    for version in versions:
        result = invoke_skill(
            skill="plot-generation",
            inputs={
                "spec_markdown": load_spec(spec_id),
                "library": "matplotlib",
                "rule_version": version
            }
        )

        results[version] = {
            "success": result.success,
            "quality_score": result.quality_score,
            "attempt_count": result.attempt_count,
            "code": result.code
        }

    # Compare results
    return generate_comparison_report(results)

# Usage
report = compare_rule_versions(
    spec_id="scatter-basic-001",
    versions=["v1.0.0", "v2.0.0"]
)
```

---

## Advanced Features

### Feature 1: Custom Quality Criteria

```python
# Add project-specific criteria
result = invoke_skill(
    skill="plot-generation",
    inputs={
        "spec_markdown": spec,
        "library": "matplotlib",
        "custom_criteria": [
            {
                "id": "brand_colors",
                "requirement": "Use company brand colors only",
                "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
                "weight": 1.0
            },
            {
                "id": "max_figure_width",
                "requirement": "Figure width must not exceed 10 inches",
                "max_width": 10,
                "weight": 0.5
            }
        ]
    }
)
```

### Feature 2: Style Templates

```python
# Use predefined style templates
result = invoke_skill(
    skill="plot-generation",
    inputs={
        "spec_markdown": spec,
        "library": "matplotlib",
        "style_template": "academic_paper",  # or "presentation", "web", etc.
        "style_overrides": {
            "font_family": "Arial",
            "font_size": 12
        }
    }
)
```

### Feature 3: Multi-Library Generation

```python
# Generate for all suitable libraries in one call
result = invoke_skill(
    skill="plot-generation",
    inputs={
        "spec_markdown": spec,
        "library": "all",  # Special value: generate for all suitable libraries
        "rule_version": "v1.0.0"
    }
)

# Result contains implementations for multiple libraries
# result.implementations = {
#     "matplotlib": {...},
#     "seaborn": {...},
#     "plotly": {...}
# }
```

### Feature 4: Incremental Refinement

```python
# Start with a draft, refine iteratively
draft_result = invoke_skill(
    skill="plot-generation",
    inputs={
        "spec_markdown": spec,
        "library": "matplotlib",
        "strict_mode": False,  # Allow lower quality for draft
        "max_attempts": 1       # Quick draft
    }
)

# Review and refine
final_result = invoke_skill(
    skill="plot-generation",
    inputs={
        "spec_markdown": spec,
        "library": "matplotlib",
        "initial_code": draft_result.code,  # Start from draft
        "feedback": "Improve colorblind safety and font sizes",
        "strict_mode": True,
        "max_attempts": 3
    }
)
```

---

## Integration with Rule Versioning

### Linking Skills to Rules

```yaml
# skills/plot-generation/versions.yaml
skill_versions:
  - version: "1.0.0"
    compatible_rule_versions:
      generation: ["v1.0.0", "v1.1.0"]
      evaluation: ["v1.0.0"]
    status: "active"

  - version: "1.1.0"
    compatible_rule_versions:
      generation: ["v2.0.0", "v2.1.0"]
      evaluation: ["v2.0.0"]
    status: "active"
```

### Automatic Rule Selection

```python
# Skill automatically selects appropriate rules
result = invoke_skill(
    skill="plot-generation",
    skill_version="1.1.0",  # Skill version
    inputs={
        "spec_markdown": spec,
        "library": "matplotlib",
        # rule_version not specified → use latest compatible
    }
)

# Skill uses:
# - Skill logic version 1.1.0
# - Latest compatible generation rules (v2.1.0)
# - Latest compatible evaluation rules (v2.0.0)
```

---

## Performance Optimization

### Caching

```python
# Cache generated code to avoid regeneration
result = invoke_skill(
    skill="plot-generation",
    inputs={
        "spec_markdown": spec,
        "library": "matplotlib",
        "rule_version": "v1.0.0"
    },
    cache_key=f"{spec_hash}:{library}:v1.0.0"
)

# If cache hit: return cached result (instant)
# If cache miss: generate and cache (15-30 seconds)
```

### Parallel Generation

```python
# Generate for multiple libraries in parallel
from concurrent.futures import ThreadPoolExecutor

libraries = ["matplotlib", "seaborn", "plotly"]

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(
            invoke_skill,
            skill="plot-generation",
            inputs={"spec_markdown": spec, "library": lib}
        )
        for lib in libraries
    ]

    results = {lib: future.result() for lib, future in zip(libraries, futures)}
```

---

## Error Handling

### Graceful Degradation

```python
try:
    result = invoke_skill(
        skill="plot-generation",
        inputs={...},
        timeout_seconds=60  # Don't wait forever
    )

    if result.success:
        # Use generated code
        save_code(result.code)
    else:
        # Fall back to template or manual generation
        log_failure(result.feedback)
        use_fallback_template()

except TimeoutError:
    # Skill took too long
    log_error("Generation timeout")
    use_fallback_template()

except SkillError as e:
    # Skill crashed or invalid input
    log_error(f"Skill error: {e}")
    use_fallback_template()
```

### Retry Logic

```python
# Retry with exponential backoff
def generate_with_retry(spec, library, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = invoke_skill(...)

            if result.success:
                return result
            elif result.quality_score > 75:
                # Close enough, acceptable
                return result
            else:
                # Try again with more attempts
                continue

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 1s, 2s, 4s
                continue
            else:
                raise
```

---

## Monitoring & Telemetry

### Metrics to Track

```python
{
  "skill_invocations": {
    "total": 1234,
    "successful": 1180,
    "failed": 54,
    "success_rate": 0.956
  },

  "performance": {
    "avg_generation_time_seconds": 18.3,
    "p50": 15.2,
    "p95": 35.7,
    "p99": 48.1
  },

  "quality": {
    "avg_quality_score": 89.2,
    "avg_attempts_to_pass": 1.7,
    "first_attempt_success_rate": 0.68
  },

  "by_rule_version": {
    "v1.0.0": {
      "invocations": 523,
      "avg_quality_score": 87.1
    },
    "v2.0.0": {
      "invocations": 711,
      "avg_quality_score": 91.3
    }
  }
}
```

---

## Future Enhancements

### 1. Learning from Feedback

```python
# Skill learns which strategies work best
skill.train(
    successful_generations=database.get_successful_generations(),
    failed_generations=database.get_failed_generations()
)

# Improves:
# - Which libraries work best for which plot types
# - Common pitfalls to avoid
# - Optimization strategies
```

### 2. Multi-Modal Input

```python
# Generate plot from image + description
result = invoke_skill(
    skill="plot-generation",
    inputs={
        "reference_image": "path/to/example.png",  # What they want
        "description": "Like this but for time series data",
        "library": "matplotlib"
    }
)
```

### 3. Interactive Refinement

```python
# User provides feedback, skill refines
result1 = invoke_skill(...)  # First version

user_feedback = "The legend is too large and covers data"

result2 = invoke_skill(
    inputs={
        "initial_code": result1.code,
        "user_feedback": user_feedback,
        "refine_only": ["legend"]  # Only change legend
    }
)
```

---

## Summary

### Skill Benefits

✅ **Consistent quality** through versioned rules
✅ **Automated feedback loops** reduce manual work
✅ **Testable** via A/B testing of rule versions
✅ **Scalable** from CLI to full automation
✅ **Auditable** - know exactly what generated each plot

### Next Steps

1. **Define initial ruleset** (v1.0.0-draft)
2. **Prototype skill logic** (Python script)
3. **Test with 5-10 specs** manually
4. **Refine based on results**
5. **Formalize as Claude Skill** (if system supports)
6. **Integrate with automation** (GitHub Actions, n8n)

---

## Related Documentation

- [Rule Versioning System](../architecture/rule-versioning.md)
- [A/B Testing Rules](./ab-testing-rules.md)
- [Automation Workflows](../architecture/automation-workflows.md)

---

*"A skill is a reusable unit of AI capability. Make it good, make it versioned, make it testable."*
