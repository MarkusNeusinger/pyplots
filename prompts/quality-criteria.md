# Quality Criteria

Definition of what makes a high-quality plot implementation.

## Overview

Quality is evaluated across **3 areas**:

| Area | Weight | Focus |
|------|--------|-------|
| **Spec Compliance** | 40% | Does the plot match the specification? |
| **Visual Quality** | 40% | Is the plot professional and beautiful? |
| **Code Quality** | 20% | Is the code clean and idiomatic? |

## Scoring

**Range**: 0-100 points (simply add up all criteria)
**Pass Threshold**: >= 85

| Score | Rating |
|-------|--------|
| >= 90 | Excellent |
| 85-89 | Good (acceptable) |
| 75-84 | Needs improvement |
| < 75 | Rejected |

---

## 1. Spec Compliance (40 Points)

**Question**: Does the plot match what the specification requested?

| ID | Criterion | Points | Description |
|----|-----------|--------|-------------|
| SC-01 | **Plot Type** | 12 | Correct chart type (scatter != line != bar) |
| SC-02 | **Data Mapping** | 8 | X/Y data correctly assigned, no mix-ups |
| SC-03 | **Required Features** | 8 | All features mentioned in spec are implemented |
| SC-04 | **Data Range** | 4 | Axis ranges show all data appropriately |
| SC-05 | **Legend Accuracy** | 4 | Legend labels match the data series |
| SC-06 | **Title Format** | 4 | Uses `{spec-id} · {library} · pyplots.ai` format |

### SC-01: Plot Type (12 points)

The generated plot must be the correct visualization type.

```
Spec says "scatter plot" -> Must use scatter/point markers
Spec says "bar chart"    -> Must use bars, not lines
Spec says "heatmap"      -> Must use color matrix, not scatter
```

### SC-02: Data Mapping (8 points)

Data columns are correctly mapped to visual elements.

```
# Good: X and Y match spec description
ax.scatter(df['age'], df['income'])  # age on X, income on Y

# Bad: Swapped X and Y
ax.scatter(df['income'], df['age'])  # Wrong mapping!
```

### SC-03: Required Features (8 points)

All features explicitly mentioned in the spec are present.

```
Spec mentions:
- "color by category" -> Must have color encoding
- "with trend line"   -> Must include regression line
- "logarithmic scale" -> Must use log scale
```

### SC-04: Data Range (4 points)

Axis ranges display all data points appropriately.

```
# Good: All data visible with reasonable padding
ax.set_xlim(data.min() - margin, data.max() + margin)

# Bad: Data cut off or excessive whitespace
ax.set_xlim(0, 100)  # When data ranges 50-200
```

### SC-05: Legend Accuracy (4 points)

Legend entries match the actual data series.

```python
# Good: Labels match what's plotted
ax.scatter(x, y1, label='Sales 2023')
ax.scatter(x, y2, label='Sales 2024')

# Bad: Misleading labels
ax.scatter(x, y1, label='Revenue')  # Actually plotting sales
```

### SC-06: Title Format (4 points)

Title follows the pyplots.ai format.

```python
# Good
ax.set_title('scatter-basic · matplotlib · pyplots.ai')
ax.set_title('Stock Prices · candle-ohlc · plotly · pyplots.ai')

# Bad
ax.set_title('My Scatter Plot')
ax.set_title('scatter-basic')  # Missing library and pyplots.ai
```

---

## 2. Visual Quality (40 Points)

**Question**: Does the plot look professional and appealing?

| ID | Criterion | Points | Description |
|----|-----------|--------|-------------|
| VQ-01 | **Axis Labels** | 8 | Meaningful labels (not "x", "y", or empty) |
| VQ-02 | **No Overlap** | 7 | Text/labels don't overlap, everything readable |
| VQ-03 | **Color Choice** | 6 | Harmonious, distinguishable, colorblind-safe |
| VQ-04 | **Element Clarity** | 6 | Points/bars/lines clearly visible (size, alpha) |
| VQ-05 | **Layout Balance** | 5 | Good proportions, no cut-off content |
| VQ-06 | **Grid Subtlety** | 3 | Grid (if present) is subtle, not dominant |
| VQ-07 | **Legend Placement** | 3 | Legend doesn't obscure data |
| VQ-08 | **Image Size** | 2 | 4800x2700 px, 16:9 aspect ratio |

