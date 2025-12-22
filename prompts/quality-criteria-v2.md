# Quality Criteria v2

Definition of what makes a high-quality plot implementation.

## Overview

Quality is evaluated across **5 areas**:

| Area | Weight | Focus |
|------|--------|-------|
| **Library Authenticity** | 20% | Does the implementation actually use the designated library? |
| **Spec Compliance** | 25% | Does the plot match the specification? |
| **Visual Quality** | 30% | Is the plot professional, readable, and well-designed? |
| **Data Quality** | 15% | Are the example data realistic and comprehensive? |
| **Code Quality** | 10% | Is the code clean and idiomatic? |

## Scoring

**Range**: 0-100 points (simply add up all criteria)

### Quality Tiers

| Score | Tier | Result |
|-------|------|--------|
| **90-100** | Excellent | ✅ High quality - flagship example |
| **70-89** | Good | ✅ Solid implementation - acceptable |
| **50-69** | Acceptable | ✅ Basic implementation - needs improvement |
| **< 50** | Poor | ❌ Rejected - not usable |

**Pass Threshold**: >= 50 (allows more implementations, but quality tiers are visible)

### Interpretation Guide

| Score | What It Means |
|-------|---------------|
| 95-100 | Exceptional - could be used in official documentation |
| 85-94 | High quality - professional level |
| 70-84 | Good - functional with minor issues |
| 50-69 | Acceptable - works but has notable shortcomings |
| < 50 | Poor - significant problems, needs major revision |

---

## 1. Library Authenticity (20 Points) - NEW

**Question**: Does the implementation genuinely use the designated library's plotting capabilities?

This is a **critical** criterion. An implementation labeled as "seaborn" must actually use seaborn's plotting functions, not just matplotlib with `import seaborn`.

| ID | Criterion | Points | Description |
|----|-----------|--------|-------------|
| LA-01 | **Library Plot Functions** | 12 | Uses the library's actual plotting API |
| LA-02 | **Library-Specific Features** | 5 | Leverages features unique to this library |
| LA-03 | **Not Feasible Declaration** | 3 | Correctly identifies when a library cannot implement the spec |

### LA-01: Library Plot Functions (12 points)

The core plotting must use the designated library's functions, not just styling.

**Scoring:**
- **12 pts**: Primary plot created with library's plotting functions
- **6 pts**: Mixed usage (some library functions, some matplotlib fallback)
- **0 pts**: Only uses library for styling/theming (e.g., only `sns.set_style()`)

```python
# GOOD - seaborn: Uses sns.scatterplot
sns.scatterplot(data=df, x='x', y='y', ax=ax)

# GOOD - plotly: Uses px.scatter
fig = px.scatter(df, x='x', y='y')

# BAD - seaborn: Only uses set_style, plots with matplotlib
sns.set_style("white")  # This alone = 0 points!
ax.scatter(x, y)        # This is matplotlib, not seaborn
```

**Library-specific requirements:**

| Library | Must Use | Not Sufficient |
|---------|----------|----------------|
| seaborn | `sns.scatterplot`, `sns.barplot`, `sns.heatmap`, etc. | Only `sns.set_style()` or `sns.set_theme()` |
| plotly | `px.*` or `go.*` plotting functions | Only layout/style functions |
| bokeh | `figure.scatter()`, `figure.line()`, etc. | Only styling |
| altair | `alt.Chart().mark_*()` | Only configuration |
| plotnine | `ggplot() + geom_*()` | Only theme functions |
| pygal | Chart type classes with data | Only styling |
| highcharts | Chart definitions with series | Only options |
| letsplot | `ggplot() + geom_*()` | Only theme |

### LA-02: Library-Specific Features (5 points)

Uses features that showcase why someone would choose this library.

**Scoring:**
- **5 pts**: Uses distinctive features of the library
- **2 pts**: Uses library but in a way identical to matplotlib
- **0 pts**: No library-specific advantages visible

```python
# GOOD - seaborn: Uses built-in statistical features
sns.regplot(data=df, x='x', y='y', ax=ax)  # Built-in regression line!

# GOOD - plotly: Uses interactivity
fig = px.scatter(df, x='x', y='y', hover_data=['name'])

# OK - seaborn: Works but doesn't showcase seaborn strengths
sns.scatterplot(x=x, y=y)  # Could have been matplotlib

# POOR - seaborn: Just wrapping matplotlib
fig, ax = plt.subplots()
ax.bar(x, y)  # Pure matplotlib in a "seaborn" file
```

### LA-03: Not Feasible Declaration (3 points)

When a library genuinely cannot implement a specification (e.g., pygal cannot do 3D plots), the implementation should clearly state this.

