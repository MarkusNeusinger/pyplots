"""pyplots.ai
area-basic: Basic Area Chart
Library: altair 6.0.0 | Python 3.14.2
Quality: /100 | Updated: 2026-02-11
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - daily website visitors over a month
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
# Simulate visitor pattern: weekday higher, weekend lower, with growth trend
base = 5000
trend = np.linspace(0, 2000, 30)
weekly_pattern = np.array([1.2, 1.1, 1.0, 1.05, 1.15, 0.8, 0.7] * 5)[:30]
noise = np.random.randn(30) * 300
visitors = (base + trend) * weekly_pattern + noise
# Add a traffic spike mid-month (e.g., marketing campaign on Jan 15)
visitors[14] *= 1.4
visitors = np.maximum(visitors, 1000).astype(int)

df = pd.DataFrame({"date": dates, "visitors": visitors})

# Create area chart
chart = (
    alt.Chart(df)
    .mark_area(opacity=0.4, color="#306998", line={"color": "#306998", "strokeWidth": 3})
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("visitors:Q", title="Daily Visitors (count)", scale=alt.Scale(domain=[0, df["visitors"].max() * 1.1])),
        tooltip=[
            alt.Tooltip("date:T", title="Date", format="%b %d, %Y"),
            alt.Tooltip("visitors:Q", title="Visitors", format=","),
        ],
    )
    .properties(width=1600, height=900, title=alt.Title("area-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(grid=True, gridOpacity=0.3, gridDash=[4, 4], labelFontSize=18, titleFontSize=22)
    .configure_view(strokeWidth=0)
)

# Save as PNG (1600 × 900 at scale_factor=3 → 4800 × 2700 px)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML version
chart.interactive().save("plot.html")
