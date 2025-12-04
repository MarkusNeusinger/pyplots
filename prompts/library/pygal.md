# pygal

## Import

```python
import pygal
from pygal.style import Style
```

## Create Chart

```python
# Target: 4800 × 2700 px (see default-style-guide.md)
chart = pygal.Bar(
    width=4800,
    height=2700,
    title=title,
    x_title=x_label,
    y_title=y_label
)
```

## Chart Types

```python
pygal.Bar()          # Vertical bars
pygal.HorizontalBar()# Horizontal bars
pygal.Line()         # Lines
pygal.XY()           # Scatter (XY coordinates)
pygal.Pie()          # Pie chart
pygal.Box()          # Boxplot
pygal.Histogram()    # Histogram
```

## Add Data

```python
chart.add('Series 1', [1, 2, 3, 4])
chart.add('Series 2', [4, 3, 2, 1])

# X-axis labels
chart.x_labels = ['A', 'B', 'C', 'D']
```

## Save

```python
# SVG (native)
chart.render_to_file('plot.svg')

# PNG (requires cairosvg)
chart.render_to_png('plot.png')
```

## Styling

```python
custom_style = Style(
    background='white',
    plot_background='white',
    foreground='#333',
    foreground_strong='#333',
    foreground_subtle='#666',
    colors=('#3498db', '#2ecc71', '#e74c3c', '#9b59b6')
)

chart = pygal.Bar(style=custom_style)
```

## Grid

```python
chart = pygal.Bar(
    show_x_guides=True,
    show_y_guides=True
)
```

## Folder-Name

`plots/pygal/{chart_type}/`

| Type | Folder |
|-----|--------|
| `pygal.Bar()` | `bar/` |
| `pygal.Line()` | `line/` |
| `pygal.XY()` | `xy/` |
| `pygal.Pie()` | `pie/` |
| `pygal.Box()` | `box/` |

## Return Type

```python
def create_plot(...) -> pygal.Bar:  # or corresponding type
```
