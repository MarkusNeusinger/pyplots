"""pyplots.ai
cat-strip: Categorical Strip Plot
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Plant growth measurements across different soil types
np.random.seed(42)

categories = ["Sandy Soil", "Clay Soil", "Loamy Soil", "Peat Soil"]
n_per_category = 25

data = []
# Different distributions for each soil type to show variation
means = [15, 22, 28, 20]
stds = [3, 4, 5, 2.5]

for cat, mean, std in zip(categories, means, stds, strict=True):
    values = np.random.normal(mean, std, n_per_category)
    # Add a few outliers
    if cat == "Clay Soil":
        values = np.append(values, [35, 8])
    elif cat == "Loamy Soil":
        values = np.append(values, [42])
    for v in values:
        data.append({"Soil Type": cat, "Plant Height (cm)": v})

df = pd.DataFrame(data)

# Create strip plot with jitter
chart = (
    alt.Chart(df)
    .mark_circle(size=200, opacity=0.7)
    .encode(
        x=alt.X("Soil Type:N", title="Soil Type", axis=alt.Axis(labelFontSize=18, titleFontSize=22, labelAngle=0)),
        y=alt.Y(
            "Plant Height (cm):Q",
            title="Plant Height (cm)",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22),
        ),
        xOffset="jitter:Q",
        color=alt.Color(
            "Soil Type:N", scale=alt.Scale(range=["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B"]), legend=None
        ),
        tooltip=["Soil Type:N", alt.Tooltip("Plant Height (cm):Q", format=".1f")],
    )
    .transform_calculate(jitter="sqrt(-2*log(random()))*cos(2*PI*random())")
    .properties(
        width=1600, height=900, title=alt.Title("cat-strip · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save as PNG (4800 x 2700 px with scale_factor=3)
chart.save("plot.png", scale_factor=3.0)

# Save interactive HTML version
chart.save("plot.html")
