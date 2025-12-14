"""
contour-basic: Basic Contour Plot
Library: pygal
"""

import matplotlib.pyplot as plt
import numpy as np
import pygal
from pygal.style import Style


# Data - create a 2D Gaussian surface for demonstration
np.random.seed(42)
grid_size = 50

x = np.linspace(-3, 3, grid_size)
y = np.linspace(-3, 3, grid_size)
X, Y = np.meshgrid(x, y)

# Create a 2D Gaussian function with two peaks
Z = np.exp(-(X**2 + Y**2) / 2) + 0.5 * np.exp(-((X - 1.5) ** 2 + (Y + 1) ** 2) / 1.5)

# Use matplotlib to extract contour lines (pygal has no native contour support)
fig_temp, ax_temp = plt.subplots()
levels = np.linspace(Z.min(), Z.max(), 6)  # 6 levels to fit all in legend
contour = ax_temp.contour(X, Y, Z, levels=levels)
plt.close(fig_temp)

# Viridis-inspired color palette for 6 levels (sequential, colorblind-safe)
contour_colors = (
    "#440154",  # Dark purple (low)
    "#31688e",  # Blue
    "#21918c",  # Teal
    "#35b779",  # Green
    "#90d743",  # Yellow-green
    "#fde725",  # Yellow (high)
)

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=contour_colors,
    opacity=1.0,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=36,
    value_font_size=32,
    tooltip_font_size=36,
    stroke_width=6,  # Thicker lines for visibility
)

# Create XY chart for contour lines
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="contour-basic · pygal · pyplots.ai",
    x_title="X Coordinate",
    y_title="Y Coordinate",
    show_legend=True,
    legend_box_size=24,  # Larger legend color boxes
    stroke=True,
    show_dots=False,
    show_x_guides=True,
    show_y_guides=True,
    truncate_legend=-1,  # Don't truncate legend text
)

# Extract contour paths from matplotlib and add to pygal
for i, level_segments in enumerate(contour.allsegs):
    level_value = levels[i]

    if level_segments:
        # Combine all segments for this level into one series
        all_points = []
        for segment in level_segments:
            if len(segment) > 1:
                # Add None separator between disconnected segments
                if all_points:
                    all_points.append(None)
                for vertex in segment:
                    all_points.append((float(vertex[0]), float(vertex[1])))

        if all_points:
            # Format level label for legend
            label = f"z = {level_value:.2f}"
            chart.add(label, all_points)

# Save outputs
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Also save HTML for interactivity
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>contour-basic - pygal</title>
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
