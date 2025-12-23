""" pyplots.ai
violin-basic: Basic Violin Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-23
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Salary distributions by department with varied shapes
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Support"]
data = []

for cat in categories:
    if cat == "Engineering":
        # Higher salaries with moderate spread
        values = np.random.normal(92000, 16000, 150)
    elif cat == "Marketing":
        # Mid-range salaries
        values = np.random.normal(70000, 13000, 150)
    elif cat == "Sales":
        # Bimodal: base salary + high performers with commissions
        values = np.concatenate([np.random.normal(50000, 8000, 75), np.random.normal(92000, 11000, 75)])
    else:  # Support
        # Lower salary, tighter distribution
        values = np.random.normal(55000, 10000, 150)

    for v in values:
        data.append({"Department": cat, "Salary": v})

df = pd.DataFrame(data)

# Calculate statistics for quartile markers
stats = (
    df.groupby("Department")["Salary"]
    .agg(q1=lambda x: x.quantile(0.25), median=lambda x: x.quantile(0.5), q3=lambda x: x.quantile(0.75))
    .reset_index()
)

# Merge stats for layering
df_with_stats = df.merge(stats, on="Department")

# Colors - Python palette
colors = ["#306998", "#FFD43B", "#4B8BBE", "#FFE873"]
color_scale = alt.Scale(domain=categories, range=colors)

# Base chart
base = alt.Chart(df_with_stats)

# Violin shape using kernel density transform
violin = (
    base.transform_density(
        density="Salary",
        as_=["Salary", "density"],
        groupby=["Department"],
        extent=[df["Salary"].min() - 8000, df["Salary"].max() + 8000],
    )
    .mark_area(orient="horizontal", opacity=0.75)
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

# IQR rule (black vertical line)
quartile_rule = base.mark_rule(color="black", strokeWidth=5).encode(y="q1:Q", y2="q3:Q")

# Median point (white dot with black border)
median_point = base.mark_point(color="white", size=250, filled=True, strokeWidth=3, stroke="black").encode(y="median:Q")

# Combine layers and facet by department
chart = (
    alt.layer(violin, quartile_rule, median_point)
    .facet(
        column=alt.Column(
            "Department:N",
            header=alt.Header(labelFontSize=20, labelOrient="bottom", title=None, labelPadding=15),
            sort=categories,
        )
    )
    .resolve_scale(x="independent")
    .properties(title=alt.Title("violin-basic · altair · pyplots.ai", fontSize=28, anchor="middle"))
    .configure_facet(spacing=20)
    .configure_view(stroke=None, continuousWidth=350, continuousHeight=750)
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3, gridDash=[3, 3])
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
