# bokeh

## Import

```python
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.io import export_png
```

## Figure erstellen

```python
p = figure(
    width=1600,
    height=900,
    title=title,
    x_axis_label=x_label,
    y_axis_label=y_label
)
```

## Plot-Methoden

```python
# Numerische Daten
p.scatter(x='x', y='y', source=source)
p.line(x='x', y='y', source=source)

# WICHTIG: Kategorische Achsen
p = figure(x_range=categories, ...)  # x_range definieren!
source = ColumnDataSource(data={'x': cat_data, 'y': num_data})
p.scatter(x='x', y='y', source=source)
```

## ColumnDataSource

```python
# Immer ColumnDataSource verwenden für Flexibilität
source = ColumnDataSource(data={
    'x': df['col_x'],
    'y': df['col_y'],
    'color': df['col_color']
})
```

## Speichern (PNG)

```python
from bokeh.io import export_png

export_png(p, filename='plot.png')
```

**Hinweis**: Benötigt `selenium` und WebDriver für PNG-Export.

## Styling

```python
p.grid.grid_line_alpha = 0.3
p.xaxis.axis_label = x_label
p.yaxis.axis_label = y_label
```

## Folder-Name

`plots/bokeh/{glyph_method}/`

| Methode | Folder |
|---------|--------|
| `p.scatter()` | `scatter/` |
| `p.line()` | `line/` |
| `p.vbar()` | `vbar/` |
| `p.hbar()` | `hbar/` |
| Custom (kein natives) | `custom/` |

## Return Type

```python
def create_plot(...) -> figure:
    # Hinweis: bokeh.plotting.figure (lowercase)
```
