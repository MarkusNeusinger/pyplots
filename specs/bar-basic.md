# bar-basic: Basic Bar Chart

A fundamental vertical bar chart that visualizes categorical data with numeric values, ideal for comparing quantities across discrete categories.

## Description

A basic bar chart displays rectangular bars with heights proportional to the values they represent. Each bar corresponds to a category, with the bar height indicating the numeric value for that category. This chart type is essential for comparing values across distinct groups and is one of the most widely used visualization types for categorical comparisons.

## Data Requirements

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| category | string | Yes | Category labels for the x-axis (e.g., product names, regions) |
| value | numeric | Yes | Numeric values determining bar heights |

## Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| figsize | tuple | (10, 6) | Figure size as (width, height) |
| color | string | "steelblue" | Bar fill color |
| edgecolor | string | "black" | Bar edge color |
| alpha | float | 0.8 | Transparency level for bars |
| title | string | None | Plot title |
| xlabel | string | None | X-axis label (defaults to column name) |
| ylabel | string | None | Y-axis label (defaults to column name) |
| rotation | int | 0 | Rotation angle for x-axis labels |

## Quality Criteria

- [ ] X-axis displays category labels clearly without overlap
- [ ] Y-axis shows numeric scale with appropriate tick marks
- [ ] Both axes are labeled (custom or column names)
- [ ] Grid lines are visible but subtle (alpha ≤ 0.3) on y-axis only
- [ ] Bars have consistent width and spacing
- [ ] Bar colors are distinguishable from background
- [ ] Title is present when specified
- [ ] No visual clutter or overlapping elements
- [ ] Y-axis starts at zero to avoid misleading representation

## Expected Output

A clean vertical bar chart where each category is represented by a rectangular bar. The bars should be evenly spaced along the x-axis with category labels beneath them. The y-axis should display a numeric scale starting from zero with subtle horizontal grid lines for easy value reading. The chart should have a professional appearance with proper margins, readable fonts, and a balanced layout. When there are many categories, the x-axis labels should be rotated to prevent overlap.

## Example Data

```python
import pandas as pd

data = pd.DataFrame({
    'category': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
    'value': [45, 78, 52, 91, 63]
})

fig = create_plot(data, 'category', 'value', title='Sales by Product')
```

## Tags

bar, comparison, categorical, basic, 1d

## Use Cases

- Comparing sales figures across different product categories in retail analytics
- Displaying survey response counts for multiple-choice questions
- Showing population counts across different age groups or regions
- Visualizing budget allocation across departments in business reporting
- Presenting test scores or performance metrics across different groups
- Comparing website traffic or user engagement metrics across pages

## Implementation Notes

- Handle long category labels gracefully (rotation or truncation)
- Validate that category column contains appropriate categorical data
- Ensure value column is numeric and handle missing values
- Y-axis should always start at zero for accurate visual comparison
- Bar width should be proportional to available space
