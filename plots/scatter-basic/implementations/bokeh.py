"""pyplots.ai
scatter-basic: Basic Scatter Plot
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-22
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, output_file, save


# Data - Study hours vs exam scores (realistic scenario)
np.random.seed(42)
study_hours = np.random.uniform(1, 10, 100)
exam_scores = study_hours * 8 + np.random.randn(100) * 5 + 20
exam_scores = np.clip(exam_scores, 0, 100)

# Create ColumnDataSource
source = ColumnDataSource(data={"study_hours": study_hours, "exam_scores": exam_scores})

# Create figure (4800 x 2700 px for 16:9 aspect ratio)
p = figure(
    width=4800,
    height=2700,
    title="scatter-basic · bokeh · pyplots.ai",
    x_axis_label="Study Hours (hrs)",
    y_axis_label="Exam Score (%)",
)

# Plot scatter points (size increased for visibility on large canvas)
p.scatter(x="study_hours", y="exam_scores", source=source, size=28, color="#306998", alpha=0.7)

# Add HoverTool for interactivity (key Bokeh distinctive feature)
hover = HoverTool(tooltips=[("Study Hours", "@study_hours{0.1} hrs"), ("Exam Score", "@exam_scores{0.1}%")])
p.add_tools(hover)

# Styling (scaled for 4800x2700 px canvas)
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_dash = "dashed"

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML (interactive)
output_file("plot.html")
save(p)
