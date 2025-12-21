""" pyplots.ai
violin-basic: Basic Violin Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-14
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Support"]
data = []

for cat in categories:
    # Different distribution shapes per category
    if cat == "Engineering":
        values = np.random.normal(85000, 15000, 150)
    elif cat == "Marketing":
        values = np.random.normal(70000, 12000, 150)
    elif cat == "Sales":
        # Bimodal distribution for sales
        values = np.concatenate([np.random.normal(55000, 8000, 75), np.random.normal(90000, 10000, 75)])
    else:  # Support
        values = np.random.normal(55000, 10000, 150)

    for v in values:
        data.append({"Department": cat, "Salary": v})

df = pd.DataFrame(data)

# Calculate statistics for each department
stats = (
    df.groupby("Department")["Salary"]
    .agg(q1=lambda x: x.quantile(0.25), median=lambda x: x.quantile(0.5), q3=lambda x: x.quantile(0.75))
    .reset_index()
)

# Merge stats back to main df for layering
df_with_stats = df.merge(stats, on="Department")

# Define colors
colors = ["#306998", "#FFD43B", "#306998", "#FFD43B"]
color_scale = alt.Scale(domain=categories, range=colors)

# Base chart with shared data
base = alt.Chart(df_with_stats)

# Violin shape using density transform
violin = (
    base.transform_density(
        density="Salary",
        as_=["Salary", "density"],
        groupby=["Department"],
        extent=[df["Salary"].min() - 5000, df["Salary"].max() + 5000],
    )
    .mark_area(orient="horizontal", opacity=0.7)
    .encode(
        y=alt.Y("Salary:Q", title="Salary ($)"),
        x=alt.X(
            "density:Q",
            stack="center",
            impute=None,
            title=None,
            axis=alt.Axis(labels=False, values=[0], grid=False, ticks=False),
        ),
        color=alt.Color("Department:N", scale=color_scale, legend=None),
    )
)

# Quartile rule (IQR line)
quartile_rule = base.mark_rule(color="black", strokeWidth=4).encode(y="q1:Q", y2="q3:Q")

# Median point
median_point = base.mark_point(color="white", size=200, filled=True, strokeWidth=2, stroke="black").encode(y="median:Q")

# Combine layers, then facet
chart = (
    alt.layer(violin, quartile_rule, median_point)
    .facet(
        column=alt.Column(
            "Department:N",
            header=alt.Header(labelFontSize=18, labelOrient="bottom", title=None, labelPadding=10),
            sort=categories,
        )
    )
    .resolve_scale(x="independent")
    .properties(title=alt.Title("violin-basic · altair · pyplots.ai", fontSize=28))
    .configure_facet(spacing=15)
    .configure_view(stroke=None, continuousWidth=350, continuousHeight=700)
    .configure_axis(labelFontSize=16, titleFontSize=20, gridOpacity=0.3)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
