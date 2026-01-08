""" pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 75/100 | Created: 2026-01-08
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from plotnine import (
    aes,
    element_blank,
    element_line,
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
    scale_size_identity,
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

# Selection: x > 4.5 (roughly selects Cluster B)
selection_threshold = 4.5
selected = x > selection_threshold

df = pd.DataFrame(
    {
        "x": x,
        "y": y,
        "category": categories,
        "value": value,
        "selected": selected,
        "selection_state": np.where(selected, "Selected", "Unselected"),
        "point_alpha": np.where(selected, 0.9, 0.25),
        "point_size": np.where(selected, 5, 3),
    }
)

n_selected = int(selected.sum())
n_total = len(df)

# Colors
color_selected = "#306998"
color_unselected = "#CCCCCC"
color_highlight = "#FFD43B"

# Shared theme
shared_theme = theme_minimal() + theme(
    text=element_text(size=14),
    axis_title=element_text(size=18),
    axis_text=element_text(size=14),
    plot_title=element_text(size=18, weight="bold", hjust=0.5),
    legend_text=element_text(size=14),
    legend_title=element_text(size=16),
    legend_position="none",
    panel_grid_major=element_line(color="#E5E5E5", size=0.5),
    panel_grid_minor=element_blank(),
)

color_scale = scale_color_manual(values={"Selected": color_selected, "Unselected": color_unselected})
fill_scale = scale_fill_manual(values={"Selected": color_selected, "Unselected": color_unselected})

# View 1: Scatter Plot (x vs y)
plot1 = (
    ggplot(df, aes("x", "y", color="selection_state", alpha="point_alpha", size="point_size"))
    + geom_point()
    + geom_vline(xintercept=selection_threshold, linetype="dashed", color=color_highlight, size=1.2)
    + color_scale
    + scale_alpha_identity()
    + scale_size_identity()
    + labs(title="Scatter Plot", x="X Coordinate", y="Y Coordinate")
    + shared_theme
)

# View 2: Histogram of Value by Selection
plot2 = (
    ggplot(df, aes("value", fill="selection_state", alpha="point_alpha"))
    + geom_histogram(bins=20, position="identity")
    + fill_scale
    + scale_alpha_identity()
    + labs(title="Value Distribution", x="Value", y="Count")
    + shared_theme
)

# View 3: Bar chart - Count by Category and Selection
count_df = df.groupby(["category", "selection_state"]).size().reset_index(name="count")

plot3 = (
    ggplot(count_df, aes("category", "count", fill="selection_state"))
    + geom_bar(stat="identity", position=position_dodge(width=0.8), width=0.7)
    + fill_scale
    + labs(title="Count by Category", x="Category", y="Count")
    + shared_theme
    + theme(axis_text_x=element_text(size=14))
)

# Save individual plots
plot1.save("_temp1.png", dpi=300, width=16, height=5, verbose=False)
plot2.save("_temp2.png", dpi=300, width=8, height=5, verbose=False)
plot3.save("_temp3.png", dpi=300, width=8, height=5, verbose=False)

# Load and combine
img1 = Image.open("_temp1.png")
img2 = Image.open("_temp2.png")
img3 = Image.open("_temp3.png")

# Calculate dimensions for 16:9 final output at 300 DPI
final_width = 4800
final_height = 2700

# Create final canvas
final_img = Image.new("RGB", (final_width, final_height), "white")

# Title area height
title_height = 200

# Scale and paste images
# Top row: scatter plot (full width)
img1_scaled = img1.resize((final_width, (final_height - title_height) // 2), Image.Resampling.LANCZOS)
final_img.paste(img1_scaled, (0, title_height))

# Bottom row: histogram and bar chart (half width each)
bottom_y = title_height + (final_height - title_height) // 2
half_width = final_width // 2
bottom_height = (final_height - title_height) // 2

img2_scaled = img2.resize((half_width, bottom_height), Image.Resampling.LANCZOS)
img3_scaled = img3.resize((half_width, bottom_height), Image.Resampling.LANCZOS)

final_img.paste(img2_scaled, (0, bottom_y))
final_img.paste(img3_scaled, (half_width, bottom_y))

# Add title using PIL
draw = ImageDraw.Draw(final_img)
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
except OSError:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

title_text = "linked-views-selection · plotnine · pyplots.ai"
subtitle_text = f"Selection: x > {selection_threshold} ({n_selected}/{n_total} points selected)"

# Center title
title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
draw.text(((final_width - title_width) // 2, 30), title_text, fill="black", font=title_font)

subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
draw.text(((final_width - subtitle_width) // 2, 110), subtitle_text, fill="#666666", font=subtitle_font)

# Add legend
legend_y = 170
legend_x_start = final_width // 2 - 200
# Selected box
draw.rectangle([legend_x_start, legend_y, legend_x_start + 30, legend_y + 20], fill=color_selected)
draw.text((legend_x_start + 40, legend_y - 5), "Selected", fill="black", font=subtitle_font)
# Unselected box
draw.rectangle([legend_x_start + 200, legend_y, legend_x_start + 230, legend_y + 20], fill=color_unselected)
draw.text((legend_x_start + 240, legend_y - 5), "Unselected", fill="black", font=subtitle_font)

final_img.save("plot.png")

# Cleanup temp files
os.remove("_temp1.png")
os.remove("_temp2.png")
os.remove("_temp3.png")

plt.close("all")
