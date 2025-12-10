"""
violin-basic: Basic Violin Plot
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import FixedTicker
from bokeh.plotting import figure
from scipy import stats


# Data - Employee performance scores by department
np.random.seed(42)

departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
n_per_dept = 150

data = {
    "Engineering": np.random.normal(75, 12, n_per_dept),
    "Marketing": np.concatenate(
        [np.random.normal(65, 8, n_per_dept // 2), np.random.normal(80, 6, n_per_dept // 2)]
    ),  # Bimodal
    "Sales": np.random.normal(70, 15, n_per_dept),
    "HR": np.random.normal(78, 10, n_per_dept),
    "Finance": np.random.normal(72, 9, n_per_dept),
}

# Style guide colors
colors = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6"]

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="Employee Performance Scores by Department",
    x_axis_label="Department",
    y_axis_label="Performance Score",
    tools="",
    toolbar_location=None,
)

# KDE grid for smooth density estimation
y_grid = np.linspace(20, 120, 500)
max_width = 0.4  # Maximum half-width of violin

# Calculate and draw violins
for idx, (_dept, values) in enumerate(data.items()):
    # Compute KDE
    kde = stats.gaussian_kde(values)
    density = kde(y_grid)

    # Normalize density to max width
    density_normalized = density / density.max() * max_width

    # Create mirrored violin shape (patch coordinates)
    # Left side (negative x offset from center)
    x_left = idx - density_normalized
    # Right side (positive x offset from center)
    x_right = idx + density_normalized

    # Build closed polygon: go up left side, then down right side
    xs = np.concatenate([x_left, x_right[::-1]])
    ys = np.concatenate([y_grid, y_grid[::-1]])

    # Draw violin body
    p.patch(xs, ys, fill_color=colors[idx], fill_alpha=0.7, line_color="white", line_width=2)

    # Calculate statistics for inner box plot markers
    q1 = np.percentile(values, 25)
    median = np.percentile(values, 50)
    q3 = np.percentile(values, 75)

    # Draw inner quartile box (thin rectangle)
    box_width = 0.08
    p.vbar(x=idx, width=box_width, bottom=q1, top=q3, fill_color="#333333", fill_alpha=0.8, line_color="#333333")

    # Draw median line (white for visibility)
    p.segment(x0=idx - box_width / 2, y0=median, x1=idx + box_width / 2, y1=median, line_color="white", line_width=4)

# Configure x-axis with department names
p.xaxis.ticker = FixedTicker(ticks=list(range(len(departments))))
p.xaxis.major_label_overrides = dict(enumerate(departments))

# Styling
p.title.text_font_size = "32pt"
p.title.align = "center"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "22pt"
p.yaxis.major_label_text_font_size = "22pt"

p.ygrid.grid_line_alpha = 0.3
p.xgrid.visible = False

p.outline_line_color = None
p.background_fill_color = "#FAFAFA"

# Save outputs
export_png(p, filename="plot.png")

output_file("plot.html")
save(p)
