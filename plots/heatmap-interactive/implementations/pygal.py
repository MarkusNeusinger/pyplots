""" pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-08
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


class InteractiveHeatmap(Graph):
    """Custom Interactive Heatmap for pygal with hover tooltips and zoom support."""

    def __init__(self, *args, **kwargs):
        self.matrix_data = kwargs.pop("matrix_data", [])
        self.row_labels = kwargs.pop("row_labels", [])
        self.col_labels = kwargs.pop("col_labels", [])
        self.colormap = kwargs.pop("colormap", ["#f7fbff", "#6baed6", "#2171b5", "#08306b"])
        self.cell_ids = []  # Store cell IDs for JavaScript interactivity
        super().__init__(*args, **kwargs)

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
        """Draw the interactive matrix heatmap."""
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
        label_margin_left = 200
        label_margin_bottom = 180
        label_margin_top = 50
        label_margin_right = 200

        available_width = plot_width - label_margin_left - label_margin_right
        available_height = plot_height - label_margin_bottom - label_margin_top

        cell_width = available_width / n_cols * 0.98
        cell_height = available_height / n_rows * 0.98
        gap = min(cell_width, cell_height) * 0.02

        # Calculate offsets to center the grid
        grid_width = n_cols * (cell_width + gap) - gap
        grid_height = n_rows * (cell_height + gap) - gap

        x_offset = self.view.x(0) + label_margin_left + (available_width - grid_width) / 2
        y_offset = self.view.y(n_rows) + label_margin_top + (available_height - grid_height) / 2

        # Create group for the heatmap
        plot_node = self.nodes["plot"]
        heatmap_group = self.svg.node(plot_node, class_="interactive-heatmap", id="heatmap-grid")

        # Draw cells with data attributes for interactivity
        for i in range(n_rows):
            for j in range(n_cols):
                value = self.matrix_data[i][j]
                color = self._interpolate_color(value, min_val, max_val)

                x = x_offset + j * (cell_width + gap)
                y = y_offset + i * (cell_height + gap)

                cell_id = f"cell-{i}-{j}"

                # Draw cell rectangle with data attributes
                rect = self.svg.node(
                    heatmap_group, "rect", x=x, y=y, width=cell_width, height=cell_height, rx=2, ry=2, id=cell_id
                )
                rect.set("fill", color)
                rect.set("stroke", "#ffffff")
                rect.set("stroke-width", "1")
                rect.set("class", "heatmap-cell")
                rect.set("data-row", str(i))
                rect.set("data-col", str(j))
                rect.set("data-row-label", self.row_labels[i])
                rect.set("data-col-label", self.col_labels[j])
                rect.set("data-value", f"{value:.1f}")

        # Draw row labels on the left
        row_font_size = min(28, int(cell_height * 0.8))
        for i, label in enumerate(self.row_labels):
            y = y_offset + i * (cell_height + gap) + cell_height / 2
            text_node = self.svg.node(
                heatmap_group, "text", x=x_offset - 15, y=y + row_font_size * 0.35, id=f"row-label-{i}"
            )
            text_node.set("text-anchor", "end")
            text_node.set("fill", "#333333")
            text_node.set("class", "row-label")
            text_node.set("style", f"font-size:{row_font_size}px;font-weight:normal;font-family:sans-serif")
            text_node.text = label

        # Draw column labels at the bottom (rotated for larger matrices)
        col_font_size = min(28, int(cell_width * 0.8))
        for j, label in enumerate(self.col_labels):
            x = x_offset + j * (cell_width + gap) + cell_width / 2
            y = y_offset + n_rows * (cell_height + gap) + 20
            text_node = self.svg.node(heatmap_group, "text", x=x, y=y, id=f"col-label-{j}")
            text_node.set("text-anchor", "start")
            text_node.set("fill", "#333333")
            text_node.set("class", "col-label")
            text_node.set("style", f"font-size:{col_font_size}px;font-weight:normal;font-family:sans-serif")
            text_node.set("transform", f"rotate(45 {x} {y})")
            text_node.text = label

        # Draw colorbar on the right
        colorbar_width = 40
        colorbar_height = grid_height * 0.8
        colorbar_x = x_offset + grid_width + 60
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
        cb_label_size = 28
        # Max value
        text_node = self.svg.node(
            heatmap_group, "text", x=colorbar_x + colorbar_width + 15, y=colorbar_y + cb_label_size * 0.35
        )
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{cb_label_size}px;font-family:sans-serif")
        text_node.text = f"{max_val:.0f}"

        # Mid value
        mid_y = colorbar_y + colorbar_height / 2
        text_node = self.svg.node(
            heatmap_group, "text", x=colorbar_x + colorbar_width + 15, y=mid_y + cb_label_size * 0.35
        )
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{cb_label_size}px;font-family:sans-serif")
        text_node.text = f"{(min_val + max_val) / 2:.0f}"

        # Min value
        text_node = self.svg.node(
            heatmap_group,
            "text",
            x=colorbar_x + colorbar_width + 15,
            y=colorbar_y + colorbar_height + cb_label_size * 0.35,
        )
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{cb_label_size}px;font-family:sans-serif")
        text_node.text = f"{min_val:.0f}"

        # Colorbar title
        cb_title_size = 32
        cb_title_x = colorbar_x + colorbar_width / 2
        cb_title_y = colorbar_y - 30
        text_node = self.svg.node(heatmap_group, "text", x=cb_title_x, y=cb_title_y)
        text_node.set("text-anchor", "middle")
        text_node.set("fill", "#333333")
        text_node.set("style", f"font-size:{cb_title_size}px;font-weight:bold;font-family:sans-serif")
        text_node.text = "Value"

        # Create crosshair lines (hidden by default)
        crosshair_group = self.svg.node(plot_node, class_="crosshair", id="crosshair")
        crosshair_group.set("style", "opacity:0;pointer-events:none")

        # Horizontal crosshair line
        h_line = self.svg.node(
            crosshair_group, "line", x1=x_offset, y1=0, x2=x_offset + grid_width, y2=0, id="crosshair-h"
        )
        h_line.set("stroke", "#306998")
        h_line.set("stroke-width", "3")
        h_line.set("stroke-dasharray", "8,4")

        # Vertical crosshair line
        v_line = self.svg.node(
            crosshair_group, "line", x1=0, y1=y_offset, x2=0, y2=y_offset + grid_height, id="crosshair-v"
        )
        v_line.set("stroke", "#306998")
        v_line.set("stroke-width", "3")
        v_line.set("stroke-dasharray", "8,4")

    def _compute(self):
        """Compute the box for rendering."""
        n_rows = len(self.matrix_data) if self.matrix_data else 1
        n_cols = len(self.matrix_data[0]) if self.matrix_data and len(self.matrix_data) > 0 else 1
        self._box.xmin = 0
        self._box.xmax = n_cols
        self._box.ymin = 0
        self._box.ymax = n_rows


# Generate data - Website interaction matrix (pages x user segments)
np.random.seed(42)

# 20x20 matrix for interactive exploration (spec suggests 10-100)
n_rows = 20
n_cols = 20

# Row labels - website pages
pages = [f"Page {i + 1}" for i in range(n_rows)]

# Column labels - user segments
segments = [f"Seg {j + 1}" for j in range(n_cols)]

# Generate engagement scores (0-100) with some patterns
# Some pages are popular with certain segments, creating clusters
base_engagement = np.random.randint(20, 50, size=(n_rows, n_cols)).astype(float)

# Add high-engagement clusters
base_engagement[2:6, 3:8] += 35  # Cluster 1
base_engagement[10:14, 12:17] += 40  # Cluster 2
base_engagement[15:18, 1:5] += 30  # Cluster 3

# Add some hot spots
base_engagement[0, 0] = 95
base_engagement[5, 10] = 92
base_engagement[12, 5] = 88
base_engagement[18, 18] = 90

# Clip to valid range
matrix_data = np.clip(base_engagement, 0, 100).tolist()

# Custom style for 4800x2700 landscape canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=64,
    legend_font_size=40,
    label_font_size=36,
    value_font_size=28,
    font_family="sans-serif",
)

# Blue-to-orange colormap (Python colors, colorblind-safe)
colormap = ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08519c", "#FFD43B", "#FF8C00"]

# Create heatmap
chart = InteractiveHeatmap(
    width=4800,
    height=2700,
    style=custom_style,
    title="heatmap-interactive · pygal · pyplots.ai",
    matrix_data=matrix_data,
    row_labels=pages,
    col_labels=segments,
    colormap=colormap,
    show_legend=False,
    margin=100,
    margin_top=180,
    margin_bottom=80,
    show_x_labels=False,
    show_y_labels=False,
)

# Add a dummy series to trigger _plot (pygal requires at least one series)
chart.add("", [0])

# Get the SVG content
svg_content = chart.render(is_unicode=True)

# Save PNG for static preview
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Create interactive HTML with zoom, pan, and hover tooltips
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>heatmap-interactive - pygal - pyplots.ai</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}
        .controls {{
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}
        .controls button {{
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 500;
        }}
        .controls button:hover {{
            transform: translateY(-1px);
        }}
        .btn-zoom {{
            background: #306998;
            color: white;
        }}
        .btn-zoom:hover {{
            background: #245a7a;
        }}
        .btn-reset {{
            background: #FFD43B;
            color: #333;
        }}
        .btn-reset:hover {{
            background: #f0c420;
        }}
        .zoom-info {{
            margin-left: auto;
            color: #666;
            font-size: 14px;
        }}
        .chart-wrapper {{
            position: relative;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .chart-container {{
            width: 100%;
            height: 80vh;
            overflow: hidden;
            cursor: grab;
        }}
        .chart-container:active {{
            cursor: grabbing;
        }}
        .chart-container svg {{
            display: block;
            transform-origin: 0 0;
            transition: transform 0.1s ease-out;
        }}
        .tooltip {{
            position: fixed;
            background: rgba(48, 105, 152, 0.95);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            pointer-events: none;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            opacity: 0;
            transition: opacity 0.15s;
            max-width: 250px;
        }}
        .tooltip.visible {{
            opacity: 1;
        }}
        .tooltip-title {{
            font-weight: bold;
            margin-bottom: 6px;
            font-size: 15px;
        }}
        .tooltip-value {{
            font-size: 24px;
            font-weight: bold;
            color: #FFD43B;
        }}
        .tooltip-coords {{
            color: rgba(255,255,255,0.8);
            font-size: 13px;
            margin-top: 4px;
        }}
        .heatmap-cell {{
            transition: stroke-width 0.1s, stroke 0.1s;
        }}
        .heatmap-cell:hover {{
            stroke: #306998 !important;
            stroke-width: 4 !important;
        }}
        .instructions {{
            margin-top: 15px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            font-size: 14px;
            color: #666;
        }}
        .instructions strong {{
            color: #306998;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="controls">
            <button class="btn-zoom" onclick="zoomIn()">🔍 Zoom In</button>
            <button class="btn-zoom" onclick="zoomOut()">🔍 Zoom Out</button>
            <button class="btn-reset" onclick="resetView()">↺ Reset View</button>
            <span class="zoom-info">Zoom: <span id="zoom-level">100%</span></span>
        </div>
        <div class="chart-wrapper">
            <div class="chart-container" id="chart-container">
                {svg_content}
            </div>
        </div>
        <div class="tooltip" id="tooltip">
            <div class="tooltip-title" id="tooltip-title"></div>
            <div class="tooltip-value" id="tooltip-value"></div>
            <div class="tooltip-coords" id="tooltip-coords"></div>
        </div>
        <div class="instructions">
            <strong>Interactive Controls:</strong> Hover over cells to see values •
            Click and drag to pan • Use buttons or scroll wheel to zoom •
            Double-click or press Reset to return to original view
        </div>
    </div>

    <script>
        // Zoom and pan state
        let scale = 1;
        let translateX = 0;
        let translateY = 0;
        let isDragging = false;
        let startX, startY;

        const container = document.getElementById('chart-container');
        const svg = container.querySelector('svg');
        const tooltip = document.getElementById('tooltip');
        const zoomLevelSpan = document.getElementById('zoom-level');

        // Set SVG to fill container
        svg.style.width = '100%';
        svg.style.height = '100%';

        function updateTransform() {{
            svg.style.transform = `translate(${{translateX}}px, ${{translateY}}px) scale(${{scale}})`;
            zoomLevelSpan.textContent = Math.round(scale * 100) + '%';
        }}

        function zoomIn() {{
            scale = Math.min(scale * 1.3, 5);
            updateTransform();
        }}

        function zoomOut() {{
            scale = Math.max(scale / 1.3, 0.5);
            updateTransform();
        }}

        function resetView() {{
            scale = 1;
            translateX = 0;
            translateY = 0;
            updateTransform();
        }}

        // Mouse wheel zoom
        container.addEventListener('wheel', (e) => {{
            e.preventDefault();
            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            scale = Math.max(0.5, Math.min(5, scale * delta));
            updateTransform();
        }});

        // Pan with mouse drag
        container.addEventListener('mousedown', (e) => {{
            isDragging = true;
            startX = e.clientX - translateX;
            startY = e.clientY - translateY;
            container.style.cursor = 'grabbing';
        }});

        document.addEventListener('mousemove', (e) => {{
            if (isDragging) {{
                translateX = e.clientX - startX;
                translateY = e.clientY - startY;
                updateTransform();
            }}
        }});

        document.addEventListener('mouseup', () => {{
            isDragging = false;
            container.style.cursor = 'grab';
        }});

        // Double-click to reset
        container.addEventListener('dblclick', resetView);

        // Tooltip handling for heatmap cells
        const cells = document.querySelectorAll('.heatmap-cell');
        const crosshair = document.getElementById('crosshair');

        cells.forEach(cell => {{
            cell.addEventListener('mouseenter', (e) => {{
                const row = cell.getAttribute('data-row-label');
                const col = cell.getAttribute('data-col-label');
                const value = cell.getAttribute('data-value');

                document.getElementById('tooltip-title').textContent = `${{row}} × ${{col}}`;
                document.getElementById('tooltip-value').textContent = value;
                document.getElementById('tooltip-coords').textContent = `Row: ${{row}} | Column: ${{col}}`;

                tooltip.classList.add('visible');

                // Show crosshair
                if (crosshair) {{
                    crosshair.style.opacity = '0.6';
                    const rect = cell.getBBox();
                    const hLine = document.getElementById('crosshair-h');
                    const vLine = document.getElementById('crosshair-v');
                    if (hLine && vLine) {{
                        hLine.setAttribute('y1', rect.y + rect.height / 2);
                        hLine.setAttribute('y2', rect.y + rect.height / 2);
                        vLine.setAttribute('x1', rect.x + rect.width / 2);
                        vLine.setAttribute('x2', rect.x + rect.width / 2);
                    }}
                }}
            }});

            cell.addEventListener('mousemove', (e) => {{
                tooltip.style.left = (e.clientX + 15) + 'px';
                tooltip.style.top = (e.clientY + 15) + 'px';
            }});

            cell.addEventListener('mouseleave', () => {{
                tooltip.classList.remove('visible');
                if (crosshair) {{
                    crosshair.style.opacity = '0';
                }}
            }});
        }});

        // Initial setup
        updateTransform();
    </script>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
