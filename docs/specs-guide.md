# 📝 Plot Specification Guide

## Overview

Plot specifications are **library-agnostic descriptions** of what a plot should do, written in Markdown. They serve as the contract between what users want and what AI generates.

**Key Principle**: A spec describes the **what**, not the **how**. Implementations handle library-specific details.

---

## Spec File Format

### Location
All specs live in `specs/` directory:
```
specs/
├── scatter-basic-001.md
├── heatmap-corr-002.md
└── bar-grouped-004.md
```

### Naming Convention
Format: `{type}-{variant}-{number}.md`

**Examples**:
- `scatter-basic-001.md` - Basic scatter plot
- `scatter-advanced-005.md` - Advanced scatter with features
- `heatmap-corr-002.md` - Correlation heatmap
- `bar-grouped-004.md` - Grouped bar chart

**Rules**:
- Lowercase only
- Hyphens as separators
- Three-digit number (001-999)
- Descriptive type and variant names

---

## Spec Template

```markdown
# {spec-id}: {Title}

## Description

{2-3 sentences describing what this plot does and when to use it}

## Data Requirements

- **{param_name}**: {Description of required data}
- **{param_name}**: {Description of required data}

## Optional Parameters

- `{param}`: {Description} (default: {value})
- `{param}`: {Description}

## Quality Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}
- [ ] {Criterion 4}
- [ ] {Criterion 5}

## Expected Output

{Detailed description of what the plot should look like}

## Tags

{tag1}, {tag2}, {tag3}, {tag4}

## Use Cases

- {Use case 1}
- {Use case 2}
- {Use case 3}
```

---

## Complete Example

```markdown
# scatter-basic-001: Basic 2D Scatter Plot

## Description

Create a simple scatter plot showing the relationship between two numeric variables.
Perfect for correlation analysis, outlier detection, and exploring bivariate relationships.
Works with any dataset containing two numeric columns.

## Data Requirements

- **x**: Numeric values for x-axis (continuous or discrete)
- **y**: Numeric values for y-axis (continuous or discrete)

## Optional Parameters

- `color`: Point color (string like "blue") or column name for color mapping
- `size`: Point size in pixels (numeric like 50) or column name for size mapping
- `alpha`: Transparency level (0.0-1.0, default: 0.8)
- `title`: Plot title (string, optional)
- `xlabel`: Custom x-axis label (default: column name)
- `ylabel`: Custom y-axis label (default: column name)

## Quality Criteria

- [ ] X and Y axes are labeled with column names (or custom labels)
- [ ] Grid is visible but subtle (not overpowering the data)
- [ ] Points are clearly distinguishable (appropriate size and alpha)
- [ ] No overlapping axis labels or tick marks
- [ ] Legend is shown if color/size mapping is used
- [ ] Colorblind-safe colors when color mapping is used
- [ ] Appropriate figure size (10x6 inches default, or responsive)
- [ ] Title is centered and clearly readable (if provided)

## Expected Output

A 2D scatter plot with clearly visible points showing the correlation or distribution
between x and y variables. The plot should be immediately understandable without
additional explanation. If color or size mapping is used, the legend should clearly
indicate what each variation means.

## Tags

correlation, bivariate, basic, 2d, statistical, exploratory, scatter

## Use Cases

- Correlation analysis between two variables (e.g., height vs weight)
- Outlier detection in bivariate data
- Pattern recognition in data (linear, quadratic, clusters)
- Relationship visualization (e.g., price vs demand)
- Quality control charts (e.g., measurement vs target)
- Scientific data exploration (e.g., temperature vs pressure)
```

---

## Section Details

### 1. Title (H1)

Format: `# {spec-id}: {Human-Readable Title}`

**Requirements**:
- Start with spec ID
- Followed by colon and space
- Clear, descriptive title
- Title case

**Examples**:
- `# scatter-basic-001: Basic 2D Scatter Plot`
- `# heatmap-corr-002: Correlation Heatmap`
- `# bar-grouped-004: Grouped Bar Chart`

