# scatter-brush-zoom: Interactive Scatter Plot with Brush Selection and Zoom

## Description

An interactive scatter plot enabling brush selection (click and drag to select a rectangular region) and zoom functionality. Users can draw selection boxes to highlight or filter data points, zoom into specific areas for detailed analysis, and use the selection to trigger downstream actions like filtering or linked views. This interaction pattern is fundamental for exploratory data analysis and brushing-and-linking visualizations.

## Applications

- Exploratory data analysis where users need to select outliers or clusters for further investigation
- Linked-view dashboards where brushing on a scatter plot filters data in other charts
- Financial analysis selecting specific time periods and value ranges from large datasets
- Scientific data exploration identifying regions of interest in multi-dimensional datasets

## Data

- `x` (numeric) - Values for the horizontal axis
- `y` (numeric) - Values for the vertical axis
- `color` (categorical, optional) - Category for color-coding different groups
- `label` (string, optional) - Point labels for identification
- Size: 50-1000 points (interactivity handles larger datasets well)
- Example: Simulated 2D data with multiple clusters or real dataset with continuous variables

## Notes

- Brush selection should draw a visible rectangle while dragging
- Selected points should be visually highlighted (color change, opacity, or border)
- Zoom can be triggered via mouse wheel, double-click, or toolbar buttons
- Include a reset/clear selection button to deselect all points
- For libraries supporting linked selections, demonstrate how selection state can be accessed
- Pan functionality should be available when zoomed in
- Consider showing count of selected points in a status area
