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
    width=1600,
    height=900
)
```

## Save (PNG)

```python
fig.write_image('plot.png', width=1600, height=900, scale=2)
```

**Note**: Requires `kaleido` for PNG export.

## Interactivity

Plotly is interactive by default (hover, zoom, pan).
For static outputs → `write_image()`.

## Folder-Name

`plots/plotly/{trace_type}/`

| Trace | Folder |
|-------|--------|
| `go.Scatter` | `scatter/` |
| `go.Bar` | `bar/` |
| `go.Box` | `box/` |
| `go.Heatmap` | `heatmap/` |
| `go.Scatter3d` | `scatter3d/` |
| `go.Candlestick` | `candlestick/` |

## Return Type

```python
def create_plot(...) -> go.Figure:
```
