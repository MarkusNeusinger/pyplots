"""pyplots.ai
residual-basic: Residual Plot
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, Span
from bokeh.plotting import figure


# Data - Simulate regression residuals from house price model
np.random.seed(42)
n_points = 150

# Generate fitted values (predictions from a housing price model)
fitted = np.linspace(150, 500, n_points) + np.random.randn(n_points) * 20

# Generate residuals with slight heteroscedasticity pattern for realism
base_residuals = np.random.randn(n_points) * 25
heteroscedasticity = 0.03 * (fitted - 325) * np.random.randn(n_points)
residuals = base_residuals + heteroscedasticity

# Add a few outliers for realistic diagnostic scenario
residuals[15] = 95
residuals[75] = -80
residuals[120] = 85

# Create ColumnDataSource
source = ColumnDataSource(data={"fitted": fitted, "residuals": residuals})

# Create figure (4800 x 2700 px for 16:9 aspect ratio)
p = figure(width=4800, height=2700, title="residual-basic · bokeh · pyplots.ai")

# Set axis labels
p.xaxis.axis_label = "Fitted Values ($K)"
p.yaxis.axis_label = "Residuals ($K)"

# Add horizontal reference line at y=0
zero_line = Span(location=0, dimension="width", line_color="#333333", line_width=4, line_dash="dashed", line_alpha=0.7)
p.add_layout(zero_line)

# Plot residuals (size scaled for visibility on large canvas)
p.scatter(
    x="fitted", y="residuals", source=source, size=40, color="#306998", alpha=0.6, line_color="#1a3d5c", line_width=2
)

# Add HoverTool for interactivity (key Bokeh distinctive feature)
hover = HoverTool(tooltips=[("Fitted", "@fitted{0.0} $K"), ("Residual", "@residuals{0.0} $K")])
p.add_tools(hover)

# Styling (scaled for 4800x2700 px canvas)
p.title.text_font_size = "72pt"
p.xaxis.axis_label_text_font_size = "48pt"
p.yaxis.axis_label_text_font_size = "48pt"
p.xaxis.major_label_text_font_size = "36pt"
p.yaxis.major_label_text_font_size = "36pt"

# Grid styling (subtle, per quality criteria VQ-07)
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_width = 2
p.grid.grid_line_dash = [6, 4]

# Axis styling
p.xaxis.axis_line_width = 3
p.yaxis.axis_line_width = 3
p.xaxis.major_tick_line_width = 3
p.yaxis.major_tick_line_width = 3

# Set symmetric y-axis range around zero for visual balance
y_max = max(abs(residuals.min()), abs(residuals.max())) * 1.15
p.y_range.start = -y_max
p.y_range.end = y_max

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML (interactive)
output_file("plot.html")
save(p)
