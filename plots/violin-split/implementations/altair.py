"""pyplots.ai
violin-split: Split Violin Plot
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import altair as alt
import numpy as np
import pandas as pd


# Data: Test scores by department comparing control vs treatment groups
np.random.seed(42)

departments = ["Engineering", "Marketing", "Sales", "HR"]
data = []

for dept in departments:
    # Control group - baseline performance
    if dept == "Engineering":
        control_scores = np.random.normal(72, 12, 100)
        treatment_scores = np.random.normal(85, 10, 100)  # Larger improvement
    elif dept == "Marketing":
        control_scores = np.random.normal(68, 15, 100)
        treatment_scores = np.random.normal(78, 12, 100)
    elif dept == "Sales":
        control_scores = np.random.normal(75, 14, 100)
        treatment_scores = np.random.normal(80, 11, 100)
    else:  # HR
        control_scores = np.random.normal(70, 10, 100)
        treatment_scores = np.random.normal(76, 9, 100)

    for score in control_scores:
        data.append({"Department": dept, "Score": np.clip(score, 30, 100), "Group": "Control"})
    for score in treatment_scores:
        data.append({"Department": dept, "Score": np.clip(score, 30, 100), "Group": "Treatment"})

df = pd.DataFrame(data)

# Create split violin using density transform with xOffset for split
# Each half of the violin is a separate area mark positioned with xOffset

base = alt.Chart(df).transform_density(
    density="Score", as_=["Score", "density"], groupby=["Department", "Group"], extent=[30, 100]
)

# For split violin, we transform density to go left/right based on Group
split_violin = (
    base.transform_calculate(
        # Control goes left (negative), Treatment goes right (positive)
        signed_density="datum.Group === 'Control' ? -datum.density : datum.density"
    )
    .mark_area(orient="horizontal", opacity=0.8)
    .encode(
        x=alt.X("signed_density:Q", title=None, axis=alt.Axis(labels=False, ticks=False, domain=False), stack=None),
        y=alt.Y("Score:Q", title="Score", scale=alt.Scale(domain=[30, 100])),
        color=alt.Color(
            "Group:N",
            scale=alt.Scale(domain=["Control", "Treatment"], range=["#306998", "#FFD43B"]),
            legend=alt.Legend(title="Group", titleFontSize=18, labelFontSize=16, symbolSize=400, orient="right"),
        ),
        column=alt.Column("Department:N", title=None, header=alt.Header(labelFontSize=20, labelPadding=15)),
    )
)

# Configure chart
chart = (
    split_violin.properties(width=200, height=500, title=alt.Title("violin-split · altair · pyplots.ai", fontSize=28))
    .configure_facet(spacing=50)
    .configure_view(stroke=None)
    .configure_axis(labelFontSize=16, titleFontSize=20, titlePadding=15)
    .configure_title(anchor="middle", offset=20)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
