# Code Style and Conventions

## Python Style (API, Core, Tests)
- **Linter/Formatter**: Ruff (enforces PEP 8)
- **Line Length**: 120 characters
- **Type Hints**: Required for all functions
- **Docstrings**: Google style for all public functions
- **Import Order**: Standard library → Third-party → Local

### Example (for API/core code):
```python
def get_spec_by_id(spec_id: str, db: Session) -> Spec:
    """
    Retrieve a spec by its ID.

    Args:
        spec_id: The unique spec identifier
        db: Database session

    Returns:
        Spec object if found

    Raises:
        NotFoundError: If spec doesn't exist
    """
    pass
```

## Plot Implementation Style (KISS)
Plot implementations should be simple, readable scripts - like matplotlib gallery examples:

```python
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
ax.scatter(x, y, alpha=0.7, s=50, color='#306998')

ax.set_xlabel('X Value')
ax.set_ylabel('Y Value')
ax.set_title('Basic Scatter Plot')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
```

### Plot Code Rules:
- No functions, no classes
- No `if __name__ == '__main__':`
- No type hints or docstrings (in plot code)
- Just: imports → data → plot → save

## Naming Conventions

### Spec IDs
Format: `{plot-type}-{variant}-{modifier}` (lowercase, hyphens only)
- `scatter-basic` - Simple 2D scatter plot
- `bar-grouped-horizontal` - Horizontal grouped bars
- `heatmap-correlation` - Correlation matrix heatmap

### Files
- Implementation files: `{library}.py` (e.g., `matplotlib.py`)
- Metadata files: `{library}.yaml`

## General Rules
- Always write in English
- Testing coverage target: 90%+
- Test naming: `test_{what_it_does}`
