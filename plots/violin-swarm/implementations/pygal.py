"""pyplots.ai
violin-swarm: Violin Plot with Overlaid Swarm Points
Library: pygal | Python 3.13
Quality: pending | Created: 2025-01-09
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

# Custom style for 4800x2700 px canvas with semi-transparent violin fill
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#4CAF50", "#FF9800", "#9C27B0", "#FFD43B", "#E91E63", "#00BCD4", "#795548"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=36,
    value_font_size=36,
    opacity=0.35,
    opacity_hover=0.5,
)

# Create XY chart for violin plot with swarm overlay
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="violin-swarm · pygal · pyplots.ai",
    x_title="Experimental Condition",
    y_title="Reaction Time (ms)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    stroke=True,
    fill=True,
    dots_size=0,
    show_x_guides=False,
    show_y_guides=True,
    range=(50, 600),
    xrange=(0, 5),
    margin=50,
)

# Parameters for violin and swarm
violin_width = 0.35
n_points = 100


# Function to compute swarm positions (beeswarm-like jitter within violin bounds)
def compute_swarm_positions(values, center_x, density_func, max_density):
    """Compute x positions for swarm points, staying within violin bounds."""
    n = len(values)
    sorted_indices = np.argsort(values)
    x_positions = np.zeros(n)

    # For each point, compute its allowed width based on density at that y-value
    for idx in sorted_indices:
        y_val = values[idx]
        # Get the density at this y-value to determine max width
        local_density = density_func(y_val) / max_density * violin_width * 0.85
        # Spread points within this width using a simple dodge algorithm
        x_positions[idx] = center_x + np.random.uniform(-local_density, local_density)

    return x_positions


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

    # Add violin shape
    chart.add(category, violin_points)

    # Create interpolation function for density lookup
    def make_density_func(y_r, dens):
        def func(y_val):
            return np.interp(y_val, y_r, dens)

        return func

    density_func = make_density_func(y_range, density)

    # Compute swarm x-positions for each data point
    x_swarm = compute_swarm_positions(values, center_x, density_func, max_density)

    # Add swarm points as individual markers (using a darker shade)
    swarm_points = [(float(x), float(y)) for x, y in zip(x_swarm, values, strict=True)]
    chart.add(None, swarm_points, stroke=False, fill=False, dots_size=8, stroke_style={"width": 1})

# X-axis labels at violin positions
chart.x_labels = ["", "Control", "Low Dose", "Medium Dose", "High Dose", ""]
chart.x_labels_major_count = 4

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
