"""pyplots.ai
pictogram-basic: Pictogram Chart (Isotype Visualization)
Library: pygal 3.1.0 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-10
"""

import pygal
from pygal.style import Style


# Data - Fruit production (thousands of tonnes)
# Apples leads strongly; mix of exact multiples and remainders
categories = ["Apples", "Oranges", "Bananas", "Grapes", "Mangoes"]
values = [35, 22, 18, 15, 8]  # 35 and 15 are exact multiples of 5
icon_unit = 5  # Each dot represents 5 thousand tonnes

# Build dot matrix data: each full unit = 1.0, partial = visible fraction
# Minimum 0.6 keeps partial dots clearly visible as "partial"
max_icons = max(v // icon_unit + (1 if v % icon_unit else 0) for v in values)
dot_data = {}
for cat, val in zip(categories, values, strict=True):
    full = val // icon_unit
    remainder = val % icon_unit
    row = [1.0] * full
    if remainder:
        row.append(max(remainder / icon_unit, 0.6))
    # Pad with None so all rows same length
    row += [None] * (max_icons - len(row))
    dot_data[cat] = row

# Cohesive colorblind-safe palette: deep blue leader, then amber/teal/violet/coral
# Avoids green-teal confusion; warm-cool contrast for clear distinction
palette = (
    "#1B4F72",  # Deep navy for leader (Apples) — bold focal point
    "#D68910",  # Rich amber (Oranges)
    "#148F77",  # Teal (Bananas) — distinct from navy
    "#6C3483",  # Deep violet (Grapes)
    "#C0392B",  # Warm coral-red (Mangoes)
)

# Style — refined typography and clean background
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#2C3E50",
    foreground_strong="#1B2631",
    foreground_subtle="transparent",
    colors=palette,
    title_font_size=52,
    label_font_size=44,
    major_label_font_size=36,
    legend_font_size=36,
    value_font_size=24,
    tooltip_font_size=24,
    font_family="sans-serif",
)

# Chart — pygal.Dot as pictogram approximation with large dots
chart = pygal.Dot(
    width=4800,
    height=2700,
    style=custom_style,
    title=("Fruit Production by Type (each dot ≈ 5 000 tonnes)\npictogram-basic · pygal · pyplots.ai"),
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    legend_box_size=28,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=True,
    spacing=50,
    margin=60,
    margin_left=100,
    margin_right=60,
    margin_top=120,
    margin_bottom=180,
    x_label_rotation=0,
    truncate_label=-1,
    truncate_legend=-1,
    dot_size=48,
    print_values=False,
)

# X-axis labels show cumulative value scale
chart.x_labels = [str((i + 1) * icon_unit) for i in range(max_icons)]

# Add each category as a series in descending order — visual hierarchy
for cat in categories:
    chart.add(cat, dot_data[cat])

# Save
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
