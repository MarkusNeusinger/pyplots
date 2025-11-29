# heatmap-correlation

Correlation matrix heatmap showing pairwise correlations between variables

## Requirements

### Data
- DataFrame with 4-6 numeric variables suitable for correlation analysis
- Compute correlation matrix using pandas `.corr()` method

### Visual
- Display correlation coefficients (-1 to 1) as colors
- Use diverging color scheme (blue-white-red)
- Show correlation values in cells (formatted to 2 decimal places)
- Variable names as axis labels
- Color bar legend showing the scale
- Clear cell boundaries
- Readable text annotations
- Color scale centered at 0

### Parameters

#### Required
- `data`: pd.DataFrame - Input data with numeric columns to correlate

#### Optional
- `cmap`: str = 'RdBu_r' - Colormap for the heatmap (diverging)
- `annot`: bool = True - Whether to show values in cells
- `fmt`: str = '.2f' - Format for cell annotations
- `vmin`: float = -1.0 - Minimum value for color scale
- `vmax`: float = 1.0 - Maximum value for color scale
- `cbar_label`: str = 'Correlation' - Label for color bar
- `title`: str = None - Optional plot title

## Sample Data

```python
import pandas as pd
import numpy as np

np.random.seed(42)
n = 100

data = pd.DataFrame({
    'Temperature': np.random.normal(20, 5, n),
    'Humidity': np.random.normal(60, 10, n),
    'Pressure': np.random.normal(1013, 10, n),
    'Wind Speed': np.random.normal(10, 3, n),
    'Rainfall': np.random.normal(5, 2, n)
})

# Add correlations
data['Humidity'] = 100 - data['Temperature'] * 1.5 + np.random.normal(0, 5, n)
data['Rainfall'] = data['Humidity'] * 0.1 + np.random.normal(0, 1, n)
data['Wind Speed'] = 15 - data['Pressure'] * 0.01 + np.random.normal(0, 2, n)
```

## Expected Output

A heatmap showing:
- 5x5 correlation matrix
- Values from -1 to 1 displayed in each cell
- Blue for negative correlations
- Red for positive correlations
- White for no correlation (0)
- Color bar on the right side
- Variable names on both axes