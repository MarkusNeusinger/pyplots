""" pyplots.ai
dashboard-synchronized-crosshair: Synchronized Multi-Chart Dashboard
Library: pygal 3.1.0 | Python 3.13.11
Quality: 55/100 | Created: 2026-01-20
"""

import io

import numpy as np
import pygal
from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style


# Data - 200 trading days of stock data with price, volume, and RSI
np.random.seed(42)
n_days = 200

dates = [f"Day {i + 1}" for i in range(n_days)]

# Price series (random walk starting at 100)
returns = np.random.randn(n_days) * 0.02
price = 100 * np.cumprod(1 + returns)

# Volume series (correlated with price changes)
volume = np.abs(np.random.randn(n_days)) * 1000000 + 500000
volume = volume * (1 + np.abs(returns) * 10)  # Higher volume on bigger moves

# RSI-like indicator (bounded 0-100)
rsi = 50 + np.cumsum(np.random.randn(n_days) * 2)
rsi = np.clip(rsi, 0, 100)

# Style for Price chart (top)
price_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=32,
    value_font_size=24,
    stroke_width=4,
    font_family="sans-serif",
)

# Style for Volume chart (middle)
volume_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#FFD43B",),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=32,
    value_font_size=24,
    stroke_width=2,
    font_family="sans-serif",
)

# Style for RSI chart (bottom)
rsi_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#E74C3C",),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=32,
    value_font_size=24,
    stroke_width=4,
    font_family="sans-serif",
)

# Chart 1: Price Line Chart (top panel)
price_chart = pygal.Line(
    width=4800,
    height=850,
    style=price_style,
    title="Price ($)",
    x_title="",
    y_title="Price ($)",
    show_x_labels=False,
    show_legend=True,
    legend_at_bottom=False,
    show_y_guides=True,
    show_x_guides=True,
    dots_size=0,
    stroke_style={"width": 4},
    fill=False,
    truncate_label=-1,
    margin_bottom=5,
)
price_chart.add("Stock Price", price.tolist())
price_chart.x_labels = dates

# Chart 2: Volume Bar Chart (middle panel)
volume_chart = pygal.Line(
    width=4800,
    height=750,
    style=volume_style,
    title="Volume (Millions)",
    x_title="",
    y_title="Volume (M)",
    show_x_labels=False,
    show_legend=True,
    legend_at_bottom=False,
    show_y_guides=True,
    show_x_guides=True,
    dots_size=0,
    stroke_style={"width": 3},
    fill=True,
    truncate_label=-1,
    margin_top=5,
    margin_bottom=5,
)
volume_chart.add("Trading Volume", (volume / 1000000).tolist())
volume_chart.x_labels = dates

# Chart 3: RSI Indicator (bottom panel)
rsi_chart = pygal.Line(
    width=4800,
    height=850,
    style=rsi_style,
    title="RSI Indicator (0-100)",
    x_title="Trading Day",
    y_title="RSI",
    show_x_labels=True,
    show_legend=True,
    legend_at_bottom=False,
    show_y_guides=True,
    show_x_guides=True,
    dots_size=0,
    stroke_style={"width": 4},
    fill=False,
    x_labels_major_count=12,
    show_minor_x_labels=False,
    truncate_label=-1,
    x_label_rotation=45,
    range=(0, 100),
    margin_top=5,
)
rsi_chart.add("RSI", rsi.tolist())
rsi_chart.x_labels = dates

