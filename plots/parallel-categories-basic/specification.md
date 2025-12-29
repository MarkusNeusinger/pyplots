# parallel-categories-basic: Basic Parallel Categories Plot

## Description

A parallel categories plot visualizes categorical data across multiple dimensions, with vertical axes representing each categorical variable and ribbons connecting categories to show observation flow. Unlike parallel coordinates (which use lines for numeric data), parallel categories use width-proportional ribbons to show counts or frequencies, making it ideal for understanding how categorical values co-occur and flow across multiple classification dimensions.

## Applications

- Analyzing customer journey paths from acquisition channel through product category to purchase outcome
- Visualizing survey response patterns across multiple demographic or preference questions
- Exploring classification results showing predicted vs actual categories with feature breakdowns
- Understanding multi-stage process flows like support ticket routing through departments

## Data

- `dimension_1` through `dimension_n` (categorical) - Multiple categorical variables for each observation
- `count` (numeric, optional) - Observation count or weight for aggregated data
- Size: 3-6 categorical dimensions, each with 2-8 unique values
- Example: Titanic survival data with class, sex, age group, and survival status

## Notes

- Ribbon width should be proportional to observation count or frequency
- Color by first dimension (source) or last dimension (outcome) for clarity
- Interactive highlighting helps trace paths through multiple categories
- Consider ordering categories within each dimension to minimize ribbon crossings
- Too many categories per dimension reduces readability; aggregate rare values if needed
