"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: altair 6.0.0 | Python 3.14
Quality: 77/100 | Created: 2025-12-25
"""

import altair as alt
import numpy as np
import pandas as pd


# Data: Reaction times (ms) for different treatment conditions
np.random.seed(42)

control = np.random.normal(450, 60, 80)
treatment_a = np.random.normal(380, 50, 80)
treatment_b = np.concatenate([np.random.normal(340, 25, 50), np.random.normal(460, 35, 30)])

data = pd.DataFrame(
    {
        "condition": ["Control"] * 80 + ["Treatment A"] * 80 + ["Treatment B"] * 80,
        "reaction_time": np.concatenate([control, treatment_a, treatment_b]),
    }
)

# Map conditions to numeric y positions with wider spacing (1.5 units apart)
condition_order = ["Control", "Treatment A", "Treatment B"]
condition_map = {c: i * 1.5 for i, c in enumerate(condition_order)}
data["condition_num"] = data["condition"].map(condition_map)

# Jitter positions for rain — BELOW baseline (tight range to avoid category overlap)
data["jitter_pos"] = data["condition_num"] + np.random.uniform(-0.30, -0.08, len(data))

# Compute box plot statistics per condition
box_stats = data.groupby("condition")["reaction_time"].describe()[["25%", "50%", "75%"]]
box_stats["iqr"] = box_stats["75%"] - box_stats["25%"]
box_stats["lower_whisker"] = box_stats["25%"] - 1.5 * box_stats["iqr"]
box_stats["upper_whisker"] = box_stats["75%"] + 1.5 * box_stats["iqr"]
for cond in condition_order:
    cond_data = data[data["condition"] == cond]["reaction_time"]
    box_stats.loc[cond, "lower_whisker"] = max(box_stats.loc[cond, "lower_whisker"], cond_data.min())
    box_stats.loc[cond, "upper_whisker"] = min(box_stats.loc[cond, "upper_whisker"], cond_data.max())

box_df = pd.DataFrame(
    {
        "condition": condition_order,
        "condition_num": [condition_map[c] for c in condition_order],
        "q1": [box_stats.loc[c, "25%"] for c in condition_order],
        "median": [box_stats.loc[c, "50%"] for c in condition_order],
        "q3": [box_stats.loc[c, "75%"] for c in condition_order],
        "lower_w": [box_stats.loc[c, "lower_whisker"] for c in condition_order],
        "upper_w": [box_stats.loc[c, "upper_whisker"] for c in condition_order],
    }
)

# Color palette: Python Blue, warm gold, fresh green
colors = ["#306998", "#FFD43B", "#4CAF50"]
x_scale = alt.Scale(domain=[220, 580])
y_domain = [-0.5, 3.9]
x_axis = alt.Axis(
    titleFontSize=22,
    labelFontSize=18,
    grid=True,
    gridOpacity=0.35,
    gridColor="#e0e0e0",
    domainColor="#888888",
    tickColor="#888888",
)

# Half-violin cloud — extends ABOVE baseline (reduced scaling to prevent overlap)
violin = (
    alt.Chart(data)
    .transform_density(
        "reaction_time", as_=["reaction_time", "density"], groupby=["condition", "condition_num"], extent=[220, 580]
    )
    .transform_calculate(violin_pos="datum.condition_num + 0.04 + datum.density * 105")
    .mark_area(orient="vertical", opacity=0.65, interpolate="monotone")
    .encode(
        x=alt.X("reaction_time:Q", title="Reaction Time (ms)", scale=x_scale, axis=x_axis),
        y=alt.Y("condition_num:Q", axis=None, scale=alt.Scale(domain=y_domain)),
        y2="violin_pos:Q",
        color=alt.Color(
            "condition:N",
            scale=alt.Scale(domain=condition_order, range=colors),
            legend=alt.Legend(
                title="Condition",
                titleFontSize=20,
                titleFontWeight="bold",
                labelFontSize=18,
                orient="right",
                fillColor="white",
                strokeColor="#cccccc",
                padding=14,
                cornerRadius=6,
                symbolSize=200,
            ),
        ),
        tooltip=[
            alt.Tooltip("condition:N", title="Condition"),
            alt.Tooltip("reaction_time:Q", title="Reaction Time (ms)", format=".0f"),
        ],
    )
)

# Manual box plot — IQR box with dark outline
box_iqr = (
    alt.Chart(box_df)
    .mark_bar(height=18, stroke="#333333", strokeWidth=2, cornerRadius=2)
    .encode(
        x=alt.X("q1:Q", scale=x_scale),
        x2="q3:Q",
        y=alt.Y("condition_num:Q", axis=None, scale=alt.Scale(domain=y_domain)),
        color=alt.Color("condition:N", scale=alt.Scale(domain=condition_order, range=colors)),
    )
)

# Median line — contrasting red
box_median = (
    alt.Chart(box_df)
    .mark_tick(thickness=3.5, color="#E8413C", orient="vertical")
    .encode(x=alt.X("median:Q", scale=x_scale), y=alt.Y("condition_num:Q", axis=None, scale=alt.Scale(domain=y_domain)))
)

# Whisker lines
box_whiskers = (
    alt.Chart(box_df)
    .mark_rule(strokeWidth=1.5, color="#555555")
    .encode(
        x=alt.X("lower_w:Q", scale=x_scale),
        x2="upper_w:Q",
        y=alt.Y("condition_num:Q", axis=None, scale=alt.Scale(domain=y_domain)),
    )
)

# Jittered strip — rain BELOW baseline
strip = (
    alt.Chart(data)
    .mark_circle(size=50, opacity=0.55, stroke="#333333", strokeWidth=0.3)
    .encode(
        x=alt.X("reaction_time:Q", scale=x_scale),
        y=alt.Y("jitter_pos:Q", axis=None),
        color=alt.Color("condition:N", scale=alt.Scale(domain=condition_order, range=colors)),
        tooltip=[
            alt.Tooltip("condition:N", title="Condition"),
            alt.Tooltip("reaction_time:Q", title="Reaction Time (ms)", format=".1f"),
        ],
    )
)

# Annotation: highlight Treatment B bimodality
annotation_data = pd.DataFrame(
    [{"x": 340, "y": 3.0 + 0.65, "text": "Peak 1"}, {"x": 460, "y": 3.0 + 0.50, "text": "Peak 2"}]
)
bimodal_labels = (
    alt.Chart(annotation_data)
    .mark_text(fontSize=16, fontStyle="italic", color="#555555", fontWeight="bold")
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q", axis=None), text="text:N")
)

arrow_data = pd.DataFrame([{"x": 355, "y": 3.0 + 0.58, "x2": 445, "y2": 3.0 + 0.53}])
bimodal_arrow = (
    alt.Chart(arrow_data)
    .mark_rule(strokeDash=[4, 3], color="#777777", strokeWidth=1.5)
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q", axis=None), x2="x2:Q", y2="y2:Q")
)

note_data = pd.DataFrame([{"x": 400, "y": 3.0 + 0.78, "text": "Bimodal distribution"}])
bimodal_note = (
    alt.Chart(note_data)
    .mark_text(fontSize=15, color="#666666", fontStyle="italic")
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q", axis=None), text="text:N")
)

# Y-axis tick labels (clip=False renders outside the plot area)
y_label_data = pd.DataFrame({"condition": condition_order, "y_pos": [0, 1.5, 3.0]})
y_labels = (
    alt.Chart(y_label_data)
    .mark_text(fontSize=20, fontWeight="bold", align="right", baseline="middle", dx=-25, clip=False)
    .encode(x=alt.X("x:Q"), y=alt.Y("y_pos:Q", axis=None, scale=alt.Scale(domain=y_domain)), text="condition:N")
    .transform_calculate(x="220")
)

# Compose all layers
chart = (
    alt.layer(violin, box_whiskers, box_iqr, box_median, strip, bimodal_labels, bimodal_arrow, bimodal_note, y_labels)
    .resolve_scale(y="shared", x="shared")
    .properties(
        width=1600,
        height=900,
        title=alt.Title("raincloud-basic · altair · pyplots.ai", fontSize=28, anchor="middle", offset=20),
    )
    .configure(padding={"left": 140, "right": 20, "top": 10, "bottom": 40})
    .configure_axis(
        labelFontSize=18,
        titleFontSize=22,
        gridColor="#e0e0e0",
        gridOpacity=0.35,
        domainColor="#888888",
        tickColor="#888888",
    )
    .configure_view(strokeWidth=0)
    .interactive()
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
