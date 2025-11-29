# plotnine

## Import

```python
from plotnine import (
    ggplot, aes,
    geom_point, geom_line, geom_bar, geom_boxplot,
    labs, theme, theme_minimal,
    scale_fill_brewer, scale_color_brewer
)
```

## Plot erstellen

```python
plot = (
    ggplot(df, aes(x='col_x', y='col_y'))
    + geom_point()
    + labs(x=x_label, y=y_label, title=title)
    + theme_minimal()
)
```

## Figure Size

```python
plot = plot + theme(figure_size=(16, 9))
```

## Speichern (PNG)

```python
plot.save('plot.png', dpi=300)
```

## Brewer Paletten

**WICHTIG**: Palette-Typ muss zum Palette-Namen passen!

```python
# Qualitativ (kategorisch)
+ scale_fill_brewer(type='qual', palette='Set2')
+ scale_fill_brewer(type='qual', palette='Paired')
+ scale_fill_brewer(type='qual', palette='Dark2')

# Sequentiell (numerisch)
+ scale_fill_brewer(type='seq', palette='Blues')
+ scale_fill_brewer(type='seq', palette='Greens')

# Divergierend (um Nullpunkt)
+ scale_fill_brewer(type='div', palette='RdBu')
+ scale_fill_brewer(type='div', palette='PiYG')
```

```python
# FALSCH: Set2 ist NICHT sequentiell!
+ scale_fill_brewer(type='seq', palette='Set2')

# RICHTIG: Set2 ist qualitativ
+ scale_fill_brewer(type='qual', palette='Set2')
```

## Geoms

```python
geom_point()     # Scatter
geom_line()      # Line
geom_bar()       # Bar (stat='identity' für Werte)
geom_boxplot()   # Boxplot
geom_histogram() # Histogram
geom_tile()      # Heatmap
```

## Folder-Name

`plots/plotnine/{geom}/`

| Geom | Folder |
|------|--------|
| `geom_point()` | `point/` |
| `geom_line()` | `line/` |
| `geom_bar()` | `bar/` |
| `geom_boxplot()` | `boxplot/` |

## Return Type

```python
def create_plot(...) -> ggplot:
```
