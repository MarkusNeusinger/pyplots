# bar-3d: 3D Bar Chart

## Description

A three-dimensional bar chart that displays categorical data with bars rising from a 2D plane into the third dimension. This visualization extends traditional bar charts by adding depth, making it useful for comparing values across two categorical dimensions simultaneously. The 3D perspective can reveal patterns in data grids that might be less obvious in 2D representations.

## Applications

- Comparing sales performance across multiple products and regions in business analytics
- Visualizing survey responses across demographic groups and question categories
- Displaying experimental results across multiple treatment conditions and time points

## Data

- `x` (categorical) - First categorical dimension (e.g., product names, regions)
- `y` (categorical) - Second categorical dimension (e.g., time periods, categories)
- `z` (numeric) - Height values for each bar representing the measured quantity
- Size: 3-10 categories per dimension recommended for clear visualization
- Example: Sales data grid with products on x-axis, quarters on y-axis, and revenue as bar height

## Notes

- Interactive rotation is highly beneficial for exploring the data from different angles (where library supports it)
- Consider using color gradients to reinforce the z-values for better depth perception
- Keep category counts moderate to avoid visual clutter and occlusion issues
- Transparent or semi-transparent bars can help reveal bars hidden behind taller ones
