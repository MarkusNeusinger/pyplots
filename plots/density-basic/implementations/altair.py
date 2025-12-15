"""
density-basic: Basic Density Plot
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - bimodal distribution to show density estimation capability
np.random.seed(42)
values = np.concatenate(
    [
        np.random.normal(loc=35, scale=8, size=200),  # First peak
        np.random.normal(loc=65, scale=10, size=150),  # Second peak
    ]
)

df = pd.DataFrame({"values": values})

# Create density plot using transform_density
chart = (
    alt.Chart(df)
    .transform_density(
        "values",
        as_=["values", "density"],
        bandwidth=5,  # Smoothing parameter
    )
    .mark_area(
        opacity=0.7,
        color="#306998",  # Python Blue
        line={"color": "#306998", "strokeWidth": 3},
    )
    .encode(
        x=alt.X("values:Q", title="Values", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
        y=alt.Y("density:Q", title="Density", axis=alt.Axis(labelFontSize=18, titleFontSize=22)),
    )
    .properties(width=1600, height=900, title=alt.Title(text="density-basic · altair · pyplots.ai", fontSize=28))
    .configure_view(strokeWidth=0)
)

# Save as PNG (1600 * 3 = 4800, 900 * 3 = 2700)
chart.save("plot.png", scale_factor=3.0)

# Save as interactive HTML
chart.interactive().save("plot.html")