### VQ-01: Axis Labels (8 points)

Axes have meaningful, descriptive labels.

```python
# Good
ax.set_xlabel('Age (years)')
ax.set_ylabel('Income ($)')

# Bad
ax.set_xlabel('x')
ax.set_xlabel('')
# No labels at all
```

### VQ-02: No Overlap (7 points)

All text elements are readable without overlapping.

```python
# Good: Rotated labels when needed
plt.xticks(rotation=45, ha='right')

# Good: Adjusted font size for many categories
ax.tick_params(labelsize=10)

# Bad: Overlapping tick labels ignored
```

### VQ-03: Color Choice (6 points)

Colors are harmonious and colorblind-safe.

**Primary colors (use first):**
- Python Blue: `#306998`
- Python Yellow: `#FFD43B`

For additional colors: AI chooses appropriate, colorblind-safe colors.

**Bad:** Red-green combinations (not colorblind-safe)

**Good alternatives for more colors:** `viridis`, `tab10`, or other colorblind-safe palettes

### VQ-04: Element Clarity (6 points)

Data elements are clearly visible at 4800×2700 px. Default/standard sizes are too small!

**Rule:** Elements should be **~3-4x larger** than library defaults.

See `prompts/default-style-guide.md` for principles and `prompts/library/{library}.md` for library-specific guidance.

**Check:**
- Are markers/points clearly visible (not tiny dots)?
- Are lines thick enough to see clearly?
- Would this be readable on a 4K monitor at full size?

**Scaling guide by data density:**
- Few points (<50): Larger markers
- Medium points (50-200): Medium markers
- Many points (>200): Smaller markers with transparency

### VQ-05: Layout Balance (5 points)

Plot has good proportions with no cut-off content.

```python
# Good: Tight layout applied
plt.tight_layout()
plt.savefig('plot.png', bbox_inches='tight')

# Bad: Labels cut off at edges
```

### VQ-06: Grid Subtlety (3 points)

Grid enhances readability without dominating.

```python
# Good: Subtle grid
ax.grid(True, alpha=0.3, linestyle='--')

# Bad: Overpowering grid
ax.grid(True, linewidth=2, color='black')
```

### VQ-07: Legend Placement (3 points)

Legend is visible and doesn't cover data.

```python
# Good: Outside or in empty area
ax.legend(loc='upper right')
ax.legend(bbox_to_anchor=(1.05, 1))

# Bad: Legend covers data points
```

### VQ-08: Image Size (2 points)

Output image has correct dimensions.

```python
# Good: 4800x2700 px (16:9)
fig, ax = plt.subplots(figsize=(16, 9))
plt.savefig('plot.png', dpi=300)  # 16*300=4800, 9*300=2700

# For other libraries
fig.write_image('plot.png', width=4800, height=2700)
```

---

## 3. Code Quality (20 Points)

**Question**: Is the code clean, readable, and idiomatic?

| ID | Criterion | Points | Description |
|----|-----------|--------|-------------|
| CQ-01 | **KISS Structure** | 5 | Imports -> Data -> Plot -> Save (no functions/classes) |
| CQ-02 | **Reproducibility** | 4 | Uses `np.random.seed(42)` or deterministic data |
| CQ-03 | **Library Idioms** | 4 | Follows library best practices |
| CQ-04 | **Clean Imports** | 2 | Only used imports, sensible aliases |
| CQ-05 | **Helpful Comments** | 2 | Comments where logic isn't obvious |
| CQ-06 | **No Deprecated API** | 2 | No deprecated functions or methods |
| CQ-07 | **Output Correct** | 1 | Saves as `plot.png` |

### CQ-01: KISS Structure (5 points)

Code follows simple sequential structure without functions or classes.

