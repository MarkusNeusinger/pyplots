"""pyplots.ai
heatmap-basic: Basic Heatmap
Library: pygal 3.1.0 | Python 3.14.3
Quality: /100 | Updated: 2026-02-15
"""

import sys

import numpy as np


# Temporarily remove current directory from path to avoid name collision
_cwd = sys.path[0] if sys.path[0] else "."
if _cwd in sys.path:
    sys.path.remove(_cwd)

from pygal.graph.graph import Graph  # noqa: E402
from pygal.style import Style  # noqa: E402


sys.path.insert(0, _cwd)


class MatrixHeatmap(Graph):
    """Custom Matrix Heatmap for pygal - displays values in a grid with color intensity."""

    def __init__(self, *args, **kwargs):
        self.matrix_data = kwargs.pop("matrix_data", [])
        self.row_labels = kwargs.pop("row_labels", [])
        self.col_labels = kwargs.pop("col_labels", [])
        self.colormap = kwargs.pop("colormap", ["#f7fbff", "#6baed6", "#2171b5", "#08306b"])
        self.show_values = kwargs.pop("show_values", True)
        self.x_axis_title = kwargs.pop("x_axis_title", "")
        self.y_axis_title = kwargs.pop("y_axis_title", "")
        self.colorbar_title = kwargs.pop("colorbar_title", "")
        super().__init__(*args, **kwargs)

    def _interpolate_color(self, value, min_val, max_val):
        """Interpolate between colormap stops for smooth gradient."""
        if max_val == min_val:
            return self.colormap[-1]
        normalized = max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
        pos = normalized * (len(self.colormap) - 1)
        idx1 = int(pos)
        idx2 = min(idx1 + 1, len(self.colormap) - 1)
        frac = pos - idx1

        c1, c2 = self.colormap[idx1], self.colormap[idx2]
        r = int(int(c1[1:3], 16) + (int(c2[1:3], 16) - int(c1[1:3], 16)) * frac)
        g = int(int(c1[3:5], 16) + (int(c2[3:5], 16) - int(c1[3:5], 16)) * frac)
        b = int(int(c1[5:7], 16) + (int(c2[5:7], 16) - int(c1[5:7], 16)) * frac)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _plot(self):
        """Draw the matrix heatmap."""
        if not self.matrix_data:
            return

        n_rows = len(self.matrix_data)
        n_cols = len(self.matrix_data[0])

        all_values = [v for row in self.matrix_data for v in row]
        min_val, max_val = min(all_values), max(all_values)

        plot_width = self.view.width
        plot_height = self.view.height

        # Layout margins
        margin_left = 380
        margin_bottom = 260
        margin_top = 50
        margin_right = 280

        avail_w = plot_width - margin_left - margin_right
        avail_h = plot_height - margin_bottom - margin_top

        cell_w = avail_w / n_cols * 0.95
        cell_h = avail_h / n_rows * 0.95
        gap = min(cell_w, cell_h) * 0.05

        grid_w = n_cols * (cell_w + gap) - gap
        grid_h = n_rows * (cell_h + gap) - gap

        x0 = self.view.x(0) + margin_left + (avail_w - grid_w) / 2
        y0 = self.view.y(n_rows) + margin_top + (avail_h - grid_h) / 2

        plot_node = self.nodes["plot"]
        group = self.svg.node(plot_node, class_="matrix-heatmap")

        # Row labels
        row_fs = min(42, int(cell_h * 0.7))
        for i, label in enumerate(self.row_labels):
            y = y0 + i * (cell_h + gap) + cell_h / 2
            t = self.svg.node(group, "text", x=x0 - 20, y=y + row_fs * 0.35)
            t.set("text-anchor", "end")
            t.set("fill", "#333333")
            t.set("style", f"font-size:{row_fs}px;font-weight:500;font-family:sans-serif")
            t.text = label

        # Column labels (rotated for better readability)
        col_fs = min(38, int(cell_w * 0.5))
        for j, label in enumerate(self.col_labels):
            x = x0 + j * (cell_w + gap) + cell_w / 2
            y = y0 + n_rows * (cell_h + gap) + 20
            t = self.svg.node(group, "text", x=x, y=y)
            t.set("text-anchor", "end")
            t.set("fill", "#333333")
            t.set("style", f"font-size:{col_fs}px;font-weight:500;font-family:sans-serif")
            t.set("transform", f"rotate(-35, {x}, {y})")
            t.text = label

        # Cells with values
        val_fs = min(34, int(min(cell_w, cell_h) * 0.4))
        for i in range(n_rows):
            for j in range(n_cols):
                value = self.matrix_data[i][j]
                color = self._interpolate_color(value, min_val, max_val)

                cx = x0 + j * (cell_w + gap)
                cy = y0 + i * (cell_h + gap)

                rect = self.svg.node(group, "rect", x=cx, y=cy, width=cell_w, height=cell_h, rx=4, ry=4)
                rect.set("fill", color)
                rect.set("stroke", "#ffffff")
                rect.set("stroke-width", "2")

                if self.show_values:
                    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
                    brightness = (r * 299 + g * 587 + b * 114) / 1000
                    text_color = "#ffffff" if brightness < 128 else "#333333"

                    t = self.svg.node(group, "text", x=cx + cell_w / 2, y=cy + cell_h / 2 + val_fs * 0.35)
                    t.set("text-anchor", "middle")
                    t.set("fill", text_color)
                    t.set("style", f"font-size:{val_fs}px;font-weight:bold;font-family:sans-serif")
                    t.text = f"{value:.0f}"

        # Colorbar
        cb_w, cb_h = 50, grid_h * 0.75
        cb_x = x0 + grid_w + 80
        cb_y = y0 + (grid_h - cb_h) / 2

        n_segments = 50
        seg_h = cb_h / n_segments
        for i in range(n_segments):
            seg_val = min_val + (max_val - min_val) * (n_segments - 1 - i) / (n_segments - 1)
            self.svg.node(
                group,
                "rect",
                x=cb_x,
                y=cb_y + i * seg_h,
                width=cb_w,
                height=seg_h + 1,
                fill=self._interpolate_color(seg_val, min_val, max_val),
            )

        self.svg.node(group, "rect", x=cb_x, y=cb_y, width=cb_w, height=cb_h, fill="none", stroke="#999999")

        # Colorbar tick labels
        cb_fs = 36
        for frac, label_val in [(0.0, max_val), (0.5, (min_val + max_val) / 2), (1.0, min_val)]:
            ty = cb_y + cb_h * frac
            t = self.svg.node(group, "text", x=cb_x + cb_w + 20, y=ty + cb_fs * 0.35)
            t.set("fill", "#333333")
            t.set("style", f"font-size:{cb_fs}px;font-family:sans-serif")
            t.text = f"{label_val:.0f}"

        # Colorbar title
        cb_title_fs = 40
        t = self.svg.node(group, "text", x=cb_x + cb_w / 2, y=cb_y - 40)
        t.set("text-anchor", "middle")
        t.set("fill", "#333333")
        t.set("style", f"font-size:{cb_title_fs}px;font-weight:bold;font-family:sans-serif")
        t.text = self.colorbar_title or "Value"

        # Y-axis title (rotated, left of row labels)
        if self.y_axis_title:
            ax_fs = 44
            ax_x = x0 - margin_left * 0.75
            ax_y = y0 + grid_h / 2
            t = self.svg.node(group, "text", x=ax_x, y=ax_y)
            t.set("text-anchor", "middle")
            t.set("fill", "#333333")
            t.set("style", f"font-size:{ax_fs}px;font-weight:bold;font-family:sans-serif")
            t.set("transform", f"rotate(-90, {ax_x}, {ax_y})")
            t.text = self.y_axis_title

        # X-axis title (below column labels)
        if self.x_axis_title:
            ax_fs = 44
            ax_x = x0 + grid_w / 2
            ax_y = y0 + n_rows * (cell_h + gap) + margin_bottom * 0.85
            t = self.svg.node(group, "text", x=ax_x, y=ax_y)
            t.set("text-anchor", "middle")
            t.set("fill", "#333333")
            t.set("style", f"font-size:{ax_fs}px;font-weight:bold;font-family:sans-serif")
            t.text = self.x_axis_title

    def _compute(self):
        """Compute the box for rendering."""
        n_rows = len(self.matrix_data) if self.matrix_data else 1
        n_cols = len(self.matrix_data[0]) if self.matrix_data and len(self.matrix_data) > 0 else 1
        self._box.xmin = 0
        self._box.xmax = n_cols
        self._box.ymin = 0
        self._box.ymax = n_rows


