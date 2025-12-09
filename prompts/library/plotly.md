# plotly

## Import

```python
import plotly.graph_objects as go
# or
import plotly.express as px
```

## Create Figure

```python
# Graph Objects
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y))

# Express (for quick plots)
fig = px.scatter(df, x='col_x', y='col_y')
```

## Layout

```python
fig.update_layout(
    title=title,
    xaxis_title=x_label,
    yaxis_title=y_label,
    template='plotly_white',  # Clean template
)
```

## Save (PNG)

```python
# Target: 4800 × 2700 px (see default-style-guide.md)
fig.write_image('plot.png', width=1600, height=900, scale=3)
```

**Note**: Requires `kaleido` for PNG export.

## Interactivity

Plotly is interactive by default (hover, zoom, pan).
For static outputs → `write_image()`.

## Output File

`plots/{spec-id}/implementations/plotly.py`

