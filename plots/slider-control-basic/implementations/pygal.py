"""pyplots.ai
slider-control-basic: Interactive Plot with Slider Control
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Quarterly sales data across years (slider would filter by year)
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

# Custom style for pyplots - large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4B8BBE", "#FFE873", "#646464"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    stroke_width=3,
    opacity="0.85",
    opacity_hover="0.95",
    transition="400ms ease-in",
    tooltip_font_size=36,
)

# Create grouped bar chart showing all years (slider concept: each year is a slider position)
chart = pygal.Bar(
    width=4800,
    height=2700,
    style=custom_style,
    title="Quarterly Sales by Year · slider-control-basic · pygal · pyplots.ai",
    x_title="Quarter",
    y_title="Sales (thousands USD)",
    show_x_guides=False,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    margin=80,
    spacing=30,
    value_formatter=lambda x: f"${x:.0f}K",
    print_values=False,
    print_labels=False,
    truncate_legend=-1,
    x_label_rotation=0,
)

# Set x-axis labels
chart.x_labels = quarters

# Add each year's data as a series (simulating what a slider would filter)
for year in years:
    chart.add(
        f"Year {year}",
        [{"value": v, "label": f"{q} {year}: ${v:.1f}K"} for q, v in zip(quarters, sales_data[year], strict=True)],
    )

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
