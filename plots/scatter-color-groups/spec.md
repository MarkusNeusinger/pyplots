# scatter-color-groups: Scatter Plot with Color Groups

## Description

A scatter plot where data points are colored by categorical groups, creating distinct "color clouds" for different categories. This visualization reveals both the relationship between two numeric variables and how that relationship differs across groups. Essential for comparing patterns and identifying group-specific clusters or trends.

## Data

**Required columns:**
- `x` (numeric) - values for the horizontal axis
- `y` (numeric) - values for the vertical axis
- `group` (categorical) - category defining the color for each point

**Example:**
```python
import seaborn as sns
data = sns.load_dataset('iris')
# Use: x='sepal_length', y='sepal_width', group='species'
```

## Tags

scatter, groups, categorical, comparison, 2d, exploratory

## Use Cases

- Comparing customer segments by spending behavior and visit frequency
- Analyzing species characteristics in biological datasets
- Visualizing regional differences in economic indicators
- Exploring product performance across different market categories
