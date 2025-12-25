"""pyplots.ai
histogram-2d: 2D Histogram Heatmap
Library: pygal 3.1.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-25
"""

# Handle module name collision (this file is named pygal.py)
import sys


sys.path = [p for p in sys.path if "implementations" not in p]

import numpy as np  # noqa: E402
from pygal.graph.graph import Graph  # noqa: E402
from pygal.style import Style  # noqa: E402


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

# Viridis colormap for perceptually uniform colors
viridis = ["#440154", "#482878", "#3e4a89", "#31688e", "#26828e", "#1f9e89", "#35b779", "#6ece58", "#b5de2b", "#fde725"]


def interpolate_color(value, min_val, max_val):
    """Get color from viridis colormap for value."""
    if max_val == min_val:
        return viridis[-1]
    t = max(0, min(1, (value - min_val) / (max_val - min_val)))
    pos = t * (len(viridis) - 1)
    i = int(pos)
    j = min(i + 1, len(viridis) - 1)
    frac = pos - i
    c1, c2 = viridis[i], viridis[j]
    r = int(int(c1[1:3], 16) * (1 - frac) + int(c2[1:3], 16) * frac)
    g = int(int(c1[3:5], 16) * (1 - frac) + int(c2[3:5], 16) * frac)
    b = int(int(c1[5:7], 16) * (1 - frac) + int(c2[5:7], 16) * frac)
    return f"#{r:02x}{g:02x}{b:02x}"