**Scoring:**
- **3 pts**: Correctly identifies limitations and either provides best alternative OR marks as not-feasible
- **0 pts**: Forces an inappropriate implementation or fakes library usage

```python
# GOOD - Honest declaration in header
""" pyplots.ai
chord-basic: Basic Chord Diagram
Library: pygal (NOT FEASIBLE)
Reason: Pygal does not support chord diagrams. Consider plotly or matplotlib.
"""

# BAD - Pretending to use a library
# File: seaborn.py
import matplotlib.pyplot as plt  # No seaborn anywhere!
```

---

## 2. Spec Compliance (25 Points)

**Question**: Does the plot match what the specification requested?

| ID | Criterion | Points | Description |
|----|-----------|--------|-------------|
| SC-01 | **Plot Type** | 8 | Correct chart type (scatter != line != bar) |
| SC-02 | **Data Mapping** | 5 | X/Y data correctly assigned, no mix-ups |
| SC-03 | **Required Features** | 5 | All features mentioned in spec are implemented |
| SC-04 | **Data Range** | 3 | Axis ranges show all data appropriately |
| SC-05 | **Legend Accuracy** | 2 | Legend labels match the data series |
| SC-06 | **Title Format** | 2 | Uses `{spec-id} · {library} · pyplots.ai` format |

### SC-01: Plot Type (8 points)

The generated plot must be the correct visualization type.

```
Spec says "scatter plot" -> Must use scatter/point markers
Spec says "bar chart"    -> Must use bars, not lines
Spec says "heatmap"      -> Must use color matrix, not scatter
```

### SC-02: Data Mapping (5 points)

Data columns are correctly mapped to visual elements.

```python
# Good: X and Y match spec description
ax.scatter(df['age'], df['income'])  # age on X, income on Y

# Bad: Swapped X and Y
ax.scatter(df['income'], df['age'])  # Wrong mapping!
```

### SC-03: Required Features (5 points)

All features explicitly mentioned in the spec are present.

```
Spec mentions:
- "color by category" -> Must have color encoding
- "with trend line"   -> Must include regression line
- "logarithmic scale" -> Must use log scale
```

### SC-04: Data Range (3 points)

Axis ranges display all data points appropriately.

### SC-05: Legend Accuracy (2 points)

Legend entries match the actual data series.

### SC-06: Title Format (2 points)

Title follows the pyplots.ai format: `{spec-id} · {library} · pyplots.ai`

---

## 3. Visual Quality (30 Points)

**Question**: Does the plot look professional, readable, and well-designed?

| ID | Criterion | Points | Description |
|----|-----------|--------|-------------|
| VQ-01 | **Text Legibility** | 6 | All text readable at full size (min font sizes enforced) |
| VQ-02 | **No Overlap** | 5 | Text/labels don't overlap, everything readable |
| VQ-03 | **Element Visibility** | 5 | Data elements sized appropriately for data density |
| VQ-04 | **Color Accessibility** | 4 | Colorblind-safe, sufficient contrast |
| VQ-05 | **Layout Balance** | 4 | Good proportions, no cut-off content, proper whitespace |
| VQ-06 | **Axis Labels** | 3 | Meaningful labels with units where appropriate |
| VQ-07 | **Grid & Legend** | 2 | Grid subtle, legend well-placed |
| VQ-08 | **Image Size** | 1 | 4800x2700 px, 16:9 aspect ratio |

### VQ-01: Text Legibility (6 points) - ENHANCED

All text must be readable at 4800×2700 px output.

**Minimum font sizes (at 300 dpi):**

| Element | Minimum Size | Recommended |
|---------|-------------|-------------|
| Title | 20pt | 24-28pt |
| Axis labels | 16pt | 18-22pt |
| Tick labels | 12pt | 14-18pt |
| Legend | 12pt | 14-16pt |
| Annotations | 10pt | 12-14pt |

**Scoring:**
- **6 pts**: All text meets minimum sizes and is clearly readable
- **3 pts**: Most text readable, some slightly small
- **0 pts**: Text too small to read comfortably

```python
# GOOD
ax.set_title('...', fontsize=24)
ax.set_xlabel('...', fontsize=20)
ax.tick_params(labelsize=16)

# BAD - Default sizes are too small for 4800x2700
ax.set_title('...')  # Default ~12pt - too small!
```

### VQ-02: No Overlap (5 points) - ENHANCED

All text elements must be readable without overlapping.

**Scoring:**
- **5 pts**: No overlapping text anywhere
- **3 pts**: Minor overlap that doesn't affect readability
- **1 pt**: Some overlap but main content readable
- **0 pts**: Significant overlap making text unreadable

