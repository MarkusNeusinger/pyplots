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

# Create a 2D Gaussian function
Z = np.exp(-(X**2 + Y**2) / 2) + 0.5 * np.exp(-((X - 1.5) ** 2 + (Y + 1) ** 2) / 1.5)

# Use matplotlib to extract contour lines
fig_temp, ax_temp = plt.subplots()
levels = np.linspace(Z.min(), Z.max(), 12)
contour = ax_temp.contour(X, Y, Z, levels=levels)
plt.close(fig_temp)

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    # Viridis-inspired colors for contour levels
    colors=(
        "#440154",
        "#482878",
        "#3e4989",
        "#31688e",
        "#26828e",
        "#1f9e89",
        "#35b779",
        "#6ece58",
        "#b5de2b",
        "#fde725",
        "#306998",
        "#FFD43B",
    ),
    opacity=0.9,
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=36,
    value_font_size=36,
    tooltip_font_size=36,
    stroke_width=4,
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
    legend_at_bottom=True,
    legend_at_bottom_columns=6,
    stroke=True,
    show_dots=False,
    show_x_guides=True,
    show_y_guides=True,
    x_labels_major_every=2,
    y_labels_major_every=2,
)

# Extract contour paths from matplotlib and add to pygal
# Use allsegs to get contour line segments (compatible with matplotlib 3.8+)
for i, level_segments in enumerate(contour.allsegs):
    level_value = levels[i]

    if level_segments:
        # Combine all segments for this level into one series
        all_points = []
        for segment in level_segments:
            if len(segment) > 1:
                # Add points with None separator between disconnected segments
                if all_points:
                    all_points.append(None)  # Separator
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