# Data - Monthly website traffic (thousands) across content categories
np.random.seed(42)

categories = ["Tech", "Science", "Health", "Finance", "Sports", "Travel", "Food", "Culture"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Realistic traffic patterns: seasonal trends per category
base_traffic = {
    "Tech": [120, 115, 130, 135, 140, 125, 110, 105, 145, 155, 160, 150],
    "Science": [85, 80, 90, 95, 88, 82, 78, 75, 92, 98, 95, 88],
    "Health": [95, 110, 105, 100, 90, 85, 80, 82, 115, 120, 108, 130],
    "Finance": [140, 135, 150, 145, 130, 125, 120, 118, 155, 160, 165, 170],
    "Sports": [70, 65, 80, 85, 95, 100, 105, 110, 90, 75, 72, 68],
    "Travel": [60, 55, 75, 90, 110, 130, 140, 145, 105, 80, 65, 58],
    "Food": [88, 82, 85, 90, 95, 92, 98, 100, 88, 92, 105, 115],
    "Culture": [72, 68, 78, 82, 85, 88, 75, 70, 80, 90, 95, 92],
}

matrix_data = []
for cat in categories:
    row = [max(40, score + np.random.randint(-8, 9)) for score in base_traffic[cat]]
    matrix_data.append(row)

# Style
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

# Sequential blue colormap
blue_colormap = ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#3182bd", "#08519c", "#08306b"]

# Chart
chart = MatrixHeatmap(
    width=3600,
    height=3600,
    style=custom_style,
    title="heatmap-basic · pygal · pyplots.ai",
    matrix_data=matrix_data,
    row_labels=categories,
    col_labels=months,
    colormap=blue_colormap,
    show_values=True,
    show_legend=False,
    margin=120,
    margin_top=200,
    margin_bottom=100,
    show_x_labels=False,
    show_y_labels=False,
    x_axis_title="Month",
    y_axis_title="Content Category",
    colorbar_title="Visits (k)",
)

chart.add("", [0])

# Save
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

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
