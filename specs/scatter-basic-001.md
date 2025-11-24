# scatter-basic-001: Basic 2D Scatter Plot

<!--
Spec Template Version: 1.0.0
Created: 2025-01-24
Last Updated: 2025-01-24
-->

**Spec Version:** 1.0.0

## Description

Create a simple scatter plot showing the relationship between two numeric variables.
Perfect for correlation analysis, outlier detection, and exploring bivariate relationships.
Works with any dataset containing two numeric columns.

## Data Requirements

- **x**: Numeric values for x-axis (continuous or discrete)
- **y**: Numeric values for y-axis (continuous or discrete)

## Optional Parameters

- `color`: Point color (type: string or column name, default: "steelblue")
- `size`: Point size in pixels (type: numeric or column name, default: 50)
- `alpha`: Transparency level (type: float 0.0-1.0, default: 0.8)
- `title`: Plot title (type: string, default: None)
- `xlabel`: Custom x-axis label (type: string, default: column name)
- `ylabel`: Custom y-axis label (type: string, default: column name)

## Quality Criteria

- [ ] X and Y axes are labeled with column names (or custom labels if provided)
- [ ] Grid is visible but subtle with alpha=0.3 and dashed linestyle
- [ ] Points are clearly distinguishable with appropriate size (50px default)
- [ ] No overlapping axis labels or tick marks
- [ ] Legend is shown if color or size mapping is used
- [ ] Colorblind-safe colors when color mapping is used (use colormap like 'viridis' or 'tab10')
- [ ] Appropriate figure size (10x6 inches default) for readability
- [ ] Title is centered and clearly readable if provided (fontsize 14, bold)

## Expected Output

A clean 2D scatter plot with clearly visible points showing the correlation or distribution
between x and y variables. The plot should be immediately understandable without
additional explanation. Grid lines should help readability without overpowering the data.
If color or size mapping is used, the legend should clearly indicate what each variation
means. All text elements (labels, title, legend) should be legible at standard display sizes.

## Tags

correlation, bivariate, basic, 2d, statistical, exploratory, scatter

## Use Cases

- Correlation analysis between two variables (e.g., height vs weight in healthcare)
- Outlier detection in bivariate data (e.g., unusual transactions in finance)
- Pattern recognition in data (linear, quadratic, clusters - e.g., customer segmentation)
- Relationship visualization (e.g., price vs demand in economics)
- Quality control charts (e.g., measurement vs target in manufacturing)
- Scientific data exploration (e.g., temperature vs pressure in physics experiments)
