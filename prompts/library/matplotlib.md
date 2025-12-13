# matplotlib

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
ax.set_title(title, fontsize=24)
ax.set_xlabel(x_label, fontsize=20)
ax.set_ylabel(y_label, fontsize=20)
ax.tick_params(axis='both', labelsize=16)
ax.legend(fontsize=16)

# Element sizes
ax.scatter(x, y, s=200)      # s=150-300 (not s=50!)
ax.plot(x, y, linewidth=3)   # linewidth=2-4 (not 1!)

# Grid
ax.grid(True, alpha=0.3, linestyle='--')
```

## Styling

```python
ax.set_xlabel(x_label, fontsize=20)
ax.set_ylabel(y_label, fontsize=20)
ax.set_title(title, fontsize=24)
ax.legend(fontsize=16)  # if needed
plt.tight_layout()
```

## API Compatibility (3.9+)

```python
# DEPRECATED: labels in boxplot
ax.boxplot(data, labels=group_names)  # Wrong

# CORRECT: use tick_labels
ax.boxplot(data, tick_labels=group_names)  # Right
```

## Output File

`plots/{spec-id}/implementations/matplotlib.py`

