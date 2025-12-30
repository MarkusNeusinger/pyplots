# subplot-grid-custom: Custom Subplot Grid Layout

## Description

A flexible subplot grid allowing multiple different plot types arranged in a custom grid layout with non-uniform cell sizes. Unlike regular subplot grids with uniform cells, this layout supports cells that span multiple rows and/or columns, enabling complex dashboard-style visualizations where some plots require more visual real estate than others.

## Applications

- Executive dashboards with a large overview chart and smaller detail panels
- Scientific publications combining a main visualization with supporting annotations
- Financial reports with a primary price chart spanning multiple columns alongside volume and indicator panels
- Data exploration layouts with a large scatter matrix and smaller summary statistics plots

## Data

- `x` (numeric or categorical) - Primary variable for each subplot
- `y` (numeric) - Secondary variable for each subplot
- `z` (numeric, optional) - Tertiary variable for 3D or color-mapped subplots
- Size: Varies per subplot, typically 20-500 points per cell
- Example: Dashboard with main time series (spanning 2 columns), volume bar chart, and returns histogram

## Notes

- Support GridSpec-style layouts with colspan and rowspan parameters
- Allow cells to span multiple rows (e.g., a tall sidebar plot)
- Allow cells to span multiple columns (e.g., a wide header plot)
- Maintain consistent spacing and alignment despite varied cell sizes
- Clear visual hierarchy with larger plots for primary data and smaller for supporting views
- Example grid pattern: one 2x2 cell for main plot, four 1x1 cells for detail views