---

### 2. Description

**Purpose**: Quick overview for users browsing plots

**Format**: 2-3 sentences

**Should Include**:
- What the plot does
- When to use it
- What data it works with

**Example**:
```markdown
## Description

Create a simple scatter plot showing the relationship between two numeric variables.
Perfect for correlation analysis, outlier detection, and exploring bivariate relationships.
Works with any dataset containing two numeric columns.
```

---

### 3. Data Requirements

**Purpose**: Define required input data

**Format**: Bulleted list with parameter names in bold

**Requirements**:
- Use generic names (x, y, category, value, etc.)
- Specify data type (numeric, categorical, datetime)
- Describe what the data represents

**Example**:
```markdown
## Data Requirements

- **x**: Numeric values for x-axis (continuous or discrete)
- **y**: Numeric values for y-axis (continuous or discrete)
- **category**: Categorical values for grouping (string)
- **timestamp**: Datetime values for time series (datetime)
```

---

### 4. Optional Parameters

**Purpose**: Define customization options

**Format**: Bulleted list with parameter names in code

**Requirements**:
- Use `code` formatting for parameter names
- Include default values in parentheses
- Describe expected type and values

**Example**:
```markdown
## Optional Parameters

- `color`: Point color (string like "blue") or column name for color mapping
- `size`: Point size in pixels (numeric, default: 50)
- `alpha`: Transparency level (0.0-1.0, default: 0.8)
- `title`: Plot title (string, optional)
```

---

### 5. Quality Criteria

**Purpose**: Checklist for AI quality evaluation

**Format**: Markdown checklist (unchecked)

**Requirements**:
- Minimum 5 criteria
- Maximum 10 criteria
- Specific, measurable criteria
- Cover visual quality, readability, and correctness

**Categories**:
- **Labeling**: Axes labeled, legend present
- **Readability**: No overlapping text, appropriate font sizes
- **Visual Quality**: Colors, sizing, spacing
- **Accessibility**: Colorblind-safe palettes
- **Correctness**: Data accurately represented

**Example**:
```markdown
## Quality Criteria

- [ ] X and Y axes are labeled with column names
- [ ] Grid is visible but subtle
- [ ] Points are clearly distinguishable
- [ ] No overlapping axis labels
- [ ] Legend is shown if color/size mapping is used
- [ ] Colorblind-safe colors when color mapping is used
- [ ] Appropriate figure size (10x6 inches)
```

**Why Checklists?**
- ✅ AI can evaluate each criterion independently
- ✅ Human-readable quality standards
- ✅ Easy to verify visually

---

### 6. Expected Output

**Purpose**: Describe what the final plot should look like

**Format**: 1-2 paragraphs

**Should Include**:
- Visual description
- Key features
- What makes it "good"

**Example**:
```markdown
## Expected Output

A 2D scatter plot with clearly visible points showing the correlation or distribution
between x and y variables. The plot should be immediately understandable without
additional explanation. If color or size mapping is used, the legend should clearly
indicate what each variation means.
```

---

### 7. Tags

**Purpose**: Categorization for search and discovery

**Format**: Comma-separated keywords

**Categories**:
- **Type**: scatter, bar, line, heatmap, histogram, box, violin
- **Purpose**: correlation, distribution, comparison, trend, composition
- **Domain**: finance, scientific, statistical, exploratory
- **Complexity**: basic, intermediate, advanced
- **Dimensionality**: 1d, 2d, 3d, multivariate

**Example**:
```markdown
## Tags

correlation, bivariate, basic, 2d, statistical, exploratory, scatter
```

**AI Tag Generation**:
- AI can suggest additional tags
- Human can review and approve
- Tags stored in database for search

---

### 8. Use Cases

**Purpose**: Concrete examples of when to use this plot

**Format**: Bulleted list

**Requirements**:
- Specific, realistic scenarios
- 3-6 use cases
- Domain variety (science, business, etc.)

