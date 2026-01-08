"""pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-08
"""

import cairosvg
import numpy as np


# Generate data - Website page engagement by user segment
np.random.seed(42)

n_rows = 20
n_cols = 20

# Row labels - website pages
pages = [f"Page {i + 1}" for i in range(n_rows)]

# Column labels - user segments
segments = [f"Segment {j + 1}" for j in range(n_cols)]

# Generate engagement scores with wider range (0-100) including low values
base_engagement = np.random.randint(5, 40, size=(n_rows, n_cols)).astype(float)

# Add high-engagement clusters
base_engagement[2:6, 3:8] += 50
base_engagement[10:14, 12:17] += 55
base_engagement[15:18, 1:5] += 45

# Add some hot spots (high values)
base_engagement[0, 0] = 98
base_engagement[5, 10] = 95
base_engagement[12, 5] = 92
base_engagement[18, 18] = 96

# Add some cold spots (low values near 0)
base_engagement[7, 15] = 2
base_engagement[3, 19] = 5
base_engagement[16, 10] = 3

# Clip to valid range
matrix_data = np.clip(base_engagement, 0, 100).tolist()

# Find value range
min_val = min(v for row in matrix_data for v in row)
max_val = max(v for row in matrix_data for v in row)


def interpolate_color(value, vmin, vmax, colors):
    """Interpolate color from a list of colors."""
    if vmax == vmin:
        return colors[-1]
    normalized = (value - vmin) / (vmax - vmin)
    normalized = max(0, min(1, normalized))
    pos = normalized * (len(colors) - 1)
    idx1 = int(pos)
    idx2 = min(idx1 + 1, len(colors) - 1)
    frac = pos - idx1
    c1, c2 = colors[idx1], colors[idx2]
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = int(r1 + (r2 - r1) * frac)
    g = int(g1 + (g2 - g1) * frac)
    b = int(b1 + (b2 - b1) * frac)
    return f"#{r:02x}{g:02x}{b:02x}"


# Blue-to-orange colormap (colorblind-friendly)
colormap = ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08519c", "#FFD43B", "#FF8C00"]

# Chart dimensions
width = 4800
height = 2700
margin_left = 350
margin_right = 250
margin_top = 200
margin_bottom = 250

# Calculate grid dimensions
grid_width = width - margin_left - margin_right
grid_height = height - margin_top - margin_bottom
cell_width = grid_width / n_cols
cell_height = grid_height / n_rows

# Build SVG content manually for heatmap cells
svg_cells = []
for i in range(n_rows):
    for j in range(n_cols):
        value = matrix_data[i][j]
        color = interpolate_color(value, min_val, max_val, colormap)
        x = margin_left + j * cell_width
        y = margin_top + i * cell_height
        cell_id = f"cell-{i}-{j}"
        svg_cells.append(
            f'<rect id="{cell_id}" class="heatmap-cell" '
            f'x="{x:.1f}" y="{y:.1f}" width="{cell_width:.1f}" height="{cell_height:.1f}" '
            f'fill="{color}" stroke="#ffffff" stroke-width="1" rx="2" ry="2" '
            f'data-row-label="{pages[i]}" data-col-label="{segments[j]}" data-value="{value:.1f}"/>'
        )

# Row labels (Page)
svg_row_labels = []
for i, label in enumerate(pages):
    y = margin_top + i * cell_height + cell_height / 2 + 10
    svg_row_labels.append(
        f'<text x="{margin_left - 15}" y="{y:.1f}" text-anchor="end" '
        f'fill="#333333" style="font-size:28px;font-family:sans-serif">{label}</text>'
    )

# Column labels (Segment) - rotated
svg_col_labels = []
for j, label in enumerate(segments):
    x = margin_left + j * cell_width + cell_width / 2
    y = margin_top + n_rows * cell_height + 25
    svg_col_labels.append(
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="start" '
        f'fill="#333333" style="font-size:24px;font-family:sans-serif" '
        f'transform="rotate(45 {x:.1f} {y:.1f})">{label}</text>'
    )

# Axis titles
x_axis_title_x = margin_left + grid_width / 2
x_axis_title_y = height - 40
y_axis_title_x = 50
y_axis_title_y = margin_top + grid_height / 2

svg_axis_titles = f"""
<text x="{x_axis_title_x}" y="{x_axis_title_y}" text-anchor="middle"
      fill="#333333" style="font-size:36px;font-weight:bold;font-family:sans-serif">User Segment</text>
<text x="{y_axis_title_x}" y="{y_axis_title_y}" text-anchor="middle"
      fill="#333333" style="font-size:36px;font-weight:bold;font-family:sans-serif"
      transform="rotate(-90 {y_axis_title_x} {y_axis_title_y})">Page</text>
"""