# Create combined HTML dashboard with synchronized crosshair via JavaScript
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>dashboard-synchronized-crosshair · pygal · pyplots.ai</title>
    <style>
        body {{
            font-family: sans-serif;
            background: white;
            margin: 0;
            padding: 20px;
        }}
        .dashboard-title {{
            text-align: center;
            font-size: 36px;
            color: #333;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        .chart-container {{
            width: 100%;
            max-width: 4800px;
            margin: 0 auto;
            position: relative;
        }}
        .chart {{
            width: 100%;
            display: block;
        }}
        .crosshair {{
            position: absolute;
            width: 2px;
            background: #306998;
            pointer-events: none;
            display: none;
            z-index: 1000;
        }}
        #crosshair1 {{ height: 320px; top: 60px; }}
        #crosshair2 {{ height: 250px; top: 400px; }}
        #crosshair3 {{ height: 250px; top: 670px; }}
        .tooltip {{
            position: fixed;
            background: rgba(48, 105, 152, 0.95);
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-size: 14px;
            pointer-events: none;
            display: none;
            z-index: 1001;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
    </style>
</head>
<body>
    <div class="dashboard-title">dashboard-synchronized-crosshair · pygal · pyplots.ai</div>
    <div class="chart-container" id="dashboard">
        <div class="crosshair" id="crosshair1"></div>
        <div class="crosshair" id="crosshair2"></div>
        <div class="crosshair" id="crosshair3"></div>
        <div class="chart" id="chart1">{price_chart.render(is_unicode=True)}</div>
        <div class="chart" id="chart2">{volume_chart.render(is_unicode=True)}</div>
        <div class="chart" id="chart3">{rsi_chart.render(is_unicode=True)}</div>
    </div>
    <div class="tooltip" id="tooltip"></div>
    <script>
        const priceData = {price.tolist()};
        const volumeData = {(volume / 1000000).tolist()};
        const rsiData = {rsi.tolist()};
        const n = {n_days};

        const dashboard = document.getElementById('dashboard');
        const crosshairs = [
            document.getElementById('crosshair1'),
            document.getElementById('crosshair2'),
            document.getElementById('crosshair3')
        ];
        const tooltip = document.getElementById('tooltip');

        dashboard.addEventListener('mousemove', function(e) {{
            const rect = dashboard.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const chartWidth = rect.width;

            // Calculate data index based on x position (approximate chart area)
            const leftMargin = chartWidth * 0.08;
            const rightMargin = chartWidth * 0.05;
            const plotWidth = chartWidth - leftMargin - rightMargin;

            if (x >= leftMargin && x <= chartWidth - rightMargin) {{
                const relX = x - leftMargin;
                const idx = Math.min(Math.floor((relX / plotWidth) * n), n - 1);

                // Show crosshairs
                crosshairs.forEach(ch => {{
                    ch.style.left = x + 'px';
                    ch.style.display = 'block';
                }});

                // Update tooltip
                tooltip.innerHTML = `
                    <strong>Day ${{idx + 1}}</strong><br>
                    <span style="color: #89CFF0;">Price:</span> $${{priceData[idx].toFixed(2)}}<br>
                    <span style="color: #FFD43B;">Volume:</span> ${{volumeData[idx].toFixed(2)}}M<br>
                    <span style="color: #FF6B6B;">RSI:</span> ${{rsiData[idx].toFixed(1)}}
                `;
                tooltip.style.left = (e.clientX + 15) + 'px';
                tooltip.style.top = (e.clientY + 15) + 'px';
                tooltip.style.display = 'block';
            }}
        }});

        dashboard.addEventListener('mouseleave', function() {{
            crosshairs.forEach(ch => ch.style.display = 'none');
            tooltip.style.display = 'none';
        }});
    </script>
</body>
</html>"""

# Save HTML (primary interactive output)
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Save PNG for static preview - stacked multi-chart dashboard layout
# Render each chart to PNG bytes and combine vertically using PIL

# Render price chart to PNG bytes
price_png = price_chart.render_to_png()
price_img = Image.open(io.BytesIO(price_png))

# Render volume chart to PNG bytes
volume_png = volume_chart.render_to_png()
volume_img = Image.open(io.BytesIO(volume_png))

# Render RSI chart to PNG bytes
rsi_png = rsi_chart.render_to_png()
rsi_img = Image.open(io.BytesIO(rsi_png))

# Create title banner
title_height = 150
title_img = Image.new("RGB", (4800, title_height), "white")
draw = ImageDraw.Draw(title_img)
title_text = "dashboard-synchronized-crosshair · pygal · pyplots.ai"
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
except OSError:
    font = ImageFont.load_default()
bbox = draw.textbbox((0, 0), title_text, font=font)
text_width = bbox[2] - bbox[0]
text_x = (4800 - text_width) // 2
draw.text((text_x, 40), title_text, fill="#333333", font=font)

# Add crosshair annotation
annotation_text = "← Synchronized Crosshair (interactive in HTML)"
try:
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
except OSError:
    small_font = ImageFont.load_default()
draw.text((4800 - 900, 100), annotation_text, fill="#306998", font=small_font)

# Calculate total height
total_height = title_height + price_img.height + volume_img.height + rsi_img.height

# Create combined image
combined = Image.new("RGB", (4800, total_height), "white")
y_offset = 0

# Paste title
combined.paste(title_img, (0, y_offset))
y_offset += title_height

# Paste charts vertically
combined.paste(price_img, (0, y_offset))
y_offset += price_img.height

combined.paste(volume_img, (0, y_offset))
y_offset += volume_img.height

combined.paste(rsi_img, (0, y_offset))

# Draw vertical crosshair line across all charts to demonstrate the concept
crosshair_draw = ImageDraw.Draw(combined)
crosshair_x = 2400  # Middle of chart
crosshair_y_start = title_height + 100
crosshair_y_end = total_height - 200
crosshair_draw.line([(crosshair_x, crosshair_y_start), (crosshair_x, crosshair_y_end)], fill="#306998", width=4)

# Add small circles at crosshair intersection points
circle_radius = 12
chart_positions = [
    title_height + 400,  # Price chart middle
    title_height + price_img.height + 350,  # Volume chart middle
    title_height + price_img.height + volume_img.height + 400,  # RSI chart middle
]
for y_pos in chart_positions:
    crosshair_draw.ellipse(
        [crosshair_x - circle_radius, y_pos - circle_radius, crosshair_x + circle_radius, y_pos + circle_radius],
        fill="#306998",
        outline="#306998",
    )

# Save combined PNG
combined.save("plot.png", dpi=(300, 300))
