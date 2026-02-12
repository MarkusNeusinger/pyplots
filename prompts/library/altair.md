# altair

## Import

```python
import altair as alt
```

## Create Chart

```python
chart = alt.Chart(df).mark_point(size=150).encode(  # size ~3-4x default
    x='col_x:Q',
    y='col_y:Q'
).properties(
    width=1600,
    height=900,
    title=alt.Title(title, fontSize=28)
).configure_axis(
    labelFontSize=18,
    titleFontSize=22
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

## Colors

```python
# Single-series: always Python Blue
alt.value('#306998')

# Multi-series: AI picks cohesive palette starting with Python Blue
# No hardcoded second color — choose what works for the data
alt.Scale(range=['#306998', ...])  # AI selects additional colors

# Colorblind-safe required. Avoid red-green as only distinguishing feature.
# For sequential data: use perceptually-uniform colormaps (viridis, plasma, cividis)
```

## Output File

`plots/{spec-id}/implementations/altair.py`

