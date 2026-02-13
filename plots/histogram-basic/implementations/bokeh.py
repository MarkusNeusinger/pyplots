""" pyplots.ai
histogram-basic: Basic Histogram
Library: bokeh 3.8.2 | Python 3.14.0
Quality: 88/100 | Created: 2025-12-23
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, Label, NumeralTickFormatter, Span
from bokeh.plotting import figure


# Data - Marathon finish times in minutes (right-skewed with bimodal character and outliers)
np.random.seed(42)
main_group = np.random.normal(loc=240, scale=30, size=380)
slower_group = np.random.normal(loc=305, scale=18, size=100)
outliers = np.random.normal(loc=370, scale=12, size=20)
values = np.concatenate([main_group, slower_group, outliers])
values = values[(values > 120) & (values < 420)]

# Statistics for annotations
median_val = np.median(values)
mean_val = np.mean(values)

# Calculate histogram bins
counts, edges = np.histogram(values, bins=28)
left_edges = edges[:-1]
right_edges = edges[1:]

# Color gradient: darker bins near peak for visual emphasis
max_count = counts.max()
base_r, base_g, base_b = 0x30, 0x69, 0x98  # #306998
highlight_r, highlight_g, highlight_b = 0x4A, 0x8B, 0xBE  # lighter complement
bar_colors = []
bar_alphas = []
for c in counts:
    ratio = c / max_count if max_count > 0 else 0
    r = int(highlight_r + (base_r - highlight_r) * ratio)
    g = int(highlight_g + (base_g - highlight_g) * ratio)
    b = int(highlight_b + (base_b - highlight_b) * ratio)
    bar_colors.append(f"#{r:02x}{g:02x}{b:02x}")
    bar_alphas.append(0.65 + 0.30 * ratio)

source = ColumnDataSource(
    data={
        "left": left_edges,
        "right": right_edges,
        "top": counts,
        "bottom": [0] * len(counts),
        "count": counts,
        "bin_start": [f"{e:.0f}" for e in left_edges],
        "bin_end": [f"{e:.0f}" for e in right_edges],
        "bar_color": bar_colors,
        "bar_alpha": bar_alphas,
    }
)

# Create figure (4800 x 2700 px) with tighter margins for better canvas use
p = figure(
    width=4800,
    height=2700,
    title="histogram-basic · bokeh · pyplots.ai",
    x_axis_label="Finish Time (min)",
    y_axis_label="Number of Runners",
    toolbar_location=None,
    x_range=(118, 422),
)

# Plot histogram as quad glyphs with intensity-mapped colors
p.quad(
    left="left",
    right="right",
    top="top",
    bottom="bottom",
    source=source,
    fill_color="bar_color",
    line_color="white",
    line_width=1.5,
    fill_alpha="bar_alpha",
    hover_fill_color="#FFD43B",
    hover_fill_alpha=0.95,
    hover_line_color="white",
)

# HoverTool - Bokeh's distinctive interactive feature
hover = HoverTool(tooltips=[("Range", "@bin_start–@bin_end min"), ("Runners", "@count")], mode="mouse")
p.add_tools(hover)

# Annotation: median line (solid red)
median_span = Span(
    location=median_val, dimension="height", line_color="#C0392B", line_width=3.5, line_dash="solid", line_alpha=0.8
)
p.add_layout(median_span)

# Annotation: mean line (dashed teal)
mean_span = Span(
    location=mean_val, dimension="height", line_color="#1A9E76", line_width=3.5, line_dash=[10, 5], line_alpha=0.8
)
p.add_layout(mean_span)

# Place median/mean labels in upper-right clear area away from bars
median_label = Label(
    x=330,
    y=max_count * 0.95,
    text=f"\u2500\u2500  Median: {median_val:.0f} min",
    text_font_size="24pt",
    text_color="#C0392B",
    text_font_style="bold",
)
p.add_layout(median_label)

mean_label = Label(
    x=330,
    y=max_count * 0.85,
    text=f"- -  Mean: {mean_val:.0f} min",
    text_font_size="24pt",
    text_color="#1A9E76",
    text_font_style="bold",
)
p.add_layout(mean_label)

# Annotation: label the main peak with an arrow-like callout above the bars
peak_label = Label(
    x=200,
    y=max_count * 1.02,
    text="\u25bc Main group (~4 hr pace)",
    text_font_size="22pt",
    text_color="#306998",
    text_font_style="bold",
)
p.add_layout(peak_label)

# Annotation: slower group shoulder label above bars
shoulder_label = Label(
    x=300,
    y=max_count * 0.60,
    text="\u25bc Slower group (~5 hr pace)",
    text_font_size="22pt",
    text_color="#7BA1BB",
    text_font_style="bold",
)
p.add_layout(shoulder_label)

# Subtitle with dataset context
subtitle = Label(
    x=130,
    y=max_count * 1.10,
    text=f"N = {len(values)} runners  \u2502  Right-skewed bimodal distribution",
    text_font_size="22pt",
    text_color="#777777",
)
p.add_layout(subtitle)

# Typography hierarchy for 4800x2700 canvas
p.title.text_font_size = "38pt"
p.title.text_color = "#222222"
p.title.text_font_style = "bold"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.axis_label_text_color = "#444444"
p.yaxis.axis_label_text_color = "#444444"
p.xaxis.major_label_text_font_size = "22pt"
p.yaxis.major_label_text_font_size = "22pt"
p.xaxis.major_label_text_color = "#555555"
p.yaxis.major_label_text_color = "#555555"

# Format y-axis with comma separator for readability
p.yaxis.formatter = NumeralTickFormatter(format="0,0")

# Grid styling - y-axis only, very subtle
p.xgrid.visible = False
p.ygrid.grid_line_alpha = 0.15
p.ygrid.grid_line_color = "#CCCCCC"
p.ygrid.grid_line_width = 1

# Clean frame — remove top/right spines via axis visibility
p.outline_line_color = None
p.background_fill_color = "white"
p.border_fill_color = "white"
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2
p.xaxis.axis_line_color = "#AAAAAA"
p.yaxis.axis_line_color = "#AAAAAA"
p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None
p.xaxis.major_tick_line_color = "#AAAAAA"
p.yaxis.major_tick_line_color = "#AAAAAA"

# Y-axis starts at zero with headroom for annotations
p.y_range.start = 0
p.y_range.end = max_count * 1.22

# Balanced margins for full canvas utilization
p.min_border_left = 140
p.min_border_right = 80
p.min_border_bottom = 110
p.min_border_top = 80

# Save outputs
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
