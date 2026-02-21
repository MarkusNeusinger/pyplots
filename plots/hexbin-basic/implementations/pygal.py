""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: pygal 3.1.0 | Python 3.14.3
Quality: /100 | Updated: 2026-02-21
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - air quality sensor network with three pollution hotspots
np.random.seed(42)

# Dense downtown core - tight, high concentration
core_x = np.random.randn(2500) * 0.6 + 2
core_y = np.random.randn(2500) * 0.6 + 3

# Industrial zone - medium density, broader spread
industrial_x = np.random.randn(1200) * 1.2 - 3
industrial_y = np.random.randn(1200) * 1.0 - 1.5

# Highway corridor - elongated, moderate density
highway_x = np.random.randn(600) * 0.4 + 5.5
highway_y = np.random.randn(600) * 2.0 + 1

# Sparse suburban background
bg_x = np.random.uniform(-6, 8, 200)
bg_y = np.random.uniform(-5, 7, 200)

sensor_x = np.concatenate([core_x, industrial_x, highway_x, bg_x])
sensor_y = np.concatenate([core_y, industrial_y, highway_y, bg_y])

# Compute hexagonal bins with numpy
gridsize = 18
x_min, x_max = sensor_x.min() - 0.5, sensor_x.max() + 0.5
y_min, y_max = sensor_y.min() - 0.5, sensor_y.max() + 0.5

hex_width = (x_max - x_min) / gridsize
hex_height = hex_width * 2 / np.sqrt(3)

row_indices = ((sensor_y - y_min) / hex_height).astype(int)
offsets_x = np.where(row_indices % 2 == 1, 0.5, 0.0)
col_adjusted = ((sensor_x - x_min) / hex_width - offsets_x).astype(int)

bin_keys = col_adjusted * 10000 + row_indices
unique_keys, counts = np.unique(bin_keys, return_counts=True)

center_cols = unique_keys // 10000
center_rows = unique_keys % 10000
center_x = x_min + (center_cols + np.where(center_rows % 2 == 1, 0.5, 0.0)) * hex_width + hex_width / 2
center_y = y_min + center_rows * hex_height + hex_height / 2

# Viridis palette for density levels
viridis_5 = ("#440154", "#31688e", "#21918c", "#5ec962", "#fde725")

custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#222222",
    foreground_subtle="#e0e0e0",
    colors=viridis_5,
    opacity=0.90,
    opacity_hover=1.0,
    title_font_size=48,
    label_font_size=36,
    major_label_font_size=30,
    legend_font_size=26,
    value_font_size=22,
    tooltip_font_size=22,
)

# Chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="hexbin-basic \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Sensor Grid X (km)",
    y_title="Sensor Grid Y (km)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    stroke=False,
    dots_size=5,
    show_x_guides=True,
    show_y_guides=True,
)

# Bin into 5 density levels using log-spaced thresholds for better separation
n_bins = 5
count_min, count_max = float(counts.min()), float(counts.max())
bin_edges = np.logspace(np.log10(count_min), np.log10(count_max + 1), n_bins + 1)
bin_edges[0] = count_min
bin_edges[-1] = count_max + 1

density_names = ["Sparse", "Low", "Moderate", "Dense", "Hotspot"]
bin_labels = [f"{density_names[i]} ({int(bin_edges[i])}\u2013{int(bin_edges[i + 1])})" for i in range(n_bins)]

series_data = [[] for _ in range(n_bins)]
for cx, cy, cnt in zip(center_x, center_y, counts, strict=True):
    idx = min(np.searchsorted(bin_edges[1:], cnt), n_bins - 1)
    series_data[idx].append((round(float(cx), 2), round(float(cy), 2)))

# Dramatically different dot sizes for clear visual hierarchy
dot_sizes = [3, 8, 16, 28, 44]
for i in range(n_bins):
    if series_data[i]:
        chart.add(bin_labels[i], series_data[i], dots_size=dot_sizes[i])

# Save
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")
