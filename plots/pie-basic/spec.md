# pie-basic: Basic Pie Chart

## Description

A circular chart divided into slices showing proportions of a whole. Each slice represents a category's share relative to the total, making it ideal for displaying composition and percentage breakdowns. Best suited for a small number of categories (3-7) where the focus is on part-to-whole relationships.

## Data

**Required columns:**
- `category` (categorical) - names for each slice
- `value` (numeric) - values representing each category's proportion

**Example:**
```python
import pandas as pd
data = pd.DataFrame({
    'category': ['Product A', 'Product B', 'Product C', 'Product D', 'Other'],
    'value': [35, 25, 20, 15, 5]
})
```

## Tags

pie, composition, proportions, categorical, basic

## Use Cases

- Market share distribution showing company percentages
- Budget allocation breakdown across departments
- Survey response analysis showing answer percentages
- Portfolio composition showing asset allocation
