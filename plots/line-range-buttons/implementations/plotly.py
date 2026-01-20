""" pyplots.ai
line-range-buttons: Line Chart with Range Selector Buttons
Library: plotly 6.5.2 | Python 3.13.11
Quality: 92/100 | Created: 2026-01-20
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Data - 3 years of daily stock-like price data
np.random.seed(42)
dates = pd.date_range(start="2022-01-01", end="2024-12-31", freq="D")
n_points = len(dates)

# Generate realistic price movement (random walk with drift)
returns = np.random.normal(0.0003, 0.015, n_points)  # Small positive drift
prices = 100 * np.cumprod(1 + returns)

df = pd.DataFrame({"date": dates, "value": prices})

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["value"],
        mode="lines",
        line={"color": "#306998", "width": 2},
        name="Price",
        hovertemplate="%{x|%b %d, %Y}<br>Value: %{y:.2f}<extra></extra>",
    )
)

# Configure range selector buttons
fig.update_layout(
    title={
        "text": "line-range-buttons · plotly · pyplots.ai",
        "font": {"size": 28},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.98,
    },
    xaxis={
        "title": {"text": "Date", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "rangeselector": {
            "buttons": [
                {"count": 1, "label": "1M", "step": "month", "stepmode": "backward"},
                {"count": 3, "label": "3M", "step": "month", "stepmode": "backward"},
                {"count": 6, "label": "6M", "step": "month", "stepmode": "backward"},
                {"count": 1, "label": "YTD", "step": "year", "stepmode": "todate"},
                {"count": 1, "label": "1Y", "step": "year", "stepmode": "backward"},
                {"label": "All", "step": "all"},
            ],
            "bgcolor": "#f0f0f0",
            "activecolor": "#306998",
            "font": {"size": 16, "color": "#333333"},
            "x": 0.01,
            "xanchor": "left",
            "y": 1.12,
            "yanchor": "bottom",
        },
        "rangeslider": {"visible": True, "thickness": 0.05},
        "type": "date",
    },
    yaxis={"title": {"text": "Value", "font": {"size": 22}}, "tickfont": {"size": 18}, "gridcolor": "rgba(0,0,0,0.1)"},
    template="plotly_white",
    showlegend=False,
    margin={"t": 140, "b": 80, "l": 80, "r": 40},
    hovermode="x unified",
)

# Save as PNG
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs="cdn")