**Example**:
```markdown
## Use Cases

- Correlation analysis between two variables (e.g., height vs weight)
- Outlier detection in bivariate data
- Pattern recognition (linear, quadratic, clusters)
- Relationship visualization (e.g., price vs demand)
- Quality control charts (e.g., measurement vs target)
```

---

## How Specs Become Code

### 1. From Issue to Spec File

**User creates GitHub Issue**:
```markdown
Title: Basic scatter plot for correlation analysis

I need a simple scatter plot to show the relationship between
two numeric variables. Should support color and size mapping.

Required:
- x: numeric
- y: numeric

Optional:
- color mapping
- size mapping
- transparency
```

**GitHub Action converts to spec**:
- Extracts requirements
- Assigns spec ID (scatter-basic-001)
- Creates `specs/scatter-basic-001.md`
- Fills template with issue content

---

### 2. AI Code Generation

**Input**: Spec Markdown file

**Process**:
1. Claude reads spec
2. Determines suitable libraries (matplotlib, seaborn, plotly)
3. For each library:
   - Generates implementation code
   - Uses spec ID for file structure
   - Implements all data requirements
   - Supports optional parameters
   - Follows quality criteria

**Output**: `plots/{library}/{type}/{spec-id}/default.py`

---

### 3. Multi-LLM Quality Check

**Input**:
- Spec Markdown file
- Generated preview PNG image

**Process**:
1. Load spec and extract quality criteria
2. Load preview image from GCS
3. For each LLM (Claude, Gemini, GPT):
   - Show spec + image
   - Ask: "Does this plot meet the quality criteria?"
   - Get score (0-100) and detailed feedback
4. Calculate median score
5. Pass if ≥ 85

**Example Prompt to LLM**:
```
Here is the plot specification:

{spec markdown content}

I'm showing you the generated plot image.

Please evaluate:
1. Does it meet all quality criteria?
2. Is the data correctly represented?
3. Are there any visual issues?

Respond in JSON:
{
  "score": 0-100,
  "criteria_met": ["criterion1", "criterion2"],
  "criteria_failed": ["criterion3"],
  "feedback": "Detailed explanation"
}
```

---

## Quality Evaluation Details

### What LLMs Check

**Criteria Compliance**:
- ✅ Each checkbox in Quality Criteria section
- ✅ Visual inspection of image
- ✅ Comparison with Expected Output

**Visual Quality**:
- Font sizes (labels readable?)
- Colors (distinguishable? colorblind-safe?)
- Spacing (elements overlapping?)
- Proportions (appropriate aspect ratio?)
- Legend (clear and positioned well?)

**Data Representation**:
- Axes labeled correctly?
- Data points visible?
- Scales appropriate?

### Scoring Rubric

**90-100**: Excellent
- All criteria met
- Visually appealing
- Production-ready

**85-89**: Good
- Minor issues
- Still acceptable
- May suggest improvements

**75-84**: Needs Improvement
- Some criteria failed
- Regeneration recommended
- Specific feedback provided

**< 75**: Rejected
- Major issues
- Regeneration required
- Detailed feedback for fixes

### Feedback Loop

**Attempt 1 (Score 78)**:
```
❌ X-axis labels overlapping
❌ Legend not colorblind-safe
✅ Grid is subtle
✅ Points clearly visible

Feedback: Rotate x-axis labels 45° and use colorblind-safe palette
```

**Attempt 2 (Score 92)**:
```
✅ All criteria met
✅ Colorblind-safe colors
✅ Labels properly spaced

Approved!
```

---

## Writing Good Specs

### DO ✅

**Be Specific**:
```markdown
✅ Good:
- [ ] X and Y axes are labeled with column names
- [ ] Grid has alpha=0.3 (subtle but visible)

❌ Bad:
- [ ] Plot looks good
- [ ] Axes are labeled
```

**Use Concrete Examples**:
```markdown
✅ Good:
- Correlation analysis between height and weight

❌ Bad:
- Analyzing data
```

**Define Clear Requirements**:
```markdown
✅ Good:
- **x**: Numeric values for x-axis (continuous or discrete)

❌ Bad:
- **x**: Data
```

