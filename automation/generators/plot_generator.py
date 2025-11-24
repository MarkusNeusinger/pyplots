#!/usr/bin/env python3
"""
Plot Code Generator

Generates plot implementations from specifications using Claude with versioned rules.
"""

import os
import sys
from pathlib import Path
from typing import Literal
import anthropic


LibraryType = Literal["matplotlib", "seaborn", "plotly", "bokeh", "altair"]


def load_spec(spec_id: str) -> str:
    """Load specification from specs/ directory"""
    spec_path = Path(f"specs/{spec_id}.md")
    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path}")
    return spec_path.read_text()


def load_generation_rules(version: str = "v1.0.0-draft") -> str:
    """Load code generation rules"""
    rules_path = Path(f"rules/generation/{version}/code-generation-rules.md")
    if not rules_path.exists():
        raise FileNotFoundError(f"Rules not found: {rules_path}")
    return rules_path.read_text()


def load_quality_criteria(version: str = "v1.0.0-draft") -> str:
    """Load quality criteria for self-review"""
    criteria_path = Path(f"rules/generation/{version}/quality-criteria.md")
    if not criteria_path.exists():
        raise FileNotFoundError(f"Quality criteria not found: {criteria_path}")
    return criteria_path.read_text()


def load_self_review_checklist(version: str = "v1.0.0-draft") -> str:
    """Load self-review checklist"""
    checklist_path = Path(f"rules/generation/{version}/self-review-checklist.md")
    if not checklist_path.exists():
        raise FileNotFoundError(f"Self-review checklist not found: {checklist_path}")
    return checklist_path.read_text()


