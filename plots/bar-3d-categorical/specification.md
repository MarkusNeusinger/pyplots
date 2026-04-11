# bar-3d-categorical: 3D Bar Chart for Categorical Comparison

## Description

A three-dimensional bar chart where bars rise from a 2D categorical grid, with height encoding the measured value. Two categorical axes define the grid position on the base plane while the vertical axis shows magnitude. This visualization extends the bar chart family into 3D space, making it effective for comparing values across two categorical dimensions simultaneously.

## Applications

- Comparing sales figures across product categories and geographic regions simultaneously
- Displaying survey responses across two demographic dimensions (e.g., age group vs education level)
- Showing experimental results with two categorical factors in factorial designs
- Visualizing frequency tables or cross-tabulations with two grouping variables

## Data

- `x_category` (str) - first categorical dimension (e.g., product type, region)
- `y_category` (str) - second categorical dimension (e.g., time period, segment)
- `value` (float) - bar height representing the measured quantity
- Size: 3-10 categories per axis, forming a grid of 9-100 bars

## Notes

- Bars should have slight spacing between them for visual clarity and depth perception
- Color can encode the value magnitude or a third categorical variable
- Viewing angle should be adjustable; a default elevation of ~30 degrees and azimuth of ~45 degrees provides good readability
- Grid lines on the base plane help relate bars to their categorical positions
- Consider adding value labels on top of bars when the grid is small (under 25 bars)
- A color bar or legend should indicate the mapping when color encodes a variable
