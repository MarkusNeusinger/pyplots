""" pyplots.ai
scatter-complex-plane: Complex Plane Visualization (Argand Diagram)
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 84/100 | Created: 2026-03-04
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    arrow,
    coord_fixed,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_path,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
    theme_void,
)


# Data — complex numbers: 5th roots of unity + arbitrary points
n_roots = 5
angles_roots = np.array([2 * np.pi * k / n_roots for k in range(n_roots)])
roots_real = np.cos(angles_roots)
roots_imag = np.sin(angles_roots)
roots_labels = [f"ω{k}" for k in range(n_roots)]

arbitrary_real = np.array([1.5, -1.3, 0.4, -0.8, 1.6])
arbitrary_imag = np.array([0.7, -0.5, 1.8, -1.5, -1.4])
arbitrary_labels = ["z₁", "z₂", "z₃", "z₄", "z₅"]

real = np.concatenate([roots_real, arbitrary_real])
imag = np.concatenate([roots_imag, arbitrary_imag])
labels = roots_labels + arbitrary_labels
category = ["5th Root of Unity"] * n_roots + ["Arbitrary Point"] * len(arbitrary_real)

# Compute magnitude for size encoding (storytelling: inside vs outside unit circle)
magnitude = np.sqrt(real**2 + imag**2)
size_cat = ["On ∣z∣=1" if abs(m - 1.0) < 0.01 else ("∣z∣ > 1" if m > 1 else "∣z∣ < 1") for m in magnitude]

df_points = pd.DataFrame(
    {"real": real, "imag": imag, "label": labels, "category": category, "magnitude": magnitude, "size_cat": size_cat}
)

# Annotation labels: name + rectangular form (a+bi) + polar magnitude
annotations = []
for r, i, lbl in zip(real, imag, labels, strict=True):
    sign = "+" if i >= 0 else "−"
    annotations.append(f"{lbl} = {r:.2f}{sign}{abs(i):.2f}i")
df_points["annotation"] = annotations

# Vectors from origin to each point
df_vectors = pd.DataFrame(
    {"x": [0.0] * len(real), "y": [0.0] * len(real), "xend": real, "yend": imag, "category": category}
)

# Unit circle
theta = np.linspace(0, 2 * np.pi, 300)
df_circle = pd.DataFrame({"x": np.cos(theta), "y": np.sin(theta)})

# Smart label positioning — use angle from origin to push labels outward
angles = np.arctan2(imag, real)
label_radius = 0.28
x_offsets = label_radius * np.cos(angles)
y_offsets = label_radius * np.sin(angles)
# Horizontal alignment based on position
ha_values = ["left" if np.cos(a) >= 0 else "right" for a in angles]
# Vertical nudge: push labels up if in upper half, down if in lower half
va_values = ["bottom" if np.sin(a) >= 0 else "top" for a in angles]

df_labels = pd.DataFrame(
    {"x": real + x_offsets, "y": imag + y_offsets, "annotation": annotations, "ha": ha_values, "va": va_values}
)

# Refined palette — deeper blue and warm amber for contrast
color_roots = "#1B4F72"
color_arb = "#D35400"
colors = [color_roots, color_arb]

# Plot — layered grammar of graphics with visual hierarchy
plot = (
    ggplot()
    # Subtle unit circle fill to create focal region
    + annotate("rect", xmin=-2.5, xmax=2.5, ymin=-2.3, ymax=2.3, fill="#F8F9FA", color="none")
    # Axes through origin — styled as thin reference lines
    + annotate("segment", x=-2.5, xend=2.5, y=0, yend=0, color="#B0B0B0", size=0.4, linetype="solid")
    + annotate("segment", x=0, xend=0, y=-2.3, yend=2.3, color="#B0B0B0", size=0.4, linetype="solid")
    # Axis arrows/labels at ends
    + annotate("text", x=2.4, y=-0.15, label="Re(z)", size=11, color="#555555", fontstyle="italic")
    + annotate("text", x=0.18, y=2.2, label="Im(z)", size=11, color="#555555", fontstyle="italic")
    # Unit circle — prominent dashed reference
    + geom_path(df_circle, aes(x="x", y="y"), color="#7F8C8D", linetype="dashed", size=0.9, alpha=0.7)
    # Radial guide at |z|=1 label
    + annotate("text", x=0.72, y=0.72, label="∣z∣ = 1", size=9, color="#7F8C8D", fontstyle="italic", angle=45)
    # Vectors from origin — different alpha per category for depth
    + geom_segment(
        df_vectors,
        aes(x="x", y="y", xend="xend", yend="yend", color="category"),
        size=0.9,
        alpha=0.55,
        arrow=arrow(length=0.10, type="closed"),
    )
    # Points — sized by category for visual hierarchy (roots smaller, on circle)
    + geom_point(df_points, aes(x="real", y="imag", color="category"), size=5.5, alpha=0.95)
    # Highlight unit circle points with a subtle outer ring
    + geom_point(
        df_points[df_points["size_cat"] == "On ∣z∣=1"],
        aes(x="real", y="imag"),
        size=9,
        color=color_roots,
        alpha=0.15,
        shape="o",
    )
    # Annotations — split by horizontal alignment for readability
    + geom_text(
        df_labels[df_labels["ha"] == "left"],
        aes(x="x", y="y", label="annotation"),
        size=8,
        color="#2C3E50",
        ha="left",
        fontweight="bold",
    )
    + geom_text(
        df_labels[df_labels["ha"] == "right"],
        aes(x="x", y="y", label="annotation"),
        size=8,
        color="#2C3E50",
        ha="right",
        fontweight="bold",
    )
    # Labels and title
    + labs(x="Re(z)", y="Im(z)", title="scatter-complex-plane · plotnine · pyplots.ai", color="Category")
    # Axis scales with refined breaks
    + scale_x_continuous(limits=(-2.5, 2.5), breaks=[-2, -1, 0, 1, 2])
    + scale_y_continuous(limits=(-2.3, 2.3), breaks=[-2, -1, 0, 1, 2])
    + coord_fixed(ratio=1)
    # Color scale
    + scale_color_manual(values=colors, labels=["5th Root of Unity (∣z∣ = 1)", "Arbitrary Point"])
    # Theme — built from theme_void for maximum control
    + theme_void()
    + theme(
        figure_size=(16, 9),
        text=element_text(family="sans-serif", size=14, color="#2C3E50"),
        plot_title=element_text(size=22, weight="bold", color="#1A1A2E", margin={"b": 15}),
        axis_title_x=element_text(size=18, color="#34495E", margin={"t": 10}),
        axis_title_y=element_text(size=18, color="#34495E", margin={"r": 10}),
        axis_text=element_text(size=14, color="#7F8C8D"),
        axis_ticks=element_line(color="#CCCCCC", size=0.3),
        axis_ticks_length=4,
        legend_text=element_text(size=14, color="#2C3E50"),
        legend_title=element_text(size=16, weight="bold", color="#1A1A2E"),
        legend_position="bottom",
        legend_background=element_rect(fill="#FFFFFF", color="#E0E0E0", size=0.5),
        legend_key=element_rect(fill="none", color="none"),
        legend_margin=10,
        panel_background=element_rect(fill="#FAFBFC", color="none"),
        plot_background=element_rect(fill="#FFFFFF", color="none"),
        panel_grid_major=element_line(color="#E8E8E8", size=0.25),
        panel_grid_minor=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
