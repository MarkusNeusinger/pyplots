"""pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: pygal 3.1.0 | Python 3.13.11
Quality: 45/100 | Created: 2026-01-08
"""

import io

import numpy as np
import pygal
from PIL import Image, ImageDraw, ImageFont
from pygal.style import Style


# Data - Simulated multivariate dataset with 3 clusters
np.random.seed(42)

# Generate clustered data
categories = ["Cluster A", "Cluster B", "Cluster C"]
n_per_cluster = 50

# Cluster centers and spreads
centers_x = [2.0, 5.5, 4.0]
centers_y = [3.0, 6.5, 2.0]
centers_val = [25, 45, 35]

x_data = []
y_data = []
value_data = []
cat_data = []

for i, cat in enumerate(categories):
    x_data.extend(np.random.normal(centers_x[i], 0.8, n_per_cluster))
    y_data.extend(np.random.normal(centers_y[i], 0.7, n_per_cluster))
    value_data.extend(np.random.normal(centers_val[i], 6, n_per_cluster))
    cat_data.extend([cat] * n_per_cluster)

x_data = np.array(x_data)
y_data = np.array(y_data)
value_data = np.array(value_data)
cat_data = np.array(cat_data)

# Simulate selection: Cluster B is selected
selected_category = "Cluster B"
selected_mask = cat_data == selected_category
n_selected = np.sum(selected_mask)
n_total = len(cat_data)

# Colors
color_selected = "#306998"  # Python Blue for selected
color_unselected = "#CCCCCC"  # Gray for unselected

# Final output dimensions (4800 x 2700)
combined_width = 4800
combined_height = 2700
title_height = 150
grid_height = combined_height - title_height
chart_w = combined_width // 2  # 2400
chart_h = grid_height // 2  # 1275

# Custom style for charts - using exact chart dimensions
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(color_unselected, color_selected),
    title_font_size=32,
    label_font_size=20,
    major_label_font_size=18,
    legend_font_size=18,
    value_font_size=16,
    stroke_width=2,
    opacity=0.8,
    opacity_hover=1.0,
)

# Style for bar chart (different color order for category highlighting)
bar_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(color_unselected, color_selected, color_unselected),
    title_font_size=32,
    label_font_size=20,
    major_label_font_size=18,
    legend_font_size=18,
    value_font_size=16,
    stroke_width=2,
    opacity=0.8,
)

# --- View 1: Scatter Plot (X vs Y) ---
scatter_chart = pygal.XY(
    width=chart_w,
    height=chart_h,
    style=custom_style,
    title="View 1: Scatter Plot (X vs Y)",
    x_title="X Coordinate",
    y_title="Y Coordinate",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=16,
    dots_size=8,
    stroke=False,
    show_x_guides=True,
    show_y_guides=True,
)

# Unselected points (gray)
unselected_scatter = [(x_data[i], y_data[i]) for i in range(len(x_data)) if not selected_mask[i]]
scatter_chart.add(f"Unselected ({n_total - n_selected})", unselected_scatter, stroke=False)

# Selected points (blue)
selected_scatter = [(x_data[i], y_data[i]) for i in range(len(x_data)) if selected_mask[i]]
scatter_chart.add(f"Selected: {selected_category} ({n_selected})", selected_scatter, stroke=False)

# --- View 2: Histogram of Value distribution ---
histogram_chart = pygal.Histogram(
    width=chart_w,
    height=chart_h,
    style=custom_style,
    title="View 2: Histogram (Value Distribution)",
    x_title="Value",
    y_title="Frequency",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=16,
    show_x_guides=True,
    show_y_guides=True,
)

# Create histogram bins
bins = np.linspace(value_data.min() - 5, value_data.max() + 5, 15)
unselected_values = value_data[~selected_mask]
selected_values = value_data[selected_mask]

# Calculate histogram data as (height, start, end) tuples
unselected_hist, _ = np.histogram(unselected_values, bins=bins)
selected_hist, _ = np.histogram(selected_values, bins=bins)

unselected_hist_data = [(int(h), float(bins[i]), float(bins[i + 1])) for i, h in enumerate(unselected_hist)]
selected_hist_data = [(int(h), float(bins[i]), float(bins[i + 1])) for i, h in enumerate(selected_hist)]

histogram_chart.add(f"Unselected ({n_total - n_selected})", unselected_hist_data)
histogram_chart.add(f"Selected: {selected_category} ({n_selected})", selected_hist_data)

