""" pyplots.ai
voronoi-basic: Voronoi Diagram for Spatial Partitioning
Library: altair 6.0.0 | Python 3.13.11
Quality: 87/100 | Created: 2026-01-09
"""

import altair as alt
import numpy as np
import pandas as pd
from scipy.spatial import Voronoi


# Data - Generate seed points for weather stations
np.random.seed(42)
n_points = 15
x_points = np.random.uniform(5, 95, n_points)
y_points = np.random.uniform(5, 95, n_points)
labels = [f"Station {i + 1}" for i in range(n_points)]

points = np.column_stack([x_points, y_points])

# Add boundary points to help with clipping (mirror points outside bounds)
x_min, x_max = 0, 100
y_min, y_max = 0, 100
margin = 200

boundary_points = []
for px, py in points:
    boundary_points.append([2 * x_min - margin - px, py])
    boundary_points.append([2 * x_max + margin - px, py])
    boundary_points.append([px, 2 * y_min - margin - py])
    boundary_points.append([px, 2 * y_max + margin - py])

all_points = np.vstack([points, boundary_points])

# Compute Voronoi diagram
vor = Voronoi(all_points)

# Color palette - colorblind safe with variety
color_palette = [
    "#306998",
    "#FFD43B",
    "#4B8BBE",
    "#FFE873",
    "#6A9BC3",
    "#3776AB",
    "#FFC61E",
    "#5A8AB5",
    "#E6C430",
    "#2E5984",
    "#FFCC00",
    "#4A7A9E",
    "#D4AA00",
    "#1E3F5A",
    "#FFB800",
]

# Create edge data for Voronoi cell borders (color-coded by cell)
edge_data = []
for point_idx in range(n_points):
    region_idx = vor.point_region[point_idx]
    region = vor.regions[region_idx]

    if not region or -1 in region:
        continue

    vertices = vor.vertices[region]
    clipped_x = np.clip(vertices[:, 0], x_min, x_max)
    clipped_y = np.clip(vertices[:, 1], y_min, y_max)

    # Sort vertices by angle for proper polygon ordering
    center_x = np.mean(clipped_x)
    center_y = np.mean(clipped_y)
    angles = np.arctan2(clipped_y - center_y, clipped_x - center_x)
    sorted_indices = np.argsort(angles)

    sorted_x = clipped_x[sorted_indices]
    sorted_y = clipped_y[sorted_indices]

    color = color_palette[point_idx % len(color_palette)]
    for i in range(len(sorted_x)):
        next_i = (i + 1) % len(sorted_x)
        edge_data.append(
            {
                "x1": sorted_x[i],
                "y1": sorted_y[i],
                "x2": sorted_x[next_i],
                "y2": sorted_y[next_i],
                "cell_id": point_idx,
                "color": color,
                "label": labels[point_idx],
            }
        )

df_edges = pd.DataFrame(edge_data)

# Create DataFrame for seed points
df_points = pd.DataFrame(
    {
        "x": x_points,
        "y": y_points,
        "label": labels,
        "color": [color_palette[i % len(color_palette)] for i in range(n_points)],
    }
)

# Create Voronoi edge borders layer with colored edges
voronoi_edges = (
    alt.Chart(df_edges)
    .mark_rule(strokeWidth=4, opacity=0.9)
    .encode(
        x=alt.X("x1:Q", scale=alt.Scale(domain=[x_min - 2, x_max + 2])),
        y=alt.Y("y1:Q", scale=alt.Scale(domain=[y_min - 2, y_max + 2])),
        x2="x2:Q",
        y2="y2:Q",
        color=alt.Color("color:N", scale=None, legend=None),
    )
)

# Create seed points layer
points_layer = (
    alt.Chart(df_points)
    .mark_circle(size=500, stroke="#FFFFFF", strokeWidth=3)
    .encode(
        x=alt.X("x:Q", title="X Coordinate"),
        y=alt.Y("y:Q", title="Y Coordinate"),
        color=alt.Color("color:N", scale=None, legend=None),
        tooltip=["label:N", alt.Tooltip("x:Q", format=".1f"), alt.Tooltip("y:Q", format=".1f")],
    )
)

# Add station labels
labels_layer = (
    alt.Chart(df_points)
    .mark_text(dy=-24, fontSize=16, fontWeight="bold", color="#1a1a1a")
    .encode(x="x:Q", y="y:Q", text="label:N")
)

# Combine layers
chart = (
    (voronoi_edges + points_layer + labels_layer)
    .properties(
        width=1600, height=900, title=alt.Title("voronoi-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, grid=True, gridOpacity=0.25, gridColor="#AAAAAA")
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
