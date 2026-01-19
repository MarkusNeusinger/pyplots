"""pyplots.ai
chart-export-menu: Chart with Built-in Export Menu
Library: plotly | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import numpy as np
import plotly.graph_objects as go


# Data: Monthly sales data for demonstration
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
product_a = np.random.randint(80, 150, size=12).cumsum()
product_b = np.random.randint(60, 120, size=12).cumsum()

# Create figure with multiple traces
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=months,
        y=product_a,
        mode="lines+markers",
        name="Product A",
        line={"width": 4, "color": "#306998"},
        marker={"size": 14, "color": "#306998"},
    )
)

fig.add_trace(
    go.Scatter(
        x=months,
        y=product_b,
        mode="lines+markers",
        name="Product B",
        line={"width": 4, "color": "#FFD43B"},
        marker={"size": 14, "color": "#FFD43B"},
    )
)

# Configure layout with export-friendly modebar
fig.update_layout(
    title={"text": "chart-export-menu · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Month", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.1)",
    },
    yaxis={
        "title": {"text": "Cumulative Sales (units)", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "rgba(0,0,0,0.1)",
    },
    legend={
        "font": {"size": 18},
        "x": 0.02,
        "y": 0.98,
        "bgcolor": "rgba(255,255,255,0.8)",
        "bordercolor": "rgba(0,0,0,0.2)",
        "borderwidth": 1,
    },
    template="plotly_white",
    margin={"l": 100, "r": 80, "t": 120, "b": 100},
)

# Configure modebar with export options (hamburger menu with download capabilities)
# Plotly's native modebar includes: toImage (PNG/SVG), zoom, pan, etc.
fig.update_layout(
    modebar={"orientation": "v", "bgcolor": "rgba(255,255,255,0.9)", "color": "#306998", "activecolor": "#FFD43B"},
    modebar_add=["v1hovermode", "toggleSpikelines"],
    modebar_remove=[],
)

# Configure export defaults for the modebar download button
config = {
    "toImageButtonOptions": {
        "format": "png",
        "filename": "chart-export-menu",
        "height": 2700,
        "width": 4800,
        "scale": 1,
    },
    "displaylogo": False,
    "modeBarButtonsToAdd": ["drawline", "drawopenpath", "eraseshape"],
    "modeBarButtonsToRemove": [],
    "displayModeBar": True,
    "scrollZoom": True,
}

# Save static PNG for preview
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML with full export menu functionality
fig.write_html("plot.html", config=config, include_plotlyjs=True, full_html=True)
