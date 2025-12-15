# dumbbell-basic: Basic Dumbbell Chart

## Description

A dumbbell chart (also called a connected dot plot or Cleveland dot plot) compares two values for each category by displaying two dots connected by a line. It effectively visualizes differences, changes, or ranges between two data points such as before/after comparisons, gaps, or min/max values. The connected dots make it easy to see both the magnitude and direction of change.

## Applications

- Before/after performance comparisons (e.g., test scores before and after training)
- Gap analysis between groups (e.g., salary differences by department or gender)
- Comparing metrics between two time periods (e.g., Q1 vs Q4 sales by region)
- Displaying ranges such as minimum and maximum values per category

## Data

- `category` (string) - Labels for each comparison group
- `start_value` (numeric) - The first/left data point value
- `end_value` (numeric) - The second/right data point value
- Size: 5-20 categories for optimal readability
- Example: Employee satisfaction scores before and after policy changes

## Notes

- Horizontal orientation preferred with categories on y-axis and values on x-axis
- Use distinct colors for start and end dots to differentiate the two values
- Sort by difference or one of the values to reveal patterns
- Connecting line should be thin and subtle to not overpower the dots
