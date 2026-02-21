""" pyplots.ai
violin-basic: Basic Violin Plot
Library: bokeh 3.8.2 | Python 3.14.3
Quality: 82/100 | Updated: 2026-02-21
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure
from scipy.stats import gaussian_kde


# Data - Salary distributions by department (realistic scenario)
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Support"]
data = {
    "Engineering": np.random.normal(85000, 15000, 150),
    "Marketing": np.random.normal(65000, 12000, 150),
    "Sales": np.random.normal(70000, 20000, 150),
    "Support": np.random.normal(50000, 8000, 150),
}

# Colors - Python Blue first, then accessible palette
colors = ["#306998", "#FFD43B", "#4B8BBE", "#FFE873"]

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="violin-basic \u00b7 bokeh \u00b7 pyplots.ai",
    x_axis_label="Department",
    y_axis_label="Annual Salary (USD)",
    x_range=categories,
    toolbar_location=None,
)

# Text sizing for 4800x2700 px
p.title.text_font_size = "36pt"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "22pt"
p.yaxis.major_label_text_font_size = "22pt"

# Format y-axis as readable currency
p.yaxis.formatter = NumeralTickFormatter(format="$0,0")

# Visual refinement - clean design
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.2
p.ygrid.grid_line_dash = "dashed"
p.outline_line_color = None
p.axis.minor_tick_line_color = None
p.axis.major_tick_line_color = None
p.axis.axis_line_color = "#cccccc"

# Violin width scaling
violin_width = 0.4

# Draw violins for each category
for i, cat in enumerate(categories):
    values = data[cat]

    # Compute KDE using scipy (idiomatic, robust bandwidth selection)
    kde = gaussian_kde(values)
    std = np.std(values)
    y_grid = np.linspace(values.min() - std, values.max() + std, 100)
    density = kde(y_grid)

    # Scale density to violin width
    density_scaled = density / density.max() * violin_width

    # Create mirrored violin shape using categorical offset tuples
    xs_left = [(cat, float(-d)) for d in density_scaled]
    xs_right = [(cat, float(d)) for d in density_scaled[::-1]]

    # Draw violin patch
    p.patch(
        xs_left + xs_right,
        list(y_grid) + list(y_grid[::-1]),
        fill_color=colors[i],
        fill_alpha=0.7,
        line_color=colors[i],
        line_width=3,
    )

    # Quartiles and median
    q1, median, q3 = np.percentile(values, [25, 50, 75])

    # Inner box (Q1-Q3)
    box_width = 0.06
    p.quad(
        left=[(cat, -box_width)],
        right=[(cat, box_width)],
        top=[q3],
        bottom=[q1],
        fill_color="white",
        fill_alpha=0.9,
        line_color="black",
        line_width=3,
    )

    # Median line
    p.segment(
        x0=[(cat, -box_width * 1.5)],
        y0=[median],
        x1=[(cat, box_width * 1.5)],
        y1=[median],
        line_color="black",
        line_width=5,
    )

    # Whiskers (1.5*IQR or data extent)
    iqr_val = q3 - q1
    whisker_low = max(values.min(), q1 - 1.5 * iqr_val)
    whisker_high = min(values.max(), q3 + 1.5 * iqr_val)

    p.segment(x0=[cat], y0=[q1], x1=[cat], y1=[whisker_low], line_color="black", line_width=3)
    p.segment(x0=[cat], y0=[q3], x1=[cat], y1=[whisker_high], line_color="black", line_width=3)

    # Whisker caps
    cap_width = 0.04
    p.segment(
        x0=[(cat, -cap_width)],
        y0=[whisker_low],
        x1=[(cat, cap_width)],
        y1=[whisker_low],
        line_color="black",
        line_width=3,
    )
    p.segment(
        x0=[(cat, -cap_width)],
        y0=[whisker_high],
        x1=[(cat, cap_width)],
        y1=[whisker_high],
        line_color="black",
        line_width=3,
    )

# Save outputs
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
