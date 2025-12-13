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

## Sizing for 4800×2700 px

```python
# Text sizes (seaborn uses matplotlib underneath)
ax.set_title(title, fontsize=24)
ax.set_xlabel(x_label, fontsize=20)
ax.set_ylabel(y_label, fontsize=20)
ax.tick_params(axis='both', labelsize=16)

# Or use sns.set_context for global scaling
sns.set_context("talk", font_scale=1.2)

# Element sizes in seaborn functions
sns.scatterplot(..., s=200)           # marker size
sns.lineplot(..., linewidth=3)        # line width
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

