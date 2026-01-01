"""pyplots.ai
subplot-grid-custom: Custom Subplot Grid Layout
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import tempfile
import time
from pathlib import Path

import numpy as np
import pygal
from pygal.style import Style
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
np.random.seed(42)

# Time series data for main plot (spanning 2 columns)
days = 90
base_price = 100
returns = np.random.randn(days) * 0.02
prices = base_price * np.cumprod(1 + returns)

# Volume data for bar chart
volume = np.random.uniform(1, 5, days) * 1e6

# Returns distribution for histogram
daily_returns = np.diff(prices) / prices[:-1] * 100

# Scatter data for correlation plot
x_corr = np.random.randn(25) * 10 + 50
y_corr = x_corr * 0.7 + np.random.randn(25) * 5

# Category data for bar chart
categories = ["Tech", "Health", "Finance", "Energy"]
performance = [87, 72, 95, 63]

# Custom style for pygal charts
main_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#9467BD", "#17BECF"),
    title_font_size=44,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=24,
    value_font_size=20,
    stroke_width=4,
)

detail_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#9467BD", "#17BECF"),
    title_font_size=42,
    label_font_size=28,
    major_label_font_size=22,
    legend_font_size=22,
    value_font_size=18,
    stroke_width=3,
)

# Main chart - Line chart for price trend (spans 2 columns)
main_chart = pygal.Line(
    width=2300,
    height=1100,
    style=main_style,
    title="Stock Price (90 Days)",
    x_title="Trading Day",
    y_title="Price ($)",
    show_dots=False,
    fill=True,
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=0,
    show_legend=True,
    legend_at_bottom=False,
)
main_chart.x_labels = [str(i) if i % 15 == 0 else "" for i in range(days)]
main_chart.add("Price", list(prices))

# Volume chart - Bar chart
volume_chart = pygal.Bar(
    width=1150,
    height=530,
    style=detail_style,
    title="Daily Volume",
    x_title="Day",
    y_title="Volume (M)",
    show_x_guides=False,
    show_y_guides=True,
    show_legend=True,
    legend_at_bottom=True,
    x_label_rotation=0,
)
volume_sampled = volume[::5] / 1e6  # Sample every 5th day for readability
volume_chart.x_labels = [str(i * 5) if i % 4 == 0 else "" for i in range(len(volume_sampled))]
volume_chart.add("Volume", list(volume_sampled))

# Returns histogram
hist_counts, hist_edges = np.histogram(daily_returns, bins=12)
hist_chart = pygal.Bar(
    width=1150,
    height=530,
    style=detail_style,
    title="Returns Distribution",
    x_title="Daily Return (%)",
    y_title="Frequency",
    show_x_guides=False,
    show_y_guides=True,
    show_legend=True,
    legend_at_bottom=True,
    x_label_rotation=30,
)
hist_labels = [f"{hist_edges[i]:.1f}" for i in range(len(hist_counts))]
hist_chart.x_labels = hist_labels
hist_chart.add("Returns", list(hist_counts))

# Scatter plot for sector performance
scatter_chart = pygal.XY(
    width=1150,
    height=530,
    style=detail_style,
    title="Risk vs Return",
    x_title="Volatility (%)",
    y_title="Return (%)",
    show_x_guides=True,
    show_y_guides=True,
    show_legend=True,
    legend_at_bottom=True,
    stroke=False,
    dots_size=16,
)
scatter_data = [(float(x_corr[i]), float(y_corr[i])) for i in range(len(x_corr))]
scatter_chart.add("Sectors", scatter_data)

# Category bar chart for performance
perf_chart = pygal.Bar(
    width=1150,
    height=530,
    style=detail_style,
    title="Sector Performance",
    x_title="Sector",
    y_title="Score",
    show_x_guides=False,
    show_y_guides=True,
    show_legend=False,
    x_label_rotation=0,
)
perf_chart.x_labels = categories
for i, (cat, val) in enumerate(zip(categories, performance, strict=True)):
    color = "#306998" if i % 2 == 0 else "#FFD43B"
    perf_chart.add(cat, [{"value": val, "color": color}])

# Render charts to SVG strings
main_svg = main_chart.render().decode("utf-8")
volume_svg = volume_chart.render().decode("utf-8")
hist_svg = hist_chart.render().decode("utf-8")
scatter_svg = scatter_chart.render().decode("utf-8")
perf_svg = perf_chart.render().decode("utf-8")

# Dashboard title
main_title = "subplot-grid-custom · pygal · pyplots.ai"

# Create HTML with CSS Grid layout
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 30px;
            background: #ffffff;
            font-family: Arial, sans-serif;
        }}
        .dashboard-title {{
            text-align: center;
            font-size: 56px;
            font-weight: bold;
            color: #333;
            margin-bottom: 25px;
            padding: 15px 0;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 20px;
            width: 4700px;
            height: 2350px;
        }}
        .chart-cell {{
            background: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .chart-cell svg {{
            width: 100%;
            height: 100%;
        }}
        .main-chart {{
            grid-column: 1 / 3;
            grid-row: 1 / 3;
        }}
        .cell-1 {{
            grid-column: 3;
            grid-row: 1;
        }}
        .cell-2 {{
            grid-column: 4;
            grid-row: 1;
        }}
        .cell-3 {{
            grid-column: 3;
            grid-row: 2;
        }}
        .cell-4 {{
            grid-column: 4;
            grid-row: 2;
        }}
    </style>
</head>
<body>
    <div class="dashboard-title">{main_title}</div>
    <div class="grid-container">
        <div class="chart-cell main-chart">{main_svg}</div>
        <div class="chart-cell cell-1">{volume_svg}</div>
        <div class="chart-cell cell-2">{scatter_svg}</div>
        <div class="chart-cell cell-3">{hist_svg}</div>
        <div class="chart-cell cell-4">{perf_svg}</div>
    </div>
</body>
</html>"""

# Save interactive HTML version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Write temp HTML for screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Screenshot with Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(3)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
