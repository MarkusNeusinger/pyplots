# slider-control-basic: Interactive Plot with Slider Control

## Description

An interactive visualization featuring a slider widget that allows users to dynamically control a parameter such as filtering data by year, adjusting a threshold value, or changing a coefficient. As the slider moves, the plot updates in real-time to reflect the new parameter value, enabling intuitive exploration of how variables affect the visualization. This pattern is fundamental for dashboards and exploratory data analysis where users need to understand parameter sensitivity.

## Applications

- Filtering sales data by year or quarter to see trends across different time periods
- Adjusting a threshold value to visualize how many data points fall above/below different cutoffs
- Exploring model behavior by changing a parameter like polynomial degree or smoothing factor

## Data

- `x` (numeric/categorical) - Independent variable or categories for the visualization
- `y` (numeric) - Dependent variable or values to be plotted
- `parameter` (numeric) - The value controlled by the slider (e.g., year, threshold, coefficient)
- Size: 50-500 points per parameter value
- Example: Time series data with multiple years, scatter data with adjustable threshold line

## Notes

- Slider should have clear min/max labels and current value display
- Updates should be smooth and responsive (no lag on slider movement)
- Consider showing the current parameter value prominently near the slider
- For time-based filtering, include play/pause animation option if supported
- Ensure the slider range covers meaningful values for the data
