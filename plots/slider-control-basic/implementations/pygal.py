"""pyplots.ai
slider-control-basic: Interactive Plot with Slider Control
Library: pygal 3.1.0 | Python 3.13.11
Quality: 52/100 | Created: 2025-12-31
"""

import json

import numpy as np
import pygal
from pygal.style import Style


# Data - Quarterly sales data across years (slider will filter by year)
np.random.seed(42)

years = [2020, 2021, 2022, 2023, 2024]
quarters = ["Q1", "Q2", "Q3", "Q4"]

# Generate realistic sales data with growth trend
base_sales = 100
sales_data = {}
for i, year in enumerate(years):
    growth_factor = 1 + 0.15 * i + np.random.uniform(-0.05, 0.05)
    seasonal = [0.8, 1.0, 0.9, 1.3]  # Q4 is strongest
    sales_data[year] = [base_sales * growth_factor * s * (1 + np.random.uniform(-0.1, 0.1)) for s in seasonal]

# Custom style for pyplots - large canvas with distinct colors
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Primary blue for the single series
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=48,
    value_font_size=42,
    stroke_width=3,
    opacity="0.9",
    opacity_hover="1.0",
    transition="300ms ease-in-out",
    tooltip_font_size=40,
)

# Create bar chart showing single year (slider switches years)
# Start with first year (2020)
initial_year = years[0]

chart = pygal.Bar(
    width=4800,
    height=2700,
    style=custom_style,
    title=f"Quarterly Sales for Year {initial_year} · slider-control-basic · pygal · pyplots.ai",
    x_title="Quarter",
    y_title="Sales (thousands USD)",
    show_x_guides=False,
    show_y_guides=True,
    legend_at_bottom=False,
    show_legend=True,
    margin=100,
    margin_top=150,
    margin_bottom=120,
    spacing=50,
    value_formatter=lambda x: f"${x:.0f}K",
    print_values=True,
    print_values_position="top",
    truncate_legend=-1,
    x_label_rotation=0,
    y_labels_major_every=2,
    range=(0, 220),  # Fixed range for consistent comparison across years
)

# Set x-axis labels
chart.x_labels = quarters

# Add the initial year's data
chart.add(
    f"Year {initial_year}",
    [{"value": v, "label": f"{q}: ${v:.1f}K"} for q, v in zip(quarters, sales_data[initial_year], strict=True)],
)

# Save PNG with initial year (static preview)
chart.render_to_png("plot.png")

# Create interactive HTML with slider control
# We'll generate separate SVG for each year and embed with JavaScript slider
html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Quarterly Sales by Year - Interactive Slider | pyplots.ai</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: white;
            margin: 0;
            padding: 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .container {{
            width: 100%;
            max-width: 1600px;
        }}
        .slider-container {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 30px 40px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .slider-label {{
            font-size: 24px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .year-display {{
            font-size: 36px;
            font-weight: 700;
            color: #306998;
            background: white;
            padding: 10px 25px;
            border-radius: 8px;
            border: 2px solid #306998;
        }}
        .slider-wrapper {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        .year-label {{
            font-size: 18px;
            font-weight: 500;
            color: #666;
            min-width: 50px;
        }}
        input[type="range"] {{
            flex: 1;
            height: 12px;
            -webkit-appearance: none;
            appearance: none;
            background: #ddd;
            border-radius: 6px;
            outline: none;
        }}
        input[type="range"]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 32px;
            height: 32px;
            background: #306998;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }}
        input[type="range"]::-webkit-slider-thumb:hover {{
            transform: scale(1.15);
        }}
        input[type="range"]::-moz-range-thumb {{
            width: 32px;
            height: 32px;
            background: #306998;
            border-radius: 50%;
            cursor: pointer;
            border: none;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }}
        .chart-container {{
            position: relative;
            width: 100%;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .chart {{
            display: none;
            width: 100%;
        }}
        .chart.active {{
            display: block;
        }}
        .chart svg {{
            width: 100%;
            height: auto;
        }}
        .summary {{
            margin-top: 20px;
            padding: 20px;
            background: #f0f7ff;
            border-radius: 8px;
            text-align: center;
        }}
        .summary-text {{
            font-size: 20px;
            color: #333;
        }}
        .summary-value {{
            font-weight: 700;
            color: #306998;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="slider-container">
            <div class="slider-label">
                <span>Select Year to View</span>
                <span class="year-display" id="yearDisplay">{initial_year}</span>
            </div>
            <div class="slider-wrapper">
                <span class="year-label">{min_year}</span>
                <input type="range" id="yearSlider" min="0" max="{max_index}" value="0" step="1">
                <span class="year-label">{max_year}</span>
            </div>
        </div>
        <div class="chart-container">
            {charts_html}
        </div>
        <div class="summary">
            <span class="summary-text">
                Total Annual Sales: <span class="summary-value" id="totalSales"></span>
            </span>
        </div>
    </div>
    <script>
        const years = {years_json};
        const totals = {totals_json};
        const slider = document.getElementById('yearSlider');
        const yearDisplay = document.getElementById('yearDisplay');
        const totalSales = document.getElementById('totalSales');
        const charts = document.querySelectorAll('.chart');

        function updateChart() {{
            const index = parseInt(slider.value);
            const year = years[index];
            yearDisplay.textContent = year;
            totalSales.textContent = '$' + totals[index].toFixed(1) + 'K';

            charts.forEach((chart, i) => {{
                chart.classList.toggle('active', i === index);
            }});
        }}

        slider.addEventListener('input', updateChart);
        updateChart();
    </script>
</body>
</html>
"""

# Generate SVG for each year
charts_html_parts = []
totals = []

for idx, year in enumerate(years):
    year_chart = pygal.Bar(
        width=4800,
        height=2700,
        style=custom_style,
        title=f"Quarterly Sales for Year {year} · slider-control-basic · pygal · pyplots.ai",
        x_title="Quarter",
        y_title="Sales (thousands USD)",
        show_x_guides=False,
        show_y_guides=True,
        legend_at_bottom=False,
        show_legend=True,
        margin=100,
        margin_top=150,
        margin_bottom=120,
        spacing=50,
        value_formatter=lambda x: f"${x:.0f}K",
        print_values=True,
        print_values_position="top",
        truncate_legend=-1,
        x_label_rotation=0,
        y_labels_major_every=2,
        range=(0, 220),  # Fixed range for consistent comparison
    )
    year_chart.x_labels = quarters
    year_chart.add(
        f"Year {year}",
        [{"value": v, "label": f"{q}: ${v:.1f}K"} for q, v in zip(quarters, sales_data[year], strict=True)],
    )

    svg_content = year_chart.render().decode("utf-8")
    active_class = "active" if idx == 0 else ""
    charts_html_parts.append(f'<div class="chart {active_class}" data-year="{year}">{svg_content}</div>')
    totals.append(sum(sales_data[year]))

# Combine into final HTML
final_html = html_template.format(
    initial_year=years[0],
    min_year=years[0],
    max_year=years[-1],
    max_index=len(years) - 1,
    charts_html="\n".join(charts_html_parts),
    years_json=json.dumps(years),
    totals_json=json.dumps(totals),
)

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(final_html)
