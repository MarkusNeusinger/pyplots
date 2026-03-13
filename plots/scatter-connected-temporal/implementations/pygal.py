"""pyplots.ai
scatter-connected-temporal: Connected Scatter Plot with Temporal Path
Library: pygal | Python 3.13
Quality: pending | Created: 2026-03-13
"""

import numpy as np
import pygal
from pygal.style import Style


# Data — Life expectancy vs GDP per capita for a fictional country (1990-2023)
np.random.seed(42)
years = list(range(1990, 2024))
n_years = len(years)

# GDP per capita starts ~8000, grows with occasional dips (recessions)
gdp_base = 8000
gdp_growth = np.cumsum(np.random.normal(450, 300, n_years))
gdp_growth[8:10] -= 1500  # 1998-1999 recession dip
gdp_growth[18:20] -= 2000  # 2008-2009 financial crisis
gdp_growth[30:32] -= 800  # 2020-2021 pandemic dip
gdp_per_capita = gdp_base + gdp_growth
gdp_per_capita = np.maximum(gdp_per_capita, 5000)

# Life expectancy starts ~68, rises gradually with dips during crises
le_base = 68.0
le_growth = np.cumsum(np.random.normal(0.25, 0.12, n_years))
le_growth[18:20] -= 0.4  # Financial crisis stress
le_growth[30:32] -= 1.2  # Pandemic drop
life_expectancy = le_base + le_growth
life_expectancy = np.clip(life_expectancy, 64, 82)

# Select key years to annotate
annotate_years = [1990, 1998, 2008, 2015, 2020, 2023]

# Build color gradient from light to dark blue to encode temporal progression
start_color = np.array([0x8E, 0xC8, 0xE8])  # Light blue
end_color = np.array([0x1A, 0x3A, 0x5C])  # Dark navy
colors_hex = []
for i in range(n_years):
    t = i / (n_years - 1)
    rgb = (1 - t) * start_color + t * end_color
    colors_hex.append(f"#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}")

# Style
font = "DejaVu Sans, Helvetica, Arial, sans-serif"
custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#2a2a2a",
    foreground_strong="#2a2a2a",
    foreground_subtle="#dddddd",
    guide_stroke_color="#e0e0e0",
    colors=("#306998", "#8ec8e8", "#1a3a5c"),
    font_family=font,
    title_font_family=font,
    title_font_size=52,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=32,
    legend_font_family=font,
    value_font_size=26,
    tooltip_font_size=26,
    tooltip_font_family=font,
    opacity=0.85,
    opacity_hover=1.0,
    stroke_opacity=0.6,
    stroke_opacity_hover=1.0,
)

# Axis ranges
x_min = float(np.floor(gdp_per_capita.min() / 1000) * 1000)
x_max = float(np.ceil(gdp_per_capita.max() / 1000) * 1000)
y_min = float(np.floor(life_expectancy.min()))
y_max = float(np.ceil(life_expectancy.max()) + 1)

# Create XY chart with connected path
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Life Expectancy vs GDP · scatter-connected-temporal · pygal · pyplots.ai",
    x_title="GDP per Capita (USD)",
    y_title="Life Expectancy (years)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=22,
    stroke=True,
    dots_size=7,
    show_x_guides=True,
    show_y_guides=True,
    x_value_formatter=lambda x: f"${x:,.0f}",
    value_formatter=lambda y: f"{y:.1f} yrs",
    margin_bottom=100,
    margin_left=60,
    margin_right=50,
    margin_top=50,
    range=(y_min, y_max),
    xrange=(x_min, x_max),
    x_labels_major_count=7,
    y_labels_major_count=8,
    print_values=False,
    js=[],
)

# Add temporal path as connected line with dots
path_points = [
    {"value": (float(gdp_per_capita[i]), float(life_expectancy[i])), "label": str(years[i])} for i in range(n_years)
]
chart.add(
    "Temporal path (1990-2023)",
    path_points,
    stroke=True,
    show_dots=True,
    dots_size=6,
    stroke_style={"width": 5, "linecap": "round", "linejoin": "round"},
)

# Highlight annotated key years with larger dots
annotated_points = []
for yr in annotate_years:
    idx = yr - 1990
    annotated_points.append(
        {
            "value": (float(gdp_per_capita[idx]), float(life_expectancy[idx])),
            "label": f"{yr}: GDP ${gdp_per_capita[idx]:,.0f}, LE {life_expectancy[idx]:.1f}",
        }
    )
chart.add("Key years", annotated_points, stroke=False, dots_size=14)

# Highlight start and end with distinct markers
chart.add(
    f"Start ({years[0]})",
    [{"value": (float(gdp_per_capita[0]), float(life_expectancy[0])), "label": f"{years[0]}: Beginning"}],
    stroke=False,
    dots_size=18,
)
chart.add(
    f"End ({years[-1]})",
    [{"value": (float(gdp_per_capita[-1]), float(life_expectancy[-1])), "label": f"{years[-1]}: Present"}],
    stroke=False,
    dots_size=18,
)

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
