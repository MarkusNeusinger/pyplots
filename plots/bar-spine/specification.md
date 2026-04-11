# bar-spine: Spine Plot for Two-Variable Proportions

## Description

A spine plot (spineplot) is a stacked bar chart where bar widths are proportional to the marginal frequency of one categorical variable and the subdivisions within each bar show the conditional distribution of a second categorical variable. All bars are normalized to the same height (100%), so visual comparison focuses on how the conditional proportions shift across categories. It is a one-dimensional specialization of mosaic plots and excels at revealing associations between two categorical variables in contingency table data.

## Applications

- Showing survival rates across passenger classes in the Titanic dataset
- Visualizing disease prevalence across demographic age groups
- Displaying customer churn rates segmented by subscription tier
- Comparing pass/fail rates across different experimental test conditions

## Data

- `x_category` (categorical) - Primary categorical variable that determines bar width (marginal frequency)
- `fill_category` (categorical) - Secondary categorical variable shown as stacked segments within each bar
- `count` (integer) - Frequency count for each combination of x_category and fill_category
- Size: 3-8 x-categories, 2-5 fill categories for readability
- Example: Titanic survival data with passenger class as x_category, survival status as fill_category, and passenger counts

## Notes

- Bar width must be proportional to the marginal count of each x_category
- Segments within each bar represent conditional proportions of fill_category (heights sum to 100%)
- All bars share the same total height (normalized to 100%)
- Bars should be adjacent with no gaps to emphasize the continuous proportion axis
- Use distinct colors for each fill_category with a clear legend
- X-axis labels should be centered under each variable-width bar
- Consider adding percentage labels within segments when space permits
- Complements the existing mosaic-categorical spec as a simpler 1D alternative
