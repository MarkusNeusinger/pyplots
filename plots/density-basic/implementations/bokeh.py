"""pyplots.ai
density-basic: Basic Density Plot
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Response times (ms) for a web service
np.random.seed(42)
response_times = np.concatenate(
    [
        np.random.normal(150, 30, 300),  # Fast responses
        np.random.normal(280, 40, 100),  # Slower responses (shows bimodality)
    ]
)

# Calculate kernel density estimation (Silverman's rule for bandwidth)
n = len(response_times)
std = np.std(response_times)
iqr = np.percentile(response_times, 75) - np.percentile(response_times, 25)
bandwidth = 0.9 * min(std, iqr / 1.34) * n ** (-0.2)

# Evaluate density on a grid
x_range = np.linspace(response_times.min() - 40, response_times.max() + 40, 500)
density = np.zeros_like(x_range)
for xi in response_times:
    density += np.exp(-0.5 * ((x_range - xi) / bandwidth) ** 2)
density /= n * bandwidth * np.sqrt(2 * np.pi)

# Create data source
source = ColumnDataSource(data={"x": x_range, "density": density})

# Rug plot data (individual observations)
rug_y_pos = -0.0004  # Position below x-axis
rug_source = ColumnDataSource(
    data={
        "x": response_times,
        "y0": np.full_like(response_times, rug_y_pos),
        "y1": np.full_like(response_times, rug_y_pos + 0.0004),
    }
)

# Create figure (4800 x 2700 px for 16:9 landscape)
p = figure(
    width=4800,
    height=2700,
    title="density-basic · bokeh · pyplots.ai",
    x_axis_label="Response Time (ms)",
    y_axis_label="Density",
)

# Fill under the curve
p.varea(x="x", y1=0, y2="density", source=source, fill_color="#306998", fill_alpha=0.35)

# Density curve
p.line(x="x", y="density", source=source, line_color="#306998", line_width=5, line_alpha=0.95)

# Rug plot - vertical segments at bottom
p.segment(x0="x", y0="y0", x1="x", y1="y1", source=rug_source, line_color="#306998", line_width=2, line_alpha=0.5)

# Style text sizes for large canvas (scaled up)
p.title.text_font_size = "36pt"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "22pt"
p.yaxis.major_label_text_font_size = "22pt"

# Axis styling
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2
p.xaxis.major_tick_line_width = 2
p.yaxis.major_tick_line_width = 2

# Grid styling
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = "dashed"
p.ygrid.grid_line_dash = "dashed"

# Background
p.background_fill_color = "#fafafa"
p.border_fill_color = "#ffffff"

# Remove toolbar
p.toolbar_location = None

# Save
export_png(p, filename="plot.png")
