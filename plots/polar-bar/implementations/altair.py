"""pyplots.ai
polar-bar: Polar Bar Chart (Wind Rose)
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Wind frequency by direction
np.random.seed(42)

directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

# Realistic wind frequency data (higher from west/southwest - typical mid-latitude pattern)
frequencies = [8, 5, 6, 4, 7, 9, 12, 10, 9, 11, 15, 18, 20, 16, 14, 10]

# Create DataFrame
n_dirs = len(directions)
angle_step_rad = 2 * np.pi / n_dirs  # radians per direction

df = pd.DataFrame({"direction": directions, "frequency": frequencies, "order": range(n_dirs)})

# Create arc data in radians
# Altair mark_arc with radians: 0 at 3 o'clock (right), increasing counter-clockwise
# For compass (N at top, clockwise):
# - N (order=0) should be at top = pi/2 radians in math convention
# - Going clockwise means decreasing angle
# Transform: theta = pi/2 - compass_radians
arc_df = df[["direction", "frequency", "order"]].copy()
compass_start_rad = df["order"] * angle_step_rad
compass_end_rad = (df["order"] + 1) * angle_step_rad
arc_df["theta"] = np.pi / 2 - compass_start_rad
arc_df["theta2"] = np.pi / 2 - compass_end_rad

# Color scale based on frequency
color_scale = alt.Scale(
    domain=[arc_df["frequency"].min(), arc_df["frequency"].max()],
    range=["#FFD43B", "#306998"],  # Python Yellow to Python Blue
)

# Create the wind rose using arc marks
base = (
    alt.Chart(arc_df)
    .mark_arc(stroke="white", strokeWidth=3)
    .encode(
        theta=alt.Theta("theta:Q"),
        theta2="theta2:Q",
        radius=alt.Radius("frequency:Q", scale=alt.Scale(type="sqrt", zero=True, rangeMax=350)),
        color=alt.Color(
            "frequency:Q",
            scale=color_scale,
            legend=alt.Legend(title="Frequency (%)", titleFontSize=22, labelFontSize=18, orient="right", offset=20),
        ),
        tooltip=[alt.Tooltip("direction:N", title="Direction"), alt.Tooltip("frequency:Q", title="Frequency (%)")],
    )
)

# Create direction labels at correct compass positions
# Using same transform: theta = pi/2 - compass_radians
label_radius = 28
label_data = []
for _idx, row in df.iterrows():
    compass_rad = row["order"] * angle_step_rad + angle_step_rad / 2
    theta = np.pi / 2 - compass_rad
    label_data.append(
        {"direction": row["direction"], "x": label_radius * np.cos(theta), "y": label_radius * np.sin(theta)}
    )

label_df = pd.DataFrame(label_data)

# Only show cardinal and intercardinal directions for cleaner labels
main_directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
label_df_filtered = label_df[label_df["direction"].isin(main_directions)]

labels = (
    alt.Chart(label_df_filtered)
    .mark_text(fontSize=24, fontWeight="bold", color="#333333")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[-35, 35]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[-35, 35]), axis=None),
        text="direction:N",
    )
)

# Combine chart with labels
chart = (
    alt.layer(base, labels)
    .properties(
        width=900,
        height=900,
        title=alt.Title("polar-bar · altair · pyplots.ai", fontSize=32, anchor="middle", offset=20),
    )
    .configure_view(strokeWidth=0)
    .configure_legend(titleFontSize=22, labelFontSize=18)
)

# Save as PNG and HTML (900 * 4 = 3600 for square format)
chart.save("plot.png", scale_factor=4.0)
chart.save("plot.html")
