"""
ridgeline-basic: Ridgeline Plot
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import Range1d
from bokeh.plotting import figure
from scipy import stats


# Data - Monthly temperature readings
np.random.seed(42)

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# Generate realistic temperature distributions for each month (Northern Hemisphere)
base_temps = [2, 4, 8, 12, 17, 21, 24, 23, 19, 13, 7, 3]
data = {}
for i, month in enumerate(months):
    temps = np.random.normal(base_temps[i], 3, 200)
    data[month] = temps

# Colors for gradient effect (from cool to warm and back)
colors = [
    "#306998",
    "#3B7AAF",
    "#4A8BC5",
    "#59A5DC",
    "#FFD43B",
    "#F97316",
    "#DC2626",
    "#F97316",
    "#FFD43B",
    "#59A5DC",
    "#4A8BC5",
    "#306998",
]

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="Monthly Temperature Distributions",
    x_axis_label="Temperature (°C)",
    y_axis_label="",
    tools="",
    toolbar_location=None,
)

# Calculate KDE for each category and plot as overlapping ridges
n_categories = len(months)
overlap = 0.7  # Overlap factor for ridgeline effect
x_range = np.linspace(-10, 35, 500)

# Plot from bottom to top (reversed order for proper layering)
for idx, month in enumerate(reversed(months)):
    values = data[month]
    kde = stats.gaussian_kde(values)
    density = kde(x_range)

    # Normalize density and scale for visual effect
    density_scaled = density / density.max() * 0.8

    # Calculate vertical offset for this category
    y_offset = idx * overlap

    # Create patch coordinates (filled area)
    xs = np.concatenate([[x_range[0]], x_range, [x_range[-1]]])
    ys = np.concatenate([[y_offset], density_scaled + y_offset, [y_offset]])

    # Draw filled patch
    color_idx = n_categories - 1 - idx
    p.patch(xs, ys, fill_color=colors[color_idx], fill_alpha=0.7, line_color="white", line_width=1.5)

# Configure y-axis to show month labels
y_positions = [i * overlap for i in range(n_categories)]
y_labels = list(reversed(months))

p.yaxis.ticker = y_positions
p.yaxis.major_label_overrides = dict(zip(y_positions, y_labels, strict=False))

# Styling
p.y_range = Range1d(-0.3, (n_categories - 1) * overlap + 1.2)
p.x_range = Range1d(-10, 35)

p.title.text_font_size = "32pt"
p.xaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "22pt"
p.yaxis.major_label_text_font_size = "22pt"

p.xgrid.grid_line_color = "#E0E0E0"
p.xgrid.grid_line_alpha = 0.5
p.ygrid.grid_line_color = None

p.outline_line_color = None
p.background_fill_color = "#FAFAFA"

# Save outputs
export_png(p, filename="plot.png")

output_file("plot.html")
save(p)
