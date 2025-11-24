# scatter-basic-006: Multiple Scatter Plots in Single Figure

## Description
Create a figure with three scatter plots showing the relationship between x and three different y variables (y1, y2, y3) in a single visualization. This demonstrates how to compare multiple relationships using scatter plots.

## Requirements
- Display three scatter plots in one figure
- Plot x vs y1, x vs y2, and x vs y3
- Use different colors for each scatter plot series
- Include a legend to distinguish between the three series
- Add grid for better readability
- Use appropriate labels and title

## Data Format
The plot should work with:
- A single x variable (numeric array)
- Three y variables: y1, y2, y3 (numeric arrays of same length as x)
- All arrays should be of the same length

## Visual Elements
- **Figure size**: 10x6 inches
- **Point size**: 50 (for visibility)
- **Alpha**: 0.7 (for slight transparency to show overlaps)
- **Colors**: Different for each series (e.g., blue for y1, orange for y2, green for y3)
- **Grid**: Enabled with alpha=0.3
- **Legend**: Upper right corner
- **Title**: "Multiple Scatter Plots: x vs y1, y2, y3"
- **X-axis label**: "X Values"
- **Y-axis label**: "Y Values"

## Example Use Case
This type of visualization is useful when comparing how one independent variable relates to multiple dependent variables, such as:
- Temperature vs different atmospheric measurements
- Time vs multiple stock prices
- Distance vs various performance metrics