"""pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: altair | Python 3.13
Quality: pending | Created: 2025-01-11
"""

import altair as alt
import numpy as np
import pandas as pd


# Data: Generate realistic stock price data (random walk)
np.random.seed(42)
dates = pd.date_range(start="2021-01-01", end="2024-12-31", freq="B")  # Business days
n_days = len(dates)

# Simulate stock price with random walk + trend
initial_price = 150
returns = np.random.normal(0.0003, 0.015, n_days)  # Daily returns
price = initial_price * np.cumprod(1 + returns)

df = pd.DataFrame({"date": dates, "price": price})

# Calculate nice y-axis range
y_min = df["price"].min() * 0.95
y_max = df["price"].max() * 1.05

# Range selector brush (interval selection on x-axis)
brush = alt.selection_interval(encodings=["x"])

# Main chart: Area chart that zooms to selected range
main_chart = (
    alt.Chart(df)
    .mark_area(
        line={"color": "#306998", "strokeWidth": 2.5},
        color=alt.Gradient(
            gradient="linear",
            stops=[
                alt.GradientStop(color="rgba(48, 105, 152, 0.15)", offset=0),
                alt.GradientStop(color="rgba(48, 105, 152, 0.5)", offset=1),
            ],
            x1=1,
            x2=1,
            y1=1,
            y2=0,
        ),
    )
    .encode(
        x=alt.X("date:T", title="Date", scale=alt.Scale(domain=brush), axis=alt.Axis(format="%b %Y", labelAngle=-45)),
        y=alt.Y("price:Q", title="Price (USD)", scale=alt.Scale(domain=[y_min, y_max])),
        tooltip=[
            alt.Tooltip("date:T", title="Date", format="%Y-%m-%d"),
            alt.Tooltip("price:Q", title="Price", format="$,.2f"),
        ],
    )
    .properties(
        width=1500, height=650, title=alt.Title("area-stock-range · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
)

# Range selector: Mini overview chart at bottom
range_selector = (
    alt.Chart(df)
    .mark_area(line={"color": "#306998", "strokeWidth": 1}, color="rgba(48, 105, 152, 0.3)")
    .encode(
        x=alt.X("date:T", title="Date", axis=alt.Axis(format="%b %Y")),
        y=alt.Y("price:Q", title=None, scale=alt.Scale(domain=[y_min, y_max])),
    )
    .properties(width=1500, height=100, title=alt.Title("Drag to select date range", fontSize=16))
    .add_params(brush)
)

# Combine charts vertically
chart = (
    alt.vconcat(main_chart, range_selector, spacing=20)
    .configure_axis(labelFontSize=16, titleFontSize=20)
    .configure_title(fontSize=28)
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
