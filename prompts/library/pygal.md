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

## Sizing for 4800×2700 px

```python
custom_style = Style(
    background='white',
    plot_background='white',
    foreground='#333',
    foreground_strong='#333',
    foreground_subtle='#666',
    colors=('#306998', '#FFD43B'),  # pyplots primary colors
    title_font_size=28,
    label_font_size=18,
    major_label_font_size=16,
    legend_font_size=16,
    value_font_size=14,
    stroke_width=3              # line width
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

## Output File

`plots/{spec-id}/implementations/pygal.py`

