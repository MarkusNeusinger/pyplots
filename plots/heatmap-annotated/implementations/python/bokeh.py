""" anyplot.ai
heatmap-annotated: Annotated Heatmap
Library: bokeh 3.9.0 | Python 3.13.13
Quality: 84/100 | Updated: 2026-05-06
"""

import os
import sys
import time
from pathlib import Path

import numpy as np


# Ensure we import the installed bokeh, not a local module with the same name
sys.path.insert(0, "/home/runner/work/anyplot/anyplot/.venv/lib/python3.13/site-packages")

from bokeh.io import output_file, save
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, HoverTool, LinearColorMapper
from bokeh.palettes import BrBG11
from bokeh.plotting import figure
from bokeh.transform import transform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"

# Data: Correlation matrix for financial metrics
np.random.seed(42)
variables = ["Revenue", "Profit", "Assets", "Debt", "Growth", "ROI", "Market Cap", "Volume"]
n = len(variables)

# Generate realistic correlation matrix
base = np.random.randn(100, n)
base[:, 1] = base[:, 0] * 0.8 + np.random.randn(100) * 0.5
base[:, 5] = base[:, 1] * 0.7 + np.random.randn(100) * 0.6
base[:, 6] = base[:, 0] * 0.6 + np.random.randn(100) * 0.7
base[:, 3] = -base[:, 5] * 0.5 + np.random.randn(100) * 0.8
corr_matrix = np.corrcoef(base.T)
np.fill_diagonal(corr_matrix, 1.0)

# Prepare data for bokeh
x_coords = []
y_coords = []
values = []
text_values = []
text_colors = []

for i, row_var in enumerate(variables):
    for j, col_var in enumerate(variables):
        x_coords.append(col_var)
        y_coords.append(row_var)
        val = corr_matrix[i, j]
        values.append(val)
        text_values.append(f"{val:.2f}")
        text_colors.append("white" if abs(val) > 0.5 else "black")

source = ColumnDataSource(
    data={"x": x_coords, "y": y_coords, "value": values, "text": text_values, "text_color": text_colors}
)

# Create color mapper with diverging palette
mapper = LinearColorMapper(palette=BrBG11, low=-1, high=1)

# Create figure
p = figure(
    width=3600,
    height=3600,
    x_range=variables,
    y_range=list(reversed(variables)),
    title="heatmap-annotated · bokeh · anyplot.ai",
    x_axis_location="above",
    toolbar_location=None,
)

# Add heatmap rectangles
p.rect(
    x="x",
    y="y",
    width=1,
    height=1,
    source=source,
    fill_color=transform("value", mapper),
    line_color="white",
    line_width=2,
)

# Add text annotations
p.text(
    x="x",
    y="y",
    text="text",
    source=source,
    text_align="center",
    text_baseline="middle",
    text_font_size="24pt",
    text_color="text_color",
)

# Add hover tooltip for interactivity
hover = HoverTool(
    tooltips=[("Row Metric", "@y"), ("Column Metric", "@x"), ("Pearson Correlation", "@value{0.00}")], mode="mouse"
)
p.add_tools(hover)

# Style the figure
p.background_fill_color = PAGE_BG
p.border_fill_color = PAGE_BG
p.outline_line_color = INK_SOFT

p.title.text_font_size = "32pt"
p.title.text_color = INK
p.title.align = "center"

p.xaxis.axis_label = "Financial Metric"
p.yaxis.axis_label = "Financial Metric"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.axis_label_text_color = INK
p.yaxis.axis_label_text_color = INK
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"
p.xaxis.major_label_text_color = INK_SOFT
p.yaxis.major_label_text_color = INK_SOFT
p.xaxis.axis_line_color = INK_SOFT
p.yaxis.axis_line_color = INK_SOFT
p.xaxis.major_tick_line_color = None
p.yaxis.major_tick_line_color = None
p.xaxis.major_label_orientation = 0.7
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.grid.grid_line_color = None

# Add colorbar
color_bar = ColorBar(
    color_mapper=mapper,
    ticker=BasicTicker(desired_num_ticks=9),
    label_standoff=12,
    major_label_text_font_size="16pt",
    title="Pearson Correlation",
    title_text_font_size="20pt",
    width=40,
    location=(0, 0),
)
p.add_layout(color_bar, "right")


# Save
output_file(f"plot-{THEME}.html")
save(p)

# Screenshot with headless Chrome
W, H = 3600, 3600
opts = Options()
for arg in (
    "--headless=new",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    f"--window-size={W},{H}",
    "--hide-scrollbars",
):
    opts.add_argument(arg)
driver = webdriver.Chrome(options=opts)
driver.set_window_size(W, H)
driver.get(f"file://{Path(f'plot-{THEME}.html').resolve()}")
time.sleep(3)
driver.save_screenshot(f"plot-{THEME}.png")
driver.quit()
