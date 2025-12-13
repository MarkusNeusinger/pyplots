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

## Layout & Sizing for 4800×2700 px

```python
fig.update_layout(
    title=dict(text=title, font=dict(size=28)),
    xaxis=dict(title=dict(text=x_label, font=dict(size=22)), tickfont=dict(size=18)),
    yaxis=dict(title=dict(text=y_label, font=dict(size=22)), tickfont=dict(size=18)),
    template='plotly_white',
)

# Marker/line sizes
fig.update_traces(marker=dict(size=12))   # ~3-4x default
fig.update_traces(line=dict(width=3))
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

