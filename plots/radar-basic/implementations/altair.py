"""
radar-basic: Basic Radar Chart
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Performance metrics for two athletes
categories = ["Speed", "Power", "Accuracy", "Stamina", "Technique"]
athlete_a = [85, 70, 90, 65, 80]
athlete_b = [70, 85, 75, 80, 70]

# Calculate angles for each category (starting from top, going clockwise)
n = len(categories)
angles = [2 * np.pi * i / n - np.pi / 2 for i in range(n)]


# Create DataFrame for radar polygon
def create_radar_data(values, entity_name, categories, angles):
    # Close the polygon by repeating the first point
    values_closed = values + [values[0]]
    angles_closed = angles + [angles[0]]
    categories_closed = categories + [categories[0]]

    x = [v * np.cos(a) for v, a in zip(values_closed, angles_closed, strict=True)]
    y = [v * np.sin(a) for v, a in zip(values_closed, angles_closed, strict=True)]

    return pd.DataFrame(
        {
            "x": x,
            "y": y,
            "value": values_closed,
            "category": categories_closed,
            "entity": entity_name,
            "order": list(range(len(values_closed))),
        }
    )


df_a = create_radar_data(athlete_a, "Athlete A", categories, angles)
df_b = create_radar_data(athlete_b, "Athlete B", categories, angles)
df = pd.concat([df_a, df_b], ignore_index=True)

# Create grid data (concentric circles at 25, 50, 75, 100)
grid_levels = [25, 50, 75, 100]
grid_points = 100

grid_data = []
for level in grid_levels:
    for i in range(grid_points + 1):
        angle = 2 * np.pi * i / grid_points
        grid_data.append({"x": level * np.cos(angle), "y": level * np.sin(angle), "level": level, "order": i})
df_grid = pd.DataFrame(grid_data)

# Create axis lines (spokes)
axis_data = []
for i, (cat, angle) in enumerate(zip(categories, angles, strict=True)):
    axis_data.append({"x": 0, "y": 0, "category": cat, "order": 0, "group": i})
    axis_data.append({"x": 100 * np.cos(angle), "y": 100 * np.sin(angle), "category": cat, "order": 1, "group": i})
df_axes = pd.DataFrame(axis_data)

# Create axis labels positioned just outside the outer circle
label_data = []
for cat, angle in zip(categories, angles, strict=True):
    # Adjust label position based on angle for better placement
    radius = 115
    label_data.append({"x": radius * np.cos(angle), "y": radius * np.sin(angle), "category": cat})
df_labels = pd.DataFrame(label_data)

# Color palette from style guide
colors = ["#306998", "#DC2626"]

# Grid circles
grid_chart = (
    alt.Chart(df_grid)
    .mark_line(strokeWidth=1, stroke="#cccccc", strokeOpacity=0.6)
    .encode(
        x=alt.X("x:Q", axis=None, scale=alt.Scale(domain=[-140, 140])),
        y=alt.Y("y:Q", axis=None, scale=alt.Scale(domain=[-140, 140])),
        detail="level:N",
        order="order:O",
    )
)

# Axis lines (spokes)
axes_chart = (
    alt.Chart(df_axes)
    .mark_line(strokeWidth=1, stroke="#999999", strokeOpacity=0.7)
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), detail="group:N", order="order:O")
)

# Axis labels
labels_chart = (
    alt.Chart(df_labels)
    .mark_text(fontSize=18, fontWeight="bold")
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), text="category:N")
)

# Radar polygon lines with filled area using mark_trail for thickness effect
# Create separate charts for each entity to enable proper polygon rendering
radar_line_a = (
    alt.Chart(df_a)
    .mark_line(strokeWidth=3, opacity=0.9, color=colors[0])
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), order="order:O")
)

radar_line_b = (
    alt.Chart(df_b)
    .mark_line(strokeWidth=3, opacity=0.9, color=colors[1])
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), order="order:O")
)

# Use geoshape with custom GeoJSON-like polygon for filled areas
# Since Altair doesn't support arbitrary polygon fills well, use mark_trail for a thicker line effect
radar_trail_a = (
    alt.Chart(df_a)
    .mark_trail(opacity=0.3)
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), size=alt.value(30), color=alt.value(colors[0]), order="order:O")
)

radar_trail_b = (
    alt.Chart(df_b)
    .mark_trail(opacity=0.3)
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), size=alt.value(30), color=alt.value(colors[1]), order="order:O")
)

# Data points on radar (with legend)
radar_points = (
    alt.Chart(df)
    .mark_point(filled=True, size=120)
    .encode(
        x=alt.X("x:Q"),
        y=alt.Y("y:Q"),
        color=alt.Color(
            "entity:N",
            scale=alt.Scale(range=colors),
            legend=alt.Legend(title="Entity", orient="bottom", titleFontSize=18, labelFontSize=16),
        ),
        tooltip=["category:N", "value:Q", "entity:N"],
    )
)

# Combine all layers
chart = (
    alt.layer(
        grid_chart, axes_chart, radar_trail_a, radar_trail_b, radar_line_a, radar_line_b, radar_points, labels_chart
    )
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            text="Basic Radar Chart",
            subtitle="Comparing performance metrics across two athletes",
            fontSize=28,
            subtitleFontSize=18,
            anchor="middle",
        ),
    )
    .configure_view(strokeWidth=0)
    .configure_axis(grid=False, domain=False, labels=False, ticks=False, title=None)
)

# Save as PNG (scale_factor=3 gives 4800x2700)
chart.save("plot.png", scale_factor=3.0)

# Save as HTML for interactivity
chart.save("plot.html")
