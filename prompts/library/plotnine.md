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

## Create Plot

```python
plot = (
    ggplot(df, aes(x='col_x', y='col_y'))
    + geom_point()
    + labs(x=x_label, y=y_label, title=title)
    + theme_minimal()
)
```

## Figure Size & Sizing for 4800×2700 px

```python
plot = plot + theme(
    figure_size=(16, 9),
    text=element_text(size=14),           # Base text
    axis_title=element_text(size=20),     # Axis labels
    axis_text=element_text(size=16),      # Tick labels
    plot_title=element_text(size=24),     # Title
    legend_text=element_text(size=16)
)

# Element sizes in geoms
+ geom_point(size=4)    # ~3-4x default
+ geom_line(size=1.5)   # line width
```

## Save (PNG)

```python
plot.save('plot.png', dpi=300)
```

## Brewer Palettes

**IMPORTANT**: Palette type must match the palette name!

```python
# Qualitative (categorical)
+ scale_fill_brewer(type='qual', palette='Set2')
+ scale_fill_brewer(type='qual', palette='Paired')
+ scale_fill_brewer(type='qual', palette='Dark2')

# Sequential (numeric)
+ scale_fill_brewer(type='seq', palette='Blues')
+ scale_fill_brewer(type='seq', palette='Greens')

# Diverging (around zero)
+ scale_fill_brewer(type='div', palette='RdBu')
+ scale_fill_brewer(type='div', palette='PiYG')
```

```python
# WRONG: Set2 is NOT sequential!
+ scale_fill_brewer(type='seq', palette='Set2')

# RIGHT: Set2 is qualitative
+ scale_fill_brewer(type='qual', palette='Set2')
```

## Geoms

```python
geom_point()     # Scatter
geom_line()      # Line
geom_bar()       # Bar (stat='identity' for values)
geom_boxplot()   # Boxplot
geom_histogram() # Histogram
geom_tile()      # Heatmap
```

## Output File

`plots/{spec-id}/implementations/plotnine.py`

