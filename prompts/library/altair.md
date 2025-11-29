# altair

## Import

```python
import altair as alt
```

## Chart erstellen

```python
chart = alt.Chart(df).mark_point().encode(
    x='col_x:Q',
    y='col_y:Q'
).properties(
    width=800,
    height=450,
    title=title
)
```

## Encoding Types

```python
# Q = Quantitative (numerisch)
x='value:Q'

# N = Nominal (kategorisch, keine Ordnung)
color='category:N'

# O = Ordinal (kategorisch, mit Ordnung)
x='month:O'

# T = Temporal (Datum/Zeit)
x='date:T'
```

## Marks

```python
.mark_point()      # Scatter
.mark_line()       # Line
.mark_bar()        # Bar
.mark_boxplot()    # Boxplot
.mark_rect()       # Heatmap
.mark_area()       # Area
```

## Speichern (PNG)

```python
chart.save('plot.png', scale_factor=2.0)
```

**Hinweis**: Benötigt `vl-convert-python` für PNG-Export.

## Interaktivität

```python
# Zoom/Pan aktivieren
chart = chart.interactive()

# Tooltips
.encode(tooltip=['col_x', 'col_y'])
```

## Folder-Name

`plots/altair/{mark_type}/`

| Mark | Folder |
|------|--------|
| `mark_point()` | `point/` |
| `mark_line()` | `line/` |
| `mark_bar()` | `bar/` |
| `mark_boxplot()` | `boxplot/` |
| `mark_rect()` | `rect/` |

## Return Type

```python
def create_plot(...) -> alt.Chart:
```
