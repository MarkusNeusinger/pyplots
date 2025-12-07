"""
box-basic: Basic Box Plot
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
data = pd.DataFrame(
    {
        "group": ["A"] * 50 + ["B"] * 50 + ["C"] * 50 + ["D"] * 50,
        "value": np.concatenate(
            [
                np.random.normal(50, 10, 50),
                np.random.normal(60, 15, 50),
                np.random.normal(45, 8, 50),
                np.random.normal(70, 20, 50),
            ]
        ),
    }
)

# Color palette from style guide
colors = ["#306998", "#FFD43B", "#DC2626", "#059669"]

# Create chart
chart = (
    alt.Chart(data)
    .mark_boxplot(size=60, outliers={"size": 8})
    .encode(
        x=alt.X("group:N", title="Group", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
        y=alt.Y("value:Q", title="Value", axis=alt.Axis(labelFontSize=16, titleFontSize=20)),
        color=alt.Color("group:N", scale=alt.Scale(domain=["A", "B", "C", "D"], range=colors), legend=None),
    )
    .properties(width=1600, height=900, title=alt.Title("Basic Box Plot", fontSize=20))
    .configure_view(strokeWidth=0)
)

# Save (4800 × 2700 px via scale_factor=3)
chart.save("plot.png", scale_factor=3.0)
