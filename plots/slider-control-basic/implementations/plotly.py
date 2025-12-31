""" pyplots.ai
slider-control-basic: Interactive Plot with Slider Control
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-31
"""

import numpy as np
import plotly.graph_objects as go


# Data - Quarterly sales data for multiple years
np.random.seed(42)
years = [2019, 2020, 2021, 2022, 2023, 2024]
quarters = ["Q1", "Q2", "Q3", "Q4"]

# Generate sales data with yearly growth trend
sales_data = {}
base_sales = [120, 145, 160, 135]  # Q1-Q4 seasonal pattern
for i, year in enumerate(years):
    growth = 1 + i * 0.08 + np.random.uniform(-0.05, 0.05)
    noise = np.random.normal(0, 10, 4)
    sales_data[year] = np.maximum(50, np.array(base_sales) * growth + noise)

# Create figure with initial year (2019)
fig = go.Figure()

# Add trace for bar chart
fig.add_trace(
    go.Bar(
        x=quarters,
        y=sales_data[2019],
        marker=dict(color="#306998"),
        name="Quarterly Sales",
        text=[f"${v:.0f}K" for v in sales_data[2019]],
        textposition="outside",
        textfont=dict(size=16),
    )
)

# Create slider steps
steps = []
for year in years:
    step = dict(
        method="update",
        args=[
            {"y": [sales_data[year]], "text": [[f"${v:.0f}K" for v in sales_data[year]]]},
            {
                "title.text": f"Quarterly Sales Performance · {year}<br><sup>slider-control-basic · plotly · pyplots.ai</sup>"
            },
        ],
        label=str(year),
    )
    steps.append(step)

# Create slider
sliders = [
    dict(
        active=0,
        currentvalue=dict(prefix="Year: ", visible=True, xanchor="center", font=dict(size=20, color="#306998")),
        pad=dict(t=60, b=20),
        len=0.7,
        x=0.15,
        xanchor="left",
        steps=steps,
        ticklen=8,
        tickwidth=2,
        font=dict(size=16),
        bgcolor="#E0E0E0",
        activebgcolor="#FFD43B",
        bordercolor="#306998",
        borderwidth=2,
    )
]

# Update layout
fig.update_layout(
    title=dict(
        text="Quarterly Sales Performance · 2019<br><sup>slider-control-basic · plotly · pyplots.ai</sup>",
        font=dict(size=28),
        x=0.5,
        xanchor="center",
    ),
    xaxis=dict(title=dict(text="Quarter", font=dict(size=22)), tickfont=dict(size=18)),
    yaxis=dict(
        title=dict(text="Sales ($ Thousands)", font=dict(size=22)),
        tickfont=dict(size=18),
        range=[0, 280],
        gridcolor="rgba(0,0,0,0.1)",
        gridwidth=1,
    ),
    sliders=sliders,
    template="plotly_white",
    margin=dict(t=120, b=160, l=100, r=80),
    showlegend=False,
    plot_bgcolor="white",
    annotations=[
        dict(
            text="Drag the slider to explore sales data by year",
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.32,
            showarrow=False,
            font=dict(size=16, color="#666666"),
            xanchor="center",
        )
    ],
)

# Update bar appearance
fig.update_traces(marker=dict(line=dict(color="#1a3a5c", width=2)), width=0.6)

# Save as PNG (4800 x 2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as interactive HTML
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