```python
# Good: Simple sequential structure
"""
scatter-basic: Basic Scatter Plot
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np

# Data
np.random.seed(42)
x = np.random.randn(100)
y = x * 0.8 + np.random.randn(100) * 0.5

# Plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.scatter(x, y, alpha=0.7, s=50)

# Style
ax.set_xlabel('X Value')
ax.set_ylabel('Y Value')
ax.set_title('scatter-basic · matplotlib · pyplots.ai')

plt.tight_layout()
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
```

```python
# Bad: Unnecessary complexity
def create_plot(data):
    ...

if __name__ == '__main__':
    create_plot(data)
```

### CQ-02: Reproducibility (4 points)

Same code produces same output every time.

```python
# Good: Fixed seed
np.random.seed(42)
x = np.random.randn(100)

# Good: Deterministic data
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Good: Standard dataset
df = sns.load_dataset('iris')

# Bad: Random without seed
x = np.random.randn(100)  # Different every run!
```

### CQ-03: Library Idioms (4 points)

Code uses library-specific best practices.

```python
# matplotlib - Good
fig, ax = plt.subplots(figsize=(16, 9))
ax.scatter(x, y)

# matplotlib - Bad (old style)
plt.figure(figsize=(16, 9))
plt.scatter(x, y)

# seaborn - Good
fig, ax = plt.subplots(figsize=(16, 9))
sns.scatterplot(data=df, x='x', y='y', ax=ax)

# plotly - Good
fig = px.scatter(df, x='x', y='y')
fig.update_layout(width=4800, height=2700)
```

### CQ-04: Clean Imports (2 points)

Only import what's used, with standard aliases.

```python
# Good
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Bad: Unused imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns  # Never used!
from datetime import datetime  # Never used!
```

### CQ-05: Helpful Comments (2 points)

Comments explain non-obvious logic, not obvious code.

```python
# Good: Explains why
# Offset by 0.4 to center bars between tick marks
ax.bar(x - 0.4, y1, width=0.4)
ax.bar(x, y2, width=0.4)

# Bad: States the obvious
# Create scatter plot
ax.scatter(x, y)

# Bad: No comments on complex logic
ax.bar(x - width/2, y1, width)
ax.bar(x + width/2, y2, width)
```

### CQ-06: No Deprecated API (2 points)

Uses current, non-deprecated functions.

```python
# Good: Current API
fig, ax = plt.subplots()
ax.set_xlabel('X')

# Bad: Deprecated
plt.xlabel('X')  # Use ax.set_xlabel instead
df.append(row)   # Use pd.concat instead
```

### CQ-07: Output Correct (1 point)

Saves output as `plot.png`.

```python
# Good
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
fig.write_image('plot.png', width=4800, height=2700)

# Bad
plt.savefig('output.png')
plt.savefig('matplotlib_scatter.png')
plt.show()  # No file saved!
```

---

## Evaluation Checklist

Quick reference for reviewers:

### Spec Compliance (40 pts)
- [ ] SC-01: Correct plot type (12)
- [ ] SC-02: Data mapped correctly (8)
- [ ] SC-03: All required features present (8)
- [ ] SC-04: Appropriate data range (4)
- [ ] SC-05: Legend labels accurate (4)
- [ ] SC-06: Title format correct (4)

### Visual Quality (40 pts)
- [ ] VQ-01: Meaningful axis labels (8)
- [ ] VQ-02: No overlapping text (7)
- [ ] VQ-03: Good color choice (6)
- [ ] VQ-04: Clear data elements (6)
- [ ] VQ-05: Balanced layout (5)
- [ ] VQ-06: Subtle grid (3)
- [ ] VQ-07: Well-placed legend (3)
- [ ] VQ-08: Correct image size (2)

### Code Quality (20 pts)
- [ ] CQ-01: KISS structure (5)
- [ ] CQ-02: Reproducible output (4)
- [ ] CQ-03: Library idioms (4)
- [ ] CQ-04: Clean imports (2)
- [ ] CQ-05: Helpful comments (2)
- [ ] CQ-06: No deprecated API (2)
- [ ] CQ-07: Saves as plot.png (1)

**Total: ___ / 100**
