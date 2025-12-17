"""
ternary-basic: Basic Ternary Plot
Library: letsplot
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_point,
    geom_polygon,
    geom_segment,
    geom_text,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_color_manual,
    theme,
)


LetsPlot.setup_html()


# Helper function to convert ternary to Cartesian coordinates
def ternary_to_cartesian(a, b, c):
    """Convert ternary coordinates (a, b, c) to Cartesian (x, y)."""
    total = a + b + c
    b_norm = b / total
    c_norm = c / total
    # Cartesian x: shifts right with more b, shifts to center with more c
    x = 0.5 * (2 * b_norm + c_norm)
    # Cartesian y: increases with more c (toward apex)
    y = (np.sqrt(3) / 2) * c_norm
    return x, y


# Data: Soil composition samples (Sand, Silt, Clay)
np.random.seed(42)

# Generate realistic soil composition data in different regions
samples = []
soil_types = []

# Sandy soils (high sand)
for _ in range(20):
    sand = np.random.uniform(60, 90)
    remaining = 100 - sand
    silt = np.random.uniform(0, remaining)
    clay = remaining - silt
    samples.append((sand, silt, clay))
    soil_types.append("Sandy")

# Silty soils (high silt)
for _ in range(20):
    silt = np.random.uniform(50, 80)
    remaining = 100 - silt
    sand = np.random.uniform(0, remaining)
    clay = remaining - sand
    samples.append((sand, silt, clay))
    soil_types.append("Silty")

# Clay soils (high clay)
for _ in range(20):
    clay = np.random.uniform(40, 70)
    remaining = 100 - clay
    sand = np.random.uniform(0, remaining)
    silt = remaining - sand
    samples.append((sand, silt, clay))
    soil_types.append("Clayey")

# Convert to Cartesian coordinates
x_coords = []
y_coords = []
for sand, silt, clay in samples:
    x, y = ternary_to_cartesian(sand, silt, clay)
    x_coords.append(x)
    y_coords.append(y)

df = pd.DataFrame({"x": x_coords, "y": y_coords, "soil_type": soil_types})

# Triangle vertices (Sand at bottom-left, Silt at bottom-right, Clay at top)
vertices = pd.DataFrame({"x": [0, 1, 0.5, 0], "y": [0, 0, np.sqrt(3) / 2, 0]})

# Grid lines at 20% intervals
grid_segments = []
for pct in [0.2, 0.4, 0.6, 0.8]:
    # Lines parallel to Sand-Silt edge (constant Clay)
    x1, y1 = ternary_to_cartesian(100 - pct * 100, 0, pct * 100)
    x2, y2 = ternary_to_cartesian(0, 100 - pct * 100, pct * 100)
    grid_segments.append({"x": x1, "y": y1, "xend": x2, "yend": y2})

    # Lines parallel to Sand-Clay edge (constant Silt)
    x1, y1 = ternary_to_cartesian(100 - pct * 100, pct * 100, 0)
    x2, y2 = ternary_to_cartesian(0, pct * 100, 100 - pct * 100)
    grid_segments.append({"x": x1, "y": y1, "xend": x2, "yend": y2})

    # Lines parallel to Silt-Clay edge (constant Sand)
    x1, y1 = ternary_to_cartesian(pct * 100, 100 - pct * 100, 0)
    x2, y2 = ternary_to_cartesian(pct * 100, 0, 100 - pct * 100)
    grid_segments.append({"x": x1, "y": y1, "xend": x2, "yend": y2})

grid_df = pd.DataFrame(grid_segments)

# Vertex labels
label_offset = 0.08
labels_df = pd.DataFrame(
    {
        "x": [0 - label_offset, 1 + label_offset, 0.5],
        "y": [-label_offset, -label_offset, np.sqrt(3) / 2 + label_offset],
        "label": ["Sand", "Silt", "Clay"],
    }
)

# Tick labels along edges (at 20%, 40%, 60%, 80%)
tick_labels = []
for pct in [20, 40, 60, 80]:
    # Sand axis (bottom-left to top): along left edge
    x, y = ternary_to_cartesian(100 - pct, 0, pct)
    tick_labels.append({"x": x - 0.05, "y": y, "label": str(pct)})

    # Silt axis (bottom-right to top): along right edge
    x, y = ternary_to_cartesian(0, 100 - pct, pct)
    tick_labels.append({"x": x + 0.05, "y": y, "label": str(pct)})

    # Clay axis (bottom): along bottom edge
    x, y = ternary_to_cartesian(100 - pct, pct, 0)
    tick_labels.append({"x": x, "y": y - 0.05, "label": str(pct)})

tick_df = pd.DataFrame(tick_labels)

# Plot
plot = (
    ggplot()
    # Triangle outline
    + geom_polygon(data=vertices, mapping=aes(x="x", y="y"), fill="white", color="#333333", size=1.5, alpha=1)
    # Grid lines
    + geom_segment(
        data=grid_df, mapping=aes(x="x", y="y", xend="xend", yend="yend"), color="#CCCCCC", size=0.8, alpha=0.6
    )
    # Data points
    + geom_point(data=df, mapping=aes(x="x", y="y", color="soil_type"), size=6, alpha=0.8)
    # Vertex labels
    + geom_text(data=labels_df, mapping=aes(x="x", y="y", label="label"), size=20, fontface="bold", color="#333333")
    # Tick labels
    + geom_text(data=tick_df, mapping=aes(x="x", y="y", label="label"), size=12, color="#666666")
    # Color scale
    + scale_color_manual(values=["#306998", "#FFD43B", "#DC2626"])
    # Labels and title
    + labs(title="Soil Composition · ternary-basic · letsplot · pyplots.ai", color="Soil Type")
    # Theme - remove axes since ternary uses its own coordinate system
    + theme(
        plot_title=element_text(size=24, face="bold"),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid=element_blank(),
        legend_position="right",
    )
    + ggsize(1600, 900)
)

# Save as PNG (scale 3x to get 4800 x 2700 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save as HTML for interactive version
ggsave(plot, "plot.html", path=".")
