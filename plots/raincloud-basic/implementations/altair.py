""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 90/100 | Created: 2025-12-25
"""

import altair as alt
import numpy as np
import pandas as pd


# Data: Reaction times (ms) for different treatment conditions
np.random.seed(42)

# Create realistic reaction time data with different distributions
control = np.random.normal(450, 60, 80)
treatment_a = np.random.normal(380, 50, 80)  # Faster responses
treatment_b = np.concatenate(
    [
        np.random.normal(350, 30, 50),  # Bimodal distribution
        np.random.normal(450, 40, 30),
    ]
)

data = pd.DataFrame(
    {
        "condition": ["Control"] * 80 + ["Treatment A"] * 80 + ["Treatment B"] * 80,
        "reaction_time": np.concatenate([control, treatment_a, treatment_b]),
    }
)

# Map conditions to numeric positions - HORIZONTAL: y=categories, x=values
condition_order = ["Control", "Treatment A", "Treatment B"]
condition_map = {c: i for i, c in enumerate(condition_order)}
data["condition_num"] = data["condition"].map(condition_map)

# Create jittered y positions for strip plot (rain BELOW the cloud)
np.random.seed(42)
data["jitter"] = np.random.uniform(-0.35, -0.15, len(data))
data["jitter_pos"] = data["condition_num"] + data["jitter"]

# Half-violin (cloud) - positioned on TOP (positive y offset from center)
violin = (
    alt.Chart(data)
    .transform_density(
        "reaction_time", as_=["reaction_time", "density"], groupby=["condition", "condition_num"], extent=[200, 600]
    )
    .transform_calculate(
        # Scale density and offset to create half-violin on TOP (positive y direction)
        violin_pos="datum.condition_num + 0.05 + datum.density * 180"
    )
    .mark_area(orient="vertical", opacity=0.7)
    .encode(
        x=alt.X("reaction_time:Q"),
        y=alt.Y("condition_num:Q", axis=None).scale(domain=[-0.6, 2.6]),
        y2="violin_pos:Q",
        color=alt.Color(
            "condition:N",
            scale=alt.Scale(domain=condition_order, range=["#306998", "#FFD43B", "#4CAF50"]),
            legend=alt.Legend(
                title="Condition",
                titleFontSize=20,
                labelFontSize=18,
                orient="right",
                fillColor="white",
                strokeColor="#cccccc",
                padding=12,
                cornerRadius=4,
            ),
        ),
        tooltip=[
            alt.Tooltip("condition:N", title="Condition"),
            alt.Tooltip("reaction_time:Q", title="Reaction Time (ms)", format=".0f"),
        ],
    )
)

# Box plot - HORIZONTAL orientation (values on x, categories on y)
boxplot = (
    alt.Chart(data)
    .transform_calculate(box_pos="datum.condition_num + 0.02")
    .mark_boxplot(
        size=30,
        orient="horizontal",
        median={"color": "white", "strokeWidth": 3},
        box={"strokeWidth": 2},
        outliers={"opacity": 0},  # Hide outliers, shown as jittered points
    )
    .encode(
        x=alt.X("reaction_time:Q", title="Reaction Time (ms)", scale=alt.Scale(domain=[200, 600])),
        y=alt.Y("box_pos:Q", axis=None),
        color=alt.Color(
            "condition:N", scale=alt.Scale(domain=condition_order, range=["#306998", "#FFD43B", "#4CAF50"])
        ),
    )
)

# Jittered strip plot (rain) - positioned clearly BELOW the center
strip = (
    alt.Chart(data)
    .mark_circle(size=40, opacity=0.6)
    .encode(
        x=alt.X("reaction_time:Q"),
        y=alt.Y("jitter_pos:Q", axis=None),
        color=alt.Color(
            "condition:N", scale=alt.Scale(domain=condition_order, range=["#306998", "#FFD43B", "#4CAF50"])
        ),
        tooltip=[
            alt.Tooltip("condition:N", title="Condition"),
            alt.Tooltip("reaction_time:Q", title="Reaction Time (ms)", format=".1f"),
        ],
    )
)

# Main chart layer with raincloud elements
main_chart = (
    alt.layer(violin, boxplot, strip).properties(width=1600, height=850).interactive()  # Enable zoom and pan
)

# Y-axis labels as a separate chart on the left
y_axis_data = pd.DataFrame({"condition": condition_order, "y_pos": [0, 1, 2]})

y_axis_labels = (
    alt.Chart(y_axis_data)
    .mark_text(fontSize=20, fontWeight="bold", align="right", baseline="middle")
    .encode(y=alt.Y("y_pos:Q", scale=alt.Scale(domain=[-0.6, 2.6]), axis=None), text="condition:N")
    .properties(width=120, height=850)
)

# Combine using horizontal concatenation
chart = (
    alt.hconcat(y_axis_labels, main_chart, spacing=5)
    .properties(title=alt.Title("raincloud-basic · altair · pyplots.ai", fontSize=28, anchor="middle"))
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
