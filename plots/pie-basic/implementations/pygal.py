""" pyplots.ai
pie-basic: Basic Pie Chart
Library: pygal 3.1.0 | Python 3.14.0
Quality: 86/100 | Created: 2025-12-23
"""

import math

import pygal
from pygal.style import Style


# Data - Global smartphone market share (2024)
categories = [("Apple", 23.3), ("Samsung", 19.4), ("Xiaomi", 14.1), ("OPPO", 8.7), ("vivo", 7.5), ("Others", 27.0)]

# Identify the largest slice for explosion (spec: "explode largest or smallest")
values = [v for _, v in categories]
largest_idx = values.index(max(values))

# Calculate explode offset — pygal draws slices clockwise from top (−π/2).
# Compute the angular bisector of the largest slice to translate it outward.
total = sum(values)
cumulative_before = sum(values[:largest_idx])
slice_mid_frac = (cumulative_before + values[largest_idx] / 2) / total
mid_angle = -math.pi / 2 + slice_mid_frac * 2 * math.pi
explode_px = 30
explode_dx = math.cos(mid_angle) * explode_px
explode_dy = math.sin(mid_angle) * explode_px

# Saturated, high-contrast palette — colorblind-safe (no red-green ambiguity)
palette = ("#2563EB", "#D97706", "#0D9488", "#E11D48", "#7C3AED", "#475569")

custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#1E293B",
    foreground_strong="#0F172A",
    foreground_subtle="#94A3B8",
    colors=palette,
    title_font_size=72,
    label_font_size=44,
    major_label_font_size=44,
    value_label_font_size=40,
    legend_font_size=52,
    value_font_size=52,
    tooltip_font_size=36,
    value_colors=("#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"),
    stroke_opacity=1,
)

chart = pygal.Pie(
    width=3600,
    height=3600,
    style=custom_style,
    title="Smartphone Market Share · pie-basic · pygal · pyplots.ai",
    inner_radius=0,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=36,
    print_values=True,
    print_labels=True,
    print_values_position="center",
    value_formatter=lambda x: f"{x:.1f}%",
    margin=40,
    margin_bottom=80,
)

# Storytelling: legend names convey narrative; labels add on-chart annotations
legend_names = {"Others": "Others (largest share)", "Apple": "Apple (top brand)"}

for i, (company, value) in enumerate(categories):
    slice_css = "stroke: white; stroke-width: 5"
    slice_data = {"value": value, "style": slice_css}

    # Explode the largest slice outward for emphasis
    if i == largest_idx:
        slice_data["node"] = {"transform": f"translate({explode_dx:.1f}, {explode_dy:.1f})"}
        slice_data["label"] = "Largest"
    elif company == "Apple":
        slice_data["label"] = "#1 brand"

    name = legend_names.get(company, company)
    chart.add(name, [slice_data])

chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
