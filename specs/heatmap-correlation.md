# heatmap-correlation

## Title
Correlation Matrix Heatmap

## Description
Display a correlation matrix as a heatmap showing pairwise correlations between numeric variables. The plot shows correlation coefficients as colors with values annotated in each cell.

## Required Parameters
- `data`: DataFrame with numeric columns to correlate

## Optional Parameters
- `cmap`: str = 'coolwarm' - Diverging colormap (blue-white-red)
- `annotate`: bool = True - Show correlation values in cells
- `fmt`: str = '.2f' - Format for annotations
- `vmin`: float = -1.0 - Minimum value for color scale
- `vmax`: float = 1.0 - Maximum value for color scale
- `center`: float = 0.0 - Center point for diverging colormap
- `square`: bool = True - Make cells square-shaped
- `cbar_label`: str = 'Correlation' - Label for color bar
- `figsize`: tuple = (10, 8) - Figure size (width, height)
- `font_size`: int = 10 - Font size for annotations

## Requirements
- Calculate correlation matrix from input data
- Use diverging color scheme centered at 0
- Display correlation values in cells when annotate=True
- Show variable names as axis labels
- Include color bar with label
- Handle NaN values in data gracefully

## Example Usage
```python
# Sample data with correlated variables
import pandas as pd
import numpy as np

np.random.seed(42)
n = 100
data = pd.DataFrame({
    'Temperature': np.random.normal(25, 5, n),
    'Ice_Cream_Sales': np.random.normal(25, 5, n) * 2 + np.random.normal(0, 5, n),
    'Beach_Visitors': np.random.normal(25, 5, n) * 1.5 + np.random.normal(0, 8, n),
    'Sunscreen_Sales': np.random.normal(25, 5, n) * 1.2 + np.random.normal(0, 4, n),
    'AC_Usage': np.random.normal(25, 5, n) * 0.8 + np.random.normal(0, 3, n)
})

# Create heatmap
fig = create_plot(data)
```

## Visual Expectations
- Clear cell boundaries with square cells
- Readable text annotations (if enabled)
- Color scale centered at 0 (white)
- Negative correlations in blue tones
- Positive correlations in red tones
- Variable names clearly visible on both axes
- Color bar showing correlation scale