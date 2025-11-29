# heatmap-correlation: Correlation Matrix Heatmap

## Description
A correlation matrix heatmap showing pairwise correlations between variables. The heatmap visualizes correlation coefficients with colors and displays the actual values in each cell.

## Required Parameters
- **data**: Input DataFrame with numeric columns
- **variables**: List of column names to include in correlation matrix (if None, use all numeric columns)

## Optional Parameters
- **title**: Title for the plot (default: "Correlation Matrix")
- **figsize**: Figure size tuple (default: (10, 8))
- **cmap**: Color scheme name (default: "RdBu_r" for diverging blue-white-red)
- **vmin**: Minimum value for color scale (default: -1)
- **vmax**: Maximum value for color scale (default: 1)
- **annot**: Show values in cells (default: True)
- **fmt**: Format string for annotations (default: ".2f")
- **cbar**: Show color bar (default: True)

## Visual Requirements
- Display correlation coefficients (-1 to 1) as colors
- Use diverging color scheme (blue-white-red by default)
- Show values in cells with 2 decimal places
- Variable names as axis labels
- Color bar legend showing scale
- Clear cell boundaries
- Readable text annotations
- Color scale centered at 0
- Grid lines to separate cells

## Data Handling
- Compute correlation matrix using pandas corr() method
- Handle NaN values appropriately
- Support both Pearson correlation (default) and other methods

## Example Data
Generate sample data with 4-6 correlated variables for testing.