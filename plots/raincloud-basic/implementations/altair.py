""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-25
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

# Create jittered x positions for strip plot (rain below the cloud)
# For vertical layout: rain should be on LEFT (lower x values), cloud on RIGHT (higher x values)
np.random.seed(42)
data["jitter"] = np.random.uniform(-0.35, -0.15, len(data))  # Wider range, more offset left

# Map conditions to numeric positions for layering
condition_map = {"Control": 0, "Treatment A": 1, "Treatment B": 2}
data["condition_num"] = data["condition"].map(condition_map)
data["jitter_pos"] = data["condition_num"] + data["jitter"]

# Half-violin (cloud) - positioned to the RIGHT side (positive offset from center)
violin = (
    alt.Chart(data)
    .transform_density(
        "reaction_time", as_=["reaction_time", "density"], groupby=["condition", "condition_num"], extent=[200, 600]
    )
    .transform_calculate(
        # Scale density and offset to create half-violin on RIGHT side (cloud)
        violin_pos="datum.condition_num + 0.05 + datum.density * 180"
    )
    .mark_area(orient="horizontal", opacity=0.7)
    .encode(
        y=alt.Y("reaction_time:Q"),
        x=alt.X("condition_num:Q", axis=None).scale(domain=[-0.6, 2.6]),
        x2="violin_pos:Q",
        color=alt.Color(
            "condition:N",
            scale=alt.Scale(range=["#306998", "#FFD43B", "#4CAF50"]),
            legend=alt.Legend(title="Condition", titleFontSize=20, labelFontSize=18, orient="right"),
        ),
    )
)

# Box plot - slightly offset towards the right (between rain and cloud)
boxplot = (
    alt.Chart(data)
    .transform_calculate(box_pos="datum.condition_num + 0.02")
    .mark_boxplot(
        size=30,
        median={"color": "white", "strokeWidth": 3},
        box={"strokeWidth": 2},
        outliers={"opacity": 0},  # Hide outliers, shown as jittered points
    )
    .encode(
        x=alt.X("box_pos:Q", axis=None),
        y=alt.Y("reaction_time:Q", title="Reaction Time (ms)", scale=alt.Scale(domain=[200, 600])),
        color=alt.Color("condition:N", scale=alt.Scale(range=["#306998", "#FFD43B", "#4CAF50"])),
    )
)

# Jittered strip plot (rain) - positioned clearly to the LEFT (below/before the cloud)
strip = (
    alt.Chart(data)
    .mark_circle(size=50, opacity=0.6)  # Smaller point size to reduce overlap
    .encode(
        x=alt.X("jitter_pos:Q", axis=None),
        y=alt.Y("reaction_time:Q"),
        color=alt.Color("condition:N", scale=alt.Scale(range=["#306998", "#FFD43B", "#4CAF50"])),
    )
)

# Create X-axis using rule marks at condition positions with text labels
x_axis_data = pd.DataFrame({"condition": ["Control", "Treatment A", "Treatment B"], "x_pos": [0, 1, 2]})

x_axis_labels = (
    alt.Chart(x_axis_data)
    .mark_text(fontSize=20, fontWeight="bold", baseline="top", dy=15)
    .encode(x=alt.X("x_pos:Q", scale=alt.Scale(domain=[-0.6, 2.6])), y=alt.value(900), text="condition:N")
)

# Combine all layers
chart = (
    alt.layer(violin, boxplot, strip, x_axis_labels)
    .properties(
        width=1600, height=900, title=alt.Title("raincloud-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
    .configure_legend(padding=10)  # Removed stroke border for cleaner look
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