def generate_code(
    spec_id: str,
    library: LibraryType,
    variant: str = "default",
    rules_version: str = "v1.0.0-draft",
    max_attempts: int = 3
) -> dict:
    """
    Generate plot implementation code using Claude

    Args:
        spec_id: Specification ID (e.g., "scatter-basic-001")
        library: Target library (matplotlib, seaborn, etc.)
        variant: Implementation variant (default, style variant, etc.)
        rules_version: Version of generation rules to use
        max_attempts: Maximum number of self-review attempts

    Returns:
        dict with 'code', 'file_path', 'attempt_count', 'passed_review'
    """
    # Load inputs
    spec_content = load_spec(spec_id)
    generation_rules = load_generation_rules(rules_version)
    quality_criteria = load_quality_criteria(rules_version)
    self_review = load_self_review_checklist(rules_version)

    # Initialize Claude
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    # Determine output path
    # Format: plots/{library}/{plot_type}/{spec_id}/{variant}.py
    spec_type = spec_id.split('-')[0]  # e.g., "scatter" from "scatter-basic-001"

    # Library-specific plot type mapping
    plot_type_map = {
        "matplotlib": {"scatter": "scatter", "bar": "bar", "line": "line", "heatmap": "imshow"},
        "seaborn": {"scatter": "scatterplot", "bar": "barplot", "line": "lineplot", "heatmap": "heatmap"},
        "plotly": {"scatter": "scatter", "bar": "bar", "line": "line", "heatmap": "heatmap"},
    }

    plot_type = plot_type_map.get(library, {}).get(spec_type, spec_type)
    file_path = Path(f"plots/{library}/{plot_type}/{spec_id}/{variant}.py")

    # Self-review loop
    for attempt in range(1, max_attempts + 1):
        print(f"🔄 Attempt {attempt}/{max_attempts} for {spec_id}/{library}/{variant}")

        # Build prompt
        if attempt == 1:
            prompt = f"""You are an expert Python data visualization developer.

# Task
Generate a production-ready implementation of this plot specification for {library}.

# Specification
{spec_content}

# Generation Rules (Version: {rules_version})
{generation_rules}

# Quality Criteria
{quality_criteria}

# Requirements
1. Follow the generation rules exactly
2. Implement all data requirements and optional parameters from the spec
3. Meet all quality criteria listed in the spec
4. Use type hints (Python 3.10+ syntax)
5. Include comprehensive docstring
6. Add input validation
7. Make the code deterministic (use fixed random seeds if needed)
8. Add a standalone execution block for testing

# Output Format
Provide ONLY the Python code, no explanations. The code should be production-ready.

# Target
- Library: {library}
- Variant: {variant}
- Python: 3.10+
- File: {file_path}

Generate the implementation now:"""
        else:
            # For subsequent attempts, include the previous code and ask for improvements
            prompt = f"""Your previous implementation needs improvements. Please revise based on the feedback below.

# Previous Code
```python
{code}
```

# Self-Review Feedback
{review_feedback}

# Requirements
1. Fix all issues identified in the feedback
2. Ensure all quality criteria are met
3. Maintain the same structure and function signature

Generate the improved implementation:"""

        # Call Claude
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        code = response.content[0].text

        # Extract code if wrapped in markdown
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].split("```")[0].strip()

        # Self-review
        print(f"🔍 Running self-review...")
        review_prompt = f"""Review this generated plot implementation against the specification and quality criteria.

# Specification
{spec_content}

# Generated Code
```python
{code}
```

# Self-Review Checklist
{self_review}

# Task
Go through the self-review checklist and verify each item. For each item, respond with:
- ✅ PASS: [brief reason]
- ❌ FAIL: [specific issue and how to fix]

After reviewing all items, provide:
- Overall verdict: PASS or FAIL
- If FAIL: Specific improvements needed

Format your response as:
## Review Results
[checklist items with ✅/❌]

## Verdict
[PASS or FAIL]

## Improvements Needed (if FAIL)
[specific actionable items]
"""

        review_response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": review_prompt}]
        )

        review_feedback = review_response.content[0].text

        # Check if passed
        if "## Verdict\nPASS" in review_feedback or "Verdict: PASS" in review_feedback:
            print(f"✅ Self-review passed on attempt {attempt}")
            return {
                "code": code,
                "file_path": str(file_path),
                "attempt_count": attempt,
                "passed_review": True,
                "review_feedback": review_feedback
            }
        else:
            print(f"❌ Self-review failed on attempt {attempt}")
            if attempt < max_attempts:
                print(f"🔄 Regenerating with feedback...")
            else:
                print(f"⚠️ Max attempts reached. Returning best effort code.")

    # Max attempts reached without passing
    return {
        "code": code,
        "file_path": str(file_path),
        "attempt_count": max_attempts,
        "passed_review": False,
        "review_feedback": review_feedback
    }


def save_implementation(result: dict) -> Path:
    """Save generated code to file"""
    file_path = Path(result["file_path"])
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(result["code"])
    print(f"💾 Saved to: {file_path}")
    return file_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate plot implementation from spec")
    parser.add_argument("spec_id", help="Specification ID (e.g., scatter-basic-001)")
    parser.add_argument("library", choices=["matplotlib", "seaborn", "plotly", "bokeh", "altair"],
                        help="Target library")
    parser.add_argument("--variant", default="default", help="Variant name (default: default)")
    parser.add_argument("--rules-version", default="v1.0.0-draft", help="Rules version")
    parser.add_argument("--max-attempts", type=int, default=3, help="Max self-review attempts")

    args = parser.parse_args()

    try:
        result = generate_code(
            spec_id=args.spec_id,
            library=args.library,
            variant=args.variant,
            rules_version=args.rules_version,
            max_attempts=args.max_attempts
        )

        # Save code
        file_path = save_implementation(result)

        # Print summary
        print("\n" + "="*60)
        print(f"✅ Generation complete!")
        print(f"   Spec: {args.spec_id}")
        print(f"   Library: {args.library}")
        print(f"   Variant: {args.variant}")
        print(f"   File: {file_path}")
        print(f"   Attempts: {result['attempt_count']}")
        print(f"   Review: {'✅ PASSED' if result['passed_review'] else '❌ FAILED'}")
        print("="*60)

        # Exit with appropriate code
        sys.exit(0 if result['passed_review'] else 1)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
