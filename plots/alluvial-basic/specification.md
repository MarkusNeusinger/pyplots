# alluvial-basic: Basic Alluvial Diagram

## Description

An alluvial diagram visualizes how entities flow or transition between discrete categories across multiple time points or ordered stages. Unlike general Sankey diagrams, alluvial diagrams enforce strict vertical ordering where each column represents a specific time step or category dimension. Bands connect related segments to show how proportions shift over time, making it ideal for tracking structural changes, migrations, and transitions in categorical data.

## Applications

- Tracking voter migration between political parties across multiple election cycles
- Visualizing customer journey stages from acquisition through retention or churn
- Showing how students transition between academic tracks or performance categories over semesters

## Data

- `time_point` (categorical/ordinal) - discrete time steps or ordered stages (columns)
- `category` (categorical) - the category or state at each time point
- `value` (numeric) - count or proportion of entities in each category at each time point
- `flow` (numeric) - magnitude of transition between categories across time points
- Size: 3-6 time points, 3-8 categories per time point
- Example: Election data with years as time points, parties as categories, and voter counts as values

## Notes

- Time points should be arranged left-to-right in chronological or logical order
- Use consistent colors for categories that persist across time points
- Band width should be proportional to flow magnitude
- Consider using transparency for overlapping flows to improve readability
- Labels should clearly identify both time points (column headers) and categories (node labels)
