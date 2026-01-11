# mosaic-categorical: Mosaic Plot for Categorical Association Analysis

## Description

A mosaic plot visualizes contingency tables by dividing a rectangular area into smaller rectangles whose areas are proportional to cell frequencies. This statistical visualization technique effectively shows relationships and associations between two or more categorical variables, making it easy to identify patterns, dependencies, and deviations from expected frequencies in cross-tabulated data.

## Applications

- Analyzing survey response patterns across demographic groups
- Exploring relationships between categorical variables in social science research
- Visualizing contingency tables in medical studies (treatment vs outcome)
- Examining association between product categories and customer segments

## Data

- `category_1` (categorical) - First categorical variable (rows in contingency table)
- `category_2` (categorical) - Second categorical variable (columns in contingency table)
- `frequency` (numeric, optional) - Count or frequency for each combination; if omitted, computed from data
- Size: Typically 2-6 levels per categorical variable for readability
- Example: Titanic survival data cross-tabulated by class and survival status

## Notes

- Rectangle widths represent marginal proportions of the first variable
- Rectangle heights within each column represent conditional proportions of the second variable
- Area of each rectangle is proportional to the cell frequency in the contingency table
- Use statsmodels.graphics.mosaicplot for the core visualization
- Color coding can indicate residuals or deviations from independence
- Gap spacing between rectangles helps distinguish categories
- Labels should identify both categorical variables clearly
