# plotly

## Import

```python
import plotly.graph_objects as go
# oder
import plotly.express as px
```

## Figure erstellen

```python
# Graph Objects
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y))

# Express (für schnelle Plots)
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

## Speichern (PNG)

```python
fig.write_image('plot.png', width=1600, height=900, scale=2)
```

**Hinweis**: Benötigt `kaleido` für PNG-Export.

## Interaktivität

Plotly ist standardmäßig interaktiv (Hover, Zoom, Pan).
Für statische Outputs → `write_image()`.

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
