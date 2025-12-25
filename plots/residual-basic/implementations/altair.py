""" pyplots.ai
residual-basic: Residual Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-25
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Simulate regression with some heteroscedasticity for realistic diagnostics
np.random.seed(42)
n_points = 100

# Create fitted values
fitted = np.linspace(10, 50, n_points)

# Create residuals with slight heteroscedasticity pattern (variance increases with fitted)
# This creates realistic diagnostic data showing both well-behaved and problematic regions
base_residuals = np.random.randn(n_points)
# Add some structure: slight funnel shape and a few outliers
residuals = base_residuals * (1 + 0.02 * (fitted - 30))
# Add a few outliers for interesting diagnostics
residuals[15] = 4.5
residuals[75] = -4.2
residuals[50] = 3.8

df = pd.DataFrame({"fitted": fitted, "residuals": residuals})

# Base scatter plot with residuals
points = (
    alt.Chart(df)
    .mark_point(size=150, filled=True, opacity=0.6, color="#306998")
    .encode(
        x=alt.X("fitted:Q", title="Fitted Values", scale=alt.Scale(domain=[5, 55])),
        y=alt.Y("residuals:Q", title="Residuals", scale=alt.Scale(domain=[-6, 6])),
        tooltip=["fitted:Q", "residuals:Q"],
    )
)

# Horizontal reference line at y=0
zero_line = (
    alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="#333333", strokeWidth=2, strokeDash=[6, 4]).encode(y="y:Q")
)

# LOESS smoothed trend line to detect non-linear patterns
loess_line = (
    alt.Chart(df)
    .mark_line(color="#FFD43B", strokeWidth=3, opacity=0.8)
    .transform_loess("fitted", "residuals", bandwidth=0.4)
    .encode(x="fitted:Q", y="residuals:Q")
)

# Combine layers
chart = (
    alt.layer(zero_line, points, loess_line)
    .properties(
        width=1600, height=900, title=alt.Title("residual-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
