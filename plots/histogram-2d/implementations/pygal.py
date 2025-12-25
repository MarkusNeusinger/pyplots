""" pyplots.ai
histogram-2d: 2D Histogram Heatmap
Library: pygal 3.1.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-25
"""

import sys

import numpy as np


# Temporarily remove current directory from path to avoid name collision
_cwd = sys.path[0] if sys.path[0] else "."
if _cwd in sys.path:
    sys.path.remove(_cwd)

from pygal.graph.graph import Graph  # noqa: E402
from pygal.style import Style  # noqa: E402


# Restore path
sys.path.insert(0, _cwd)


class Histogram2D(Graph):
    """Custom 2D Histogram Heatmap for pygal - displays joint distribution as color-mapped bins."""

    def __init__(self, *args, **kwargs):
        self.histogram_counts = kwargs.pop("histogram_counts", [])
        self.x_edges = kwargs.pop("x_edges", [])
        self.y_edges = kwargs.pop("y_edges", [])
        self.colormap = kwargs.pop("colormap", ["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"])
        self.colorbar_label = kwargs.pop("colorbar_label", "Count")
        self.x_axis_label = kwargs.pop("x_axis_label", "X")
        self.y_axis_label = kwargs.pop("y_axis_label", "Y")
        super().__init__(*args, **kwargs)

    def _interpolate_color(self, value, min_val, max_val):
        """Interpolate color for smooth gradient using viridis-like colormap."""
        if max_val == min_val:
            return self.colormap[-1]

        # Normalize value to 0-1 range
        normalized = (value - min_val) / (max_val - min_val)
        normalized = max(0, min(1, normalized))

        # Get position in colormap
        pos = normalized * (len(self.colormap) - 1)
        idx1 = int(pos)
        idx2 = min(idx1 + 1, len(self.colormap) - 1)
        frac = pos - idx1

        # Interpolate between colors
        c1 = self.colormap[idx1]
        c2 = self.colormap[idx2]

        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)

        r = int(r1 + (r2 - r1) * frac)
        g = int(g1 + (g2 - g1) * frac)
        b = int(b1 + (b2 - b1) * frac)

        return f"#{r:02x}{g:02x}{b:02x}"

    def _plot(self):
        """Draw the 2D histogram heatmap."""
        if len(self.histogram_counts) == 0:
            return

        n_rows = len(self.histogram_counts)
        n_cols = len(self.histogram_counts[0]) if n_rows > 0 else 0

        # Find value range (counts)
        all_values = [v for row in self.histogram_counts for v in row]
        min_val = min(all_values)
        max_val = max(all_values)

        # Get plot dimensions
        plot_width = self.view.width
        plot_height = self.view.height

        # Calculate layout margins
        label_margin_left = 250  # Space for y-axis labels
        label_margin_bottom = 220  # Space for x-axis labels
        label_margin_top = 80
        label_margin_right = 280  # Space for colorbar

        available_width = plot_width - label_margin_left - label_margin_right
        available_height = plot_height - label_margin_bottom - label_margin_top

        cell_width = available_width / n_cols
        cell_height = available_height / n_rows

        # Calculate offsets
        x_offset = self.view.x(0) + label_margin_left
        y_offset = self.view.y(n_rows) + label_margin_top

        # Create group for the heatmap
        plot_node = self.nodes["plot"]
        heatmap_group = self.svg.node(plot_node, class_="histogram-2d")

        # Draw cells (note: histogram counts are oriented with y-axis from bottom to top)
        for i in range(n_rows):
            for j in range(n_cols):
                # Flip row index so y increases upward
                value = self.histogram_counts[n_rows - 1 - i][j]
                color = self._interpolate_color(value, min_val, max_val)

                x = x_offset + j * cell_width
                y = y_offset + i * cell_height

                # Draw cell rectangle (no gap for continuous heatmap appearance)
                rect = self.svg.node(
                    heatmap_group,
                    "rect",
                    x=x,
                    y=y,
                    width=cell_width + 0.5,  # Slight overlap to avoid gaps
                    height=cell_height + 0.5,
                )
                rect.set("fill", color)

        # Draw border around the entire heatmap
        grid_width = n_cols * cell_width
        grid_height = n_rows * cell_height
        self.svg.node(
            heatmap_group,
            "rect",
            x=x_offset,
            y=y_offset,
            width=grid_width,
            height=grid_height,
            fill="none",
            stroke="#333333",
        )
        rect_border = self.svg.node(heatmap_group, "rect", x=x_offset, y=y_offset, width=grid_width, height=grid_height)
        rect_border.set("fill", "none")
        rect_border.set("stroke", "#333333")
        rect_border.set("stroke-width", "2")

        # Draw X-axis ticks and labels
        x_tick_font_size = 36
        n_x_ticks = min(7, len(self.x_edges))
        x_tick_indices = np.linspace(0, len(self.x_edges) - 1, n_x_ticks, dtype=int)

        for idx in x_tick_indices:
            x_pos = x_offset + idx * cell_width
            tick_y = y_offset + grid_height

            # Tick mark
            self.svg.node(heatmap_group, "line", x1=x_pos, y1=tick_y, x2=x_pos, y2=tick_y + 15, stroke="#333333")
            tick_line = self.svg.node(heatmap_group, "line", x1=x_pos, y1=tick_y, x2=x_pos, y2=tick_y + 15)
            tick_line.set("stroke", "#333333")
            tick_line.set("stroke-width", "2")

            # Label
            text_node = self.svg.node(heatmap_group, "text", x=x_pos, y=tick_y + 50)
            text_node.set("text-anchor", "middle")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{x_tick_font_size}px;font-family:sans-serif")
            text_node.text = f"{self.x_edges[idx]:.1f}"

        # X-axis label
        x_label_x = x_offset + grid_width / 2
        x_label_y = y_offset + grid_height + 120
        text_node = self.svg.node(heatmap_group, "text", x=x_label_x, y=x_label_y)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", "font-size:48px;font-weight:bold;font-family:sans-serif")
        text_node.text = self.x_axis_label

        # Draw Y-axis ticks and labels
        y_tick_font_size = 36
        n_y_ticks = min(7, len(self.y_edges))
        y_tick_indices = np.linspace(0, len(self.y_edges) - 1, n_y_ticks, dtype=int)

        for idx in y_tick_indices:
            # Y increases upward, so invert position
            y_pos = y_offset + grid_height - idx * cell_height
            tick_x = x_offset

            # Tick mark
            tick_line = self.svg.node(heatmap_group, "line", x1=tick_x - 15, y1=y_pos, x2=tick_x, y2=y_pos)
            tick_line.set("stroke", "#333333")
            tick_line.set("stroke-width", "2")

            # Label
            text_node = self.svg.node(heatmap_group, "text", x=tick_x - 25, y=y_pos + y_tick_font_size * 0.35)
            text_node.set("text-anchor", "end")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{y_tick_font_size}px;font-family:sans-serif")
            text_node.text = f"{self.y_edges[idx]:.1f}"

        # Y-axis label (rotated)
        y_label_x = x_offset - 180
        y_label_y = y_offset + grid_height / 2
        text_node = self.svg.node(heatmap_group, "text", x=y_label_x, y=y_label_y)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", "font-size:48px;font-weight:bold;font-family:sans-serif")
        text_node.set("transform", f"rotate(-90, {y_label_x}, {y_label_y})")
        text_node.text = self.y_axis_label

        # Draw colorbar on the right
        colorbar_width = 50
        colorbar_height = grid_height * 0.85
        colorbar_x = x_offset + grid_width + 60
        colorbar_y = y_offset + (grid_height - colorbar_height) / 2

        # Draw gradient colorbar using multiple rectangles
        n_segments = 60
        segment_height = colorbar_height / n_segments
        for i in range(n_segments):
            seg_value = min_val + (max_val - min_val) * (n_segments - 1 - i) / (n_segments - 1)
            seg_color = self._interpolate_color(seg_value, min_val, max_val)
            seg_y = colorbar_y + i * segment_height

            self.svg.node(
                heatmap_group,
                "rect",
                x=colorbar_x,
                y=seg_y,
                width=colorbar_width,
                height=segment_height + 1,
                fill=seg_color,
            )

        # Colorbar border
        cb_border = self.svg.node(
            heatmap_group, "rect", x=colorbar_x, y=colorbar_y, width=colorbar_width, height=colorbar_height
        )
        cb_border.set("fill", "none")
        cb_border.set("stroke", "#333333")
        cb_border.set("stroke-width", "2")

        # Colorbar tick labels
        cb_label_size = 36
        n_cb_ticks = 5
        for i in range(n_cb_ticks):
            frac = i / (n_cb_ticks - 1)
            tick_value = max_val - frac * (max_val - min_val)
            tick_y = colorbar_y + frac * colorbar_height

            # Tick mark
            tick_line = self.svg.node(
                heatmap_group,
                "line",
                x1=colorbar_x + colorbar_width,
                y1=tick_y,
                x2=colorbar_x + colorbar_width + 10,
                y2=tick_y,
            )
            tick_line.set("stroke", "#333333")
            tick_line.set("stroke-width", "2")

            # Label
            text_node = self.svg.node(
                heatmap_group, "text", x=colorbar_x + colorbar_width + 20, y=tick_y + cb_label_size * 0.35
            )
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{cb_label_size}px;font-family:sans-serif")
            text_node.text = f"{int(tick_value)}"

        # Colorbar title
        cb_title_size = 42
        cb_title_x = colorbar_x + colorbar_width / 2
        cb_title_y = colorbar_y - 30
        text_node = self.svg.node(heatmap_group, "text", x=cb_title_x, y=cb_title_y)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{cb_title_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = self.colorbar_label

    def _compute(self):
        """Compute the box for rendering."""
        n_rows = len(self.histogram_counts) if self.histogram_counts else 1
        n_cols = len(self.histogram_counts[0]) if self.histogram_counts and len(self.histogram_counts) > 0 else 1
        self._box.xmin = 0
        self._box.xmax = n_cols
        self._box.ymin = 0
        self._box.ymax = n_rows


# Generate bivariate normal data with correlation
np.random.seed(42)

# Create correlated bivariate data representing customer age vs purchase frequency
n_points = 5000
mean = [35, 12]  # Mean age ~35, mean purchases ~12 per year
cov = [[100, 35], [35, 25]]  # Positive correlation between age and purchases

data = np.random.multivariate_normal(mean, cov, n_points)
x = data[:, 0]  # Customer age
y = data[:, 1]  # Annual purchase frequency

# Add a second cluster to show density variation
n_points2 = 2000
mean2 = [55, 8]  # Older customers, fewer purchases
cov2 = [[64, -20], [-20, 16]]
data2 = np.random.multivariate_normal(mean2, cov2, n_points2)
x = np.concatenate([x, data2[:, 0]])
y = np.concatenate([y, data2[:, 1]])

# Clip to realistic ranges
x = np.clip(x, 18, 75)  # Age 18-75
y = np.clip(y, 0, 30)  # 0-30 purchases per year

# Create 2D histogram
n_bins = 25
counts, x_edges, y_edges = np.histogram2d(x, y, bins=n_bins)
counts = counts.T  # Transpose so rows correspond to y values

# Viridis-like colormap for perceptually uniform colors
viridis_colors = [
    "#440154",  # Dark purple
    "#482878",
    "#3e4a89",
    "#31688e",
    "#26828e",
    "#1f9e89",
    "#35b779",
    "#6ece58",
    "#b5de2b",
    "#fde725",  # Yellow
]

# Custom style for square canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=64,
    legend_font_size=48,
    label_font_size=42,
    value_font_size=36,
    font_family="sans-serif",
)

# Create 2D histogram chart
chart = Histogram2D(
    width=3600,
    height=3600,
    style=custom_style,
    title="histogram-2d · pygal · pyplots.ai",
    histogram_counts=counts.tolist(),
    x_edges=x_edges.tolist(),
    y_edges=y_edges.tolist(),
    colormap=viridis_colors,
    colorbar_label="Count",
    x_axis_label="Customer Age (years)",
    y_axis_label="Annual Purchases",
    show_legend=False,
    margin=100,
    margin_top=180,
    margin_bottom=80,
    show_x_labels=False,
    show_y_labels=False,
)

# Add a dummy series to trigger _plot (pygal requires at least one series)
chart.add("", [0])

# Save output
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Also save HTML for interactivity
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>histogram-2d - pygal</title>
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
