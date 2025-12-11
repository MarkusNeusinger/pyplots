# bar-stacked: Stacked Bar Chart

## Description

A stacked bar chart displays multiple data series stacked vertically on top of each other within single bars. Each segment represents a sub-category's contribution to the total, making it ideal for showing part-to-whole relationships across categories. Commonly used for time-series data like monthly breakdowns where you want to see both individual components and totals.

## Applications

- Tracking monthly revenue breakdown by product line or region
- Showing budget allocation across departments over quarters
- Visualizing website traffic sources (organic, paid, referral) by month
- Displaying inventory levels by category over time periods

## Data

- `period` (categorical/datetime) - time periods or categories for the x-axis (e.g., months)
- `category` (categorical) - sub-categories that form the stacked segments
- `value` (numeric) - values determining segment heights
- Size: 6-12 time periods, 2-5 stacked categories
- Example: monthly sales data with 3-4 product categories
