"""pyplots.ai
area-basic: Basic Area Chart
Library: pygal 3.1.0 | Python 3.14.2
"""

import pygal
from pygal.style import Style


# Data - Daily website visitors over a month
days = list(range(1, 31))
visitors = [
    1250,
    1380,
    1420,
    1180,
    980,
    890,
    920,
    1340,
    1520,
    1680,
    1590,
    1450,
    1120,
    1080,
    1560,
    1720,
    1890,
    2010,
    1850,
    1420,
    1380,
    1680,
    1920,
    2150,
    2080,
    1950,
    1620,
    1540,
    1780,
    1920,
]

# Key data points for storytelling
peak_idx = visitors.index(max(visitors))
low_idx = visitors.index(min(visitors))

# Trend line (linear regression via two-point approximation)
n = len(visitors)
x_mean = (n - 1) / 2.0
y_mean = sum(visitors) / n
slope = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(visitors)) / sum((i - x_mean) ** 2 for i in range(n))
intercept = y_mean - slope * x_mean
trend = [slope * i + intercept for i in range(n)]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#cccccc",
    colors=("#306998", "#e8913a", "#cc4444", "#5a9e6f"),
    title_font_size=56,
    label_font_size=40,
    major_label_font_size=36,
    value_font_size=32,
    legend_font_size=34,
    opacity=0.30,
    opacity_hover=0.5,
)

# Create area chart (Line with fill=True)
chart = pygal.Line(
    width=4800,
    height=2700,
    title="Daily Website Visitors \u00b7 area-basic \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Day of Month",
    y_title="Visitors",
    style=custom_style,
    fill=True,
    show_dots=True,
    dots_size=10,
    stroke_style={"width": 5},
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=0,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=28,
    value_formatter=lambda x: f"{x:,.0f}",
    min_scale=4,
    margin_bottom=120,
    margin_left=100,
)

# Main area series
chart.add("Daily Visitors", visitors, fill=True, stroke_style={"width": 5})

# Trend line (dashed, no fill) for storytelling
chart.add(
    f"Trend (+{slope:.0f} visitors/day)",
    [round(t) for t in trend],
    fill=False,
    show_dots=False,
    stroke_style={"width": 4, "dasharray": "20, 12"},
)

# Peak marker as separate series (visible in PNG)
peak_series = [None] * n
peak_series[peak_idx] = {"value": visitors[peak_idx], "label": f"Peak: {visitors[peak_idx]:,} (Day {peak_idx + 1})"}
chart.add(f"Peak: {visitors[peak_idx]:,}", peak_series, fill=False, show_dots=True, dots_size=22, stroke=False)

# Low marker as separate series (visible in PNG)
low_series = [None] * n
low_series[low_idx] = {"value": visitors[low_idx], "label": f"Low: {visitors[low_idx]:,} (Day {low_idx + 1})"}
chart.add(f"Low: {visitors[low_idx]:,}", low_series, fill=False, show_dots=True, dots_size=22, stroke=False)

# X-axis labels - show every 5th day for readability
chart.x_labels = [str(d) if d % 5 == 0 or d == 1 else "" for d in days]

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