**Common issues to check:**
- Tick labels overlapping each other (especially on x-axis with many categories)
- Axis labels overlapping tick labels
- Legend text overlapping data
- Annotations overlapping each other or data

```python
# GOOD: Rotated labels prevent overlap
plt.xticks(rotation=45, ha='right')

# GOOD: Reduced tick frequency for many values
ax.xaxis.set_major_locator(plt.MaxNLocator(10))

# BAD: Many categories with horizontal labels
ax.set_xticklabels(['Very Long Category Name'] * 20)  # Will overlap!
```

### VQ-03: Element Visibility (5 points) - NEW

Data elements (points, lines, bars) must be appropriately sized based on data density.

**Adaptive sizing requirements:**

| Data Points | Marker Size (s=) | Line Width | Alpha |
|-------------|------------------|------------|-------|
| < 20 | 300-500 | 4-5 | 1.0 |
| 20-50 | 150-300 | 3-4 | 0.9 |
| 50-100 | 80-150 | 2-3 | 0.7-0.8 |
| 100-200 | 50-80 | 1.5-2 | 0.5-0.7 |
| 200-500 | 20-50 | 1-1.5 | 0.3-0.5 |
| > 500 | 10-20 | 0.5-1 | 0.1-0.3 |

**Scoring:**
- **5 pts**: Element sizes perfectly matched to data density
- **3 pts**: Elements visible but not optimally sized
- **1 pt**: Elements barely visible or overly large
- **0 pts**: Elements invisible (tiny dots) or so large they obscure data

```python
# GOOD - Few points, large markers
n_points = 30
ax.scatter(x, y, s=300, alpha=0.8)

# GOOD - Many points, smaller with transparency
n_points = 500
ax.scatter(x, y, s=30, alpha=0.4)

# BAD - Many points with large opaque markers
n_points = 500
ax.scatter(x, y, s=200, alpha=1.0)  # Overlapping mess

# BAD - Few points with tiny markers
n_points = 20
ax.scatter(x, y, s=10)  # Can barely see them
```

### VQ-04: Color Accessibility (4 points) - ENHANCED

Colors must be distinguishable by colorblind users and have sufficient contrast.

**Requirements:**
- Never use red-green as the only distinguishing factor
- Background contrast: 4.5:1 minimum for text, 3:1 for data elements
- Use colorblind-safe palettes: `viridis`, `colorblind`, `tab10`

**Scoring:**
- **4 pts**: All colors colorblind-safe with good contrast
- **2 pts**: Minor accessibility issues
- **0 pts**: Red-green distinction or low contrast

**Primary pyplots colors:**
- Python Blue: `#306998`
- Python Yellow: `#FFD43B`

### VQ-05: Layout Balance (4 points)

Good proportions with no cut-off content.

**Scoring:**
- **4 pts**: Perfect layout, good whitespace, nothing cut off
- **2 pts**: Minor layout issues
- **0 pts**: Content cut off or severe imbalance

### VQ-06: Axis Labels (3 points)

Meaningful labels with units where appropriate.

```python
# GOOD
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Growth Rate (mm/day)')

# BAD
ax.set_xlabel('x')
ax.set_ylabel('')
```

### VQ-07: Grid & Legend (2 points)

Grid subtle (alpha 0.2-0.4), legend doesn't obscure data.

### VQ-08: Image Size (1 point)

Output: 4800×2700 px (16:9 at 300 dpi).

---

## 4. Data Quality (15 Points)

**Question**: Are the example data realistic, comprehensive, and well-constructed?

| ID | Criterion | Points | Description |
|----|-----------|--------|-------------|
| DQ-01 | **Feature Coverage** | 6 | Data demonstrates ALL aspects of the plot type |
| DQ-02 | **Realistic Context** | 5 | Data represents a plausible real-world scenario |
| DQ-03 | **Appropriate Scale** | 4 | Data values and ranges are sensible for the context |

### DQ-01: Feature Coverage (6 points)

The example data must demonstrate ALL visual features of the plot type.

```python
# GOOD: Candlestick shows both bullish AND bearish candles
# GOOD: Box plot shows outliers AND varying distributions
# GOOD: Histogram shows multimodal distribution

# BAD: Only showing one type of pattern
# BAD: All groups look identical
```

### DQ-02: Realistic Context (5 points)

Data represents a plausible real-world scenario.

### DQ-03: Appropriate Scale (4 points)

Values and ranges are sensible for the domain.

---

## 5. Code Quality (10 Points)

**Question**: Is the code clean, readable, and idiomatic?

