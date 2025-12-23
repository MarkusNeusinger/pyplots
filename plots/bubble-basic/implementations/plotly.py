""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-23
"""

import numpy as np
import plotly.graph_objects as go


# Data - Company performance metrics
np.random.seed(42)
n_companies = 40

# Revenue (millions) - x axis
revenue = np.random.randn(n_companies) * 15 + 50
revenue = np.clip(revenue, 10, 100)

# Growth rate (%) - y axis
growth = revenue * 0.3 + np.random.randn(n_companies) * 8 + 5
growth = np.clip(growth, -5, 45)

# Market share (%) - bubble size
market_share = np.abs(np.random.randn(n_companies) * 8 + 12)
market_share = np.clip(market_share, 2, 35)

# Normalize size for bubble scaling (area-based perception)
size_min, size_max = 20, 90
size_normalized = (market_share - market_share.min()) / (market_share.max() - market_share.min())
bubble_sizes = size_min + size_normalized * (size_max - size_min)

# Plot
fig = go.Figure()

# Main bubble scatter
fig.add_trace(
    go.Scatter(
        x=revenue,
        y=growth,
        mode="markers",
        marker={
            "size": bubble_sizes,
            "color": "#306998",
            "opacity": 0.6,
            "line": {"width": 1.5, "color": "#1a3d5c"},
            "sizemode": "diameter",
        },
        text=[f"Market Share: {s:.1f}%" for s in market_share],
        hovertemplate="<b>Revenue:</b> $%{x:.1f}M<br><b>Growth:</b> %{y:.1f}%<br>%{text}<extra></extra>",
        showlegend=False,
    )
)

# Size legend - representative bubbles
legend_sizes = [5, 15, 30]
legend_bubble_sizes = [
    size_min + ((s - market_share.min()) / (market_share.max() - market_share.min())) * (size_max - size_min)
    for s in legend_sizes
]

for label_size, bubble_size in zip(legend_sizes, legend_bubble_sizes, strict=True):
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker={
                "size": bubble_size,
                "color": "#306998",
                "opacity": 0.6,
                "line": {"width": 1.5, "color": "#1a3d5c"},
            },
            name=f"{label_size}%",
            showlegend=True,
        )
    )

# Layout
fig.update_layout(
    title={"text": "bubble-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Revenue ($ millions)", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    yaxis={
        "title": {"text": "Growth Rate (%)", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(0,0,0,0.1)",
        "gridwidth": 1,
    },
    template="plotly_white",
    legend={
        "title": {"text": "Market Share", "font": {"size": 18}},
        "font": {"size": 16},
        "x": 1.02,
        "y": 0.98,
        "xanchor": "left",
        "yanchor": "top",
        "bgcolor": "rgba(255,255,255,0.8)",
        "bordercolor": "rgba(0,0,0,0.2)",
        "borderwidth": 1,
    },
    margin={"l": 100, "r": 180, "t": 120, "b": 100},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
