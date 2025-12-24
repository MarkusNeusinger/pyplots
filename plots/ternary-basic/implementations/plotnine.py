"""pyplots.ai
ternary-basic: Basic Ternary Plot
Library: plotnine | Python 3.13
Quality: pending | Created: 2025-12-24
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

# Convert ternary coordinates to Cartesian (inline calculation)
# Formula: x = 0.5 * (2*b + c) / total, y = (sqrt(3)/2) * c / total
total = sand + silt + clay
x_data = 0.5 * (2 * silt + clay) / total
y_data = (np.sqrt(3) / 2) * clay / total

df = pd.DataFrame({"x": x_data, "y": y_data, "sand": sand, "silt": silt, "clay": clay})

# Triangle vertices (for the frame)
# A (sand) at bottom-left, B (silt) at bottom-right, C (clay) at top
vertices = pd.DataFrame({"x": [0, 1, 0.5, 0], "y": [0, 0, np.sqrt(3) / 2, 0]})

# Grid lines at 20% intervals
grid_lines = []
for pct in [0.2, 0.4, 0.6, 0.8]:
    # Lines parallel to bottom (constant clay)
    x1 = 0.5 * (2 * 0 + pct)
    y1 = (np.sqrt(3) / 2) * pct
    x2 = 0.5 * (2 * (1 - pct) + pct)
    y2 = (np.sqrt(3) / 2) * pct
    grid_lines.append({"x": x1, "y": y1, "xend": x2, "yend": y2})

    # Lines parallel to left side (constant silt)
    x1 = 0.5 * (2 * pct + (1 - pct))
    y1 = (np.sqrt(3) / 2) * (1 - pct)
    x2 = 0.5 * (2 * pct + 0)
    y2 = 0
    grid_lines.append({"x": x1, "y": y1, "xend": x2, "yend": y2})

    # Lines parallel to right side (constant sand)
    x1 = 0.5 * (2 * 0 + (1 - pct))
    y1 = (np.sqrt(3) / 2) * (1 - pct)
    x2 = 0.5 * (2 * (1 - pct) + 0)
    y2 = 0
    grid_lines.append({"x": x1, "y": y1, "xend": x2, "yend": y2})

grid_df = pd.DataFrame(grid_lines)

# Tick labels along edges
tick_labels = []
label_offset = 0.08
for pct in [0, 20, 40, 60, 80, 100]:
    frac = pct / 100
    # Sand axis (left edge going up)
    x = 0.5 * (2 * 0 + frac)
    y = (np.sqrt(3) / 2) * frac
    tick_labels.append({"x": x - label_offset, "y": y, "label": str(pct)})

    # Silt axis (bottom edge)
    x = 0.5 * (2 * frac + 0)
    y = 0
    tick_labels.append({"x": x, "y": y - label_offset * 0.7, "label": str(pct)})

    # Clay axis (right edge going up)
    x = 0.5 * (2 * (1 - frac) + frac)
    y = (np.sqrt(3) / 2) * frac
    tick_labels.append({"x": x + label_offset, "y": y, "label": str(pct)})

tick_df = pd.DataFrame(tick_labels)

# Vertex labels
vertex_labels = pd.DataFrame(
    {
        "x": [0 - 0.02, 1 + 0.02, 0.5],
        "y": [0 - 0.12, 0 - 0.12, np.sqrt(3) / 2 + 0.1],
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
