""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: plotly 6.5.2 | Python 3.14.3
Quality: 87/100 | Updated: 2026-02-15
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

# Market share (%) - bubble size and color
market_share = np.abs(np.random.randn(n_companies) * 8 + 12)
market_share = np.clip(market_share, 2, 35)

# Bubble sizing via sizeref (Plotly's idiomatic area-based scaling)
sizeref = 2.0 * max(market_share) / (55**2)

# Plot
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=revenue,
        y=growth,
        mode="markers",
        marker={
            "size": market_share,
            "sizemode": "area",
            "sizeref": sizeref,
            "sizemin": 6,
            "color": market_share,
            "colorscale": [[0, "#a8c4d8"], [0.5, "#306998"], [1, "#1a3d5c"]],
            "colorbar": {
                "title": {"text": "Market<br>Share (%)", "font": {"size": 18}},
                "tickfont": {"size": 16},
                "thickness": 18,
                "len": 0.6,
            },
            "opacity": 0.75,
            "line": {"width": 1.5, "color": "white"},
        },
        text=[f"Market Share: {s:.1f}%" for s in market_share],
        hovertemplate="<b>Revenue:</b> $%{x:.1f}M<br><b>Growth:</b> %{y:.1f}%<br>%{text}<extra></extra>",
        showlegend=False,
    )
)

# Size legend - representative bubbles
legend_sizes = [5, 15, 30]
for label_size in legend_sizes:
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker={
                "size": label_size,
                "sizemode": "area",
                "sizeref": sizeref,
                "sizemin": 4,
                "color": "#306998",
                "opacity": 0.75,
                "line": {"width": 1.5, "color": "white"},
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
        "gridcolor": "rgba(0,0,0,0.15)",
        "gridwidth": 1,
        "zeroline": False,
    },
    yaxis={
        "title": {"text": "Growth Rate (%)", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(0,0,0,0.15)",
        "gridwidth": 1,
        "zeroline": False,
    },
    template="plotly_white",
    legend={
        "title": {"text": "Market Share", "font": {"size": 18}},
        "font": {"size": 16},
        "x": 1.12,
        "y": 0.98,
        "xanchor": "left",
        "yanchor": "top",
        "bgcolor": "rgba(255,255,255,0.8)",
        "bordercolor": "rgba(0,0,0,0.15)",
        "borderwidth": 1,
    },
    margin={"l": 100, "r": 220, "t": 120, "b": 100},
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
