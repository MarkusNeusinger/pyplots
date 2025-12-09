# histogram-basic: Basic Histogram

## Description

A histogram showing the frequency distribution of numeric data across bins. Each bin represents a range of values, with bar height indicating how many data points fall within that range. Ideal for understanding data spread, identifying patterns, and detecting outliers in continuous distributions.

## Data

**Required columns:**
- `value` (numeric) - continuous values for distribution analysis

**Example:**
```python
import pandas as pd
import numpy as np
np.random.seed(42)
data = pd.DataFrame({
    'value': np.random.normal(100, 15, 500)  # 500 values, mean=100, std=15
})
```

## Tags

histogram, distribution, univariate, basic, statistical

## Use Cases

- Analyzing customer purchase amount distribution across transactions
- Visualizing test score distribution in educational assessments
- Understanding response time distribution in system performance data
- Examining income or salary distribution in demographic studies
