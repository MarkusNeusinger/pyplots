"""pyplots.ai
band-basic: Basic Band Plot
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Time series with 95% confidence interval
np.random.seed(42)
x = np.linspace(0, 10, 100)
y_center = 2 + 0.5 * x + 0.3 * np.sin(2 * x)  # Central trend with slight oscillation
uncertainty = 0.5 + 0.1 * x  # Growing uncertainty over time
y_upper = y_center + 1.96 * uncertainty  # 95% CI upper bound
y_lower = y_center - 1.96 * uncertainty  # 95% CI lower bound

# Create ColumnDataSource for band (patch requires closed polygon)
x_band = np.concatenate([x, x[::-1]])
y_band = np.concatenate([y_upper, y_lower[::-1]])
band_source = ColumnDataSource(data={"x": x_band, "y": y_band})

# Create ColumnDataSource for center line
line_source = ColumnDataSource(data={"x": x, "y": y_center})

# Create figure (4800 × 2700 px)
p = figure(width=4800, height=2700, title="band-basic · bokeh · pyplots.ai", x_axis_label="Time", y_axis_label="Value")

# Plot band (semi-transparent fill)
p.patch(
    x="x",
    y="y",
    source=band_source,
    fill_color="#306998",
    fill_alpha=0.3,
    line_color="#306998",
    line_alpha=0.5,
    line_width=2,
    legend_label="95% Confidence Interval",
)

# Plot center line
p.line(x="x", y="y", source=line_source, line_color="#FFD43B", line_width=4, legend_label="Mean Trend")

# Styling for 4800×2700 px
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_dash = [6, 4]

# Legend styling
p.legend.label_text_font_size = "18pt"
p.legend.location = "top_left"
p.legend.background_fill_alpha = 0.7

# Save as PNG and HTML
export_png(p, filename="plot.png")
save(p, filename="plot.html", title="band-basic · bokeh · pyplots.ai")
