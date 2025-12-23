"""pyplots.ai
heatmap-basic: Basic Heatmap
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-23
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


class MatrixHeatmap(Graph):
    """Custom Matrix Heatmap for pygal - displays values in a grid with color intensity."""

    def __init__(self, *args, **kwargs):
        self.matrix_data = kwargs.pop("matrix_data", [])
        self.row_labels = kwargs.pop("row_labels", [])
        self.col_labels = kwargs.pop("col_labels", [])
        self.colormap = kwargs.pop("colormap", ["#f7fbff", "#6baed6", "#2171b5", "#08306b"])
        self.show_values = kwargs.pop("show_values", True)
        super().__init__(*args, **kwargs)

    def _get_color(self, value, min_val, max_val):
        """Get color based on value intensity."""
        if max_val == min_val:
            return self.colormap[-1]
        # Normalize value to 0-1 range
        normalized = (value - min_val) / (max_val - min_val)
        # Map to color index
        idx = min(int(normalized * (len(self.colormap) - 1)), len(self.colormap) - 1)
        return self.colormap[idx]

    def _interpolate_color(self, value, min_val, max_val):
        """Interpolate color for smooth gradient."""
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
        """Draw the matrix heatmap."""
        if not self.matrix_data:
            return

        n_rows = len(self.matrix_data)
        n_cols = len(self.matrix_data[0]) if n_rows > 0 else 0

        # Find value range
        all_values = [v for row in self.matrix_data for v in row]
        min_val = min(all_values)
        max_val = max(all_values)

        # Get plot dimensions
        plot_width = self.view.width
        plot_height = self.view.height

        # Calculate cell size - leave space for labels
        label_margin_left = 350  # Space for row labels
        label_margin_bottom = 200  # Space for column labels
        label_margin_top = 50
        label_margin_right = 250  # Space for colorbar

        available_width = plot_width - label_margin_left - label_margin_right
        available_height = plot_height - label_margin_bottom - label_margin_top

        cell_width = available_width / n_cols * 0.95
        cell_height = available_height / n_rows * 0.95
        gap = min(cell_width, cell_height) * 0.05

        # Calculate offsets to center the grid
        grid_width = n_cols * (cell_width + gap) - gap
        grid_height = n_rows * (cell_height + gap) - gap

        x_offset = self.view.x(0) + label_margin_left + (available_width - grid_width) / 2
        y_offset = self.view.y(n_rows) + label_margin_top + (available_height - grid_height) / 2

        # Create group for the heatmap
        plot_node = self.nodes["plot"]
        heatmap_group = self.svg.node(plot_node, class_="matrix-heatmap")

        # Draw row labels on the left
        row_font_size = min(42, int(cell_height * 0.7))
        for i, label in enumerate(self.row_labels):
            y = y_offset + i * (cell_height + gap) + cell_height / 2
            text_node = self.svg.node(heatmap_group, "text", x=x_offset - 20, y=y + row_font_size * 0.35)
            text_node.set("text-anchor", "end")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{row_font_size}px;font-weight:bold;font-family:sans-serif")
            text_node.text = label

        # Draw column labels at the bottom
        col_font_size = min(38, int(cell_width * 0.5))
        for j, label in enumerate(self.col_labels):
            x = x_offset + j * (cell_width + gap) + cell_width / 2
            y = y_offset + n_rows * (cell_height + gap) + 30
            text_node = self.svg.node(heatmap_group, "text", x=x, y=y)
            text_node.set("text-anchor", "middle")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{col_font_size}px;font-weight:bold;font-family:sans-serif")
            text_node.text = label

        # Draw cells
        value_font_size = min(32, int(min(cell_width, cell_height) * 0.4))
        for i in range(n_rows):
            for j in range(n_cols):
                value = self.matrix_data[i][j]
                color = self._interpolate_color(value, min_val, max_val)

                x = x_offset + j * (cell_width + gap)
                y = y_offset + i * (cell_height + gap)

                # Draw cell rectangle
                rect = self.svg.node(heatmap_group, "rect", x=x, y=y, width=cell_width, height=cell_height, rx=3, ry=3)
                rect.set("fill", color)
                rect.set("stroke", "#ffffff")
                rect.set("stroke-width", "2")

                # Add value text if enabled
                if self.show_values:
                    # Determine text color based on background brightness
                    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
                    brightness = (r * 299 + g * 587 + b * 114) / 1000
                    text_color = "#ffffff" if brightness < 128 else "#333333"

                    text_x = x + cell_width / 2
                    text_y = y + cell_height / 2 + value_font_size * 0.35

                    text_node = self.svg.node(heatmap_group, "text", x=text_x, y=text_y)
                    text_node.set("text-anchor", "middle")
                    text_node.set("fill", text_color)
                    text_node.set("style", f"font-size:{value_font_size}px;font-weight:bold;font-family:sans-serif")
                    text_node.text = f"{value:.1f}" if isinstance(value, float) else str(value)

        # Draw colorbar on the right
        colorbar_width = 50
        colorbar_height = grid_height * 0.75
        colorbar_x = x_offset + grid_width + 80
        colorbar_y = y_offset + (grid_height - colorbar_height) / 2

        # Draw gradient colorbar using multiple rectangles
        n_segments = 50
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
        self.svg.node(
            heatmap_group,
            "rect",
            x=colorbar_x,
            y=colorbar_y,
            width=colorbar_width,
            height=colorbar_height,
            fill="none",
            stroke="#333333",
        )

        # Colorbar labels
        cb_label_size = 36
        # Max value
        text_node = self.svg.node(
            heatmap_group, "text", x=colorbar_x + colorbar_width + 20, y=colorbar_y + cb_label_size * 0.35
        )
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{cb_label_size}px;font-family:sans-serif")
        text_node.text = f"{max_val:.0f}"

        # Mid value
        mid_y = colorbar_y + colorbar_height / 2
        text_node = self.svg.node(
            heatmap_group, "text", x=colorbar_x + colorbar_width + 20, y=mid_y + cb_label_size * 0.35
        )
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{cb_label_size}px;font-family:sans-serif")
        text_node.text = f"{(min_val + max_val) / 2:.0f}"

        # Min value
        text_node = self.svg.node(
            heatmap_group,
            "text",
            x=colorbar_x + colorbar_width + 20,
            y=colorbar_y + colorbar_height + cb_label_size * 0.35,
        )
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{cb_label_size}px;font-family:sans-serif")
        text_node.text = f"{min_val:.0f}"

        # Colorbar title
        cb_title_size = 40
        cb_title_x = colorbar_x + colorbar_width / 2
        cb_title_y = colorbar_y - 40
        text_node = self.svg.node(heatmap_group, "text", x=cb_title_x, y=cb_title_y)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{cb_title_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = "Score"

    def _compute(self):
        """Compute the box for rendering."""
        n_rows = len(self.matrix_data) if self.matrix_data else 1
        n_cols = len(self.matrix_data[0]) if self.matrix_data and len(self.matrix_data) > 0 else 1
        self._box.xmin = 0
        self._box.xmax = n_cols
        self._box.ymin = 0
        self._box.ymax = n_rows


# Generate data - Performance metrics across departments and quarters
np.random.seed(42)

# Row and column labels - realistic business context
departments = ["Sales", "Marketing", "Engineering", "Support", "Finance", "HR", "Operations", "R&D"]
quarters = ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]

# Generate performance scores (0-100)
# Create realistic patterns: some departments improve over time, others fluctuate
base_scores = {
    "Sales": [72, 75, 68, 82, 85, 88, 91, 94],
    "Marketing": [65, 70, 72, 75, 78, 80, 82, 85],
    "Engineering": [88, 90, 92, 85, 87, 91, 93, 96],
    "Support": [78, 75, 72, 70, 73, 76, 79, 82],
    "Finance": [85, 86, 87, 88, 89, 90, 91, 92],
    "HR": [70, 72, 74, 76, 78, 80, 75, 77],
    "Operations": [80, 78, 82, 85, 83, 86, 88, 90],
    "R&D": [60, 65, 70, 75, 80, 85, 88, 92],
}

# Add some noise
matrix_data = []
for dept in departments:
    row = []
    for score in base_scores[dept]:
        noisy_score = score + np.random.randint(-3, 4)
        row.append(max(50, min(100, noisy_score)))
    matrix_data.append(row)

# Custom style for 3600x3600 square canvas (better for heatmap)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=72,
    legend_font_size=48,
    label_font_size=42,
    value_font_size=36,
    font_family="sans-serif",
)

# Blue sequential colormap (Python Blue theme)
blue_colormap = ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08519c", "#08306b"]

# Create heatmap
chart = MatrixHeatmap(
    width=3600,
    height=3600,
    style=custom_style,
    title="heatmap-basic · pygal · pyplots.ai",
    matrix_data=matrix_data,
    row_labels=departments,
    col_labels=quarters,
    colormap=blue_colormap,
    show_values=True,
    show_legend=False,
    margin=120,
    margin_top=200,
    margin_bottom=100,
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
    <title>heatmap-basic - pygal</title>
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
