"""pyplots.ai
dashboard-synchronized-crosshair: Synchronized Multi-Chart Dashboard
Library: pygal | Python 3.13
Quality: pending | Created: 2025-01-20
"""

import numpy as np
import pygal
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

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#E74C3C"),
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=28,
    value_font_size=20,
    stroke_width=3,
    font_family="sans-serif",
)

# Chart 1: Price Line Chart
price_chart = pygal.Line(
    width=4800,
    height=900,
    style=custom_style,
    title="Price",
    x_title="",
    y_title="Price ($)",
    show_x_labels=False,
    show_legend=True,
    legend_at_bottom=False,
    show_y_guides=True,
    show_x_guides=False,
    dots_size=0,
    stroke_style={"width": 3},
    fill=False,
    truncate_label=-1,
    x_label_rotation=0,
)
price_chart.add("Price", price.tolist())
price_chart.x_labels = dates

# Chart 2: Volume Bar Chart
volume_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#FFD43B",),
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=28,
    value_font_size=20,
    stroke_width=1,
    font_family="sans-serif",
)

volume_chart = pygal.Bar(
    width=4800,
    height=700,
    style=volume_style,
    title="Volume",
    x_title="",
    y_title="Volume",
    show_x_labels=False,
    show_legend=True,
    legend_at_bottom=False,
    show_y_guides=True,
    show_x_guides=False,
    truncate_label=-1,
)
volume_chart.add("Volume", (volume / 1000000).tolist())  # In millions

# Chart 3: RSI Indicator
rsi_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#E74C3C",),
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=28,
    value_font_size=20,
    stroke_width=3,
    font_family="sans-serif",
)

rsi_chart = pygal.Line(
    width=4800,
    height=700,
    style=rsi_style,
    title="RSI Indicator",
    x_title="Trading Day",
    y_title="RSI",
    show_x_labels=True,
    show_legend=True,
    legend_at_bottom=False,
    show_y_guides=True,
    show_x_guides=False,
    dots_size=0,
    stroke_style={"width": 3},
    fill=False,
    x_labels_major_count=10,
    show_minor_x_labels=False,
    truncate_label=-1,
    x_label_rotation=45,
    range=(0, 100),
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

# Save PNG for static preview
# Create a combined chart view for PNG
preview_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#E74C3C"),
    title_font_size=72,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=36,
    value_font_size=28,
    stroke_width=4,
    font_family="sans-serif",
)

# For PNG, create a single chart showing all three series normalized
preview_chart = pygal.Line(
    width=4800,
    height=2700,
    style=preview_style,
    title="dashboard-synchronized-crosshair · pygal · pyplots.ai",
    x_title="Trading Day",
    y_title="Normalized Value",
    show_x_labels=True,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    show_y_guides=True,
    show_x_guides=False,
    dots_size=0,
    stroke_style={"width": 4},
    fill=False,
    x_labels_major_count=10,
    show_minor_x_labels=False,
    truncate_label=-1,
    x_label_rotation=45,
    secondary_range=(0, 100),
)

# Normalize data for combined view
price_norm = (price - price.min()) / (price.max() - price.min()) * 100
volume_norm = (volume - volume.min()) / (volume.max() - volume.min()) * 100

preview_chart.add("Price (normalized)", price_norm.tolist())
preview_chart.add("Volume (normalized)", volume_norm.tolist())
preview_chart.add("RSI", rsi.tolist(), secondary=True)
preview_chart.x_labels = dates

preview_chart.render_to_png("plot.png")
