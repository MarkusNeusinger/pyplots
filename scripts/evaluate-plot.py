#!/usr/bin/env python3
"""
Local Plot Quality Evaluator

Evaluates a plot implementation using AI quality review criteria.
This simulates the AI review process used in the impl-review.yml workflow.

Usage:
    # Evaluate a specific implementation
    python scripts/evaluate-plot.py scatter-basic matplotlib

    # Evaluate with verbose output
    python scripts/evaluate-plot.py scatter-basic seaborn --verbose

    # Evaluate all libraries for a spec
    python scripts/evaluate-plot.py scatter-basic --all

    # Generate the plot image before evaluating
    python scripts/evaluate-plot.py scatter-basic matplotlib --generate

Requirements:
    - Claude API key set in ANTHROPIC_API_KEY environment variable
    - OR Claude Code OAuth token for local testing
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


SUPPORTED_LIBRARIES = [
    "matplotlib",
    "seaborn",
    "plotly",
    "bokeh",
    "altair",
    "plotnine",
    "pygal",
    "highcharts",
    "letsplot",
]


def get_plot_paths(spec_id: str, library: str) -> dict:
    """Get all relevant paths for a plot implementation."""
    plots_dir = PROJECT_ROOT / "plots" / spec_id
    return {
        "spec": plots_dir / "specification.md",
        "impl": plots_dir / "implementations" / f"{library}.py",
        "metadata": plots_dir / "metadata" / f"{library}.yaml",
        "image": plots_dir / "implementations" / "plot.png",
        "library_rules": PROJECT_ROOT / "prompts" / "library" / f"{library}.md",
        "quality_criteria": PROJECT_ROOT / "prompts" / "quality-criteria-v2.md",
        "quality_criteria_old": PROJECT_ROOT / "prompts" / "quality-criteria.md",
    }


def check_files_exist(paths: dict) -> list[str]:
    """Check which required files exist."""
    missing = []
    for name, path in paths.items():
        if name in ["spec", "impl", "library_rules"]:  # Required files
            if not path.exists():
                missing.append(f"{name}: {path}")
    return missing


def generate_plot(spec_id: str, library: str) -> bool:
    """Generate the plot image by running the implementation."""
    paths = get_plot_paths(spec_id, library)
    impl_path = paths["impl"]

    if not impl_path.exists():
        print(f"Error: Implementation not found: {impl_path}")
        return False

    # Run the implementation
    impl_dir = impl_path.parent
    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"  # Non-interactive backend

    try:
        result = subprocess.run(
            [sys.executable, str(impl_path)],
            cwd=str(impl_dir),
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            print(f"Error running implementation:")
            print(result.stderr)
            return False

        # Check if plot.png was created
        plot_path = impl_dir / "plot.png"
        if plot_path.exists():
            print(f"Generated: {plot_path}")
            return True
        else:
            print("Warning: plot.png was not created")
            return False

    except subprocess.TimeoutExpired:
        print("Error: Implementation timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def analyze_library_usage(impl_path: Path, library: str) -> dict:
    """Analyze how much the implementation actually uses the designated library."""
    with open(impl_path) as f:
        code = f.read()

    # Library-specific patterns
    library_patterns = {
        "seaborn": {
            "import": ["import seaborn", "from seaborn"],
            "plot_functions": [
                "sns.scatterplot", "sns.lineplot", "sns.barplot", "sns.histplot",
                "sns.boxplot", "sns.violinplot", "sns.heatmap", "sns.pairplot",
                "sns.relplot", "sns.catplot", "sns.displot", "sns.jointplot",
                "sns.regplot", "sns.lmplot", "sns.countplot", "sns.kdeplot",
                "sns.stripplot", "sns.swarmplot", "sns.pointplot", "sns.rugplot",
            ],
            "style_only": ["sns.set_style", "sns.set_theme", "sns.set_context", "sns.set_palette"],
        },
        "plotly": {
            "import": ["import plotly", "from plotly"],
            "plot_functions": [
                "px.scatter", "px.line", "px.bar", "px.histogram", "px.box",
                "px.violin", "px.pie", "px.sunburst", "px.treemap", "px.funnel",
                "go.Figure", "go.Scatter", "go.Bar", "go.Heatmap", "go.Pie",
            ],
            "style_only": ["update_layout", "update_traces"],
        },
        "bokeh": {
            "import": ["from bokeh", "import bokeh"],
            "plot_functions": [
                "figure(", ".scatter(", ".line(", ".circle(", ".square(",
                ".triangle(", ".vbar(", ".hbar(", ".rect(", ".segment(",
            ],
            "style_only": [],
        },
        "altair": {
            "import": ["import altair", "from altair"],
            "plot_functions": [
                "alt.Chart", ".mark_point", ".mark_line", ".mark_bar", ".mark_circle",
                ".mark_square", ".mark_rect", ".mark_area", ".mark_boxplot",
            ],
            "style_only": [".configure_"],
        },
        "plotnine": {
            "import": ["from plotnine", "import plotnine"],
            "plot_functions": [
                "ggplot(", "geom_point", "geom_line", "geom_bar", "geom_histogram",
                "geom_boxplot", "geom_violin", "geom_area", "geom_tile",
            ],
            "style_only": ["theme(", "theme_"],
        },
        "pygal": {
            "import": ["import pygal", "from pygal"],
            "plot_functions": [
                "pygal.Bar", "pygal.Line", "pygal.Pie", "pygal.Histogram",
                "pygal.XY", "pygal.Dot", "pygal.Radar", "pygal.Box",
            ],
            "style_only": [],
        },
        "highcharts": {
            "import": ["from highcharts", "import highcharts"],
            "plot_functions": [
                "Chart(", "Highcharts", "series", "highcharts.Chart",
            ],
            "style_only": [],
        },
        "letsplot": {
            "import": ["from lets_plot", "import lets_plot"],
            "plot_functions": [
                "ggplot(", "geom_point", "geom_line", "geom_bar", "geom_histogram",
                "geom_boxplot", "geom_violin", "geom_area", "geom_tile",
            ],
            "style_only": ["theme(", "ggsize("],
        },
        "matplotlib": {
            "import": ["import matplotlib", "from matplotlib"],
            "plot_functions": [
                "ax.scatter", "ax.plot", "ax.bar", "ax.hist", "ax.boxplot",
                "plt.scatter", "plt.plot", "plt.bar", "plt.hist", "plt.boxplot",
                "ax.imshow", "ax.contour", "ax.pie", "ax.fill_between",
            ],
            "style_only": [],
        },
    }

    if library not in library_patterns:
        return {"error": f"Unknown library: {library}"}

    patterns = library_patterns[library]

    # Check imports
    has_import = any(p in code for p in patterns["import"])

    # Check plot function usage
    plot_functions_used = [p for p in patterns["plot_functions"] if p in code]

    # Check style-only usage
    style_only_used = [p for p in patterns["style_only"] if p in code]

    # Determine authenticity score
    if not has_import:
        la01_score = 0
        la01_reason = f"No {library} import found"
    elif plot_functions_used:
        la01_score = 12
        la01_reason = f"Uses library plotting: {', '.join(plot_functions_used[:3])}"
    elif style_only_used and not plot_functions_used:
        la01_score = 0
        la01_reason = f"Only uses styling functions: {', '.join(style_only_used)}"
    else:
        la01_score = 0
        la01_reason = "Library imported but no plotting functions used"

    return {
        "has_import": has_import,
        "plot_functions": plot_functions_used,
        "style_only": style_only_used,
        "la01_score": la01_score,
        "la01_reason": la01_reason,
    }


def analyze_visual_issues(impl_path: Path) -> dict:
    """Analyze potential visual issues in the code."""
    with open(impl_path) as f:
        code = f.read()

    issues = []

    # Check for font sizes
    import re

    # Look for fontsize settings
    fontsize_matches = re.findall(r'fontsize\s*=\s*(\d+)', code)
    fontsizes = [int(fs) for fs in fontsize_matches]

    if fontsizes:
        min_fontsize = min(fontsizes)
        if min_fontsize < 12:
            issues.append(f"Font sizes may be too small (min: {min_fontsize}pt)")

    # Check for marker size in scatter plots
    if 'scatter' in code.lower():
        s_matches = re.findall(r'\bs\s*=\s*(\d+)', code)
        if s_matches:
            sizes = [int(s) for s in s_matches]
            if max(sizes) < 50:
                issues.append(f"Marker sizes may be too small (s={max(sizes)})")

    # Check for missing tight_layout
    if 'tight_layout' not in code and 'bbox_inches' not in code:
        issues.append("Missing tight_layout() or bbox_inches='tight'")

    # Check for overlapping label prevention
    if 'rotation' not in code and 'set_xticklabels' in code:
        issues.append("X-axis labels might overlap (no rotation set)")

    return {
        "issues": issues,
        "fontsizes": fontsizes,
    }


def create_evaluation_prompt(spec_id: str, library: str, paths: dict) -> str:
    """Create the evaluation prompt for Claude."""

    # Read files
    spec_content = paths["spec"].read_text() if paths["spec"].exists() else "NOT FOUND"
    impl_content = paths["impl"].read_text() if paths["impl"].exists() else "NOT FOUND"

    # Use v2 criteria if available, fall back to v1
    criteria_path = paths["quality_criteria"]
    if not criteria_path.exists():
        criteria_path = paths["quality_criteria_old"]
    criteria_content = criteria_path.read_text() if criteria_path.exists() else "NOT FOUND"

    library_rules = paths["library_rules"].read_text() if paths["library_rules"].exists() else ""

    prompt = f"""## Task: Evaluate Plot Quality

