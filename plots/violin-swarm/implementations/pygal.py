"""pyplots.ai
violin-swarm: Violin Plot with Overlaid Swarm Points
Library: pygal 3.1.0 | Python 3.13.11
Quality: 75/100 | Created: 2026-01-09
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Reaction times (ms) across 4 experimental conditions
np.random.seed(42)
data = {
    "Control": np.random.gamma(3, 80, 50) + 200,
    "Low Dose": np.random.gamma(4, 60, 50) + 180,
    "Medium Dose": np.random.gamma(5, 50, 50) + 150,
    "High Dose": np.random.gamma(6, 40, 50) + 120,
}

# Violin fill colors (semi-transparent) and contrasting swarm point colors
violin_colors = ["#306998", "#4CAF50", "#FF9800", "#9C27B0"]
swarm_colors = ["#FFD43B", "#E91E63", "#00BCD4", "#FF5722"]

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(violin_colors + swarm_colors),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=36,
    value_font_size=36,
    opacity=0.35,
    opacity_hover=0.5,
    tooltip_font_size=32,
)

# Create XY chart for violin plot with swarm overlay
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="violin-swarm · pygal · pyplots.ai",
    x_title="Experimental Condition",
    y_title="Reaction Time (ms)",
    show_legend=False,
    stroke=True,
    fill=True,
    dots_size=0,
    show_x_guides=False,
    show_y_guides=True,
    range=(50, 650),
    xrange=(0, 5),
    margin=50,
)

# Parameters for violin and swarm
violin_width = 0.35
n_points = 100

# Add violins and swarm points for each category
for i, (category, values) in enumerate(data.items()):
    center_x = i + 1

    # Compute KDE using Silverman's rule
    n = len(values)
    std = np.std(values)
    iqr = np.percentile(values, 75) - np.percentile(values, 25)
    bandwidth = 0.9 * min(std, iqr / 1.34) * n ** (-0.2)

    # Create range of y values for density
    y_min, y_max = values.min(), values.max()
    y_range = np.linspace(y_min - 20, y_max + 20, n_points)

    # Gaussian kernel density estimation
    density = np.zeros_like(y_range)
    for v in values:
        density += np.exp(-0.5 * ((y_range - v) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Normalize density to desired width
    max_density = density.max()
    density_norm = density / max_density * violin_width

    # Create violin shape (mirrored density)
    left_points = [(center_x - d, y) for y, d in zip(y_range, density_norm, strict=True)]
    right_points = [(center_x + d, y) for y, d in zip(y_range[::-1], density_norm[::-1], strict=True)]
    violin_points = left_points + right_points + [left_points[0]]

    # Add violin shape with tooltip showing category info
    chart.add(
        None, [{"value": pt, "label": f"{category}: n={n}, mean={np.mean(values):.1f}ms"} for pt in violin_points]
    )

    # Compute swarm x-positions staying within violin bounds
    sorted_indices = np.argsort(values)
    x_swarm = np.zeros(n)
    for idx in sorted_indices:
        y_val = values[idx]
        local_density = np.interp(y_val, y_range, density) / max_density * violin_width * 0.85
        x_swarm[idx] = center_x + np.random.uniform(-local_density, local_density)

    # Add swarm points with contrasting color and interactive tooltips
    swarm_points = [
        {"value": (float(x), float(y)), "label": f"{category}: {y:.1f}ms"} for x, y in zip(x_swarm, values, strict=True)
    ]
    chart.add(
        None, swarm_points, stroke=False, fill=False, dots_size=10, stroke_style={"width": 2, "color": swarm_colors[i]}
    )

# X-axis labels at violin positions
chart.x_labels = ["", "Control", "Low Dose", "Medium Dose", "High Dose", ""]
chart.x_labels_major_count = 4

# Save outputs (PNG first as primary output)
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
