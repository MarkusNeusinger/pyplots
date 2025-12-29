"""pyplots.ai
venn-basic: Venn Diagram
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-12-29
"""

import os

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data: Three research fields with overlapping expertise
set_a_label = "Machine Learning"
set_b_label = "Statistics"
set_c_label = "Data Engineering"

# Set sizes and intersections
only_a = 45  # Only ML
only_b = 35  # Only Statistics
only_c = 30  # Only Data Engineering
ab_only = 25  # ML & Statistics (not DE)
ac_only = 15  # ML & DE (not Stats)
bc_only = 20  # Stats & DE (not ML)
abc = 10  # All three

# Circle parameters (for 3-set Venn diagram)
r = 1.5  # radius
cx_a, cy_a = -0.7, 0.5  # Center of set A (top left)
cx_b, cy_b = 0.7, 0.5  # Center of set B (top right)
cx_c, cy_c = 0.0, -0.6  # Center of set C (bottom)

# Generate circle points
theta = np.linspace(0, 2 * np.pi, 100)

# Create circle data
circle_a_x = cx_a + r * np.cos(theta)
circle_a_y = cy_a + r * np.sin(theta)
circle_b_x = cx_b + r * np.cos(theta)
circle_b_y = cy_b + r * np.sin(theta)
circle_c_x = cx_c + r * np.cos(theta)
circle_c_y = cy_c + r * np.sin(theta)

# Create DataFrames for circles
df_a = pd.DataFrame({"x": circle_a_x, "y": circle_a_y, "set": set_a_label})
df_b = pd.DataFrame({"x": circle_b_x, "y": circle_b_y, "set": set_b_label})
df_c = pd.DataFrame({"x": circle_c_x, "y": circle_c_y, "set": set_c_label})
df_circles = pd.concat([df_a, df_b, df_c], ignore_index=True)

# Label positions and values
labels_data = pd.DataFrame(
    {
        "x": [
            cx_a - 0.5,  # Only A (left side of A)
            cx_b + 0.5,  # Only B (right side of B)
            cx_c,  # Only C (bottom of C)
            (cx_a + cx_b) / 2,  # A & B intersection
            (cx_a + cx_c) / 2 - 0.3,  # A & C intersection
            (cx_b + cx_c) / 2 + 0.3,  # B & C intersection
            0.0,  # Center (A & B & C)
        ],
        "y": [
            cy_a + 0.3,  # Only A
            cy_b + 0.3,  # Only B
            cy_c - 0.5,  # Only C
            cy_a + 0.6,  # A & B intersection
            (cy_a + cy_c) / 2 - 0.3,  # A & C intersection
            (cy_b + cy_c) / 2 - 0.3,  # B & C intersection
            0.0,  # Center (A & B & C)
        ],
        "label": [str(only_a), str(only_b), str(only_c), str(ab_only), str(ac_only), str(bc_only), str(abc)],
    }
)

# Set name labels (outside circles)
set_labels_data = pd.DataFrame(
    {
        "x": [cx_a - 0.8, cx_b + 0.8, cx_c],
        "y": [cy_a + 1.3, cy_b + 1.3, cy_c - 1.3],
        "label": [set_a_label, set_b_label, set_c_label],
    }
)

# Colors
colors = {"Machine Learning": "#306998", "Statistics": "#FFD43B", "Data Engineering": "#DC2626"}

# Create plot
plot = (
    ggplot()
    + geom_polygon(aes(x="x", y="y", fill="set"), data=df_circles, alpha=0.35, color="white", size=2)
    + geom_text(aes(x="x", y="y", label="label"), data=labels_data, size=18, fontface="bold", color="#1a1a1a")
    + geom_text(aes(x="x", y="y", label="label"), data=set_labels_data, size=14, fontface="bold", color="#333333")
    + scale_fill_manual(values=colors)
    + coord_fixed(ratio=1)
    + labs(title="venn-basic · lets-plot · pyplots.ai")
    + theme_void()
    + theme(
        plot_title=element_text(size=24, face="bold", hjust=0.5), legend_position="none", plot_margin=[60, 40, 40, 40]
    )
    + ggsize(1200, 1200)
)

# Save as PNG and HTML
ggsave(plot, "plot.png", scale=3)
ggsave(plot, "plot.html")

# Move files from lets-plot-images subdirectory to current directory
if os.path.exists("lets-plot-images/plot.png"):
    os.rename("lets-plot-images/plot.png", "plot.png")
if os.path.exists("lets-plot-images/plot.html"):
    os.rename("lets-plot-images/plot.html", "plot.html")
if os.path.exists("lets-plot-images") and not os.listdir("lets-plot-images"):
    os.rmdir("lets-plot-images")