You are evaluating a **{library}** implementation of the **{spec_id}** plot specification.

### 1. Specification
```markdown
{spec_content}
```

### 2. Implementation Code ({library}.py)
```python
{impl_content}
```

### 3. Library-Specific Rules
```markdown
{library_rules}
```

### 4. Quality Criteria
```markdown
{criteria_content}
```

### 5. Your Task

Evaluate this implementation against the quality criteria. Pay special attention to:

1. **Library Authenticity (LA-01)**: Does the code actually use {library}'s plotting functions, or just import it for styling?
2. **Visual Quality**: Check font sizes, marker sizes, potential overlapping labels
3. **Spec Compliance**: Does it match what the specification requires?

Provide a detailed evaluation in this format:

```json
{{
  "score": <0-100>,
  "tier": "<Excellent|Good|Acceptable|Poor>",

  "library_authenticity": {{
    "la01_score": <0-12>,
    "la01_reason": "...",
    "la02_score": <0-5>,
    "la02_reason": "...",
    "la03_score": <0-3>,
    "la03_reason": "..."
  }},

  "spec_compliance": {{
    "total": <0-25>,
    "issues": ["..."]
  }},

  "visual_quality": {{
    "total": <0-30>,
    "issues": ["..."]
  }},

  "data_quality": {{
    "total": <0-15>,
    "issues": ["..."]
  }},

  "code_quality": {{
    "total": <0-10>,
    "issues": ["..."]
  }},

  "strengths": ["..."],
  "weaknesses": ["..."],
  "improvements": ["..."],

  "verdict": "<APPROVED|NEEDS_IMPROVEMENT|REJECTED>",
  "summary": "One paragraph summary"
}}
```

