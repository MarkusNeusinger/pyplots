"""anyplot.ai
scatter-basic: Basic Scatter Plot
Library: bokeh 3.9.0 | Python 3.14.4
"""

import os

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import Band, ColumnDataSource, HoverTool, Label, Slope
from bokeh.plotting import figure


# Theme-adaptive chrome tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
BRAND = "#009E73"  # Okabe-Ito position 1

# Data - Study hours vs exam scores (realistic scenario)
np.random.seed(42)
n_points = 100
study_hours = np.random.uniform(1, 10, n_points)
exam_scores = study_hours * 7 + np.random.randn(n_points) * 6 + 25

# Natural outliers (over/under-performers)
exam_scores[5] = 38
exam_scores[22] = 92
exam_scores[47] = 30
exam_scores[71] = 95
exam_scores[88] = 42

exam_scores = np.clip(exam_scores, 15, 98)

# Linear regression for trend line and R²
coeffs = np.polyfit(study_hours, exam_scores, 1)
predicted = np.polyval(coeffs, study_hours)
ss_res = np.sum((exam_scores - predicted) ** 2)
ss_tot = np.sum((exam_scores - np.mean(exam_scores)) ** 2)
r_squared = 1 - ss_res / ss_tot

# Confidence band (sorted for Band glyph)
sort_idx = np.argsort(study_hours)
x_sorted = study_hours[sort_idx]
y_pred_sorted = np.polyval(coeffs, x_sorted)
residual_std = np.std(exam_scores - predicted)
band_source = ColumnDataSource(
    data={"x": x_sorted, "upper": y_pred_sorted + 1.5 * residual_std, "lower": y_pred_sorted - 1.5 * residual_std}
)

source = ColumnDataSource(data={"study_hours": study_hours, "exam_scores": exam_scores})

p = figure(
    width=4800,
    height=2700,
    title="scatter-basic · bokeh · anyplot.ai",
    x_axis_label="Study Hours per Day",
    y_axis_label="Exam Score (%)",
    toolbar_location=None,
    x_range=(0.5, 10.5),
    y_range=(10, 105),
)

# Confidence band (Bokeh-distinctive Band glyph)
band = Band(
    base="x",
    lower="lower",
    upper="upper",
    source=band_source,
    level="underlay",
    fill_alpha=0.10,
    fill_color=BRAND,
    line_width=0,
)
p.add_layout(band)

# Trend line (Bokeh-distinctive Slope model)
trend = Slope(
    gradient=coeffs[0], y_intercept=coeffs[1], line_color=INK_SOFT, line_width=4, line_alpha=0.75, line_dash="dashed"
)
p.add_layout(trend)

# Scatter points
p.scatter(
    x="study_hours", y="exam_scores", source=source, size=45, color=BRAND, alpha=0.7, line_color=PAGE_BG, line_width=2
)

# HoverTool for HTML export (Bokeh-distinctive interactivity)
hover = HoverTool(tooltips=[("Study Hours", "@study_hours{0.0}"), ("Exam Score", "@exam_scores{0.0}%")], mode="mouse")
p.add_tools(hover)

# R² annotation (Bokeh-native Label)
r2_label = Label(
    x=0.8, y=98, text=f"R² = {r_squared:.3f}", text_font_size="42pt", text_color=INK, text_font_style="italic"
)
p.add_layout(r2_label)

# Subtitle for storytelling
subtitle = Label(
    x=0.8, y=91, text="Positive correlation — shaded band shows ±1.5σ", text_font_size="32pt", text_color=INK_SOFT
)
p.add_layout(subtitle)

# Typography scaled for 4800x2700
p.title.text_font_size = "56pt"
p.title.text_color = INK
p.xaxis.axis_label_text_font_size = "40pt"
p.yaxis.axis_label_text_font_size = "40pt"
p.xaxis.major_label_text_font_size = "30pt"
p.yaxis.major_label_text_font_size = "30pt"

# Theme-adaptive chrome
p.xaxis.axis_label_text_color = INK
p.yaxis.axis_label_text_color = INK
p.xaxis.major_label_text_color = INK_SOFT
p.yaxis.major_label_text_color = INK_SOFT
p.xaxis.axis_line_color = INK_SOFT
p.yaxis.axis_line_color = INK_SOFT
p.xaxis.major_tick_line_color = INK_SOFT
p.yaxis.major_tick_line_color = INK_SOFT
p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None

p.xgrid.grid_line_color = INK
p.ygrid.grid_line_color = INK
p.xgrid.grid_line_alpha = 0.10
p.ygrid.grid_line_alpha = 0.10

p.background_fill_color = PAGE_BG
p.border_fill_color = PAGE_BG
p.outline_line_color = None

p.xaxis.ticker.desired_num_ticks = 10
p.yaxis.ticker.desired_num_ticks = 8

# Dual output: PNG + interactive HTML
export_png(p, filename=f"plot-{THEME}.png")
output_file(f"plot-{THEME}.html")
save(p)
