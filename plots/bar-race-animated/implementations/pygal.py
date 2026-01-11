""" pyplots.ai
bar-race-animated: Animated Bar Chart Race
Library: pygal 3.1.0 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-11
"""

from io import BytesIO

import cairosvg
import numpy as np
import pygal
from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style


# Data - Technology companies market cap evolution (2019-2024)
np.random.seed(42)

companies = ["Apple", "Microsoft", "Alphabet", "Amazon", "Meta", "Tesla", "NVIDIA", "Samsung"]
years = [2019, 2020, 2021, 2022, 2023, 2024]

# Generate realistic market cap data (in billions USD)
base_values = {
    "Apple": 1200,
    "Microsoft": 900,
    "Alphabet": 800,
    "Amazon": 700,
    "Meta": 400,
    "Tesla": 100,
    "NVIDIA": 150,
    "Samsung": 300,
}

growth_rates = {
    "Apple": [1.0, 1.3, 1.8, 1.5, 2.0, 2.8],
    "Microsoft": [1.0, 1.4, 2.0, 1.6, 2.2, 2.9],
    "Alphabet": [1.0, 1.2, 1.6, 1.2, 1.5, 2.0],
    "Amazon": [1.0, 1.5, 1.6, 1.0, 1.3, 1.8],
    "Meta": [1.0, 1.5, 1.8, 0.6, 1.2, 1.8],
    "Tesla": [1.0, 5.0, 8.0, 4.0, 6.0, 7.0],
    "NVIDIA": [1.0, 2.0, 4.0, 2.5, 6.0, 14.0],
    "Samsung": [1.0, 1.1, 1.3, 0.9, 1.1, 1.4],
}

# Calculate market cap for each year
data = {}
for company in companies:
    data[company] = [int(base_values[company] * growth_rates[company][i]) for i in range(len(years))]

# Colors for consistent entity tracking
company_colors = {
    "Apple": "#306998",  # Python Blue (primary)
    "Microsoft": "#FFD43B",  # Python Yellow (primary)
    "Alphabet": "#4285F4",  # Google Blue
    "Amazon": "#FF9900",  # Amazon Orange
    "Meta": "#0866FF",  # Meta Blue
    "Tesla": "#CC0000",  # Tesla Red
    "NVIDIA": "#76B900",  # NVIDIA Green
    "Samsung": "#1428A0",  # Samsung Blue
}

# Custom style for pygal with larger fonts
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    title_font_size=72,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=36,
    value_font_size=28,
    tooltip_font_size=28,
)

# Create individual charts for each year with y-axis labels (company names)
charts = []
for year_idx, year in enumerate(years):
    # Get values for this year and sort
    year_data = [(company, data[company][year_idx]) for company in companies]
    year_data.sort(key=lambda x: x[1], reverse=True)

    chart = pygal.HorizontalBar(
        width=1600,
        height=1000,
        style=custom_style,
        show_legend=False,
        title=str(year),
        x_title="Market Cap (Billion USD)",
        print_values=True,
        print_values_position="middle",
        value_formatter=lambda x: f"${x:,.0f}B",
        margin=30,
        spacing=20,
        truncate_label=-1,
        x_labels_major_every=2,  # Show fewer x-axis tick labels
    )

    # Set y-axis labels to company names (in sorted order)
    chart.x_labels = [company for company, _ in year_data]

    # Add single series with all values
    values = []
    for company, value in year_data:
        values.append({"value": value, "color": company_colors[company]})
    chart.add("Market Cap", values)

    charts.append(chart)

# Render each chart to PNG and combine into grid
chart_images = []
for chart in charts:
    svg_data = chart.render()
    png_data = cairosvg.svg2png(bytestring=svg_data, output_width=1600, output_height=1000)
    img = Image.open(BytesIO(png_data))
    chart_images.append(img)

# Create 3x2 grid layout (4800 x 2700 final size)
grid_width = 4800
grid_height = 2700
cell_width = grid_width // 3
cell_height = (grid_height - 180) // 2  # Leave space for title

combined = Image.new("RGB", (grid_width, grid_height), "white")

# Add main title
draw = ImageDraw.Draw(combined)
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
except OSError:
    title_font = ImageFont.load_default()

title_text = "Tech Company Market Cap (2019-2024) · bar-race-animated · pygal · pyplots.ai"
bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width = bbox[2] - bbox[0]
draw.text(((grid_width - title_width) // 2, 40), title_text, fill="#333333", font=title_font)

# Paste charts into grid
positions = [
    (0, 0),
    (1, 0),
    (2, 0),  # Top row: 2019, 2020, 2021
    (0, 1),
    (1, 1),
    (2, 1),  # Bottom row: 2022, 2023, 2024
]

for idx, (col, row) in enumerate(positions):
    if idx < len(chart_images):
        img = chart_images[idx].resize((cell_width, cell_height), Image.Resampling.LANCZOS)
        x = col * cell_width
        y = 180 + row * cell_height
        combined.paste(img, (x, y))

# Save as PNG
combined.save("plot.png", dpi=(300, 300))

# Save as HTML (interactive SVG version showing evolution)
html_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    title_font_size=36,
    label_font_size=20,
    major_label_font_size=18,
    legend_font_size=18,
    value_font_size=16,
    tooltip_font_size=16,
)

html_chart = pygal.HorizontalBar(
    width=1200,
    height=800,
    style=html_style,
    show_legend=True,
    title="Tech Company Market Cap 2024 · bar-race-animated · pygal · pyplots.ai",
    x_title="Market Cap (Billion USD)",
    print_values=True,
    value_formatter=lambda x: f"${x:,.0f}B",
)

final_data = [(company, data[company][-1]) for company in companies]
final_data.sort(key=lambda x: x[1], reverse=True)
html_chart.x_labels = [company for company, _ in final_data]
values = [{"value": value, "color": company_colors[company]} for company, value in final_data]
html_chart.add("Market Cap", values)

html_chart.render_to_file("plot.html")
