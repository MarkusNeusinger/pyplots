# bokeh

## Import

```python
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.io import export_png
```

## Create Figure

```python
p = figure(
    width=1600,
    height=900,
    title=title,
    x_axis_label=x_label,
    y_axis_label=y_label
)
```

## Plot Methods

```python
# Numeric data
p.scatter(x='x', y='y', source=source)
p.line(x='x', y='y', source=source)

# IMPORTANT: Categorical axes
p = figure(x_range=categories, ...)  # define x_range!
source = ColumnDataSource(data={'x': cat_data, 'y': num_data})
p.scatter(x='x', y='y', source=source)
```

## ColumnDataSource

```python
# Always use ColumnDataSource for flexibility
source = ColumnDataSource(data={
    'x': df['col_x'],
    'y': df['col_y'],
    'color': df['col_color']
})
```

## Save (PNG)

```python
from bokeh.io import export_png

export_png(p, filename='plot.png')
```

**Note**: Requires `selenium` and WebDriver for PNG export.

## Styling

```python
p.grid.grid_line_alpha = 0.3
p.xaxis.axis_label = x_label
p.yaxis.axis_label = y_label
```

## Folder-Name

`plots/bokeh/{glyph_method}/`

| Method | Folder |
|--------|--------|
| `p.scatter()` | `scatter/` |
| `p.line()` | `line/` |
| `p.vbar()` | `vbar/` |
| `p.hbar()` | `hbar/` |
| Custom (no native) | `custom/` |

## Return Type

```python
def create_plot(...) -> figure:
    # Note: bokeh.plotting.figure (lowercase)
```
