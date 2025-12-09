# seaborn

## Import

```python
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
```

## Create Figure

```python
fig, ax = plt.subplots(figsize=(16, 9))
```

## Plot Methods

```python
# Axes-level (preferred)
sns.scatterplot(data=df, x='col_x', y='col_y', ax=ax)

# Figure-level (for complex layouts)
g = sns.relplot(data=df, x='col_x', y='col_y')
fig = g.figure
```

## Save

```python
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
```

## API Compatibility (0.14+)

```python
# WARNING: palette without hue
sns.boxplot(data=df, x='group', y='value', palette='Set2')  # Warning

# CORRECT: hue with palette
sns.boxplot(data=df, x='group', y='value', hue='group', palette='Set2', legend=False)
```

## Recommended Palettes

```python
# Categorical
palette='Set2'
palette='tab10'
palette='colorblind'

# Sequential
palette='viridis'
palette='Blues'

# Diverging
palette='RdBu'
```

## Output File

`plots/{spec-id}/implementations/seaborn.py`

