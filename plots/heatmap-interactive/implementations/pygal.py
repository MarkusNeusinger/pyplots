""" pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-08
"""

import numpy as np
import pygal
from pygal.style import Style


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
matrix_data = np.clip(base_engagement, 0, 100)

# Find value range
min_val = float(matrix_data.min())
max_val = float(matrix_data.max())

# Blue-to-orange colormap (colorblind-friendly) - 10 discrete colors
colormap = [
    "#08306b",  # Dark blue (0-10%)
    "#08519c",  # Blue (10-20%)
    "#2171b5",  # Medium blue (20-30%)
    "#4292c6",  # Light blue (30-40%)
    "#6baed6",  # Lighter blue (40-50%)
    "#9ecae1",  # Very light blue (50-60%)
    "#c6dbef",  # Pale blue (60-70%)
    "#fed976",  # Yellow (70-80%)
    "#fd8d3c",  # Orange (80-90%)
    "#d94701",  # Dark orange (90-100%)
]

# Custom style for pygal
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    title_font_size=48,
    label_font_size=20,
    major_label_font_size=18,
    legend_font_size=16,
    value_font_size=14,
    tooltip_font_size=18,
    opacity=1.0,
    opacity_hover=0.9,
    transition="100ms ease-in",
)

# Use pygal HorizontalStackedBar to simulate heatmap
# Each row is a bar, each segment is a stacked portion
chart = pygal.HorizontalStackedBar(
    width=4800,
    height=2700,
    title="heatmap-interactive · pygal · pyplots.ai",
    x_title="User Segment",
    y_title="Page",
    style=custom_style,
    show_legend=False,
    print_values=False,
    show_x_guides=True,
    show_y_guides=True,
    x_labels_major_every=5,
    truncate_label=-1,
    spacing=1,
    margin=50,
    margin_left=150,
    margin_right=200,
    margin_top=100,
    margin_bottom=100,
    tooltip_border_radius=8,
)

# Set x-axis labels (row labels / pages)
chart.x_labels = pages

# Add each column as a series (segment)
# Each value in the series corresponds to a row (page)
for j in range(n_cols):
    col_data = []
    for i in range(n_rows):
        value = float(matrix_data[i, j])
        # Determine color based on value
        normalized = (value - min_val) / (max_val - min_val) if max_val > min_val else 0
        color_idx = min(int(normalized * 10), 9)
        color = colormap[color_idx]

        # Create data point with value and custom styling
        col_data.append(
            {
                "value": 1,  # Fixed width for each cell
                "label": f"{pages[i]} × {segments[j]}: {value:.1f}",
                "color": color,
                "xlink": {"title": f"Engagement: {value:.1f}"},
            }
        )

    chart.add(segments[j], col_data)

# Render to SVG and PNG
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Create interactive HTML version with enhanced zoom/pan
svg_content = chart.render().decode("utf-8")

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
        .colorbar {{
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            background: white;
            padding: 15px 10px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .colorbar-title {{
            text-align: center;
            font-weight: bold;
            font-size: 14px;
            color: #333;
            margin-bottom: 10px;
        }}
        .colorbar-gradient {{
            width: 30px;
            height: 200px;
            background: linear-gradient(to top, #08306b, #08519c, #2171b5, #4292c6, #6baed6, #9ecae1, #c6dbef, #fed976, #fd8d3c, #d94701);
            border: 1px solid #ccc;
            border-radius: 4px;
            margin: 0 auto;
        }}
        .colorbar-labels {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 200px;
            font-size: 12px;
            color: #666;
            margin-left: 40px;
            position: absolute;
            top: 35px;
            right: -5px;
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
            <div class="colorbar">
                <div class="colorbar-title">Engagement<br>Score</div>
                <div class="colorbar-gradient"></div>
                <div class="colorbar-labels">
                    <span>{max_val:.0f}</span>
                    <span>{(max_val + min_val) / 2:.0f}</span>
                    <span>{min_val:.0f}</span>
                </div>
            </div>
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

        updateTransform();
    </script>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
