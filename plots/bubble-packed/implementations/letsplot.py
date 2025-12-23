""" pyplots.ai
bubble-packed: Basic Packed Bubble Chart
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    coord_fixed,
    element_text,
    geom_point,
    geom_text,
    ggplot,
    ggsize,
    labs,
    scale_color_manual,
    scale_size,
    theme,
    theme_void,
    xlim,
    ylim,
)
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()

# Data - department budget allocation
np.random.seed(42)
categories = [
    "Engineering",
    "Marketing",
    "Sales",
    "Operations",
    "HR",
    "Finance",
    "R&D",
    "Customer Support",
    "Legal",
    "IT",
    "Product",
    "Design",
    "Analytics",
    "QA",
    "Security",
]
values = np.array([85, 62, 58, 45, 32, 48, 72, 38, 22, 55, 68, 35, 42, 28, 30])
groups = [
    "Tech",
    "Business",
    "Business",
    "Operations",
    "Operations",
    "Operations",
    "Tech",
    "Operations",
    "Operations",
    "Tech",
    "Tech",
    "Tech",
    "Tech",
    "Tech",
    "Tech",
]

# Circle packing using force simulation (inline)
n = len(values)
radii = np.sqrt(values / np.pi) * 3.5  # Scale by area for accurate visual perception

# Initialize positions
np.random.seed(42)
x = np.random.uniform(-100, 100, n)
y = np.random.uniform(-100, 100, n)

# Force-directed packing simulation
for _ in range(600):
    # Pull toward center
    x *= 0.99
    y *= 0.99

    # Push overlapping circles apart
    for i in range(n):
        for j in range(i + 1, n):
            dx = x[j] - x[i]
            dy = y[j] - y[i]
            dist = np.sqrt(dx * dx + dy * dy)
            min_dist = radii[i] + radii[j] + 0.5

            if dist < min_dist and dist > 0:
                overlap = (min_dist - dist) / 2
                move_x = (dx / dist) * overlap
                move_y = (dy / dist) * overlap
                x[i] -= move_x
                y[i] -= move_y
                x[j] += move_x
                y[j] += move_y

df = pd.DataFrame({"label": categories, "value": values, "group": groups, "x": x, "y": y})

# Abbreviate long labels to fit inside bubbles
label_map = {
    "Customer Support": "Support",
    "Engineering": "Engineering",
    "Marketing": "Marketing",
    "Sales": "Sales",
    "Operations": "Ops",
    "Finance": "Finance",
    "R&D": "R&D",
    "HR": "HR",
    "Legal": "Legal",
    "IT": "IT",
    "Product": "Product",
    "Design": "Design",
    "Analytics": "Analytics",
    "QA": "QA",
    "Security": "Security",
}
df["short_label"] = df["label"].map(label_map)

# Plot
plot = (
    ggplot(df, aes(x="x", y="y"))
    + geom_point(aes(size="value", color="group"), alpha=0.85)
    + geom_text(aes(label="short_label"), size=7, color="white", fontface="bold")
    + scale_size(range=[20, 85], guide="none")
    + scale_color_manual(values=["#FFD43B", "#4ECDC4", "#306998"])
    + labs(title="Department Budget Allocation · bubble-packed · letsplot · pyplots.ai", color="Division")
    + xlim(-70, 70)
    + ylim(-70, 55)
    + theme_void()
    + theme(
        plot_title=element_text(size=24, hjust=0.5),
        legend_position="right",
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
    )
    + coord_fixed()
    + ggsize(1600, 900)
)

# Save PNG (scale 3x to get 4800x2700 px)
export_ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactive version
export_ggsave(plot, "plot.html", path=".")
