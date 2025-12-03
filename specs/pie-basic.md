# pie-basic: Basic Pie Chart

A fundamental pie chart that visualizes proportions and percentages of categorical data as slices of a circular chart. Each slice represents a category's share of the whole, making it ideal for showing composition and distribution across a small number of categories.

## Data Requirements

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| category | string | Yes | Category names for each slice |
| value | numeric | Yes | Numeric values representing each category's proportion |

## Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| figsize | tuple | (10, 8) | Figure size as (width, height) |
| title | string | None | Plot title |
| colors | list | None | Custom color palette for slices |
| startangle | float | 90 | Starting angle for first slice (degrees from positive x-axis) |
| autopct | string | '%1.1f%%' | Format string for percentage labels |
| explode | list | None | Offset distances for each slice (0-0.1 typical) |
| shadow | bool | False | Add shadow effect for 3D appearance |
| labels | list | None | Custom labels (defaults to category names) |
| legend | bool | True | Display legend |
| legend_loc | string | 'best' | Legend location |

## Quality Criteria

- [ ] All slices are clearly distinguishable with sufficient color contrast
- [ ] Percentage labels are readable and do not overlap with slice boundaries
- [ ] Category labels or legend clearly identify each slice
- [ ] Percentages sum to approximately 100% (within rounding tolerance)
- [ ] Chart is circular (equal aspect ratio maintained)
- [ ] Small slices (< 5%) remain visible and labeled appropriately
- [ ] Color palette is colorblind-friendly
- [ ] Title is positioned clearly above the chart
- [ ] Legend does not overlap with the pie chart
- [ ] Type hints and input validation are present

## Expected Output

A circular pie chart divided into colored slices, where each slice's arc length is proportional to its value relative to the total. The chart should display:
- Clear slice boundaries with distinct colors for each category
- Percentage labels positioned inside or near each slice
- Category names either as direct labels, in a legend, or both
- A centered, balanced appearance with no visual distortion
- Professional styling with appropriate spacing between elements

The chart should be immediately readable, allowing viewers to quickly compare relative proportions and identify the largest and smallest categories.

## Tags

pie, composition, proportions, categorical, basic, 2d

## Use Cases

- Market share distribution showing company percentages in an industry
- Budget allocation breakdown displaying spending across departments
- Survey response analysis visualizing answer percentages
- Portfolio composition showing asset class distribution in investments
- Demographic breakdown displaying population segments by age or region
- Resource utilization showing time or capacity allocation across projects

## Example Data

```python
import pandas as pd

data = pd.DataFrame({
    'category': ['Product A', 'Product B', 'Product C', 'Product D', 'Other'],
    'value': [35, 25, 20, 15, 5]
})

fig = create_plot(data, 'category', 'value', title='Market Share Distribution')
```

## Implementation Notes

- Validate that values are non-negative
- Handle cases where values sum to zero gracefully
- Consider using a donut hole (wedgeprops) for modern aesthetics in some libraries
- For many categories (> 7), consider grouping small slices into "Other"
- Ensure aspect ratio is equal to prevent elliptical distortion
- Position percentage labels to avoid overlap, especially for small slices
