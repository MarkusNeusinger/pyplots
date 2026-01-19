"""pyplots.ai
chart-export-menu: Chart with Built-in Export Menu
Library: pygal 3.1.0 | Python 3.13.11
Quality: 75/100 | Created: 2026-01-19
"""

import pygal
from pygal.style import Style


# Data - monthly sales data over a year (deterministic)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
product_a = [45, 52, 48, 61, 75, 82, 95, 88, 72, 65, 58, 70]
product_b = [30, 35, 42, 55, 63, 70, 78, 85, 68, 55, 48, 52]
product_c = [25, 28, 35, 40, 45, 52, 58, 62, 55, 48, 42, 38]

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4B8BBE"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=48,
    value_font_size=36,
    stroke_width=4,
    font_family="Arial, sans-serif",
)

# Create line chart
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="chart-export-menu · pygal · pyplots.ai",
    x_title="Month",
    y_title="Sales (thousands)",
    show_x_guides=True,
    show_y_guides=True,
    show_dots=True,
    dots_size=10,
    stroke_style={"width": 4, "linecap": "round", "linejoin": "round"},
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=36,
    margin=100,
    margin_top=200,
    show_legend=True,
    disable_xml_declaration=True,
    explicit_size=True,
    truncate_legend=-1,
    truncate_label=-1,
)

# Set x-axis labels
chart.x_labels = months

# Add data series
chart.add("Product A", product_a)
chart.add("Product B", product_b)
chart.add("Product C", product_c)

# Get SVG content for embedding
svg_data = chart.render()
svg_content = svg_data.decode("utf-8") if isinstance(svg_data, bytes) else svg_data

# Create HTML with export menu button in top-right corner
html_template = (
    """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>chart-export-menu · pygal · pyplots.ai</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: white; }
        .chart-container {
            position: relative;
            width: 100%;
            max-width: 4800px;
            margin: 0 auto;
        }
        .chart-container svg {
            width: 100%;
            height: auto;
        }
        .export-menu {
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }
        .export-btn {
            background: #306998;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 16px;
            cursor: pointer;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            transition: background 0.2s;
        }
        .export-btn:hover {
            background: #1e4f6f;
        }
        .export-btn svg {
            width: 24px;
            height: 24px;
            fill: currentColor;
        }
        .dropdown {
            display: none;
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 8px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
            min-width: 180px;
            overflow: hidden;
        }
        .dropdown.show { display: block; }
        .dropdown-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 18px;
            cursor: pointer;
            color: #333;
            text-decoration: none;
            font-size: 16px;
            border-bottom: 1px solid #eee;
            transition: background 0.15s;
        }
        .dropdown-item:last-child { border-bottom: none; }
        .dropdown-item:hover { background: #f5f5f5; }
        .dropdown-item svg {
            width: 20px;
            height: 20px;
            fill: #666;
        }
    </style>
</head>
<body>
    <div class="chart-container">
        <div class="export-menu">
            <button class="export-btn" onclick="toggleDropdown()">
                <svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
                Export
            </button>
            <div class="dropdown" id="exportDropdown">
                <a class="dropdown-item" onclick="exportPNG()">
                    <svg viewBox="0 0 24 24"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg>
                    Download PNG
                </a>
                <a class="dropdown-item" onclick="exportSVG()">
                    <svg viewBox="0 0 24 24"><path d="M14.59 2.59c-.38-.38-.89-.59-1.42-.59H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8.83c0-.53-.21-1.04-.59-1.41l-4.82-4.83zM15 18H9c-.55 0-1-.45-1-1s.45-1 1-1h6c.55 0 1 .45 1 1s-.45 1-1 1zm0-4H9c-.55 0-1-.45-1-1s.45-1 1-1h6c.55 0 1 .45 1 1s-.45 1-1 1zm-2-6V3.5L18.5 9H14c-.55 0-1-.45-1-1z"/></svg>
                    Download SVG
                </a>
                <a class="dropdown-item" onclick="exportCSV()">
                    <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm2 14H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
                    Download CSV
                </a>
            </div>
        </div>
        """
    + svg_content
    + """
    </div>
    <script>
        function toggleDropdown() {
            document.getElementById('exportDropdown').classList.toggle('show');
        }
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.export-menu')) {
                document.getElementById('exportDropdown').classList.remove('show');
            }
        });
        function exportSVG() {
            const svg = document.querySelector('.chart-container svg');
            const svgData = new XMLSerializer().serializeToString(svg);
            const blob = new Blob([svgData], {type: 'image/svg+xml'});
            downloadBlob(blob, 'chart-export-menu.svg');
        }
        function exportPNG() {
            const svg = document.querySelector('.chart-container svg');
            const canvas = document.createElement('canvas');
            canvas.width = 4800;
            canvas.height = 2700;
            const ctx = canvas.getContext('2d');
            const img = new Image();
            const svgData = new XMLSerializer().serializeToString(svg);
            const svgBlob = new Blob([svgData], {type: 'image/svg+xml;charset=utf-8'});
            const url = URL.createObjectURL(svgBlob);
            img.onload = function() {
                ctx.fillStyle = 'white';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0, 4800, 2700);
                URL.revokeObjectURL(url);
                canvas.toBlob(function(blob) {
                    downloadBlob(blob, 'chart-export-menu.png');
                }, 'image/png');
            };
            img.src = url;
        }
        function exportCSV() {
            const data = [
                ['Month', 'Product A', 'Product B', 'Product C'],
                ['Jan', 45, 30, 25], ['Feb', 52, 35, 28], ['Mar', 48, 42, 35],
                ['Apr', 61, 55, 40], ['May', 75, 63, 45], ['Jun', 82, 70, 52],
                ['Jul', 95, 78, 58], ['Aug', 88, 85, 62], ['Sep', 72, 68, 55],
                ['Oct', 65, 55, 48], ['Nov', 58, 48, 42], ['Dec', 70, 52, 38]
            ];
            const csv = data.map(row => row.join(',')).join('\\n');
            const blob = new Blob([csv], {type: 'text/csv'});
            downloadBlob(blob, 'chart-export-menu.csv');
        }
        function downloadBlob(blob, filename) {
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            link.click();
            URL.revokeObjectURL(link.href);
        }
    </script>
</body>
</html>"""
)

# Save interactive HTML with export menu
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_template)

# Save PNG for static preview
chart.render_to_png("plot.png")
