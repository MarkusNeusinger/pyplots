"""pyplots.ai
subplot-grid-custom: Custom Subplot Grid Layout
Library: pygal 3.1.0 | Python 3.13.11
Quality: 88/100 | Created: 2026-01-01
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

sidebar_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#9467BD", "#17BECF"),
    title_font_size=40,
    label_font_size=24,
    major_label_font_size=20,
    legend_font_size=20,
    value_font_size=16,
    stroke_width=3,
)

# Main chart - Line chart for price trend (spans 2 columns, row 1 only now)
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
    show_legend=False,
    truncate_label=-1,
)
# Use clear numeric labels every 15 days
main_chart.x_labels = [
    "Day 0",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "Day 15",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "Day 30",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "Day 45",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "Day 60",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "Day 75",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "Day 90",
]
main_chart.add("Price", list(prices))

# Sidebar chart - Pie chart for sector allocation (spans 2 rows, demonstrating rowspan)
pie_chart = pygal.Pie(
    width=1150,
    height=1100,
    style=sidebar_style,
    title="Portfolio Allocation",
    show_legend=True,
    legend_at_bottom=True,
    inner_radius=0.4,
)
allocations = [("Tech", 35), ("Health", 25), ("Finance", 28), ("Energy", 12)]
for sector, pct in allocations:
    pie_chart.add(sector, pct)

# Volume chart - Bar chart (no redundant legend)
volume_chart = pygal.Bar(
    width=1150,
    height=530,
    style=detail_style,
    title="Daily Volume (M)",
    x_title="Day",
    y_title="Volume",
    show_x_guides=False,
    show_y_guides=True,
    show_legend=False,
    x_label_rotation=0,
    truncate_label=-1,
)
volume_sampled = volume[::5] / 1e6  # Sample every 5th day for readability
volume_chart.x_labels = [f"{i * 5}" if i % 4 == 0 else "" for i in range(len(volume_sampled))]
volume_chart.add("Volume", list(volume_sampled))

# Scatter plot for risk vs return (no redundant legend)
scatter_chart = pygal.XY(
    width=1150,
    height=530,
    style=detail_style,
    title="Risk vs Return",
    x_title="Volatility (%)",
    y_title="Return (%)",
    show_x_guides=True,
    show_y_guides=True,
    show_legend=False,
    stroke=False,
    dots_size=16,
)
scatter_data = [(float(x_corr[i]), float(y_corr[i])) for i in range(len(x_corr))]
scatter_chart.add("Sectors", scatter_data)

# Category bar chart for performance (no redundant legend)
perf_chart = pygal.Bar(
    width=1150,
    height=530,
    style=detail_style,
    title="Sector Score",
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
pie_svg = pie_chart.render().decode("utf-8")
volume_svg = volume_chart.render().decode("utf-8")
scatter_svg = scatter_chart.render().decode("utf-8")
perf_svg = perf_chart.render().decode("utf-8")

# Dashboard title
main_title = "subplot-grid-custom · pygal · pyplots.ai"

# Create HTML with CSS Grid layout demonstrating both colspan and rowspan
# Layout: 4 columns x 2 rows
# - Main chart: colspan 2, row 1 only
# - Pie chart: column 4, rowspan 2 (spans both rows - demonstrates rowspan!)
# - Volume chart: column 3, row 1
# - Scatter chart: column 1, row 2
# - Sector Score: column 2-3, row 2 (colspan 2)
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
        /* Main chart spans 2 columns in row 1 */
        .main-chart {{
            grid-column: 1 / 3;
            grid-row: 1;
        }}
        /* Volume chart in column 3, row 1 */
        .volume-chart {{
            grid-column: 3;
            grid-row: 1;
        }}
        /* Pie chart spans 2 rows (rowspan demonstration) */
        .pie-chart {{
            grid-column: 4;
            grid-row: 1 / 3;
        }}
        /* Scatter chart in column 1, row 2 */
        .scatter-chart {{
            grid-column: 1;
            grid-row: 2;
        }}
        /* Sector score spans 2 columns in row 2 */
        .perf-chart {{
            grid-column: 2 / 4;
            grid-row: 2;
        }}
    </style>
</head>
<body>
    <div class="dashboard-title">{main_title}</div>
    <div class="grid-container">
        <div class="chart-cell main-chart">{main_svg}</div>
        <div class="chart-cell volume-chart">{volume_svg}</div>
        <div class="chart-cell pie-chart">{pie_svg}</div>
        <div class="chart-cell scatter-chart">{scatter_svg}</div>
        <div class="chart-cell perf-chart">{perf_svg}</div>
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
