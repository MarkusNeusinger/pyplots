""" pyplots.ai
band-basic: Basic Band Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-17
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Time series with 95% confidence interval
np.random.seed(42)
x = np.linspace(0, 10, 100)
y_center = 2 * np.sin(x) + 0.5 * x  # Central trend

# Confidence band widens over time (realistic uncertainty growth)
uncertainty = 0.5 + 0.15 * x
y_lower = y_center - 1.96 * uncertainty
y_upper = y_center + 1.96 * uncertainty

df = pd.DataFrame({"x": x, "y_center": y_center, "y_lower": y_lower, "y_upper": y_upper})

# Band (area between y_lower and y_upper)
band = (
    alt.Chart(df)
    .mark_area(opacity=0.3, color="#306998")
    .encode(x=alt.X("x:Q", title="Time"), y=alt.Y("y_lower:Q", title="Value"), y2=alt.Y2("y_upper:Q"))
)

# Central trend line
line = alt.Chart(df).mark_line(strokeWidth=4, color="#306998").encode(x="x:Q", y="y_center:Q")

# Combine band and line
chart = (
    (band + line)
    .properties(width=1600, height=900, title=alt.Title("band-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
