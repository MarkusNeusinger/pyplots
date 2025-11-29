# heatmap-correlation

## Title
Correlation Matrix Heatmap

## Description
Create a heatmap visualization showing pairwise correlations between multiple variables. Display correlation coefficients as colors with values annotated in cells.

## Required Parameters
- `data` (pd.DataFrame): Input data with numeric columns for correlation calculation
- `columns` (List[str], optional): Specific columns to include in correlation. If None, use all numeric columns

## Optional Parameters
- `method` (str): Correlation method ('pearson', 'spearman', 'kendall'). Default: 'pearson'
- `annot_format` (str): Format string for annotations. Default: '.2f'
- `cmap` (str): Colormap name. Default: 'RdBu_r' (diverging blue-white-red)
- `vmin` (float): Minimum value for color scale. Default: -1
- `vmax` (float): Maximum value for color scale. Default: 1
- `center` (float): Center value for diverging colormap. Default: 0
- `square` (bool): Make cells square. Default: True
- `linewidths` (float): Width of lines between cells. Default: 0.5
- `linecolor` (str): Color of lines between cells. Default: 'white'
- `cbar_label` (str): Label for colorbar. Default: 'Correlation'
- `title` (str): Title for the plot. Default: None
- `figsize` (Tuple[int, int]): Figure size in inches. Default: (10, 8)

## Returns
Figure object specific to the plotting library

## Data Characteristics
- Input should contain multiple numeric columns
- Columns may have different scales (correlation normalizes)
- Missing values handled via correlation calculation

## Visual Requirements
- Diverging color scheme centered at 0
- Values displayed in each cell
- Clear cell boundaries
- Color bar showing scale
- Variable names as tick labels on both axes
- Square cells for better readability

## Example Use Case
```python
# Create sample data with correlated features
import numpy as np
import pandas as pd

np.random.seed(42)
n = 100

data = pd.DataFrame({
    'temperature': np.random.normal(20, 5, n),
    'humidity': np.random.normal(60, 10, n),
    'pressure': np.random.normal(1013, 20, n),
    'wind_speed': np.random.normal(10, 3, n)
})

# Add correlations
data['humidity'] = 100 - 2 * data['temperature'] + np.random.normal(0, 5, n)
data['wind_speed'] = 0.5 * data['temperature'] + np.random.normal(0, 2, n)

# Generate heatmap
fig = create_plot(data)
```

## Implementation Notes
- Calculate correlation matrix from input data
- Handle both full dataset or subset of columns
- Ensure color scale is symmetric around 0
- Annotations should be readable (appropriate font size)
- Consider matrix size for layout (4-10 variables optimal)