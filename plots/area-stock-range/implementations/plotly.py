"""pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: plotly | Python 3.13
Quality: pending | Created: 2026-01-11
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Data - Generate 3 years of daily stock price data
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", end="2025-12-31", freq="B")  # Business days
n_days = len(dates)

# Simulate realistic stock price movement with trend and volatility
initial_price = 150.0
daily_returns = np.random.normal(0.0003, 0.015, n_days)  # Slight upward drift
price = initial_price * np.cumprod(1 + daily_returns)

# Add some realistic patterns - a dip and recovery
mid_point = n_days // 2
dip_factor = np.ones(n_days)
dip_factor[mid_point - 60 : mid_point + 60] = np.concatenate([np.linspace(1, 0.85, 60), np.linspace(0.85, 1, 60)])
price = price * dip_factor

df = pd.DataFrame({"date": dates, "price": price})

# Create figure with filled area
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["price"],
        mode="lines",
        name="Price",
        line={"color": "#306998", "width": 2},
        fill="tozeroy",
        fillcolor="rgba(48, 105, 152, 0.35)",
        hovertemplate="Date: %{x|%Y-%m-%d}<br>Price: $%{y:.2f}<extra></extra>",
    )
)

# Update layout with range selector and rangeslider
fig.update_layout(
    title={
        "text": "area-stock-range · plotly · pyplots.ai",
        "font": {"size": 32, "color": "#333333"},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Date", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "rangeselector": {
            "buttons": [
                {"count": 1, "label": "1M", "step": "month", "stepmode": "backward"},
                {"count": 3, "label": "3M", "step": "month", "stepmode": "backward"},
                {"count": 6, "label": "6M", "step": "month", "stepmode": "backward"},
                {"count": 1, "label": "1Y", "step": "year", "stepmode": "backward"},
                {"count": 1, "label": "YTD", "step": "year", "stepmode": "todate"},
                {"label": "All", "step": "all"},
            ],
            "font": {"size": 16},
            "bgcolor": "rgba(48, 105, 152, 0.1)",
            "activecolor": "#306998",
            "bordercolor": "#306998",
            "borderwidth": 1,
            "x": 0,
            "y": 1.12,
        },
        "rangeslider": {"visible": True, "thickness": 0.08, "bgcolor": "rgba(48, 105, 152, 0.1)"},
        "type": "date",
        "gridcolor": "rgba(0, 0, 0, 0.1)",
        "gridwidth": 1,
    },
    yaxis={
        "title": {"text": "Price (USD)", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "tickprefix": "$",
        "gridcolor": "rgba(0, 0, 0, 0.1)",
        "gridwidth": 1,
    },
    template="plotly_white",
    hovermode="x unified",
    margin={"l": 100, "r": 60, "t": 140, "b": 100},
    showlegend=False,
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