Be strict about Library Authenticity - if the code doesn't actually use {library} for plotting, LA-01 should be 0.
"""

    return prompt


def evaluate_with_claude(prompt: str, image_path: Path | None = None) -> dict:
    """Send the evaluation prompt to Claude API."""
    try:
        import anthropic
    except ImportError:
        print("Error: anthropic package not installed")
        print("Run: pip install anthropic")
        return {"error": "anthropic package not installed"}

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        print("Set your API key: export ANTHROPIC_API_KEY='your-key'")
        return {"error": "ANTHROPIC_API_KEY not set"}

    client = anthropic.Anthropic(api_key=api_key)

    messages = []
    content = [{"type": "text", "text": prompt}]

    # Add image if available
    if image_path and image_path.exists():
        import base64
        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")

        content.insert(0, {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": image_data,
            }
        })
        content.insert(1, {"type": "text", "text": "Here is the generated plot image to evaluate:"})

    messages.append({"role": "user", "content": content})

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=messages,
        )

        response_text = response.content[0].text

        # Try to extract JSON from response
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        return {"raw_response": response_text}

    except Exception as e:
        return {"error": str(e)}


def print_evaluation(result: dict, verbose: bool = False):
    """Pretty print the evaluation result."""
    if "error" in result:
        print(f"\nError: {result['error']}")
        return

    if "raw_response" in result:
        print("\nRaw Response (could not parse JSON):")
        print(result["raw_response"])
        return

    print("\n" + "="*60)
    print(f"QUALITY SCORE: {result.get('score', 'N/A')}/100")
    print(f"TIER: {result.get('tier', 'N/A')}")
    print(f"VERDICT: {result.get('verdict', 'N/A')}")
    print("="*60)

    # Library Authenticity
    la = result.get("library_authenticity", {})
    la_total = la.get("la01_score", 0) + la.get("la02_score", 0) + la.get("la03_score", 0)
    print(f"\nLibrary Authenticity: {la_total}/20")
    print(f"  LA-01 ({la.get('la01_score', 0)}/12): {la.get('la01_reason', 'N/A')}")
    if verbose:
        print(f"  LA-02 ({la.get('la02_score', 0)}/5): {la.get('la02_reason', 'N/A')}")
        print(f"  LA-03 ({la.get('la03_score', 0)}/3): {la.get('la03_reason', 'N/A')}")

    # Other sections
    print(f"\nSpec Compliance: {result.get('spec_compliance', {}).get('total', 'N/A')}/25")
    print(f"Visual Quality: {result.get('visual_quality', {}).get('total', 'N/A')}/30")
    print(f"Data Quality: {result.get('data_quality', {}).get('total', 'N/A')}/15")
    print(f"Code Quality: {result.get('code_quality', {}).get('total', 'N/A')}/10")

    # Strengths and Weaknesses
    if result.get("strengths"):
        print("\nStrengths:")
        for s in result["strengths"]:
            print(f"  + {s}")

    if result.get("weaknesses"):
        print("\nWeaknesses:")
        for w in result["weaknesses"]:
            print(f"  - {w}")

    if result.get("improvements"):
        print("\nSuggested Improvements:")
        for i in result["improvements"]:
            print(f"  > {i}")

    print(f"\nSummary: {result.get('summary', 'N/A')}")


def quick_check(spec_id: str, library: str) -> dict:
    """Quick local check without calling Claude API."""
    paths = get_plot_paths(spec_id, library)

    # Check files exist
    missing = check_files_exist(paths)
    if missing:
        return {"error": f"Missing files: {missing}"}

    # Analyze library usage
    lib_analysis = analyze_library_usage(paths["impl"], library)

    # Analyze visual issues
    visual_analysis = analyze_visual_issues(paths["impl"])

    return {
        "spec_id": spec_id,
        "library": library,
        "library_analysis": lib_analysis,
        "visual_analysis": visual_analysis,
        "files_exist": {k: v.exists() for k, v in paths.items()},
    }


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate plot implementation quality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/evaluate-plot.py scatter-basic matplotlib
  python scripts/evaluate-plot.py scatter-basic seaborn --verbose
  python scripts/evaluate-plot.py sudoku-basic seaborn --quick
  python scripts/evaluate-plot.py scatter-basic --all --quick
        """
    )
    parser.add_argument("spec_id", help="Specification ID (e.g., scatter-basic)")
    parser.add_argument("library", nargs="?", help="Library name (e.g., matplotlib)")
    parser.add_argument("--all", action="store_true", help="Evaluate all libraries")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--quick", "-q", action="store_true",
                       help="Quick local check without AI (no API call)")
    parser.add_argument("--generate", "-g", action="store_true",
                       help="Generate plot image before evaluation")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.all:
        libraries = SUPPORTED_LIBRARIES
    elif args.library:
        libraries = [args.library]
    else:
        parser.error("Must specify a library or use --all")

    results = {}

    for library in libraries:
        print(f"\n{'='*60}")
        print(f"Evaluating: {args.spec_id} / {library}")
        print("="*60)

        paths = get_plot_paths(args.spec_id, library)

        # Check if implementation exists
        if not paths["impl"].exists():
            print(f"Skipping: {library} implementation not found")
            continue

        # Generate plot if requested
        if args.generate:
            print("\nGenerating plot...")
            if not generate_plot(args.spec_id, library):
                print("Failed to generate plot, continuing with evaluation...")

        if args.quick:
            # Quick local check
            result = quick_check(args.spec_id, library)
            results[library] = result

            if args.json:
                continue

            print(f"\nLibrary Analysis:")
            lib_a = result.get("library_analysis", {})
            print(f"  LA-01 Score: {lib_a.get('la01_score', 'N/A')}/12")
            print(f"  Reason: {lib_a.get('la01_reason', 'N/A')}")
            print(f"  Plot functions used: {lib_a.get('plot_functions', [])}")
            print(f"  Style-only functions: {lib_a.get('style_only', [])}")

            print(f"\nVisual Analysis:")
            vis_a = result.get("visual_analysis", {})
            for issue in vis_a.get("issues", []):
                print(f"  ! {issue}")
            if vis_a.get("fontsizes"):
                print(f"  Font sizes found: {vis_a.get('fontsizes')}")
        else:
            # Full AI evaluation
            prompt = create_evaluation_prompt(args.spec_id, library, paths)

            # Check for image
            image_path = paths["image"]
            if not image_path.exists():
                # Try generating
                if args.generate or input("No plot.png found. Generate it? [y/N] ").lower() == 'y':
                    generate_plot(args.spec_id, library)

            print("\nSending to Claude for evaluation...")
            result = evaluate_with_claude(
                prompt,
                image_path if image_path.exists() else None
            )
            results[library] = result

            if not args.json:
                print_evaluation(result, verbose=args.verbose)

    if args.json:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
