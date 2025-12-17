# slope-basic: Basic Slope Chart (Slopegraph)

## Description

A slope chart (slopegraph) visualizes changes between two or more time points by connecting values with lines across vertical axes. It emphasizes the direction and magnitude of change rather than absolute values, making it ideal for spotting increases, decreases, and rank changes at a glance. This chart type excels at before/after comparisons and highlighting which items improved or declined.

## Applications

- Comparing company performance metrics between two fiscal years
- Showing student test score changes from pre-test to post-test
- Visualizing country rankings before and after a policy change
- Tracking product satisfaction ratings between survey periods

## Data

- `entity` (categorical) - Items being compared (e.g., countries, products, students)
- `value_start` (numeric) - Value at first time point
- `value_end` (numeric) - Value at second time point
- Size: 5-15 entities for optimal readability
- Example: Sales figures for 10 products comparing Q1 vs Q4

## Notes

- Labels should appear at both endpoints for entity identification
- Consider color coding lines by direction (increase vs decrease)
- Vertical axes should be labeled with time point names
- Avoid too many entities (>15) as lines become difficult to follow
