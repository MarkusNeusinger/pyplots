"""
bubble-packed: Basic Packed Bubble Chart
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Department budget allocation
np.random.seed(42)
data = {
    "label": [
        "Engineering",
        "Marketing",
        "Sales",
        "Operations",
        "HR",
        "Finance",
        "R&D",
        "Support",
        "Legal",
        "IT",
        "Design",
        "Product",
        "Data Science",
        "Security",
        "QA",
    ],
    "value": [850, 420, 680, 320, 180, 290, 750, 210, 150, 380, 240, 550, 460, 170, 195],
}

labels = data["label"]
values = data["value"]
n = len(labels)

# Scale values to radius (using sqrt for area-proportional sizing)
min_radius = 30
max_radius = 120
values_array = np.array(values)
radii = min_radius + (max_radius - min_radius) * np.sqrt(
    (values_array - values_array.min()) / (values_array.max() - values_array.min())
)

# Sort by size (largest first) for better packing
order = np.argsort(-radii)
radii = radii[order]
labels = [labels[i] for i in order]
values = [values[i] for i in order]

# Circle packing - place circles one by one, finding best position
x_pos = np.zeros(n)
y_pos = np.zeros(n)

# Place first circle at center
x_pos[0] = 0
y_pos[0] = 0

# Place remaining circles
for i in range(1, n):
    best_x, best_y = 0, 0
    best_dist = float("inf")

    # Try positions around existing circles
    for j in range(i):
        for angle in np.linspace(0, 2 * np.pi, 36, endpoint=False):
            # Position touching circle j
            test_x = x_pos[j] + (radii[j] + radii[i] + 2) * np.cos(angle)
            test_y = y_pos[j] + (radii[j] + radii[i] + 2) * np.sin(angle)

            # Check for overlaps with all placed circles
            valid = True
            for k in range(i):
                dx = test_x - x_pos[k]
                dy = test_y - y_pos[k]
                dist = np.sqrt(dx**2 + dy**2)
                if dist < radii[i] + radii[k] + 1:
                    valid = False
                    break

            if valid:
                # Prefer positions closer to center
                center_dist = np.sqrt(test_x**2 + test_y**2)
                if center_dist < best_dist:
                    best_dist = center_dist
                    best_x, best_y = test_x, test_y

    x_pos[i] = best_x
    y_pos[i] = best_y

# Fine-tune with physics simulation
for _ in range(200):
    for i in range(n):
        fx, fy = 0, 0
        # Gentle centering force
        fx -= x_pos[i] * 0.01
        fy -= y_pos[i] * 0.01
        # Repulsion from overlapping circles
        for j in range(n):
            if i != j:
                dx = x_pos[i] - x_pos[j]
                dy = y_pos[i] - y_pos[j]
                dist = np.sqrt(dx**2 + dy**2) + 0.1
                min_dist = radii[i] + radii[j] + 2
                if dist < min_dist:
                    force = (min_dist - dist) * 0.5
                    fx += (dx / dist) * force
                    fy += (dy / dist) * force
        x_pos[i] += fx
        y_pos[i] += fy

# Color palette - assign based on value quartiles
# Larger values get Python Blue, mid get Yellow, smaller get accent colors
colors_base = [
    "#306998",  # Python Blue
    "#FFD43B",  # Python Yellow
    "#306998",
    "#4A90A4",
    "#4A90A4",
    "#4A90A4",
    "#FFD43B",
    "#4A90A4",
    "#7B9E89",
    "#306998",
    "#FFD43B",
    "#306998",
    "#FFD43B",
    "#7B9E89",
    "#7B9E89",
]
# Reorder colors to match sorted data
colors = [colors_base[i] for i in order]

# Create DataFrame with computed positions
df = pd.DataFrame(
    {
        "label": labels,
        "value": values,
        "x": x_pos,
        "y": y_pos,
        "radius": radii,
        "color": colors[:n],
        "formatted_value": [f"${v}K" for v in values],
    }
)

# Create circles using mark_circle with computed positions
circles = (
    alt.Chart(df)
    .mark_circle(opacity=0.85, stroke="white", strokeWidth=2)
    .encode(
        x=alt.X("x:Q", axis=None),
        y=alt.Y("y:Q", axis=None),
        size=alt.Size("radius:Q", scale=alt.Scale(range=[min_radius**2 * 3, max_radius**2 * 3]), legend=None),
        color=alt.Color("color:N", scale=None, legend=None),
        tooltip=[alt.Tooltip("label:N", title="Department"), alt.Tooltip("formatted_value:N", title="Budget")],
    )
)

# Create labels for larger bubbles
# Filter to only show labels for circles large enough
df_large = df[df["radius"] > 60].copy()
df_large["display_text"] = df_large["label"] + "\n" + df_large["formatted_value"]

labels_layer = (
    alt.Chart(df_large)
    .mark_text(color="white", fontWeight="bold", fontSize=14, lineBreak="\n")
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), text="display_text:N")
)

# Combine layers
chart = (
    alt.layer(circles, labels_layer)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            "Department Budget Allocation · bubble-packed · altair · pyplots.ai",
            fontSize=28,
            fontWeight="bold",
            anchor="middle",
        ),
    )
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
