# box-basic: Basic Box Plot

## Description

A box-and-whisker plot comparing statistical distributions across multiple groups. Each box displays quartiles (Q1, median, Q3), whiskers extend to show the data range within 1.5×IQR, and outliers appear as individual points. Excellent for comparing distributions and identifying outliers without assuming normality.

## Data

**Required columns:**
- `group` (categorical) - category labels for each box
- `value` (numeric) - values for distribution analysis

**Example:**
```python
import pandas as pd
import numpy as np
np.random.seed(42)
data = pd.DataFrame({
    'group': ['A']*50 + ['B']*50 + ['C']*50 + ['D']*50,
    'value': np.concatenate([
        np.random.normal(50, 10, 50),
        np.random.normal(60, 15, 50),
        np.random.normal(45, 8, 50),
        np.random.normal(70, 20, 50)
    ])
})
```

## Tags

box, distribution, comparison, statistical, categorical

## Use Cases

- Comparing performance metrics across different teams or departments
- Analyzing price distributions across product categories
- Examining test scores across different classes or schools
- Visualizing response times across server regions
