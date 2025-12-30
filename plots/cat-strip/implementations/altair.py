""" pyplots.ai
cat-strip: Categorical Strip Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - product ratings across different departments
np.random.seed(42)

categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
n_per_category = 30

data = []
for cat in categories:
    if cat == "Electronics":
        values = np.random.normal(4.2, 0.6, n_per_category)
    elif cat == "Clothing":
        values = np.random.normal(3.8, 0.8, n_per_category)
    elif cat == "Home & Garden":
        values = np.random.normal(4.0, 0.5, n_per_category)
    elif cat == "Sports":
        values = np.random.normal(4.3, 0.4, n_per_category)
    else:  # Books
        values = np.random.normal(4.5, 0.3, n_per_category)

    values = np.clip(values, 1, 5)  # Ratings between 1-5
    for v in values:
        data.append({"Department": cat, "Rating": v})

df = pd.DataFrame(data)

# Create strip plot with jitter
chart = (
    alt.Chart(df)
    .mark_circle(size=200, opacity=0.7, color="#306998")
    .encode(
        x=alt.X("Department:N", title="Department", axis=alt.Axis(labelFontSize=18, titleFontSize=22, labelAngle=0)),
        y=alt.Y(
            "Rating:Q",
            title="Customer Rating (1-5 stars)",
            scale=alt.Scale(domain=[1, 5]),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22),
        ),
        xOffset="jitter:Q",
        tooltip=["Department:N", alt.Tooltip("Rating:Q", format=".2f")],
    )
    .transform_calculate(jitter="sqrt(-2*log(random()))*cos(2*PI*random())")
    .properties(
        width=1600, height=900, title=alt.Title("cat-strip · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(gridColor="#cccccc", gridOpacity=0.3, domainColor="#333333")
    .configure_view(strokeWidth=0)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
