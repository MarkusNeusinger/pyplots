"""pyplots.ai
line-retention-cohort: User Retention Curve by Cohort
Library: bokeh | Python 3.13
Quality: pending | Created: 2026-03-16
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Legend, Span
from bokeh.plotting import figure


# Data
np.random.seed(42)
weeks = np.arange(0, 13)

cohorts = {
    "Jan 2025": {"size": 1245, "decay": 0.18},
    "Feb 2025": {"size": 1380, "decay": 0.16},
    "Mar 2025": {"size": 1520, "decay": 0.14},
    "Apr 2025": {"size": 1410, "decay": 0.12},
    "May 2025": {"size": 1680, "decay": 0.10},
}

retention_data = {}
for cohort, params in cohorts.items():
    base = 100 * np.exp(-params["decay"] * weeks)
    noise = np.random.normal(0, 1.5, len(weeks))
    retention = np.clip(base + noise, 0, 100)
    retention[0] = 100.0
    retention_data[cohort] = retention

# Plot
colors = ["#8FAFC1", "#7B9DB7", "#5A8BA8", "#306998", "#1A4D6E"]
line_widths = [3, 3.5, 4, 4.5, 5]
alphas = [0.55, 0.65, 0.75, 0.85, 1.0]

p = figure(
    width=4800,
    height=2700,
    title="line-retention-cohort · bokeh · pyplots.ai",
    x_axis_label="Weeks Since Signup",
    y_axis_label="Retention Rate (%)",
)

legend_items = []
for i, (cohort, params) in enumerate(cohorts.items()):
    source = ColumnDataSource(data={"week": weeks, "retention": retention_data[cohort]})
    label = f"{cohort} (n={params['size']:,})"

    line = p.line(
        x="week", y="retention", source=source, line_width=line_widths[i], line_color=colors[i], line_alpha=alphas[i]
    )
    scatter = p.scatter(
        x="week",
        y="retention",
        source=source,
        size=12 + i * 2,
        fill_color=colors[i],
        fill_alpha=alphas[i],
        line_color="white",
        line_width=2,
    )
    legend_items.append((label, [line, scatter]))

# Reference line at 20% retention threshold
threshold = Span(location=20, dimension="width", line_color="#999999", line_dash="dashed", line_width=2, line_alpha=0.7)
p.add_layout(threshold)

# Legend
legend = Legend(items=legend_items, location="top_right")
legend.label_text_font_size = "20pt"
legend.glyph_height = 30
legend.glyph_width = 30
legend.spacing = 12
legend.padding = 20
legend.background_fill_alpha = 0.8
legend.border_line_alpha = 0.3
p.add_layout(legend)

# Style
p.title.text_font_size = "42pt"
p.xaxis.axis_label_text_font_size = "32pt"
p.yaxis.axis_label_text_font_size = "32pt"
p.xaxis.major_label_text_font_size = "24pt"
p.yaxis.major_label_text_font_size = "24pt"

p.y_range.start = 0
p.y_range.end = 105
p.x_range.start = -0.3
p.x_range.end = 12.3

p.ygrid.grid_line_alpha = 0.2
p.ygrid.grid_line_dash = "dashed"
p.xgrid.grid_line_alpha = 0

p.background_fill_color = "#fafafa"
p.border_fill_color = "white"

p.axis.axis_line_width = 2
p.axis.axis_line_color = "#333333"
p.axis.major_tick_line_width = 2
p.axis.minor_tick_line_width = 0

p.toolbar_location = None

# Save
export_png(p, filename="plot.png")

output_file("plot.html")
save(p)
