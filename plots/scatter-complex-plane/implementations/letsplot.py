""" pyplots.ai
scatter-complex-plane: Complex Plane Visualization (Argand Diagram)
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 79/100 | Created: 2026-03-04
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave as export_ggsave


LetsPlot.setup_html()  # noqa: F405

# Data - Complex numbers: 5th roots of unity + arbitrary points
np.random.seed(42)

n_roots = 5
roots_angles = np.array([2 * np.pi * k / n_roots for k in range(n_roots)])
roots_real = np.cos(roots_angles)
roots_imag = np.sin(roots_angles)
roots_labels = [f"ω{k}" for k in range(n_roots)]

arbitrary_real = np.array([1.8, -1.2, 0.5, -0.7, 2.3, -1.9])
arbitrary_imag = np.array([1.3, -0.8, 1.9, -1.5, -0.4, 1.1])
arbitrary_labels = [f"z{i + 1}" for i in range(len(arbitrary_real))]

sum_real = np.array([roots_real[1] + roots_real[2]])
sum_imag = np.array([roots_imag[1] + roots_imag[2]])
sum_labels = ["ω1+ω2"]

all_real = np.concatenate([roots_real, arbitrary_real, sum_real])
all_imag = np.concatenate([roots_imag, arbitrary_real * 0 + arbitrary_imag, sum_imag])
all_labels = roots_labels + arbitrary_labels + sum_labels
all_category = ["5th Root of Unity"] * n_roots + ["Arbitrary"] * len(arbitrary_real) + ["Sum"]

df = pd.DataFrame({"real": all_real, "imaginary": all_imag, "label": all_labels, "category": all_category})

# Arrow data (vectors from origin to each point)
arrows_df = pd.DataFrame(
    {
        "x_start": np.zeros(len(all_real)),
        "y_start": np.zeros(len(all_real)),
        "x_end": all_real,
        "y_end": all_imag,
        "category": all_category,
    }
)

# Unit circle
theta = np.linspace(0, 2 * np.pi, 200)
circle_df = pd.DataFrame({"x": np.cos(theta), "y": np.sin(theta)})

# Annotation labels with rectangular form
annotation_labels = []
for r, i in zip(all_real, all_imag, strict=True):
    sign = "+" if i >= 0 else "−"
    annotation_labels.append(f"{r:.2f}{sign}{abs(i):.2f}i")

label_df = pd.DataFrame({"x": all_real, "y": all_imag, "text": annotation_labels})

# Nudge labels away from points
label_df["nudge_x"] = np.where(all_real >= 0, 0.15, -0.15)
label_df["nudge_y"] = 0.18

# Colors
colors = ["#306998", "#E3882D", "#AA3377"]

# Plot
plot = (
    ggplot()  # noqa: F405
    # Unit circle (dashed reference)
    + geom_path(  # noqa: F405
        data=circle_df,
        mapping=aes(x="x", y="y"),  # noqa: F405
        color="#BBBBBB",
        size=1.0,
        linetype="dashed",
    )
    # Axes through origin
    + geom_hline(yintercept=0, color="#999999", size=0.6)  # noqa: F405
    + geom_vline(xintercept=0, color="#999999", size=0.6)  # noqa: F405
    # Vectors from origin
    + geom_segment(  # noqa: F405
        data=arrows_df,
        mapping=aes(x="x_start", y="y_start", xend="x_end", yend="y_end", color="category"),  # noqa: F405
        size=1.0,
        alpha=0.7,
        arrow=arrow(length=10, type="open"),  # noqa: F405
    )
    # Points
    + geom_point(  # noqa: F405
        data=df,
        mapping=aes(x="real", y="imaginary", color="category"),  # noqa: F405
        size=6,
        alpha=0.9,
        shape=21,
        fill="#FFFFFF",
        stroke=2.0,
    )
    # Point labels (name)
    + geom_text(  # noqa: F405
        data=df,
        mapping=aes(x="real", y="imaginary", label="label", color="category"),  # noqa: F405
        size=12,
        fontface="bold",
        nudge_y=0.25,
    )
    # Coordinate annotations (a+bi form)
    + geom_text(  # noqa: F405
        data=label_df,
        mapping=aes(x="x", y="y", label="text"),  # noqa: F405
        size=9,
        color="#666666",
        nudge_y=-0.22,
    )
    # Scales
    + scale_color_manual(values=colors)  # noqa: F405
    + coord_fixed()  # noqa: F405
    + labs(  # noqa: F405
        x="Real", y="Imaginary", title="scatter-complex-plane · letsplot · pyplots.ai", color="Category"
    )
    + scale_x_continuous(  # noqa: F405
        breaks=[-2, -1, 0, 1, 2], expand=[0.1, 0.1]
    )
    + scale_y_continuous(  # noqa: F405
        breaks=[-2, -1, 0, 1, 2], expand=[0.1, 0.1]
    )
    + theme_minimal()  # noqa: F405
    + theme(  # noqa: F405
        plot_title=element_text(size=24, color="#222222", face="bold"),  # noqa: F405
        axis_title=element_text(size=20, color="#333333"),  # noqa: F405
        axis_text=element_text(size=16, color="#555555"),  # noqa: F405
        legend_title=element_text(size=18),  # noqa: F405
        legend_text=element_text(size=16),  # noqa: F405
        panel_grid_major=element_line(color="#E8E8E8", size=0.35),  # noqa: F405
        panel_grid_minor=element_blank(),  # noqa: F405
        plot_background=element_rect(fill="#FAFAFA", color="#FAFAFA"),  # noqa: F405
        panel_background=element_rect(fill="#FAFAFA", color="#FAFAFA"),  # noqa: F405
        plot_margin=[30, 40, 20, 20],
    )
    + ggsize(1600, 900)  # noqa: F405
)

# Save
export_ggsave(plot, filename="plot.png", path=".", scale=3)
export_ggsave(plot, filename="plot.html", path=".")
