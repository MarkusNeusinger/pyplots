"""pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: pygal 3.1.0 | Python 3.13.11
Quality: 52/100 | Created: 2026-01-08
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
color_accent = "#FFD43B"  # Python Yellow

# Custom style for charts
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(color_unselected, color_selected),
    title_font_size=36,
    label_font_size=22,
    major_label_font_size=20,
    legend_font_size=22,
    value_font_size=18,
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
    colors=(color_unselected, color_selected, color_unselected),  # A=gray, B=blue, C=gray
    title_font_size=36,
    label_font_size=22,
    major_label_font_size=20,
    legend_font_size=22,
    value_font_size=18,
    stroke_width=2,
    opacity=0.8,
)

# Chart dimensions for 2x2 grid layout
chart_width = 2400
chart_height = 1350

# --- View 1: Scatter Plot (X vs Y) ---
scatter_chart = pygal.XY(
    width=chart_width,
    height=chart_height,
    style=custom_style,
    title="View 1: Scatter Plot (X vs Y)",
    x_title="X Coordinate",
    y_title="Y Coordinate",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=18,
    dots_size=10,
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
    width=chart_width,
    height=chart_height,
    style=custom_style,
    title="View 2: Histogram (Value Distribution)",
    x_title="Value",
    y_title="Frequency",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=18,
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
    width=chart_width,
    height=chart_height,
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
    width=chart_width,
    height=chart_height,
    style=Style(
        background="white",
        plot_background="white",
        foreground="#333333",
        foreground_strong="#333333",
        foreground_subtle="#666666",
        colors=(color_selected, color_unselected),
        title_font_size=36,
        label_font_size=22,
        major_label_font_size=20,
        legend_font_size=22,
        value_font_size=18,
    ),
    title=f"Selection Summary: {selected_category}",
    inner_radius=0.5,
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=18,
)

summary_chart.add(f"Selected ({n_selected})", n_selected)
summary_chart.add(f"Unselected ({n_total - n_selected})", n_total - n_selected)

# Render each chart to PNG bytes
scatter_png = scatter_chart.render_to_png()
histogram_png = histogram_chart.render_to_png()
bar_png = bar_chart.render_to_png()
summary_png = summary_chart.render_to_png()

# Combine into 2x2 grid using PIL
scatter_img = Image.open(io.BytesIO(scatter_png))
histogram_img = Image.open(io.BytesIO(histogram_png))
bar_img = Image.open(io.BytesIO(bar_png))
summary_img = Image.open(io.BytesIO(summary_png))

# Create combined image (4800 x 2700)
combined_width = 4800
combined_height = 2700

# Add space for main title
title_height = 150
grid_height = combined_height - title_height

combined = Image.new("RGB", (combined_width, combined_height), "white")

# Resize charts to fit grid
chart_w = combined_width // 2
chart_h = grid_height // 2

scatter_resized = scatter_img.resize((chart_w, chart_h), Image.Resampling.LANCZOS)
histogram_resized = histogram_img.resize((chart_w, chart_h), Image.Resampling.LANCZOS)
bar_resized = bar_img.resize((chart_w, chart_h), Image.Resampling.LANCZOS)
summary_resized = summary_img.resize((chart_w, chart_h), Image.Resampling.LANCZOS)

# Paste charts into grid (below title area)
combined.paste(scatter_resized, (0, title_height))
combined.paste(histogram_resized, (chart_w, title_height))
combined.paste(bar_resized, (0, title_height + chart_h))
combined.paste(summary_resized, (chart_w, title_height + chart_h))

# Add main title using PIL ImageDraw
draw = ImageDraw.Draw(combined)

# Try to use a reasonable font, fallback to default
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
except OSError:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

main_title = "linked-views-selection · pygal · pyplots.ai"
subtitle = (
    f"Linked Views: Selecting '{selected_category}' highlights across all views | Click any view to see selection sync"
)

# Draw centered title
title_bbox = draw.textbbox((0, 0), main_title, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
draw.text(((combined_width - title_width) // 2, 25), main_title, fill="#333333", font=title_font)

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
