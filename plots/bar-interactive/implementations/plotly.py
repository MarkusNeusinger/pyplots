""" pyplots.ai
bar-interactive: Interactive Bar Chart with Hover and Click
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2026-01-07
"""

import pandas as pd
import plotly.graph_objects as go


# Data - Product sales by category with additional details for tooltips
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Food", "Health"]
values = [4250, 3180, 2890, 2340, 1950, 1720, 1580, 1290]
percentages = [round(v / sum(values) * 100, 1) for v in values]
units_sold = [850, 1060, 578, 468, 975, 574, 790, 430]
growth = [12.5, 8.3, -2.1, 15.7, 3.2, -5.4, 9.8, 4.6]

df = pd.DataFrame(
    {"category": categories, "revenue": values, "percentage": percentages, "units": units_sold, "growth": growth}
)

# Create interactive bar chart
fig = go.Figure()

# Add bars with rich hover information and click-like interactivity
fig.add_trace(
    go.Bar(
        x=df["category"],
        y=df["revenue"],
        marker=dict(color="#306998", line=dict(color="#1f4d6b", width=2)),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: $%{y:,.0f}K<br>"
            "Market Share: %{customdata[0]:.1f}%<br>"
            "Units Sold: %{customdata[1]:,.0f}<br>"
            "YoY Growth: %{customdata[2]:+.1f}%"
            "<extra></extra>"
        ),
        customdata=df[["percentage", "units", "growth"]].values,
        hoverlabel=dict(bgcolor="white", font_size=18, font_family="Arial", bordercolor="#306998"),
    )
)

# Update layout for interactivity and large canvas
fig.update_layout(
    title=dict(
        text="bar-interactive · plotly · pyplots.ai", font=dict(size=32, color="#333333"), x=0.5, xanchor="center"
    ),
    xaxis=dict(
        title=dict(text="Product Category", font=dict(size=24, color="#333333")),
        tickfont=dict(size=18, color="#333333"),
        showgrid=False,
    ),
    yaxis=dict(
        title=dict(text="Revenue ($K)", font=dict(size=24, color="#333333")),
        tickfont=dict(size=18, color="#333333"),
        gridcolor="rgba(0, 0, 0, 0.1)",
        gridwidth=1,
    ),
    template="plotly_white",
    bargap=0.3,
    hovermode="x unified",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=100, r=60, t=120, b=100),
)

# Add annotations for additional visual feedback
fig.add_annotation(
    text="Hover over bars for detailed breakdown",
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.12,
    showarrow=False,
    font=dict(size=16, color="#666666"),
)

# Save static PNG for preview (4800x2700)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML for full interactivity
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
