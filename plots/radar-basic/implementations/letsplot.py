""" pyplots.ai
radar-basic: Basic Radar Chart
Library: letsplot 4.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-14
"""

import math

import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_line,
    geom_point,
    geom_polygon,
    geom_text,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_color_manual,
    scale_fill_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
)


LetsPlot.setup_html()

# Data - Employee performance metrics
categories = ["Technical", "Communication", "Leadership", "Creativity", "Teamwork", "Problem Solving"]
values_alice = [85, 70, 60, 90, 75, 80]
values_bob = [70, 85, 75, 65, 90, 70]

n = len(categories)

# Create angles for each category (evenly spaced around circle)
angles = [i * 2 * math.pi / n for i in range(n)]

# Build dataframe with x,y coordinates for polar plotting
# For radar chart, we need to close the polygon by repeating first point
data_rows = []
for i, (cat, val_a, val_b, angle) in enumerate(zip(categories, values_alice, values_bob, angles, strict=True)):
    data_rows.append({"category": cat, "value": val_a, "angle": angle, "series": "Alice", "order": i})
    data_rows.append({"category": cat, "value": val_b, "angle": angle, "series": "Bob", "order": i})

# Close the polygon by repeating first point
data_rows.append(
    {"category": categories[0], "value": values_alice[0], "angle": angles[0], "series": "Alice", "order": n}
)
data_rows.append({"category": categories[0], "value": values_bob[0], "angle": angles[0], "series": "Bob", "order": n})

df = pd.DataFrame(data_rows)

# Convert to cartesian coordinates for plotting
df["x"] = df["value"] * df["angle"].apply(lambda a: math.cos(a - math.pi / 2))
df["y"] = df["value"] * df["angle"].apply(lambda a: math.sin(a - math.pi / 2))

# Create gridlines data (circles at 20, 40, 60, 80, 100)
grid_rows = []
grid_angles = [i * 2 * math.pi / 100 for i in range(101)]
for radius in [20, 40, 60, 80, 100]:
    for angle in grid_angles:
        grid_rows.append(
            {"x": radius * math.cos(angle - math.pi / 2), "y": radius * math.sin(angle - math.pi / 2), "radius": radius}
        )

grid_df = pd.DataFrame(grid_rows)

# Create axis lines (spokes)
spoke_rows = []
for angle in angles:
    spoke_rows.append({"x": 0, "y": 0, "angle_group": angle})
    spoke_rows.append(
        {"x": 105 * math.cos(angle - math.pi / 2), "y": 105 * math.sin(angle - math.pi / 2), "angle_group": angle}
    )

spoke_df = pd.DataFrame(spoke_rows)

# Create axis labels data (positioned just outside the chart)
label_rows = []
for cat, angle in zip(categories, angles, strict=True):
    label_rows.append(
        {"label": cat, "x": 115 * math.cos(angle - math.pi / 2), "y": 115 * math.sin(angle - math.pi / 2)}
    )

label_df = pd.DataFrame(label_rows)

# Plot
plot = (
    ggplot()
    # Gridlines (circles)
    + geom_line(
        aes(x="x", y="y", group="radius"), data=grid_df, color="#CCCCCC", size=0.5, alpha=0.7, linetype="dashed"
    )
    # Spokes
    + geom_line(aes(x="x", y="y", group="angle_group"), data=spoke_df, color="#CCCCCC", size=0.5, alpha=0.7)
    # Filled polygons for each series
    + geom_polygon(aes(x="x", y="y", fill="series", group="series"), data=df, alpha=0.25)
    # Lines connecting points
    + geom_line(aes(x="x", y="y", color="series", group="series"), data=df, size=1.5)
    # Points at each vertex
    + geom_point(aes(x="x", y="y", color="series"), data=df[df["order"] < n], size=5)
    # Use Python Blue and Python Yellow colors
    + scale_fill_manual(values=["#306998", "#FFD43B"])
    + scale_color_manual(values=["#306998", "#FFD43B"])
    # Styling
    + scale_x_continuous(limits=(-140, 140))
    + scale_y_continuous(limits=(-140, 140))
    + labs(title="radar-basic · letsplot · pyplots.ai", fill="Employee", color="Employee")
    + ggsize(1600, 900)
    + theme(
        plot_title=element_text(size=24),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid=element_blank(),
    )
)

# Add category labels as text annotations
plot = plot + geom_text(aes(x="x", y="y", label="label"), data=label_df, size=14, color="#333333")

# Save (path='.' ensures files are saved in current directory, not lets-plot-images/)
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
