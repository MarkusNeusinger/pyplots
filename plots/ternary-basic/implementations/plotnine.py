"""
ternary-basic: Basic Ternary Plot
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_text,
    geom_point,
    geom_polygon,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    theme,
    theme_void,
)


# Data - Soil composition samples (sand, silt, clay)
np.random.seed(42)
n_points = 50

# Generate random ternary data that sums to 100
raw = np.random.dirichlet(alpha=[2, 2, 2], size=n_points) * 100
sand = raw[:, 0]
silt = raw[:, 1]
clay = raw[:, 2]


# Convert ternary coordinates to Cartesian
def ternary_to_cartesian(a, b, c):
    """Convert ternary (a, b, c) to Cartesian (x, y)."""
    total = a + b + c
    x = 0.5 * (2 * b + c) / total
    y = (np.sqrt(3) / 2) * c / total
    return x, y


# Convert data points
x_data, y_data = ternary_to_cartesian(sand, silt, clay)
df = pd.DataFrame({"x": x_data, "y": y_data, "sand": sand, "silt": silt, "clay": clay})

# Triangle vertices (for the frame)
# A (sand) at bottom-left, B (silt) at bottom-right, C (clay) at top
vertices = pd.DataFrame(
    {"x": [0, 1, 0.5, 0], "y": [0, 0, np.sqrt(3) / 2, 0]}  # Close the triangle
)

# Grid lines at 20% intervals
grid_lines = []
for pct in [0.2, 0.4, 0.6, 0.8]:
    # Lines parallel to each side
    # Parallel to bottom (constant clay)
    x1, y1 = ternary_to_cartesian(1 - pct, 0, pct)
    x2, y2 = ternary_to_cartesian(0, 1 - pct, pct)
    grid_lines.append({"x": x1, "y": y1, "xend": x2, "yend": y2})

    # Parallel to left side (constant silt)
    x1, y1 = ternary_to_cartesian(0, pct, 1 - pct)
    x2, y2 = ternary_to_cartesian(1 - pct, pct, 0)
    grid_lines.append({"x": x1, "y": y1, "xend": x2, "yend": y2})

    # Parallel to right side (constant sand)
    x1, y1 = ternary_to_cartesian(pct, 0, 1 - pct)
    x2, y2 = ternary_to_cartesian(pct, 1 - pct, 0)
    grid_lines.append({"x": x1, "y": y1, "xend": x2, "yend": y2})

grid_df = pd.DataFrame(grid_lines)

# Tick labels along edges
tick_labels = []
label_offset = 0.08
for pct in [0, 20, 40, 60, 80, 100]:
    frac = pct / 100
    # Sand axis (bottom-left edge going up-left)
    x, y = ternary_to_cartesian(1 - frac, 0, frac)
    tick_labels.append({"x": x - label_offset, "y": y, "label": str(pct)})

    # Silt axis (bottom edge)
    x, y = ternary_to_cartesian(1 - frac, frac, 0)
    tick_labels.append({"x": x, "y": y - label_offset * 0.7, "label": str(pct)})

    # Clay axis (right edge going up)
    x, y = ternary_to_cartesian(0, 1 - frac, frac)
    tick_labels.append({"x": x + label_offset, "y": y, "label": str(pct)})

tick_df = pd.DataFrame(tick_labels)

# Vertex labels
vertex_labels = pd.DataFrame(
    {
        "x": [0 - 0.05, 1 + 0.05, 0.5],
        "y": [0 - 0.08, 0 - 0.08, np.sqrt(3) / 2 + 0.08],
        "label": ["Sand (%)", "Silt (%)", "Clay (%)"],
    }
)

# Build the plot
plot = (
    ggplot()
    # Triangle frame
    + geom_polygon(data=vertices, mapping=aes(x="x", y="y"), fill="white", color="#306998", size=1.5)
    # Grid lines
    + geom_segment(
        data=grid_df, mapping=aes(x="x", y="y", xend="xend", yend="yend"), color="#cccccc", size=0.5, alpha=0.7
    )
    # Data points
    + geom_point(data=df, mapping=aes(x="x", y="y"), color="#306998", size=4, alpha=0.7)
    # Tick labels
    + geom_text(data=tick_df, mapping=aes(x="x", y="y", label="label"), size=10, color="#666666")
    # Vertex labels
    + geom_text(
        data=vertex_labels, mapping=aes(x="x", y="y", label="label"), size=14, fontweight="bold", color="#306998"
    )
    # Title and theme
    + labs(title="Soil Composition · ternary-basic · plotnine · pyplots.ai")
    + coord_fixed(ratio=1)
    + theme_void()
    + theme(figure_size=(16, 9), plot_title=element_text(size=24, ha="center", weight="bold"), plot_margin=0.1)
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
