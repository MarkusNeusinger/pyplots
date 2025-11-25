# pie-basic-labeled: Basic Pie Chart with Labels

<!--
Spec Template Version: 1.0.0
Created: 2025-01-25
Last Updated: 2025-01-25
-->

**Spec Version:** 1.0.0

## Description

Create a simple pie chart showing the composition of categorical data. Labels display both category names and values.
Perfect for showing proportions and parts-to-whole relationships in data.
Works with any dataset containing categorical and numeric columns.

## Data Requirements

- **values**: Numeric values for each slice (numeric: positive continuous values)
- **labels**: Category labels for each slice (categorical: strings or column names)

## Optional Parameters

- `colors`: List of colors for slices or column name for color mapping (type: list/string, default: None - use default palette)
- `autopct`: String format for displaying percentages (type: string, default: "%1.1f%%")
- `startangle`: Starting angle for the pie chart (type: float, default: 0)
- `explode`: Offset for slices to separate them (type: list of floats, default: None)
- `title`: Plot title (type: string, default: None)
- `figsize`: Figure size (type: tuple, default: (8, 8))

## Quality Criteria

- [ ] All slice labels are clearly visible and readable
- [ ] Percentages are displayed next to or inside slices and formatted to 1 decimal place
- [ ] Slices are distinguishable with different colors (colorblind-safe palette recommended)
- [ ] No overlapping text labels (labels should be positioned with appropriate distance)
- [ ] Legend is shown with all category names if labels are too small to fit inside
- [ ] Title is centered and clearly readable if provided
- [ ] Appropriate figure size (8x8 inches default) for readability
- [ ] All slices sum to a valid percentage (approximately 100%)

## Expected Output

A clean pie chart with clearly visible slices representing the composition of the data.
Each slice should be labeled with both the category name and its percentage of the total.
The chart should be immediately understandable, clearly showing the proportions of each category.
All text elements should be legible and properly positioned to avoid overlaps.
Color choices should make it easy to distinguish between different slices, including for colorblind viewers.

## Tags

composition, categorical, basic, pie, distribution, statistical, exploratory

## Use Cases

- Market share breakdown by company or product (e.g., smartphone market share by brand)
- Budget allocation across departments or categories (e.g., spending by expense category)
- Survey results with categorical responses (e.g., customer satisfaction breakdown)
- Sales distribution across regions (e.g., revenue percentage by geography)
- User engagement metrics by type (e.g., app usage by feature)
- Population demographics (e.g., age group distribution or gender breakdown)
