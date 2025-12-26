"""pyplots.ai
scatter-marginal: Scatter Plot with Marginal Distributions
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-26
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - bivariate distribution with correlation
np.random.seed(42)
n = 150
x = np.random.randn(n) * 15 + 50
y = 0.7 * x + np.random.randn(n) * 10 + 20

df = pd.DataFrame({"X Value": x, "Y Value": y})

# Main scatter plot
scatter = (
    alt.Chart(df)
    .mark_circle(size=120, opacity=0.65, color="#306998")
    .encode(
        x=alt.X("X Value:Q", title="X Value (units)"),
        y=alt.Y("Y Value:Q", title="Y Value (units)"),
        tooltip=["X Value:Q", "Y Value:Q"],
    )
    .properties(width=1200, height=700)
)

# Top marginal histogram
top_hist = (
    alt.Chart(df)
    .mark_bar(color="#306998", opacity=0.5)
    .encode(x=alt.X("X Value:Q", bin=alt.Bin(maxbins=25), title=""), y=alt.Y("count()", title="Count"))
    .properties(width=1200, height=150)
)

# Right marginal histogram
right_hist = (
    alt.Chart(df)
    .mark_bar(color="#306998", opacity=0.5)
    .encode(y=alt.Y("Y Value:Q", bin=alt.Bin(maxbins=25), title=""), x=alt.X("count()", title="Count"))
    .properties(width=150, height=700)
)

# Combine plots: top histogram above scatter, right histogram beside scatter
combined = (
    (top_hist & (scatter | right_hist))
    .properties(title=alt.Title(text="scatter-marginal · altair · pyplots.ai", fontSize=28, anchor="middle"))
    .configure_axis(labelFontSize=16, titleFontSize=20)
    .configure_title(fontSize=28)
    .configure_view(strokeWidth=0)
)

# Save outputs
combined.save("plot.png", scale_factor=3.0)
combined.save("plot.html")
