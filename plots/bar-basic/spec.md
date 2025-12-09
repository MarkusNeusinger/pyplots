# bar-basic: Basic Bar Chart

## Description

A fundamental vertical bar chart visualizing categorical data with numeric values. Each category is represented by a rectangular bar with height proportional to its value, making it ideal for comparing quantities across discrete groups. One of the most widely used chart types for categorical comparisons.

## Data

**Required columns:**
- `category` (categorical) - labels for each bar on the x-axis
- `value` (numeric) - values determining bar heights

**Example:**
```python
import pandas as pd
data = pd.DataFrame({
    'category': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
    'value': [45, 78, 52, 91, 63]
})
```

## Tags

bar, comparison, categorical, basic, 1d

## Use Cases

- Comparing sales figures across different product categories
- Displaying survey response counts for multiple-choice questions
- Showing population counts across different regions
- Visualizing budget allocation across departments
