"""pyplots.ai
violin-basic: Basic Violin Plot
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.plotting import figure


# Data - Salary distributions by department (realistic scenario)
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Support"]
data = {
    "Engineering": np.random.normal(85000, 15000, 150),
    "Marketing": np.random.normal(65000, 12000, 150),
    "Sales": np.random.normal(70000, 20000, 150),  # Higher variance
    "Support": np.random.normal(50000, 8000, 150),  # Lower variance
}

# Colors - Python Blue and Yellow first, then accessible colors
colors = ["#306998", "#FFD43B", "#4B8BBE", "#FFE873"]

# Create figure with categorical x-axis
p = figure(
    width=4800,
    height=2700,
    title="violin-basic · bokeh · pyplots.ai",
    x_axis_label="Department",
    y_axis_label="Annual Salary (USD)",
    x_range=categories,
    toolbar_location=None,
)

# Styling for 4800x2700 px
p.title.text_font_size = "36pt"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "22pt"
p.yaxis.major_label_text_font_size = "22pt"

# Grid styling
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"

# Violin width scaling (0.4 = 40% of category spacing)
violin_width = 0.4

# Draw violins for each category
for i, cat in enumerate(categories):
    values = data[cat]
    n = len(values)

    # Compute KDE using Gaussian kernel (Silverman's rule for bandwidth)
    std = np.std(values)
    iqr = np.percentile(values, 75) - np.percentile(values, 25)
    bandwidth = 0.9 * min(std, iqr / 1.34) * n ** (-0.2)
    bandwidth = max(bandwidth, 0.1)

    y_grid = np.linspace(values.min() - std, values.max() + std, 100)
    density = np.zeros_like(y_grid, dtype=float)
    for xi in values:
        density += np.exp(-0.5 * ((y_grid - xi) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Scale density to violin width
    density_scaled = density / density.max() * violin_width

    # Create violin shape (mirrored on both sides)
    x_left = -density_scaled
    x_right = density_scaled

    # Convert to categorical offset format for bokeh
    xs_left = [(cat, float(xl)) for xl in x_left]
    xs_right = [(cat, float(xr)) for xr in x_right[::-1]]

    # Draw violin patch
    p.patch(
        xs_left + xs_right,
        list(y_grid) + list(y_grid[::-1]),
        fill_color=colors[i],
        fill_alpha=0.7,
        line_color=colors[i],
        line_width=3,
    )

    # Compute quartiles
    q1, median, q3 = np.percentile(values, [25, 50, 75])

    # Draw thin box inside violin (quartile markers)
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

    # Draw median line
    p.segment(
        x0=[(cat, -box_width * 1.5)],
        y0=[median],
        x1=[(cat, box_width * 1.5)],
        y1=[median],
        line_color="black",
        line_width=5,
    )

    # Whiskers (to 1.5*IQR or data extent)
    iqr_val = q3 - q1
    whisker_low = max(values.min(), q1 - 1.5 * iqr_val)
    whisker_high = min(values.max(), q3 + 1.5 * iqr_val)

    # Vertical whisker lines
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
