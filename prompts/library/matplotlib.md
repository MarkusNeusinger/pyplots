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

## Styling

```python
ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
ax.set_title(title)
ax.legend()  # if needed
plt.tight_layout()
# Grid: AI discretion
```

## API Compatibility (3.9+)

```python
# DEPRECATED: labels in boxplot
ax.boxplot(data, labels=group_names)  # Wrong

# CORRECT: use tick_labels
ax.boxplot(data, tick_labels=group_names)  # Right
```

## Folder Name

`plots/matplotlib/{plot_function}/`

| Function | Folder |
|----------|--------|
| `ax.scatter()` | `scatter/` |
| `ax.plot()` | `plot/` |
| `ax.bar()` | `bar/` |
| `ax.boxplot()` | `boxplot/` |
| `ax.hist()` | `hist/` |
| `ax.imshow()` | `imshow/` |
| `ax.pie()` | `pie/` |

## Return Type

```python
def create_plot(...) -> Figure:
```
