# matplotlib

## Interactive Spec Handling

matplotlib produces **static PNG only**. When implementing specs that mention interactive features:

- Specs with primary interactivity (hover, zoom, click, brush) → **NOT_FEASIBLE**
- Specs with animation → Use small multiples or faceted grid as static alternative
- Mixed specs (static + interactive) → Implement static features only, omit interactive silently
- **NEVER** simulate tooltips, hover states, or controls. See AR-08 in `prompts/quality-criteria.md`

---

## Import

```python
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
```

## Create Figure

```python
fig, ax = plt.subplots(figsize=(16, 9))
```

## Plot Methods

Use **Axes methods** (not pyplot):

```python
# Correct
ax.scatter(x, y)
ax.plot(x, y)
ax.bar(x, y)

# Wrong
plt.scatter(x, y)
```

## Save

```python
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
```

## Sizing for 4800×2700 px

```python
# Text sizes
ax.set_title(title, fontsize=24, fontweight='medium')
ax.set_xlabel(x_label, fontsize=20)
ax.set_ylabel(y_label, fontsize=20)
ax.tick_params(axis='both', labelsize=16)
ax.legend(fontsize=16)

# Element sizes
ax.scatter(x, y, s=200, edgecolors='white', linewidth=0.5)  # s=150-300
ax.plot(x, y, linewidth=3)   # linewidth=2-4 (not 1!)

# Grid (subtle, y-axis preferred)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)

# Spine removal (default: remove top + right)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

## Styling

```python
ax.set_xlabel(x_label, fontsize=20)
ax.set_ylabel(y_label, fontsize=20)
ax.set_title(title, fontsize=24, fontweight='medium')
ax.legend(fontsize=16)  # if needed (omit for single-series)
plt.tight_layout()
```

## API Compatibility (3.9+)

```python
# DEPRECATED: labels in boxplot
ax.boxplot(data, labels=group_names)  # Wrong

# CORRECT: use tick_labels
ax.boxplot(data, tick_labels=group_names)  # Right
```

## Colors

```python
# Single-series: always Python Blue
color = '#306998'

# Multi-series: AI picks cohesive palette starting with Python Blue
# No hardcoded second color — choose what works for the data
colors = ['#306998', ...]  # AI selects additional colors

# Colorblind-safe required. Avoid red-green as only distinguishing feature.
# For sequential data: use perceptually-uniform colormaps (viridis, plasma, cividis)
```

## Output File

`plots/{spec-id}/implementations/matplotlib.py`
