""" pyplots.ai
bullet-basic: Basic Bullet Chart
Library: plotnine 0.15.1 | Python 3.13.11
Quality: 93/100 | Created: 2025-12-16
"""

import pandas as pd
from plotnine import (
    aes,
    coord_flip,
    element_blank,
    element_text,
    geom_rect,
    geom_segment,
    ggplot,
    labs,
    scale_fill_manual,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - Multiple KPIs with different performance levels
metrics = [
    {"label": "Revenue", "actual": 275, "target": 250, "ranges": [150, 225, 300]},
    {"label": "Profit", "actual": 22, "target": 26, "ranges": [15, 22.5, 30]},
    {"label": "Orders", "actual": 1050, "target": 1100, "ranges": [600, 900, 1200]},
    {"label": "Satisfaction", "actual": 4.5, "target": 4.2, "ranges": [2.5, 3.5, 5.0]},
]

# Build data for the plot - normalize all values to 0-100 scale for consistent display
range_data = []
actual_data = []
target_data = []
label_data = []

for i, m in enumerate(metrics):
    y_pos = i
    max_val = m["ranges"][-1]

    # Qualitative ranges (poor, satisfactory, good)
    range_data.append({"y": y_pos, "xmin": 0, "xmax": (m["ranges"][0] / max_val) * 100, "band": "Poor"})
    range_data.append(
        {
            "y": y_pos,
            "xmin": (m["ranges"][0] / max_val) * 100,
            "xmax": (m["ranges"][1] / max_val) * 100,
            "band": "Satisfactory",
        }
    )
    range_data.append({"y": y_pos, "xmin": (m["ranges"][1] / max_val) * 100, "xmax": 100, "band": "Good"})

    # Actual value bar
    actual_pct = (m["actual"] / max_val) * 100
    actual_data.append({"y": y_pos, "xmin": 0, "xmax": actual_pct})

    # Target marker
    target_pct = (m["target"] / max_val) * 100
    target_data.append({"y": y_pos, "target": target_pct})

    # Labels with actual values
    label_data.append({"y": y_pos, "label": m["label"], "actual": m["actual"]})

df_ranges = pd.DataFrame(range_data)
df_actual = pd.DataFrame(actual_data)
df_target = pd.DataFrame(target_data)
df_labels = pd.DataFrame(label_data)

# Grayscale colors for qualitative bands (poor=dark, satisfactory=medium, good=light)
band_colors = {"Poor": "#D0D0D0", "Satisfactory": "#A0A0A0", "Good": "#707070"}

# Bar height parameters
range_height = 0.7
actual_height = 0.3

# Plot
plot = (
    ggplot()
    # Background qualitative ranges
    + geom_rect(
        df_ranges, aes(xmin="xmin", xmax="xmax", ymin="y - range_height/2", ymax="y + range_height/2", fill="band")
    )
    + scale_fill_manual(values=band_colors, limits=["Good", "Satisfactory", "Poor"], guide=None)
    # Actual value bar (Python Blue)
    + geom_rect(
        df_actual, aes(xmin="xmin", xmax="xmax", ymin="y - actual_height/2", ymax="y + actual_height/2"), fill="#306998"
    )
    # Target marker (thin black line)
    + geom_segment(
        df_target,
        aes(x="target", xend="target", y="y - range_height/2.5", yend="y + range_height/2.5"),
        color="black",
        size=2.5,
    )
    # Flip coordinates for horizontal bullet charts
    + coord_flip()
    # Scale and labels
    + scale_y_continuous(breaks=list(range(len(metrics))), labels=[m["label"] for m in metrics], expand=(0.1, 0.1))
    + labs(title="bullet-basic · plotnine · pyplots.ai", x="", y="Performance (%)")
    # Theme
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, ha="center"),
        axis_title_x=element_text(size=20),
        axis_title_y=element_blank(),
        axis_text_x=element_text(size=16),
        axis_text_y=element_text(size=18),
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        legend_position="none",
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
