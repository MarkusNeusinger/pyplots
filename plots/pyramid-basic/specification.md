# pyramid-basic: Basic Pyramid Chart

## Description

A pyramid chart displays two opposing horizontal bar charts that share a central axis, creating a pyramid or butterfly shape. This visualization is ideal for comparing two related metrics across the same categories, revealing asymmetries and patterns in bidirectional data. Most commonly used for population pyramids showing age-gender distributions.

## Applications

- Population demographics showing age distribution by gender
- Survey analysis comparing agree vs disagree responses
- Before/after comparisons across categories
- Market research comparing two competing products or segments

## Data

- `category` (categorical) - Shared categories for central axis (e.g., age groups)
- `value_left` (numeric) - Values for left-extending bars
- `value_right` (numeric) - Values for right-extending bars
- Size: 5-15 categories typical
- Example: Age groups with male and female population counts

## Notes

- Left bars extend from center to the left, right bars extend from center to the right
- Both sides should use symmetric axis scales for fair comparison
- Use distinct colors for each side (e.g., blue/pink for gender)
- Category labels should be placed along the central axis
- Include legend or title identifying what each side represents
