# lets-plot

ggplot2-style grammar of graphics by JetBrains.

## Import

```python
from lets_plot import *
LetsPlot.setup_html()  # Required for notebook/export
```

## Create Plot

```python
plot = (
    ggplot(df, aes(x='col_x', y='col_y'))
    + geom_point()
    + labs(x=x_label, y=y_label, title=title)
)
```

## Figure Size

```python
# Target: 4800 × 2700 px (see default-style-guide.md)
plot = plot + ggsize(1600, 900)  # Base size, scaled 3x on export
```

## Save (PNG)

```python
from lets_plot import ggsave

# Scale 3x to get 4800 × 2700 px
ggsave(plot, 'plot.png', scale=3)
```

## Aesthetics

```python
# Mappings
aes(x='col_x', y='col_y', color='category', size='value')

# Fixed aesthetics (outside aes)
geom_point(color='blue', size=5, alpha=0.7)
```

## Geoms

```python
geom_point()       # Scatter
geom_line()        # Line
geom_bar()         # Bar (stat='identity' for values)
geom_histogram()   # Histogram
geom_boxplot()     # Boxplot
geom_violin()      # Violin
geom_tile()        # Heatmap
geom_smooth()      # Trend line
geom_area()        # Area
geom_density()     # Density
```

## Scales

```python
# Color scales
+ scale_color_brewer(palette='Set2')
+ scale_fill_viridis()
+ scale_color_manual(values=['#306998', '#FFD43B', '#DC2626'])

# Axis scales
+ scale_x_continuous()
+ scale_y_log10()
```

## Themes

```python
+ theme_minimal()
+ theme_classic()
+ theme_bw()
+ theme_void()

# Custom theme
+ theme(
    axis_text=element_text(size=12),
    legend_position='right'
)
```

## Facets

```python
+ facet_wrap('category', ncol=3)
+ facet_grid(x='row_var', y='col_var')
```

## Output File

`plots/{spec-id}/implementations/letsplot.py`

## Key Differences from plotnine

- Uses `lets_plot` module (not `plotnine`)
- `ggsize()` instead of `theme(figure_size=...)`
- `ggsave()` with `scale` parameter for PNG export
- More interactive features built-in
