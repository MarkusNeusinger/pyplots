# heatmap-correlation

A correlation heatmap displaying the correlation matrix between multiple numeric variables.

## Required Parameters

- `data` (pd.DataFrame): Input DataFrame with numeric columns to correlate
- `numeric_cols` (list[str], optional): List of numeric columns to include in correlation. If None, all numeric columns are used.

## Optional Parameters

- `method` (str): Correlation method ('pearson', 'spearman', 'kendall'). Default: 'pearson'
- `cmap` (str): Colormap for the heatmap. Default: 'coolwarm' or library-appropriate diverging colormap
- `annot` (bool): Whether to annotate cells with correlation values. Default: True
- `fmt` (str): Format string for annotations. Default: '.2f'
- `vmin` (float): Minimum value for colormap scale. Default: -1
- `vmax` (float): Maximum value for colormap scale. Default: 1
- `mask_upper` (bool): Whether to mask the upper triangle (redundant values). Default: False
- `title` (str, optional): Title for the plot

## Returns

- Figure/Chart object appropriate for the library

## Example Usage

```python
import pandas as pd
import numpy as np

# Generate sample data
np.random.seed(42)
data = pd.DataFrame({
    'temperature': np.random.normal(20, 5, 100),
    'humidity': np.random.normal(60, 10, 100),
    'pressure': np.random.normal(1013, 20, 100),
    'wind_speed': np.random.normal(10, 3, 100)
})

# Add some correlations
data['humidity'] += 0.5 * data['temperature']
data['pressure'] -= 0.3 * data['temperature']

# Create correlation heatmap
fig = create_plot(data)
```

## Visual Requirements

1. Square cells for proper correlation matrix display
2. Color scale centered at 0 (diverging colormap)
3. Clear labels for both axes showing variable names
4. Annotations showing correlation values (when enabled)
5. Colorbar with clear scale from -1 to 1
6. Professional appearance with subtle gridlines

## Data Validation

- Ensure DataFrame contains numeric columns
- Handle NaN values appropriately (exclude from correlation calculation)
- Minimum 2 numeric columns required for correlation
- Warn if DataFrame has fewer than 3 rows (unreliable correlations)