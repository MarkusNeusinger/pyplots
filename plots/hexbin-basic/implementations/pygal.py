""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 87/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import numpy as np
import pygal
from pygal.style import Style


# Data - generate bivariate data with clusters for density visualization
np.random.seed(42)
n_points = 5000

# Create clustered distribution
cluster1_x = np.random.randn(n_points // 2) * 1.5 + 2
cluster1_y = np.random.randn(n_points // 2) * 1.5 + 2
cluster2_x = np.random.randn(n_points // 2) * 2 - 2
cluster2_y = np.random.randn(n_points // 2) * 2 - 2

x = np.concatenate([cluster1_x, cluster2_x])
y = np.concatenate([cluster1_y, cluster2_y])

# Compute hexbin using matplotlib (extract hexagon centers and counts)
fig_temp, ax_temp = plt.subplots()
hb = ax_temp.hexbin(x, y, gridsize=20, mincnt=1)
offsets = hb.get_offsets()
counts = hb.get_array()
plt.close(fig_temp)

# Normalize counts for visualization
count_min, count_max = counts.min(), counts.max()
count_range = count_max - count_min if count_max > count_min else 1

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"),  # viridis colors
    opacity=0.85,
    opacity_hover=0.95,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    tooltip_font_size=36,
)

# Create XY chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="hexbin-basic · pygal · pyplots.ai",
    x_title="X Coordinate",
    y_title="Y Coordinate",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    stroke=False,
    dots_size=25,
    show_x_guides=True,
    show_y_guides=True,
)

# Bin hexagons by density into 5 groups (simulating colormap)
n_bins = 5
bin_edges = np.linspace(count_min, count_max + 1, n_bins + 1)
bin_labels = [f"Density: {int(bin_edges[i])}-{int(bin_edges[i + 1] - 1)}" for i in range(n_bins)]

# Create series for each density level
series_data = [[] for _ in range(n_bins)]
for offset, count in zip(offsets, counts, strict=True):
    bin_idx = min(int((count - count_min) / count_range * (n_bins - 1)), n_bins - 1)
    series_data[bin_idx].append((float(offset[0]), float(offset[1])))

# Add series with increasing dot sizes for density
dot_sizes = [15, 22, 28, 34, 40]
for i in range(n_bins):
    if series_data[i]:
        chart.add(bin_labels[i], series_data[i], dots_size=dot_sizes[i])

# Save outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Also save HTML for interactivity
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>hexbin-basic - pygal</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; }}
        .chart {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <figure class="chart">
        {chart.render(is_unicode=True)}
    </figure>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
