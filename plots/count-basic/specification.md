# count-basic: Basic Count Plot

## Description

A count plot displays the frequency of observations in each category of a categorical variable using vertical bars. Unlike a basic bar chart that requires pre-computed values, a count plot automatically counts occurrences from raw data. This makes it ideal for quick exploratory analysis of categorical distributions without manual aggregation.

## Applications

- Analyzing survey response distributions across multiple choice answers
- Visualizing the frequency of product categories in sales data
- Exploring class distributions in machine learning datasets before training

## Data

- `category` (categorical) - The categorical variable whose values will be counted
- Size: 3-20 unique categories recommended for readability
- Example: Survey responses (A/B/C/D), product types, customer segments, or any discrete categorical data

## Notes

- Bars should be sorted by frequency (descending) or kept in original/alphabetical order based on context
- Consider adding count labels on or above bars for precise reading
- Optional percentage annotations can show relative proportions
- Use consistent bar width and adequate spacing between categories
