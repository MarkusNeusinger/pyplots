"""
dumbbell-basic: Basic Dumbbell Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Employee satisfaction scores before and after policy changes
categories = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations", "Customer Support", "Product"]
before = [65, 58, 72, 45, 68, 52, 48, 70]
after = [82, 75, 78, 72, 80, 71, 68, 85]

# Sort by difference (improvement) for better pattern visibility
differences = [a - b for a, b in zip(after, before, strict=True)]
sorted_data = sorted(zip(categories, before, after, differences, strict=True), key=lambda x: x[3], reverse=True)
categories = [item[0] for item in sorted_data]
before = [item[1] for item in sorted_data]
after = [item[2] for item in sorted_data]

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B"),  # Python Blue for before, Yellow for after
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=48,
    value_font_size=36,
    value_label_font_size=36,
)

# Create XY chart for dumbbell visualization
n = len(categories)
chart = pygal.XY(
    width=4800,
    height=2700,
    title="Employee Satisfaction · dumbbell-basic · pygal · pyplots.ai",
    x_title="Satisfaction Score",
    style=custom_style,
    show_legend=True,
    legend_at_bottom=True,
    dots_size=25,
    stroke_style={"width": 6},
    show_y_guides=True,
    show_x_guides=True,
    margin=100,
    xrange=(30, 100),
    range=(0, n + 1),
    y_labels=[{"label": cat, "value": n - i} for i, cat in enumerate(categories)],
)

# Add connecting lines (gray, subtle)
# Create separate series for each dumbbell line
for i, (_cat, b, a) in enumerate(zip(categories, before, after, strict=True)):
    y_pos = n - i
    # Add thin gray connector line (no dots)
    chart.add(
        None,  # No legend entry for connector lines
        [{"value": (b, y_pos)}, {"value": (a, y_pos)}],
        stroke_style={"width": 4},
        dots_size=0,
        show_dots=False,
    )

# Add "Before" dots (Python Blue)
before_points = []
for i, (_cat, b) in enumerate(zip(categories, before, strict=True)):
    y_pos = n - i
    before_points.append((b, y_pos))
chart.add("Before Policy Change", before_points, dots_size=25, stroke=False)

# Add "After" dots (Python Yellow)
after_points = []
for i, (_cat, a) in enumerate(zip(categories, after, strict=True)):
    y_pos = n - i
    after_points.append((a, y_pos))
chart.add("After Policy Change", after_points, dots_size=25, stroke=False)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