# Colorbar
cb_x = width - margin_right + 60
cb_y = margin_top + 50
cb_width = 40
cb_height = grid_height - 100
n_segments = 50

svg_colorbar = []
for i in range(n_segments):
    seg_value = min_val + (max_val - min_val) * (n_segments - 1 - i) / (n_segments - 1)
    seg_color = interpolate_color(seg_value, min_val, max_val, colormap)
    seg_y = cb_y + i * (cb_height / n_segments)
    svg_colorbar.append(
        f'<rect x="{cb_x}" y="{seg_y:.1f}" width="{cb_width}" height="{cb_height / n_segments + 1:.1f}" '
        f'fill="{seg_color}"/>'
    )

# Colorbar border and labels
svg_colorbar.append(
    f'<rect x="{cb_x}" y="{cb_y}" width="{cb_width}" height="{cb_height}" '
    f'fill="none" stroke="#333333" stroke-width="2"/>'
)
svg_colorbar.append(
    f'<text x="{cb_x + cb_width + 15}" y="{cb_y + 10}" fill="#333333" '
    f'style="font-size:28px;font-family:sans-serif">{max_val:.0f}</text>'
)
svg_colorbar.append(
    f'<text x="{cb_x + cb_width + 15}" y="{cb_y + cb_height / 2 + 10}" fill="#333333" '
    f'style="font-size:28px;font-family:sans-serif">{(min_val + max_val) / 2:.0f}</text>'
)
svg_colorbar.append(
    f'<text x="{cb_x + cb_width + 15}" y="{cb_y + cb_height + 10}" fill="#333333" '
    f'style="font-size:28px;font-family:sans-serif">{min_val:.0f}</text>'
)
# Colorbar title
svg_colorbar.append(
    f'<text x="{cb_x + cb_width / 2}" y="{cb_y - 20}" text-anchor="middle" fill="#333333" '
    f'style="font-size:32px;font-weight:bold;font-family:sans-serif">Engagement Score</text>'
)

# Crosshair lines (hidden by default)
svg_crosshair = f"""
<g id="crosshair" style="opacity:0;pointer-events:none">
    <line id="crosshair-h" x1="{margin_left}" y1="0" x2="{margin_left + grid_width}" y2="0"
          stroke="#306998" stroke-width="3" stroke-dasharray="8,4"/>
    <line id="crosshair-v" x1="0" y1="{margin_top}" x2="0" y2="{margin_top + grid_height}"
          stroke="#306998" stroke-width="3" stroke-dasharray="8,4"/>
</g>
"""

# Title
title = "heatmap-interactive · pygal · pyplots.ai"
svg_title = f"""
<text x="{width / 2}" y="80" text-anchor="middle" fill="#333333"
      style="font-size:64px;font-weight:bold;font-family:sans-serif">{title}</text>
"""

# Complete SVG
svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <rect width="100%" height="100%" fill="white"/>
  {svg_title}
  <g id="heatmap-grid">
    {"".join(svg_cells)}
  </g>
  <g id="row-labels">{"".join(svg_row_labels)}</g>
  <g id="col-labels">{"".join(svg_col_labels)}</g>
  {svg_axis_titles}
  <g id="colorbar">{"".join(svg_colorbar)}</g>
  {svg_crosshair}
</svg>
"""

# Save SVG
with open("plot.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

# Convert SVG to PNG
cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to="plot.png", scale=1)

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
            width: 100%;
            height: 100%;
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
            <button class="btn-zoom" onclick="zoomIn()">Zoom In</button>
            <button class="btn-zoom" onclick="zoomOut()">Zoom Out</button>
            <button class="btn-reset" onclick="resetView()">Reset View</button>
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
            <strong>Interactive Controls:</strong> Hover over cells to see values |
            Click and drag to pan | Use buttons or scroll wheel to zoom |
            Double-click or press Reset to return to original view
        </div>
    </div>

    <script>
        let scale = 1;
        let translateX = 0;
        let translateY = 0;
        let isDragging = false;
        let startX, startY;

        const container = document.getElementById('chart-container');
        const svg = container.querySelector('svg');
        const tooltip = document.getElementById('tooltip');
        const zoomLevelSpan = document.getElementById('zoom-level');

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

        container.addEventListener('wheel', (e) => {{
            e.preventDefault();
            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            scale = Math.max(0.5, Math.min(5, scale * delta));
            updateTransform();
        }});

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

        container.addEventListener('dblclick', resetView);

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

        updateTransform();
    </script>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