# --- View 3: Bar Chart by Category ---
bar_chart = pygal.Bar(
    width=chart_w,
    height=chart_h,
    style=bar_style,
    title="View 3: Bar Chart (Count by Category)",
    x_title="Category",
    y_title="Count",
    show_legend=False,
    show_x_guides=False,
    show_y_guides=True,
)

# Count by category with selection highlighting
cat_counts = []
for cat in categories:
    count = np.sum(cat_data == cat)
    cat_counts.append(count)

bar_chart.x_labels = categories
# Add each category separately to control colors (gray, blue, gray)
bar_chart.add("Cluster A", [cat_counts[0], None, None])
bar_chart.add("Cluster B", [None, cat_counts[1], None])
bar_chart.add("Cluster C", [None, None, cat_counts[2]])

# --- View 4: Summary Panel with selection info ---
summary_chart = pygal.Pie(
    width=chart_w,
    height=chart_h,
    style=Style(
        background="white",
        plot_background="white",
        foreground="#333333",
        foreground_strong="#333333",
        foreground_subtle="#666666",
        colors=(color_selected, color_unselected),
        title_font_size=32,
        label_font_size=20,
        major_label_font_size=18,
        legend_font_size=18,
        value_font_size=16,
    ),
    title=f"View 4: Selection Summary ({selected_category})",
    inner_radius=0.4,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=16,
)

summary_chart.add(f"Selected ({n_selected})", n_selected)
summary_chart.add(f"Unselected ({n_total - n_selected})", n_total - n_selected)

# Create combined image first (white background)
combined = Image.new("RGB", (combined_width, combined_height), "white")

# Render each chart to PNG and paste into combined image
charts = [
    (scatter_chart, (0, title_height)),  # Top-left
    (histogram_chart, (chart_w, title_height)),  # Top-right
    (bar_chart, (0, title_height + chart_h)),  # Bottom-left
    (summary_chart, (chart_w, title_height + chart_h)),  # Bottom-right
]

for chart, position in charts:
    png_data = chart.render_to_png()
    chart_img = Image.open(io.BytesIO(png_data))
    # Resize to exact target dimensions to handle any size mismatch
    if chart_img.size != (chart_w, chart_h):
        chart_img = chart_img.resize((chart_w, chart_h), Image.Resampling.LANCZOS)
    # Convert to RGB if necessary (handle RGBA)
    if chart_img.mode == "RGBA":
        background = Image.new("RGB", chart_img.size, "white")
        background.paste(chart_img, mask=chart_img.split()[3])
        chart_img = background
    combined.paste(chart_img, position)

# Add main title using PIL ImageDraw
draw = ImageDraw.Draw(combined)

# Use default font (more reliable across environments)
title_font = ImageFont.load_default(size=48)
subtitle_font = ImageFont.load_default(size=32)

main_title = "linked-views-selection · pygal · pyplots.ai"
subtitle = f"Linked Views: '{selected_category}' highlighted across all views ({n_selected} of {n_total} points)"

# Draw centered title
title_bbox = draw.textbbox((0, 0), main_title, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
draw.text(((combined_width - title_width) // 2, 30), main_title, fill="#333333", font=title_font)

subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
draw.text(((combined_width - subtitle_width) // 2, 95), subtitle, fill="#666666", font=subtitle_font)

# Save combined image
combined.save("plot.png", dpi=(300, 300))

# Also generate HTML with all charts embedded for interactivity
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>linked-views-selection · pygal · pyplots.ai</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        h1 {{ text-align: center; color: #333; }}
        p.subtitle {{ text-align: center; color: #666; margin-bottom: 20px; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 1600px; margin: 0 auto; }}
        .chart {{ background: white; border-radius: 8px; padding: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .chart svg {{ width: 100%; height: auto; }}
        .selection-info {{ text-align: center; background: #306998; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>linked-views-selection · pygal · pyplots.ai</h1>
    <p class="subtitle">Multiple Linked Views with Selection Sync</p>
    <div class="selection-info">
        <strong>Selection Active:</strong> {selected_category} ({n_selected} of {n_total} points)
        <br><small>Blue = Selected | Gray = Unselected | Hover over any chart element for details</small>
    </div>
    <div class="grid">
        <div class="chart">{scatter_chart.render(is_unicode=True)}</div>
        <div class="chart">{histogram_chart.render(is_unicode=True)}</div>
        <div class="chart">{bar_chart.render(is_unicode=True)}</div>
        <div class="chart">{summary_chart.render(is_unicode=True)}</div>
    </div>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
