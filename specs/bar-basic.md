# bar-basic: Basic Bar Chart

<!--
Spec Template Version: 1.0.0
Created: 2025-01-25
Last Updated: 2025-01-25
-->

**Spec Version:** 1.0.0

## Description

Create a simple bar chart showing values for different categories.
Perfect for comparing discrete values across categories, displaying rankings, and showing composition.
Works with any dataset containing categorical and numeric columns.

## Data Requirements

- **x**: Category labels (categorical: strings or column name)
- **y**: Numeric values for each category (numeric: continuous values)

## Optional Parameters

- `color`: Bar color or column name for color mapping (type: string or column name, default: "steelblue")
- `alpha`: Transparency level (type: float 0.0-1.0, default: 0.8)
- `title`: Plot title (type: string, default: None)
- `xlabel`: Custom x-axis label (type: string, default: column name)
- `ylabel`: Custom y-axis label (type: string, default: column name)
- `figsize`: Figure size (type: tuple, default: (10, 6))

## Quality Criteria

- [ ] X and Y axes are labeled with column names (or custom labels if provided)
- [ ] Grid is visible but subtle with alpha=0.3 on y-axis only
- [ ] Bars are clearly distinguishable with appropriate width and spacing
- [ ] No overlapping axis labels or tick marks
- [ ] Legend is shown if color mapping is used
- [ ] Colorblind-safe colors when color mapping is used (use colormap like 'tab10' or 'Set2')
- [ ] Appropriate figure size (10x6 inches default) for readability
- [ ] Title is centered and clearly readable if provided (fontsize 14, bold)

## Expected Output

A clean bar chart with clearly visible bars showing values for each category.
The plot should be immediately understandable without additional explanation.
Grid lines on the y-axis should help with reading values without overpowering the data.
If color mapping is used, the legend should clearly indicate what each color represents.
All text elements (labels, title, legend, and tick labels) should be legible at standard display sizes.

## Tags

comparison, categorical, basic, bar, distribution, statistical, exploratory

## Use Cases

- Sales comparison across product categories (e.g., revenue by product line)
- Population statistics by region or country (e.g., top 10 countries by population)
- Survey results visualization (e.g., satisfaction scores by category)
- Performance metrics across teams (e.g., sales by department)
- Rating or score distribution (e.g., product ratings by star category)
- Time-based comparison (e.g., monthly sales totals)
