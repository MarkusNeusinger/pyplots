""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: bokeh 3.8.2 | Python 3.14
Quality: 74/100 | Created: 2025-12-22
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
p = figure(width=4800, height=2700, title="scatter-basic \u00b7 bokeh \u00b7 pyplots.ai", toolbar_location=None)

# Set axis labels
p.xaxis.axis_label = "Study Hours (hrs)"
p.yaxis.axis_label = "Exam Score (%)"

# Plot scatter points with white edge for definition
p.scatter(
    x="study_hours",
    y="exam_scores",
    source=source,
    size=30,
    color="#306998",
    alpha=0.7,
    line_color="white",
    line_width=1.5,
)

# HoverTool for interactivity (distinctive Bokeh feature, visible in HTML export)
hover = HoverTool(tooltips=[("Study Hours", "@study_hours{0.1} hrs"), ("Exam Score", "@exam_scores{0.1}%")])
p.add_tools(hover)

# Styling (scaled for 4800x2700 px canvas)
p.title.text_font_size = "72pt"
p.xaxis.axis_label_text_font_size = "48pt"
p.yaxis.axis_label_text_font_size = "48pt"
p.xaxis.major_label_text_font_size = "36pt"
p.yaxis.major_label_text_font_size = "36pt"

# Grid styling (subtle, opacity ~20%)
p.grid.grid_line_alpha = 0.2
p.grid.grid_line_width = 2

# Remove outline border for cleaner look
p.outline_line_color = None

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML (interactive)
output_file("plot.html")
save(p)