### DON'T ❌

**Avoid Library-Specific Details**:
```markdown
❌ Bad:
Use plt.scatter() with marker='o'

✅ Good:
Create scatter plot with circular markers
```

**Don't Be Vague**:
```markdown
❌ Bad:
Plot should be nice

✅ Good:
Points should be clearly distinguishable (size >= 30 pixels)
```

**Don't Over-Specify**:
```markdown
❌ Bad:
Font must be exactly Arial 12pt

✅ Good:
Labels should be clearly readable
```

---

## Spec Evolution

### Updating Existing Specs

**Scenario**: Need to add colorblind mode to scatter-basic-001

**Process**:
1. Create new issue: "Refine scatter-basic-001: Add colorblind option"
2. Reference original issue (#123)
3. Update spec file with new optional parameter
4. AI regenerates all implementations
5. Quality check with updated criteria
6. Deploy

**Changes in Spec**:
```markdown
## Optional Parameters

+ - `colorblind`: Use colorblind-safe palette (boolean, default: false)

## Quality Criteria

+ - [ ] Uses colorblind-safe palette when colorblind=true
```

### Version History

Specs are versioned via git:
```bash
# See spec evolution
git log specs/scatter-basic-001.md

# Compare versions
git diff HEAD~1 specs/scatter-basic-001.md
```

No separate version numbers needed - git handles it.

---

## Spec Validation

### Automated Checks

Before AI generates code, spec is validated:

**Required Sections**:
- ✅ Title with spec ID
- ✅ Description
- ✅ Data Requirements
- ✅ Quality Criteria (min 5 items)

**Optional Sections**:
- Optional Parameters
- Expected Output
- Tags
- Use Cases

### Validation Script

```python
# automation/scripts/validate_spec.py
def validate_spec(spec_path: str) -> dict:
    """
    Validates spec file format
    Returns: {"valid": bool, "errors": list}
    """
    content = Path(spec_path).read_text()

    errors = []

    # Check required sections
    if "## Description" not in content:
        errors.append("Missing Description section")

    if "## Data Requirements" not in content:
        errors.append("Missing Data Requirements section")

    if "## Quality Criteria" not in content:
        errors.append("Missing Quality Criteria section")

    # Check quality criteria count
    criteria = content.count("- [ ]")
    if criteria < 5:
        errors.append(f"Need at least 5 quality criteria, found {criteria}")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
```

---

## FAQ

### Q: Can I write specs for proprietary/domain-specific plots?

**A**: Yes! That's encouraged. Examples:
- Finance: Candlestick charts, Bollinger bands
- Science: Phase diagrams, Ramachandran plots
- Engineering: Smith charts, Bode plots

### Q: What if a plot can't be implemented in all libraries?

**A**: That's fine. The spec is library-agnostic, but implementations are optional:
- matplotlib: ✅ Implemented
- seaborn: ❌ Not applicable
- plotly: ✅ Implemented

### Q: How detailed should quality criteria be?

**A**: Detailed enough for AI to evaluate visually:
- ✅ "No overlapping x-axis labels"
- ❌ "Labels are good"

Aim for 5-10 criteria covering:
- Labeling (2-3 criteria)
- Visual quality (2-3 criteria)
- Accessibility (1-2 criteria)
- Correctness (1-2 criteria)

### Q: Can users submit specs without coding?

**A**: Absolutely! That's the whole point:
1. Create GitHub Issue with description
2. Community/AI helps formalize it
3. AI generates all implementations
4. User gets working code

---

## Contributing Specs

See [development.md](../development.md) for how to contribute specs via GitHub Issues.

**Quick Start**:
1. Create GitHub Issue with plot idea
2. Use template (auto-filled)
3. Describe what you want
4. Wait for AI to generate code
5. Review preview images
6. Provide feedback if needed

---

*For implementation details, see [repository-structure.md](./repository-structure.md)*
*For automation details, see [automation-workflows.md](./automation-workflows.md)*
