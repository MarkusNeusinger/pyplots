# Quality Criteria

Definition of what makes a high-quality plot implementation.

## Scoring

**Range**: 0-100 points
**Pass Threshold**: ≥ 85

| Score | Rating |
|-------|--------|
| ≥ 90 | Excellent |
| 85-89 | Good (acceptable) |
| 75-84 | Needs improvement |
| < 75 | Rejected |

---

## Visual Quality

### VQ-001: Axes Labeled (10 points, Critical)

- X and Y axes have meaningful labels
- Not empty, not just "x" or "y"

```python
# Good
ax.set_xlabel("Age (years)")
ax.set_ylabel("Income ($)")

# Bad
ax.set_xlabel("")
ax.set_xlabel("x")
```

### VQ-002: Visual Clarity (5 points, Medium)

- Grid (if present) doesn't dominate the data
- Elements are distinguishable
- AI discretion for grid style

### VQ-003: Elements Clear (8 points, High)

- Data points/bars/lines clearly visible
- Appropriate size, alpha, contrast

```python
# Good
ax.scatter(x, y, s=50, alpha=0.8)

# Bad
ax.scatter(x, y, s=5, alpha=0.1)
```

### VQ-004: No Overlap (9 points, High)

- Labels, ticks, legend don't overlap
- Text is readable

```python
# Good (when many labels)
plt.xticks(rotation=45, ha='right')

# Bad
# Overlapping labels ignored
```

### VQ-005: Legend Present (7 points, Medium)

- Legend present when >1 series or color mapping
- Not needed for single series without mapping

### VQ-006: Colorblind Safe (6 points, Medium)

- No red-green combinations
- Safe palettes: viridis, tab10, colorblind

### VQ-007: Image Size (4 points, Low)

- Target: 4800 × 2700 px (16:9 aspect ratio)
- See `prompts/default-style-guide.md`

### VQ-008: Title (3 points, Low)

- If provided: centered and clear
- Not required if not in spec

---

## Code Quality

### CQ-001: Type Hints (7 points, Medium)

```python
# Good
def create_plot(data: pd.DataFrame, x: str) -> Figure:

# Bad
def create_plot(data, x):
```

### CQ-002: Docstring (8 points, High)

Google-style with Args, Returns, Raises, Example.

```python
def create_plot(...):
    """
    Short description.

    Args:
        data: Input DataFrame
        x: Column name for X axis

    Returns:
        Matplotlib Figure

    Raises:
        ValueError: If data is empty

    Example:
        >>> fig = create_plot(df, 'age')
    """
```

### CQ-003: Input Validation (10 points, Critical)

```python
# Good
if data.empty:
    raise ValueError("Data cannot be empty")

if x not in data.columns:
    raise KeyError(f"Column '{x}' not found")

# Bad
# No validation
```

### CQ-004: Clear Error Messages (6 points, Medium)

```python
# Good
raise KeyError(f"Column '{x}' not found. Available: {list(data.columns)}")

# Bad
raise KeyError("Column not found")
```

### CQ-005: No Magic Numbers (4 points, Low)

```python
# Good
def create_plot(..., size: float = 50):
    ax.scatter(x, y, s=size)

# Bad
ax.scatter(x, y, s=50)  # What is 50?
```

---

## Correctness

### CR-001: Data Accurate (10 points, Critical)

- Correct columns used
- No X/Y confusion

### CR-002: Spec Compliance (10 points, Critical)

- All required parameters implemented
- All optional parameters with defaults

### CR-003: Edge Cases (5 points, Medium)

- Empty data → ValueError
- NaN values → Graceful handling

---

## Scoring Formula

```
Start: 50 points

For each criterion MET: +weight
For each criterion FAILED: -weight
N/A criteria: 0

Result: Clamp between 0-100
```

**Example**:
```
50 (base)
+10 (axes_labeled)
+5  (grid_subtle)
+8  (elements_clear)
+9  (no_overlap)
+7  (legend)
-6  (colorblind FAILED)
+4  (figure_size)
= 87 → PASS
```
