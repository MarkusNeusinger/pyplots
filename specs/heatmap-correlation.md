# heatmap-correlation

Correlation matrix heatmap showing pairwise correlations between variables.

## Requirements

### Data
- Input: DataFrame with 4-6 numeric columns
- Calculate correlation matrix from input data
- Use sample data with correlated variables for testing

### Parameters

#### Required
- `data`: pd.DataFrame - Input data with numeric columns

#### Optional
- `method`: str = 'pearson' - Correlation method ('pearson', 'spearman', 'kendall')
- `cmap`: str = 'RdBu_r' - Diverging colormap (blue-white-red)
- `vmin`: float = -1 - Minimum value for color scale
- `vmax`: float = 1 - Maximum value for color scale
- `show_values`: bool = True - Display correlation values in cells
- `fmt`: str = '.2f' - Format string for values
- `title`: str = None - Optional plot title
- `cbar_label`: str = 'Correlation' - Label for color bar

### Visual Requirements
- Diverging color scheme centered at 0
- Square cells with clear boundaries
- Variable names as axis labels (both x and y)
- Color bar legend showing scale from -1 to 1
- Values displayed in each cell (white text for dark cells, black for light)
- Grid lines between cells

### Sample Data
Generate synthetic data with known correlations:
- 4-6 variables (e.g., 'A', 'B', 'C', 'D', 'E')
- Mix of strong positive, negative, and weak correlations
- At least 50 data points for reliable correlation estimates

### Expected Output
- Heatmap with correlation matrix
- Values ranging from -1 (strong negative) to 1 (strong positive)
- Diagonal values = 1 (self-correlation)
- Symmetric matrix (correlation is symmetric)