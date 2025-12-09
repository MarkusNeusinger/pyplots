# altair

## Import

```python
import altair as alt
```

## Create Chart

```python
chart = alt.Chart(df).mark_point().encode(
    x='col_x:Q',
    y='col_y:Q'
).properties(
    width=1600,
    height=900,
    title=title
)
```

## Encoding Types

```python
# Q = Quantitative (numeric)
x='value:Q'

# N = Nominal (categorical, no order)
color='category:N'

# O = Ordinal (categorical, with order)
x='month:O'

# T = Temporal (date/time)
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

## Save (PNG)

```python
# Target: 4800 × 2700 px (see default-style-guide.md)
# 1600 × 3 = 4800, 900 × 3 = 2700
chart.save('plot.png', scale_factor=3.0)
```

**Note**: Requires `vl-convert-python` for PNG export.

## Interactivity

```python
# Enable zoom/pan
chart = chart.interactive()

# Tooltips
.encode(tooltip=['col_x', 'col_y'])
```

## Output File

`plots/{spec-id}/implementations/altair.py`

