# range-interval: Range Interval Chart

## Description

A range interval chart displays min-max ranges or intervals as vertical or horizontal bars/segments for each category, making it ideal for visualizing uncertainty bounds, confidence intervals, or value spreads. Unlike error bars which extend from a central data point, range intervals show the full span between two values as a filled bar or line segment, emphasizing the range itself rather than deviation from a center. This visualization excels at comparing ranges across multiple categories simultaneously.

## Applications

- Displaying temperature ranges (daily high/low) across months or locations
- Comparing salary ranges by job title or department
- Showing confidence intervals for statistical estimates across groups
- Visualizing stock price ranges (high/low) over multiple periods

## Data

- `category` (categorical) - Labels for each range group
- `min_value` (numeric) - Lower bound of the range/interval
- `max_value` (numeric) - Upper bound of the range/interval
- Size: 5-25 categories for optimal readability
- Example: Monthly temperature ranges with minimum and maximum values per month

## Notes

- Use horizontal orientation when category labels are long
- Sort categories by range size, midpoint, or logical order (e.g., chronological)
- Consider adding markers at min/max endpoints for emphasis
- Semi-transparent fill or distinct colors help differentiate overlapping ranges
- Optional: show midpoint markers or reference lines for context
