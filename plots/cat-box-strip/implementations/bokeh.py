"""pyplots.ai
cat-box-strip: Box Plot with Strip Overlay
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, Whisker
from bokeh.plotting import figure
from bokeh.transform import jitter


# Data - Test scores across different study methods
np.random.seed(42)

# Create data with different distributions for each group
groups = ["Traditional", "Online", "Hybrid", "Self-Study"]
data = {
    "Traditional": np.concatenate(
        [
            np.random.normal(72, 8, 35),
            np.array([45, 95, 98]),  # outliers
        ]
    ),
    "Online": np.random.normal(68, 12, 40),
    "Hybrid": np.concatenate(
        [
            np.random.normal(78, 6, 38),
            np.array([50, 52]),  # outliers
        ]
    ),
    "Self-Study": np.concatenate(
        [
            np.random.normal(65, 15, 30),
            np.array([95, 98, 35, 32]),  # outliers
        ]
    ),
}

# Create DataFrame for strip plot
records = []
for group, values in data.items():
    for val in values:
        records.append({"group": group, "score": val})
df = pd.DataFrame(records)

# Calculate box plot statistics
stats = []
for group in groups:
    values = data[group]
    q1 = np.percentile(values, 25)
    q2 = np.percentile(values, 50)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    whisker_low = max(values.min(), q1 - 1.5 * iqr)
    whisker_high = min(values.max(), q3 + 1.5 * iqr)
    stats.append(
        {"group": group, "q1": q1, "q2": q2, "q3": q3, "whisker_low": whisker_low, "whisker_high": whisker_high}
    )
stats_df = pd.DataFrame(stats)

# Create figure
p = figure(
    width=4800,
    height=2700,
    x_range=groups,
    title="cat-box-strip · bokeh · pyplots.ai",
    x_axis_label="Study Method",
    y_axis_label="Test Score",
    tools="",
    toolbar_location=None,
)

# Box plot components
box_source = ColumnDataSource(stats_df)

# Whiskers (vertical lines from whisker_low to whisker_high)
whisker = Whisker(
    source=box_source, base="group", lower="whisker_low", upper="whisker_high", line_width=4, line_color="#306998"
)
whisker.upper_head.size = 20
whisker.upper_head.line_width = 4
whisker.upper_head.line_color = "#306998"
whisker.lower_head.size = 20
whisker.lower_head.line_width = 4
whisker.lower_head.line_color = "#306998"
p.add_layout(whisker)

# Boxes (from q1 to q3)
p.vbar(
    x="group",
    top="q3",
    bottom="q1",
    width=0.5,
    source=box_source,
    fill_color="#306998",
    fill_alpha=0.4,
    line_color="#306998",
    line_width=3,
)

# Median lines - use segment with proper categorical offsets
# In Bokeh, categorical coordinates can use offsets like (category, offset)
for group in groups:
    median = stats_df.loc[stats_df["group"] == group, "q2"].values[0]
    p.segment(x0=[(group, -0.25)], y0=[median], x1=[(group, 0.25)], y1=[median], line_color="#FFD43B", line_width=6)

# Strip plot - overlay individual points with jitter
strip_source = ColumnDataSource(df)
p.scatter(
    x=jitter("group", width=0.35, range=p.x_range),
    y="score",
    source=strip_source,
    size=18,
    fill_color="#FFD43B",
    fill_alpha=0.7,
    line_color="#306998",
    line_width=2,
)

# Styling
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

p.xaxis.axis_line_width = 3
p.yaxis.axis_line_width = 3
p.xaxis.major_tick_line_width = 3
p.yaxis.major_tick_line_width = 3

p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"

p.background_fill_color = "white"
p.border_fill_color = "white"
p.outline_line_color = None

# Save
export_png(p, filename="plot.png")
