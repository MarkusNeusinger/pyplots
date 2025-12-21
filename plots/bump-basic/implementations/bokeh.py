""" pyplots.ai
bump-basic: Basic Bump Chart
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-17
"""

from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Legend
from bokeh.palettes import Category10
from bokeh.plotting import figure


# Data - Sports league standings over a season
entities = ["Team Alpha", "Team Beta", "Team Gamma", "Team Delta", "Team Epsilon"]
periods = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"]

# Rankings for each team across weeks (1 = best)
rankings = {
    "Team Alpha": [3, 2, 1, 1, 2, 1],
    "Team Beta": [1, 1, 2, 3, 3, 4],
    "Team Gamma": [5, 4, 4, 2, 1, 2],
    "Team Delta": [2, 3, 3, 4, 4, 3],
    "Team Epsilon": [4, 5, 5, 5, 5, 5],
}

# Colors for each team
colors = Category10[5]

# Create figure with inverted y-axis (rank 1 at top)
p = figure(
    width=4800,
    height=2700,
    title="bump-basic · bokeh · pyplots.ai",
    x_range=periods,
    y_range=(5.5, 0.5),  # Inverted: rank 1 at top
    x_axis_label="Period",
    y_axis_label="Rank",
)

# Plot lines and markers for each entity
legend_items = []
for i, (entity, ranks) in enumerate(rankings.items()):
    source = ColumnDataSource(data={"x": periods, "y": ranks})

    # Draw connecting lines
    line = p.line(x="x", y="y", source=source, line_width=4, line_color=colors[i], line_alpha=0.8)

    # Draw dot markers at each period
    scatter = p.scatter(x="x", y="y", source=source, size=20, color=colors[i], alpha=0.9)

    legend_items.append((entity, [line, scatter]))

# Add legend outside the plot
legend = Legend(items=legend_items, location="center")
legend.label_text_font_size = "18pt"
legend.spacing = 10
p.add_layout(legend, "right")

# Style title
p.title.text_font_size = "28pt"

# Style axes
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = "dashed"
p.ygrid.grid_line_dash = "dashed"

# Background styling
p.background_fill_color = "#fafafa"
p.border_fill_color = "white"

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML (interactive version)
output_file("plot.html")
save(p)
