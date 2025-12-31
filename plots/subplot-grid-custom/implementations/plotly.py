""" pyplots.ai
subplot-grid-custom: Custom Subplot Grid Layout
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Data
np.random.seed(42)

# Time series data for main plot (spanning 2 columns)
dates = pd.date_range("2024-01-01", periods=120, freq="D")
price = 100 + np.cumsum(np.random.randn(120) * 2)
volume = np.random.randint(50, 200, 120)

# Returns data for histogram
returns = np.diff(price) / price[:-1] * 100

# Scatter data for correlation plot
revenue = np.random.uniform(50, 150, 50)
expenses = revenue * 0.6 + np.random.randn(50) * 15

# Category data for bar chart
categories = ["Product A", "Product B", "Product C", "Product D"]
values = [85, 72, 91, 68]

# Create subplot grid: 2 rows × 3 columns
# Main plot spans 2 columns in top row, small plots in remaining cells
fig = make_subplots(
    rows=2,
    cols=3,
    specs=[[{"colspan": 2}, None, {}], [{}, {}, {}]],
    subplot_titles=(
        "Stock Price (2 Columns)",
        "Category Performance",
        "Trading Volume",
        "Revenue vs Expenses",
        "Daily Returns Distribution",
    ),
    horizontal_spacing=0.08,
    vertical_spacing=0.15,
)

# Main plot: Stock price time series (top-left, spans 2 columns)
fig.add_trace(
    go.Scatter(
        x=dates, y=price, mode="lines", line={"color": "#306998", "width": 3}, name="Stock Price", showlegend=False
    ),
    row=1,
    col=1,
)

# Top-right: Category bar chart
fig.add_trace(
    go.Bar(x=categories, y=values, marker_color="#FFD43B", name="Performance", showlegend=False), row=1, col=3
)

# Bottom-left: Volume bar chart
fig.add_trace(
    go.Bar(x=dates[::4], y=volume[::4], marker_color="#306998", opacity=0.7, name="Volume", showlegend=False),
    row=2,
    col=1,
)

# Bottom-center: Scatter plot (revenue vs expenses)
fig.add_trace(
    go.Scatter(
        x=revenue,
        y=expenses,
        mode="markers",
        marker={"color": "#306998", "size": 12, "opacity": 0.7, "line": {"color": "white", "width": 1}},
        name="Revenue vs Expenses",
        showlegend=False,
    ),
    row=2,
    col=2,
)

# Bottom-right: Returns histogram
fig.add_trace(
    go.Histogram(x=returns, nbinsx=20, marker_color="#FFD43B", opacity=0.8, name="Returns", showlegend=False),
    row=2,
    col=3,
)

# Update layout
fig.update_layout(
    title={"text": "subplot-grid-custom · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    template="plotly_white",
    showlegend=False,
    margin={"l": 80, "r": 60, "t": 120, "b": 80},
)

# Update all axes with proper font sizes
fig.update_xaxes(tickfont={"size": 14}, title_font={"size": 18})
fig.update_yaxes(tickfont={"size": 14}, title_font={"size": 18})

# Update specific axes labels
fig.update_xaxes(title_text="Date", row=1, col=1)
fig.update_yaxes(title_text="Price ($)", row=1, col=1)

fig.update_xaxes(title_text="Category", row=1, col=3)
fig.update_yaxes(title_text="Score", row=1, col=3)

fig.update_xaxes(title_text="Date", row=2, col=1)
fig.update_yaxes(title_text="Volume (K)", row=2, col=1)

fig.update_xaxes(title_text="Revenue ($K)", row=2, col=2)
fig.update_yaxes(title_text="Expenses ($K)", row=2, col=2)

fig.update_xaxes(title_text="Daily Return (%)", row=2, col=3)
fig.update_yaxes(title_text="Frequency", row=2, col=3)

# Update annotation font sizes for subplot titles
for annotation in fig["layout"]["annotations"]:
    annotation["font"] = {"size": 20}

# Save as PNG
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML (interactive)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
