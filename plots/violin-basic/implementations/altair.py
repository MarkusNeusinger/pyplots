"""
violin-basic: Basic Violin Plot
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Employee performance scores grouped by department
np.random.seed(42)

departments = ["Engineering", "Sales", "Marketing", "Finance", "HR"]
data = []

for dept in departments:
    # Generate different distributions per department
    if dept == "Engineering":
        scores = np.random.normal(75, 10, 150)
    elif dept == "Sales":
        scores = np.concatenate([np.random.normal(60, 8, 80), np.random.normal(85, 5, 70)])
    elif dept == "Marketing":
        scores = np.random.normal(70, 12, 120)
    elif dept == "Finance":
        scores = np.random.normal(80, 8, 100)
    else:  # HR
        scores = np.random.normal(72, 15, 90)

    scores = np.clip(scores, 30, 100)  # Clip to realistic range
    for score in scores:
        data.append({"Department": dept, "Performance Score": score})

df = pd.DataFrame(data)

# Color scale for all components
color_scale = alt.Scale(domain=departments, range=["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6"])

# Create violin shape using density transform
violin = (
    alt.Chart(df)
    .transform_density(
        density="Performance Score", as_=["Performance Score", "density"], extent=[30, 100], groupby=["Department"]
    )
    .mark_area(orient="horizontal")
    .encode(
        y=alt.Y("Performance Score:Q", title="Performance Score", scale=alt.Scale(domain=[30, 100])),
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

# Inner box plot showing quartiles
boxplot = (
    alt.Chart(df)
    .mark_boxplot(size=8, color="black", median={"color": "white", "size": 8})
    .encode(y=alt.Y("Performance Score:Q", scale=alt.Scale(domain=[30, 100])), color=alt.value("black"))
)

# Combine violin and boxplot layers
layered = alt.layer(violin, boxplot)

# Facet by department
# Target: 4800 x 2700 px with scale_factor=3.0 -> base 1600 x 900
# 5 facets with spacing -> ~300px width each, 800px height
chart = (
    layered.properties(width=300, height=800)
    .facet(
        column=alt.Column(
            "Department:N",
            header=alt.Header(
                titleOrient="bottom", labelOrient="bottom", labelFontSize=16, title="Department", titleFontSize=16
            ),
            sort=departments,
        )
    )
    .properties(title=alt.Title("Employee Performance Scores by Department", fontSize=20))
    .configure_facet(spacing=15)
    .configure_view(stroke=None)
    .configure_axis(labelFontSize=14, titleFontSize=16)
    .configure_legend(titleFontSize=16, labelFontSize=14)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