| ID | Criterion | Points | Description |
|----|-----------|--------|-------------|
| CQ-01 | **KISS Structure** | 3 | Imports -> Data -> Plot -> Save (no functions/classes) |
| CQ-02 | **Reproducibility** | 3 | Uses `np.random.seed(42)` or deterministic data |
| CQ-03 | **Clean Imports** | 2 | Only used imports, sensible aliases |
| CQ-04 | **No Deprecated API** | 1 | No deprecated functions or methods |
| CQ-05 | **Output Correct** | 1 | Saves as `plot.png` |

### CQ-01: KISS Structure (3 points)

Simple sequential structure without functions or classes.

### CQ-02: Reproducibility (3 points)

Same code produces same output every time.

```python
# GOOD
np.random.seed(42)

# BAD
x = np.random.randn(100)  # Different every run!
```

### CQ-03: Clean Imports (2 points)

Only import what's used.

```python
# BAD: Unused imports
import seaborn as sns  # Never used! (This also fails LA-01!)
```

### CQ-04: No Deprecated API (1 point)

Uses current, non-deprecated functions.

### CQ-05: Output Correct (1 point)

Saves output as `plot.png`.

---

## Evaluation Checklist

Quick reference for reviewers:

### Library Authenticity (20 pts) - CRITICAL
- [ ] LA-01: Uses library's actual plotting functions (12)
- [ ] LA-02: Uses library-specific features (5)
- [ ] LA-03: Correctly handles not-feasible cases (3)

### Spec Compliance (25 pts)
- [ ] SC-01: Correct plot type (8)
- [ ] SC-02: Data mapped correctly (5)
- [ ] SC-03: All required features present (5)
- [ ] SC-04: Appropriate data range (3)
- [ ] SC-05: Legend labels accurate (2)
- [ ] SC-06: Title format correct (2)

### Visual Quality (30 pts)
- [ ] VQ-01: Text legibility - minimum font sizes (6)
- [ ] VQ-02: No overlapping text (5)
- [ ] VQ-03: Element visibility - adaptive sizing (5)
- [ ] VQ-04: Color accessibility - colorblind-safe (4)
- [ ] VQ-05: Layout balance (4)
- [ ] VQ-06: Meaningful axis labels (3)
- [ ] VQ-07: Subtle grid, well-placed legend (2)
- [ ] VQ-08: Correct image size (1)

### Data Quality (15 pts)
- [ ] DQ-01: Feature coverage (6)
- [ ] DQ-02: Realistic context (5)
- [ ] DQ-03: Appropriate scale (4)

### Code Quality (10 pts)
- [ ] CQ-01: KISS structure (3)
- [ ] CQ-02: Reproducible output (3)
- [ ] CQ-03: Clean imports (2)
- [ ] CQ-04: No deprecated API (1)
- [ ] CQ-05: Saves as plot.png (1)

**Total: ___ / 100**

---

## Example Scoring Scenarios

### Scenario A: Seaborn implementation using only `sns.set_style()`

```
LA-01: 0/12 (no seaborn plotting functions)
LA-02: 0/5 (no library-specific features)
LA-03: 0/3 (should have been marked not-feasible or used proper seaborn)
SC-*: 25/25 (plot is correct)
VQ-*: 28/30 (looks good)
DQ-*: 15/15 (good data)
CQ-*: 8/10 (clean code but imports unused seaborn)

Total: 76/100 - BUT fails LA-01 critically, so capped at 50 maximum
Final: 50/100 (Acceptable tier - needs improvement)
```

### Scenario B: Proper seaborn implementation

```
LA-01: 12/12 (uses sns.scatterplot)
LA-02: 4/5 (uses palette but not statistical features)
LA-03: 3/3 (n/a)
SC-*: 23/25 (minor data mapping issue)
VQ-*: 27/30 (text slightly small)
DQ-*: 14/15 (good data)
CQ-*: 10/10 (clean code)

Total: 93/100 (Excellent tier)
```

### Scenario C: Matplotlib with overlapping labels and tiny markers

```
LA-01: 12/12 (proper matplotlib usage)
LA-02: 3/5 (basic usage)
LA-03: 3/3 (n/a)
SC-*: 25/25 (correct plot)
VQ-01: 3/6 (text too small)
VQ-02: 1/5 (overlapping x-axis labels)
VQ-03: 1/5 (tiny markers, can barely see)
VQ-*: 15/30 total
DQ-*: 15/15 (good data)
CQ-*: 10/10 (clean code)

Total: 77/100 (Good tier but visual issues)
```

---

## Critical Failure Rules

Certain failures result in automatic score caps:

| Failure | Maximum Score |
|---------|---------------|
| LA-01 = 0 (no library plotting) | Cap at 50 |
| VQ-02 = 0 (severe overlap) | Cap at 60 |
| VQ-03 = 0 (invisible elements) | Cap at 60 |
| SC-01 = 0 (wrong plot type) | Cap at 40 |
