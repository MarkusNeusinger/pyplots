# pygal

## Import

```python
import pygal
from pygal.style import Style
```

## Chart erstellen

```python
chart = pygal.Bar(
    width=1600,
    height=900,
    title=title,
    x_title=x_label,
    y_title=y_label
)
```

## Chart-Typen

```python
pygal.Bar()          # Vertikale Balken
pygal.HorizontalBar()# Horizontale Balken
pygal.Line()         # Linien
pygal.XY()           # Scatter (XY-Koordinaten)
pygal.Pie()          # Kreisdiagramm
pygal.Box()          # Boxplot
pygal.Histogram()    # Histogramm
```

## Daten hinzufügen

```python
chart.add('Series 1', [1, 2, 3, 4])
chart.add('Series 2', [4, 3, 2, 1])

# X-Achsen-Labels
chart.x_labels = ['A', 'B', 'C', 'D']
```

## Speichern

```python
# SVG (nativ)
chart.render_to_file('plot.svg')

# PNG (benötigt cairosvg)
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

| Typ | Folder |
|-----|--------|
| `pygal.Bar()` | `bar/` |
| `pygal.Line()` | `line/` |
| `pygal.XY()` | `xy/` |
| `pygal.Pie()` | `pie/` |
| `pygal.Box()` | `box/` |

## Return Type

```python
def create_plot(...) -> pygal.Bar:  # oder entsprechender Typ
```
