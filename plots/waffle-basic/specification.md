# waffle-basic: Basic Waffle Chart

## Description

A waffle chart displays proportions using a grid of equal-sized squares where colored squares represent parts of a whole. Each square typically represents 1% of the total, making it easy to count and compare values visually. It provides an intuitive alternative to pie charts, offering more accurate perception of proportions.

## Applications

- Visualizing survey results and polling data to show response distributions
- Displaying budget allocation across spending categories
- Tracking progress towards goals (e.g., fundraising at 73% of target)
- Showing demographic breakdowns in population studies

## Data

- `category` (categorical) - Category labels for each segment
- `value` (numeric) - Proportions or percentages for each category
- Size: 2-6 categories typical
- Note: Values should sum to 100 or be normalized to percentages

## Notes

- Standard grid is 10x10 (100 squares) where each square = 1%
- Use distinct, contrasting colors for each category
- Include a legend identifying categories with their percentages
- Round values to whole squares for clean visualization
