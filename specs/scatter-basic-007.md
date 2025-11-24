# scatter-basic-007: Financial Categories Bar Chart

<!--
Spec Template Version: 1.0.0
Created: 2025-11-24
Last Updated: 2025-11-24
-->

**Spec Version:** 1.0.0

## Description

Create a bar chart displaying financial categories with their corresponding values.
This visualization is designed to show categorical financial data such as expense categories,
revenue streams, budget allocations, or portfolio distributions. The chart provides clear
visual comparison between different financial categories.

## Data Requirements

- **categories**: List of financial category names (type: list of strings)
- **values**: Corresponding monetary values for each category (type: list of numeric)

## Optional Parameters

- `color`: Bar color or list of colors (type: string or list, default: "steelblue")
- `currency`: Currency symbol to display (type: string, default: "$")
- `title`: Chart title (type: string, default: "Financial Categories")
- `xlabel`: Custom x-axis label (type: string, default: "Categories")
- `ylabel`: Custom y-axis label (type: string, default: "Amount")
- `orientation`: Bar orientation (type: string, options: "vertical" or "horizontal", default: "vertical")
- `show_values`: Display values on bars (type: bool, default: True)

## Quality Criteria

- [ ] All category labels are visible and readable (rotate if necessary)
- [ ] Y-axis shows currency formatting with appropriate scale
- [ ] Bars are clearly separated with appropriate width
- [ ] Values are displayed on top/end of bars if show_values is True
- [ ] Grid lines present for value axis (alpha=0.3, dashed)
- [ ] Colors are professional and suitable for financial reports
- [ ] Figure size appropriate for number of categories (10x6 default)
- [ ] Title is centered and professional (fontsize 14, bold)
- [ ] No overlapping labels or values
- [ ] Negative values clearly distinguished (red color or pattern)

## Expected Output

A professional bar chart suitable for financial reports and presentations.
Each bar should clearly represent a financial category with its corresponding value.
The chart should be immediately understandable with proper labeling and formatting.
Currency values should be formatted appropriately (e.g., $1,234.56 or $1.2M for large values).
If there are many categories (>10), consider horizontal orientation for better readability.

## Tags

finance, categories, bar chart, budget, expenses, revenue, categorical, comparison

## Use Cases

- Monthly expense breakdown by category
- Revenue distribution across business segments
- Budget allocation visualization
- Investment portfolio composition
- Department spending comparison
- Product sales by category
- Cost center analysis
- Financial KPI dashboard component