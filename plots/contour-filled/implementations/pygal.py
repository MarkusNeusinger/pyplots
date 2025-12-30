""" pyplots.ai
contour-filled: Filled Contour Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-30
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


class FilledContour(Graph):
    """Custom Filled Contour Plot for pygal - displays colored regions of a 2D scalar field."""

    def __init__(self, *args, **kwargs):
        self.x_data = kwargs.pop("x_data", [])
        self.y_data = kwargs.pop("y_data", [])
        self.z_data = kwargs.pop("z_data", [])
        self.n_levels = kwargs.pop("n_levels", 15)
        self.colormap = kwargs.pop(
            "colormap",
            [
                "#08306b",
                "#08519c",
                "#2171b5",
                "#4292c6",
                "#6baed6",
                "#9ecae1",
                "#c6dbef",
                "#deebf7",
                "#fee8c8",
                "#fdbb84",
                "#fc8d59",
                "#ef6548",
                "#d7301f",
                "#b30000",
                "#7f0000",
            ],
        )
        self.x_label = kwargs.pop("x_label", "X")
        self.y_label = kwargs.pop("y_label", "Y")
        self.show_contour_lines = kwargs.pop("show_contour_lines", True)
        super().__init__(*args, **kwargs)

    def _interpolate_color(self, value, min_val, max_val):
        """Interpolate color for smooth gradient."""
        if max_val == min_val:
            return self.colormap[len(self.colormap) // 2]

        normalized = (value - min_val) / (max_val - min_val)
        normalized = max(0, min(1, normalized))

        pos = normalized * (len(self.colormap) - 1)
        idx1 = int(pos)
        idx2 = min(idx1 + 1, len(self.colormap) - 1)
        frac = pos - idx1

        c1 = self.colormap[idx1]
        c2 = self.colormap[idx2]

        r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
        r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)

        r = int(r1 + (r2 - r1) * frac)
        g = int(g1 + (g2 - g1) * frac)
        b = int(b1 + (b2 - b1) * frac)

        return f"#{r:02x}{g:02x}{b:02x}"

    def _marching_squares_cell(self, z00, z01, z10, z11, level, x0, y0, cell_width, cell_height):
        """Get line segment for a cell using marching squares algorithm."""
        # Classify corners: 0 if below level, 1 if above
        case = 0
        if z00 >= level:
            case |= 1
        if z01 >= level:
            case |= 2
        if z11 >= level:
            case |= 4
        if z10 >= level:
            case |= 8

        # Linear interpolation helper
        def interp(v1, v2, level):
            if abs(v2 - v1) < 1e-10:
                return 0.5
            return (level - v1) / (v2 - v1)

        # Edge midpoints
        left = (x0, y0 + cell_height * interp(z00, z10, level))
        right = (x0 + cell_width, y0 + cell_height * interp(z01, z11, level))
        top = (x0 + cell_width * interp(z10, z11, level), y0 + cell_height)
        bottom = (x0 + cell_width * interp(z00, z01, level), y0)

        # Return line segments based on case
        segments = []
        if case in [1, 14]:
            segments.append((left, bottom))
        elif case in [2, 13]:
            segments.append((bottom, right))
        elif case in [3, 12]:
            segments.append((left, right))
        elif case in [4, 11]:
            segments.append((right, top))
        elif case == 5:
            segments.append((left, top))
            segments.append((bottom, right))
        elif case in [6, 9]:
            segments.append((bottom, top))
        elif case in [7, 8]:
            segments.append((left, top))
        elif case == 10:
            segments.append((left, bottom))
            segments.append((right, top))

        return segments

    def _plot(self):
        """Draw the filled contour plot."""
        if len(self.z_data) == 0:
            return

        n_rows = len(self.z_data)
        n_cols = len(self.z_data[0]) if n_rows > 0 else 0

        if n_rows < 2 or n_cols < 2:
            return

        # Find value range
        all_values = [v for row in self.z_data for v in row]
        min_val = min(all_values)
        max_val = max(all_values)

        # Get plot dimensions
        plot_width = self.view.width
        plot_height = self.view.height

        # Leave space for labels and colorbar
        margin_left = 250
        margin_right = 280
        margin_bottom = 200
        margin_top = 80

        available_width = plot_width - margin_left - margin_right
        available_height = plot_height - margin_bottom - margin_top

        # Calculate cell size
        cell_width = available_width / (n_cols - 1)
        cell_height = available_height / (n_rows - 1)

        x_offset = self.view.x(0) + margin_left
        y_offset = self.view.y(n_rows) + margin_top

        # Create group for the contour plot
        plot_node = self.nodes["plot"]
        contour_group = self.svg.node(plot_node, class_="filled-contour")

        # Calculate contour levels
        levels = np.linspace(min_val, max_val, self.n_levels + 1)

        # Draw filled regions level by level (from lowest to highest)
        for level_idx in range(len(levels) - 1):
            level_low = levels[level_idx]
            level_high = levels[level_idx + 1]
            mid_level = (level_low + level_high) / 2
            color = self._interpolate_color(mid_level, min_val, max_val)

            # Draw cells that fall within this level range
            for i in range(n_rows - 1):
                for j in range(n_cols - 1):
                    z00 = self.z_data[i][j]
                    z01 = self.z_data[i][j + 1]
                    z10 = self.z_data[i + 1][j]
                    z11 = self.z_data[i + 1][j + 1]

                    cell_min = min(z00, z01, z10, z11)
                    cell_max = max(z00, z01, z10, z11)

                    # Check if this cell overlaps with current level band
                    if cell_max < level_low or cell_min > level_high:
                        continue

                    x = x_offset + j * cell_width
                    # Flip y to have origin at bottom-left
                    y = y_offset + available_height - (i + 1) * cell_height

                    # Draw filled rectangle for this cell at this level
                    rect = self.svg.node(
                        contour_group, "rect", x=x, y=y, width=cell_width + 0.5, height=cell_height + 0.5
                    )
                    rect.set("fill", color)
                    rect.set("stroke", "none")

        # Draw contour lines on top
        if self.show_contour_lines:
            line_levels = np.linspace(min_val, max_val, 10)
            for level in line_levels[1:-1]:  # Skip first and last
                for i in range(n_rows - 1):
                    for j in range(n_cols - 1):
                        z00 = self.z_data[i][j]
                        z01 = self.z_data[i][j + 1]
                        z10 = self.z_data[i + 1][j]
                        z11 = self.z_data[i + 1][j + 1]

                        x0 = x_offset + j * cell_width
                        y0 = y_offset + available_height - (i + 1) * cell_height

                        segments = self._marching_squares_cell(
                            z00, z01, z10, z11, level, x0, y0, cell_width, cell_height
                        )

                        for seg in segments:
                            (x1, y1), (x2, y2) = seg
                            line = self.svg.node(contour_group, "line", x1=x1, y1=y1, x2=x2, y2=y2)
                            line.set("stroke", "#333333")
                            line.set("stroke-width", "1.5")
                            line.set("stroke-opacity", "0.4")

        # Draw axis frame
        frame = self.svg.node(
            contour_group, "rect", x=x_offset, y=y_offset, width=available_width, height=available_height
        )
        frame.set("fill", "none")
        frame.set("stroke", "#333333")
        frame.set("stroke-width", "2")

        # X-axis labels
        x_font_size = 36
        x_vals = self.x_data if len(self.x_data) > 0 else list(range(n_cols))
        n_x_ticks = min(7, len(x_vals))
        tick_indices = np.linspace(0, len(x_vals) - 1, n_x_ticks, dtype=int)

        for idx in tick_indices:
            x = x_offset + idx * (available_width / (n_cols - 1))
            y = y_offset + available_height + 50
            val = x_vals[idx] if idx < len(x_vals) else idx

            text_node = self.svg.node(contour_group, "text", x=x, y=y)
            text_node.set("text-anchor", "middle")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{x_font_size}px;font-family:sans-serif")
            text_node.text = f"{val:.1f}" if isinstance(val, float) else str(val)

            # Tick mark
            tick = self.svg.node(
                contour_group, "line", x1=x, y1=y_offset + available_height, x2=x, y2=y_offset + available_height + 15
            )
            tick.set("stroke", "#333333")
            tick.set("stroke-width", "2")

        # X-axis title
        x_title_node = self.svg.node(
            contour_group, "text", x=x_offset + available_width / 2, y=y_offset + available_height + 120
        )
        x_title_node.set("text-anchor", "middle")
        x_title_node.set("fill", "#333333")
        x_title_node.set("style", "font-size:44px;font-weight:bold;font-family:sans-serif")
        x_title_node.text = self.x_label

        # Y-axis labels
        y_font_size = 36
        y_vals = self.y_data if len(self.y_data) > 0 else list(range(n_rows))
        n_y_ticks = min(7, len(y_vals))
        tick_indices_y = np.linspace(0, len(y_vals) - 1, n_y_ticks, dtype=int)

        for idx in tick_indices_y:
            x = x_offset - 20
            y = y_offset + available_height - idx * (available_height / (n_rows - 1))
            val = y_vals[idx] if idx < len(y_vals) else idx

            text_node = self.svg.node(contour_group, "text", x=x, y=y + y_font_size * 0.35)
            text_node.set("text-anchor", "end")
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{y_font_size}px;font-family:sans-serif")
            text_node.text = f"{val:.1f}" if isinstance(val, float) else str(val)

            # Tick mark
            tick = self.svg.node(contour_group, "line", x1=x_offset - 15, y1=y, x2=x_offset, y2=y)
            tick.set("stroke", "#333333")
            tick.set("stroke-width", "2")

        # Y-axis title (rotated)
        y_title_x = x_offset - 160
        y_title_y = y_offset + available_height / 2
        y_title_node = self.svg.node(contour_group, "text", x=y_title_x, y=y_title_y)
        y_title_node.set("text-anchor", "middle")
        y_title_node.set("fill", "#333333")
        y_title_node.set("style", "font-size:44px;font-weight:bold;font-family:sans-serif")
        y_title_node.set("transform", f"rotate(-90, {y_title_x}, {y_title_y})")
        y_title_node.text = self.y_label

        # Draw colorbar on the right
        colorbar_width = 50
        colorbar_height = available_height * 0.85
        colorbar_x = x_offset + available_width + 60
        colorbar_y = y_offset + (available_height - colorbar_height) / 2

        # Draw gradient colorbar using multiple rectangles
        n_segments = 60
        segment_height = colorbar_height / n_segments
        for i in range(n_segments):
            seg_value = max_val - (max_val - min_val) * i / (n_segments - 1)
            seg_color = self._interpolate_color(seg_value, min_val, max_val)
            seg_y = colorbar_y + i * segment_height

            self.svg.node(
                contour_group,
                "rect",
                x=colorbar_x,
                y=seg_y,
                width=colorbar_width,
                height=segment_height + 1,
                fill=seg_color,
            )

        # Colorbar border
        self.svg.node(
            contour_group,
            "rect",
            x=colorbar_x,
            y=colorbar_y,
            width=colorbar_width,
            height=colorbar_height,
            fill="none",
            stroke="#333333",
        )

        # Colorbar labels
        cb_label_size = 32
        n_cb_labels = 5
        for i in range(n_cb_labels):
            frac = i / (n_cb_labels - 1)
            val = max_val - (max_val - min_val) * frac
            cb_y = colorbar_y + frac * colorbar_height

            text_node = self.svg.node(
                contour_group, "text", x=colorbar_x + colorbar_width + 15, y=cb_y + cb_label_size * 0.35
            )
            text_node.set("fill", "#333333")
            text_node.set("style", f"font-size:{cb_label_size}px;font-family:sans-serif")
            text_node.text = f"{val:.2f}"

        # Colorbar title
        cb_title_size = 38
        cb_title_x = colorbar_x + colorbar_width / 2
        cb_title_y = colorbar_y - 35
        text_node = self.svg.node(contour_group, "text", x=cb_title_x, y=cb_title_y)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{cb_title_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = "z"

    def _compute(self):
        """Compute the box for rendering."""
        n_rows = len(self.z_data) if self.z_data else 1
        n_cols = len(self.z_data[0]) if self.z_data and len(self.z_data) > 0 else 1
        self._box.xmin = 0
        self._box.xmax = n_cols
        self._box.ymin = 0
        self._box.ymax = n_rows


# Generate data - Mathematical function: Gaussian peaks on a 2D surface
np.random.seed(42)

# Create grid
n_points = 60
x = np.linspace(-3, 3, n_points)
y = np.linspace(-3, 3, n_points)
X, Y = np.meshgrid(x, y)

# Create interesting surface: sum of Gaussian peaks
Z = (
    1.5 * np.exp(-((X - 1) ** 2 + (Y - 1) ** 2))
    - 1.0 * np.exp(-((X + 1) ** 2 + (Y + 1) ** 2))
    + 0.8 * np.exp(-((X - 1) ** 2 + (Y + 1.5) ** 2) / 0.5)
    + 0.5 * np.exp(-((X + 1.5) ** 2 + (Y - 0.5) ** 2) / 0.8)
)

# Convert to list format for pygal
z_data = Z.tolist()
x_data = x.tolist()
y_data = y.tolist()

# Custom style for 4800x2700 landscape canvas
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

# Diverging colormap (blue-white-red) - good for showing positive/negative values
diverging_colormap = [
    "#08306b",
    "#08519c",
    "#2171b5",
    "#4292c6",
    "#6baed6",
    "#9ecae1",
    "#c6dbef",
    "#f7f7f7",
    "#fddbc7",
    "#f4a582",
    "#d6604d",
    "#b2182b",
    "#67001f",
]

# Create filled contour chart
chart = FilledContour(
    width=4800,
    height=2700,
    style=custom_style,
    title="contour-filled · pygal · pyplots.ai",
    x_data=x_data,
    y_data=y_data,
    z_data=z_data,
    n_levels=20,
    colormap=diverging_colormap,
    x_label="X Coordinate",
    y_label="Y Coordinate",
    show_contour_lines=True,
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
    <title>contour-filled - pygal</title>
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