class Histogram2D(Graph):
    """2D Histogram Heatmap chart for pygal."""

    def __init__(self, hist_data, x_edges, y_edges, x_label, y_label, cb_label, **kwargs):
        self.hist_data = hist_data
        self.x_edges = x_edges
        self.y_edges = y_edges
        self.x_label = x_label
        self.y_label = y_label
        self.cb_label = cb_label
        super().__init__(**kwargs)

    def _plot(self):
        if len(self.hist_data) == 0:
            return

        n_rows, n_cols = len(self.hist_data), len(self.hist_data[0])
        min_val = min(v for row in self.hist_data for v in row)
        max_val = max(v for row in self.hist_data for v in row)

        # Layout calculations
        plot_w, plot_h = self.view.width, self.view.height
        margin_l, margin_r, margin_t, margin_b = 250, 280, 80, 220
        grid_w = plot_w - margin_l - margin_r
        grid_h = plot_h - margin_t - margin_b
        cell_w, cell_h = grid_w / n_cols, grid_h / n_rows
        x_off, y_off = self.view.x(0) + margin_l, self.view.y(n_rows) + margin_t

        plot_node = self.nodes["plot"]
        grp = self.svg.node(plot_node, class_="histogram-2d")

        # Draw heatmap cells
        for i in range(n_rows):
            for j in range(n_cols):
                val = self.hist_data[n_rows - 1 - i][j]
                color = interpolate_color(val, min_val, max_val)
                rect = self.svg.node(
                    grp, "rect", x=x_off + j * cell_w, y=y_off + i * cell_h, width=cell_w + 0.5, height=cell_h + 0.5
                )
                rect.set("fill", color)

        # Border
        border = self.svg.node(grp, "rect", x=x_off, y=y_off, width=grid_w, height=grid_h)
        border.set("fill", "none")
        border.set("stroke", "#333")
        border.set("stroke-width", "2")

        # X-axis ticks and labels
        for idx in np.linspace(0, len(self.x_edges) - 1, 7, dtype=int):
            px = x_off + idx * cell_w
            py = y_off + grid_h
            line = self.svg.node(grp, "line", x1=px, y1=py, x2=px, y2=py + 15)
            line.set("stroke", "#333")
            line.set("stroke-width", "2")
            txt = self.svg.node(grp, "text", x=px, y=py + 50)
            txt.set("text-anchor", "middle")
            txt.set("fill", "#333")
            txt.set("style", "font-size:36px;font-family:sans-serif")
            txt.text = f"{self.x_edges[idx]:.0f}"

        # X-axis label
        txt = self.svg.node(grp, "text", x=x_off + grid_w / 2, y=y_off + grid_h + 120)
        txt.set("text-anchor", "middle")
        txt.set("fill", "#333")
        txt.set("style", "font-size:48px;font-weight:bold;font-family:sans-serif")
        txt.text = self.x_label

        # Y-axis ticks and labels
        for idx in np.linspace(0, len(self.y_edges) - 1, 7, dtype=int):
            py = y_off + grid_h - idx * cell_h
            px = x_off
            line = self.svg.node(grp, "line", x1=px - 15, y1=py, x2=px, y2=py)
            line.set("stroke", "#333")
            line.set("stroke-width", "2")
            txt = self.svg.node(grp, "text", x=px - 25, y=py + 12)
            txt.set("text-anchor", "end")
            txt.set("fill", "#333")
            txt.set("style", "font-size:36px;font-family:sans-serif")
            txt.text = f"{self.y_edges[idx]:.0f}"

        # Y-axis label (rotated)
        lx, ly = x_off - 180, y_off + grid_h / 2
        txt = self.svg.node(grp, "text", x=lx, y=ly)
        txt.set("text-anchor", "middle")
        txt.set("fill", "#333")
        txt.set("style", "font-size:48px;font-weight:bold;font-family:sans-serif")
        txt.set("transform", f"rotate(-90, {lx}, {ly})")
        txt.text = self.y_label

        # Colorbar
        cb_w, cb_h = 50, grid_h * 0.85
        cb_x, cb_y = x_off + grid_w + 60, y_off + (grid_h - cb_h) / 2
        n_seg = 60
        seg_h = cb_h / n_seg
        for i in range(n_seg):
            seg_val = min_val + (max_val - min_val) * (n_seg - 1 - i) / (n_seg - 1)
            self.svg.node(
                grp,
                "rect",
                x=cb_x,
                y=cb_y + i * seg_h,
                width=cb_w,
                height=seg_h + 1,
                fill=interpolate_color(seg_val, min_val, max_val),
            )

        cb_border = self.svg.node(grp, "rect", x=cb_x, y=cb_y, width=cb_w, height=cb_h)
        cb_border.set("fill", "none")
        cb_border.set("stroke", "#333")
        cb_border.set("stroke-width", "2")

        # Colorbar ticks
        for i in range(5):
            frac = i / 4
            tick_val = max_val - frac * (max_val - min_val)
            ty = cb_y + frac * cb_h
            line = self.svg.node(grp, "line", x1=cb_x + cb_w, y1=ty, x2=cb_x + cb_w + 10, y2=ty)
            line.set("stroke", "#333")
            line.set("stroke-width", "2")
            txt = self.svg.node(grp, "text", x=cb_x + cb_w + 20, y=ty + 12)
            txt.set("fill", "#333")
            txt.set("style", "font-size:36px;font-family:sans-serif")
            txt.text = f"{int(tick_val)}"

        # Colorbar title
        txt = self.svg.node(grp, "text", x=cb_x + cb_w / 2, y=cb_y - 30)
        txt.set("text-anchor", "middle")
        txt.set("fill", "#333")
        txt.set("style", "font-size:42px;font-weight:bold;font-family:sans-serif")
        txt.text = self.cb_label

    def _compute(self):
        n_rows = len(self.hist_data) if self.hist_data else 1
        n_cols = len(self.hist_data[0]) if self.hist_data else 1
        self._box.xmin, self._box.xmax = 0, n_cols
        self._box.ymin, self._box.ymax = 0, n_rows


# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    title_font_size=64,
    font_family="sans-serif",
)

# Create chart
chart = Histogram2D(
    hist_data=counts.tolist(),
    x_edges=x_edges.tolist(),
    y_edges=y_edges.tolist(),
    x_label="Customer Age (years)",
    y_label="Annual Purchases (count)",
    cb_label="Count",
    width=3600,
    height=3600,
    style=custom_style,
    title="histogram-2d · pygal · pyplots.ai",
    show_legend=False,
    margin=100,
    margin_top=180,
    margin_bottom=80,
    show_x_labels=False,
    show_y_labels=False,
)

# Trigger rendering (pygal requires at least one series)
chart.add("", [0])

# Save output
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Save HTML for interactivity
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
