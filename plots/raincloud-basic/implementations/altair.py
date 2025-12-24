"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-24
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

# Create jittered y positions for strip plot
np.random.seed(42)
data["jitter"] = np.random.uniform(-0.15, 0.05, len(data))

# Map conditions to numeric positions for layering
condition_map = {"Control": 0, "Treatment A": 1, "Treatment B": 2}
data["condition_num"] = data["condition"].map(condition_map)
data["jitter_pos"] = data["condition_num"] + data["jitter"] + 0.25

# Half-violin (density estimate) - positioned to one side
violin = (
    alt.Chart(data)
    .transform_density(
        "reaction_time", as_=["reaction_time", "density"], groupby=["condition", "condition_num"], extent=[200, 600]
    )
    .transform_calculate(
        # Scale density and offset to create half-violin on left side
        violin_width="datum.density * 150",
        violin_pos="datum.condition_num - datum.density * 150",
    )
    .mark_area(orient="horizontal", opacity=0.7)
    .encode(
        y=alt.Y("reaction_time:Q"),
        x=alt.X("violin_pos:Q", axis=None),
        x2="condition_num:Q",
        color=alt.Color(
            "condition:N",
            scale=alt.Scale(range=["#306998", "#FFD43B", "#4CAF50"]),
            legend=alt.Legend(title="Condition", titleFontSize=20, labelFontSize=18, orient="right"),
        ),
    )
)

# Box plot in the middle
boxplot = (
    alt.Chart(data)
    .mark_boxplot(
        size=40,
        median={"color": "white", "strokeWidth": 3},
        box={"strokeWidth": 2},
        outliers={"opacity": 0},  # Hide outliers, shown as jittered points
    )
    .encode(
        x=alt.X("condition_num:Q", axis=None),
        y=alt.Y("reaction_time:Q", title="Reaction Time (ms)", scale=alt.Scale(domain=[200, 600])),
        color=alt.Color("condition:N", scale=alt.Scale(range=["#306998", "#FFD43B", "#4CAF50"])),
    )
)

# Jittered strip plot (rain) - positioned to the right
strip = (
    alt.Chart(data)
    .mark_circle(size=80, opacity=0.6)
    .encode(
        x=alt.X("jitter_pos:Q", axis=None),
        y=alt.Y("reaction_time:Q"),
        color=alt.Color("condition:N", scale=alt.Scale(range=["#306998", "#FFD43B", "#4CAF50"])),
    )
)

# Combine all layers
chart = (
    alt.layer(violin, boxplot, strip)
    .properties(
        width=1600, height=900, title=alt.Title("raincloud-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
    .configure_legend(strokeColor="gray", padding=10)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
