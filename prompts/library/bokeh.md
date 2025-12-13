# bokeh

## Import

```python
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.io import export_png
```

## Create Figure

```python
# Target: 4800 × 2700 px (see default-style-guide.md)
p = figure(
    width=4800,
    height=2700,
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

## Sizing for 4800×2700 px

```python
# Text sizes
p.title.text_font_size = '28pt'
p.xaxis.axis_label_text_font_size = '22pt'
p.yaxis.axis_label_text_font_size = '22pt'
p.xaxis.major_label_text_font_size = '18pt'
p.yaxis.major_label_text_font_size = '18pt'

# Element sizes
p.scatter(..., size=15)        # ~3-4x default
p.line(..., line_width=3)
```

## Output File

`plots/{spec-id}/implementations/bokeh.py`

