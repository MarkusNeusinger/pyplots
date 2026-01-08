""" pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import os
import tempfile

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_bar,
    geom_histogram,
    geom_point,
    geom_vline,
    ggplot,
    labs,
    position_dodge,
    scale_alpha_identity,
    scale_color_manual,
    scale_fill_manual,
    theme,
    theme_minimal,
)


# Data - Multivariate dataset with 3 clusters
np.random.seed(42)
n_per_cluster = 50

categories = np.repeat(["Cluster A", "Cluster B", "Cluster C"], n_per_cluster)

x = np.concatenate(
    [
        np.random.normal(2.5, 0.6, n_per_cluster),
        np.random.normal(5.5, 0.7, n_per_cluster),
        np.random.normal(4.0, 0.8, n_per_cluster),
    ]
)

y = np.concatenate(
    [
        np.random.normal(3.0, 0.5, n_per_cluster),
        np.random.normal(5.5, 0.6, n_per_cluster),
        np.random.normal(2.0, 0.7, n_per_cluster),
    ]
)

value = np.concatenate(
    [
        np.random.normal(30, 6, n_per_cluster),
        np.random.normal(55, 8, n_per_cluster),
        np.random.normal(42, 7, n_per_cluster),
    ]
)

# Selection: x > 4.5 (selects Cluster B and part of Cluster C)
selection_threshold = 4.5
selected = x > selection_threshold

# Create main dataframe
df = pd.DataFrame(
    {
        "x": x,
        "y": y,
        "category": categories,
        "value": value,
        "selected": selected,
        "Selection": np.where(selected, "Selected", "Unselected"),
        "point_alpha": np.where(selected, 0.9, 0.35),
    }
)

n_selected = int(selected.sum())
n_total = len(df)

# Colors - Python Blue/Yellow colorblind-safe
color_selected = "#306998"
color_unselected = "#AAAAAA"
color_threshold = "#FFD43B"
colors = {"Selected": color_selected, "Unselected": color_unselected}

# Common theme for all plots with larger sizes for visibility
base_theme = theme_minimal() + theme(
    figure_size=(8, 7),
    text=element_text(size=16),
    axis_title=element_text(size=22),
    axis_text=element_text(size=16),
    plot_title=element_text(size=24, weight="bold"),
    legend_position="none",
    panel_grid_major=element_line(color="#E0E0E0", size=0.4),
    panel_grid_minor=element_blank(),
    plot_background=element_rect(fill="white", color="white"),
    panel_background=element_rect(fill="white"),
)

# View 1: Scatter Plot (x vs y) - Selection source
p1 = (
    ggplot(df, aes("x", "y", color="Selection", alpha="point_alpha"))
    + geom_point(size=5)
    + geom_vline(xintercept=selection_threshold, linetype="dashed", color=color_threshold, size=2)
    + scale_color_manual(values=colors)
    + scale_alpha_identity()
    + labs(title="Scatter Plot (X vs Y)", x="X Value", y="Y Value")
    + base_theme
)

# View 2: Histogram of Value distribution
p2 = (
    ggplot(df, aes("value", fill="Selection"))
    + geom_histogram(bins=15, position="identity", color="white", size=0.4, alpha=0.75)
    + scale_fill_manual(values=colors)
    + labs(title="Value Distribution", x="Value", y="Count")
    + base_theme
)

# View 3: Bar chart by category showing selection breakdown
bar_data = df.groupby(["category", "Selection"]).size().reset_index(name="count")

p3 = (
    ggplot(bar_data, aes("category", "count", fill="Selection"))
    + geom_bar(stat="identity", position=position_dodge(width=0.8), width=0.7, color="white", size=0.6)
    + scale_fill_manual(values=colors)
    + labs(title="Category Breakdown", x="Category", y="Count")
    + base_theme
    + theme(axis_text_x=element_text(size=16))
)

# Save individual plots to temp files
temp_dir = tempfile.mkdtemp()
p1.save(os.path.join(temp_dir, "p1.png"), dpi=200, verbose=False)
p2.save(os.path.join(temp_dir, "p2.png"), dpi=200, verbose=False)
p3.save(os.path.join(temp_dir, "p3.png"), dpi=200, verbose=False)

# Load images
img1 = Image.open(os.path.join(temp_dir, "p1.png"))
img2 = Image.open(os.path.join(temp_dir, "p2.png"))
img3 = Image.open(os.path.join(temp_dir, "p3.png"))

# Target size: 4800 x 2700 (16:9)
final_width = 4800
final_height = 2700

# Create final canvas
final = Image.new("RGB", (final_width, final_height), "white")

# Layout: top row has 2 plots side by side, bottom row has 1 centered plot
# Calculate panel sizes to fill canvas well
top_panel_width = 2200
top_panel_height = 1250
bottom_panel_width = 2800
bottom_panel_height = 1100

# Resize panels maintaining aspect ratio by using LANCZOS
img1_resized = img1.resize((top_panel_width, top_panel_height), Image.Resampling.LANCZOS)
img2_resized = img2.resize((top_panel_width, top_panel_height), Image.Resampling.LANCZOS)
img3_resized = img3.resize((bottom_panel_width, bottom_panel_height), Image.Resampling.LANCZOS)

# Position panels
title_space = 180
panel_gap = 50

# Top row: two panels side by side
left_margin = (final_width - 2 * top_panel_width - panel_gap) // 2
final.paste(img1_resized, (left_margin, title_space))
final.paste(img2_resized, (left_margin + top_panel_width + panel_gap, title_space))

# Bottom row: one centered panel
bottom_left = (final_width - bottom_panel_width) // 2
final.paste(img3_resized, (bottom_left, title_space + top_panel_height + panel_gap))

# Add title and subtitle using PIL
draw = ImageDraw.Draw(final)

# Load fonts (with fallback)
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    legend_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
except OSError:
    title_font = ImageFont.load_default()
    subtitle_font = title_font
    legend_font = title_font

# Draw main title
title = "linked-views-selection · plotnine · pyplots.ai"
title_bbox = draw.textbbox((0, 0), title, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
draw.text(((final_width - title_width) // 2, 30), title, fill="#333333", font=title_font)

# Draw subtitle with selection info
subtitle = f"Selection: x > {selection_threshold} highlights {n_selected}/{n_total} points across all views"
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
draw.text(((final_width - subtitle_width) // 2, 105), subtitle, fill="#666666", font=subtitle_font)

# Add legend at bottom center
legend_y = final_height - 70
legend_box_size = 35

# Calculate centered legend position
legend_text_selected = "Selected"
legend_text_unselected = "Unselected"
selected_bbox = draw.textbbox((0, 0), legend_text_selected, font=legend_font)
unselected_bbox = draw.textbbox((0, 0), legend_text_unselected, font=legend_font)
total_legend_width = (
    legend_box_size
    + 10
    + (selected_bbox[2] - selected_bbox[0])
    + 80
    + legend_box_size
    + 10
    + (unselected_bbox[2] - unselected_bbox[0])
)
legend_x = (final_width - total_legend_width) // 2

# Selected legend item
draw.rectangle([legend_x, legend_y, legend_x + legend_box_size, legend_y + legend_box_size], fill=color_selected)
draw.text((legend_x + legend_box_size + 10, legend_y - 2), legend_text_selected, fill="#333333", font=legend_font)

# Unselected legend item
unselected_x = legend_x + legend_box_size + 10 + (selected_bbox[2] - selected_bbox[0]) + 80
draw.rectangle(
    [unselected_x, legend_y, unselected_x + legend_box_size, legend_y + legend_box_size], fill=color_unselected
)
draw.text((unselected_x + legend_box_size + 10, legend_y - 2), legend_text_unselected, fill="#333333", font=legend_font)

# Save final composite image
final.save("plot.png")

# Cleanup temp files
for fname in ["p1.png", "p2.png", "p3.png"]:
    try:
        os.remove(os.path.join(temp_dir, fname))
    except OSError:
        pass
try:
    os.rmdir(temp_dir)
except OSError:
    pass
