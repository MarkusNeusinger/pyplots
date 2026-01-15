"""pyplots.ai
point-and-figure-basic: Point and Figure Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-15
"""

import numpy as np
import pygal
from pygal.style import Style


# Random seed for reproducibility
np.random.seed(42)

# Generate realistic stock price data (6 months of daily data)
n_days = 150
base_price = 100.0
returns = np.random.normal(0.001, 0.02, n_days)  # Daily returns with slight upward drift
prices = base_price * np.cumprod(1 + returns)

# P&F parameters
box_size = 2.0  # Each box represents $2
reversal = 3  # 3-box reversal


# Round to nearest box
def round_to_box(price, box_sz):
    return np.floor(price / box_sz) * box_sz


# Calculate P&F chart data
columns = []  # List of (start_price, end_price, direction) tuples
current_direction = None  # 'X' for up, 'O' for down
current_column_start = None
current_column_end = None

first_price = round_to_box(prices[0], box_size)
current_column_start = first_price
current_column_end = first_price

for price in prices[1:]:
    rounded_price = round_to_box(price, box_size)

    if current_direction is None:
        # Determine initial direction
        if rounded_price >= current_column_end + box_size:
            current_direction = "X"
            current_column_end = rounded_price
        elif rounded_price <= current_column_end - box_size:
            current_direction = "O"
            current_column_end = rounded_price
    elif current_direction == "X":
        if rounded_price >= current_column_end + box_size:
            # Continue up
            current_column_end = rounded_price
        elif rounded_price <= current_column_end - (reversal * box_size):
            # Reversal down
            columns.append((current_column_start, current_column_end, "X"))
            current_column_start = current_column_end - box_size
            current_column_end = rounded_price
            current_direction = "O"
    else:  # current_direction == 'O'
        if rounded_price <= current_column_end - box_size:
            # Continue down
            current_column_end = rounded_price
        elif rounded_price >= current_column_end + (reversal * box_size):
            # Reversal up
            columns.append((current_column_start, current_column_end, "O"))
            current_column_start = current_column_end + box_size
            current_column_end = rounded_price
            current_direction = "X"

# Add final column
if current_direction:
    columns.append((current_column_start, current_column_end, current_direction))

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#22A06B", "#E53E3E"),  # Green for X, Red for O
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=48,
    value_font_size=36,
    tooltip_font_size=36,
    stroke_width=3,
)

# Create XY chart for Point and Figure visualization
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="point-and-figure-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=2,
    show_y_guides=True,
    show_x_guides=False,
    x_title="Column (Reversal)",
    y_title="Price ($)",
    margin=50,
    margin_bottom=200,
    margin_left=200,
    margin_top=150,
    stroke=False,
    dots_size=18,
)

# Plot X columns (rising) and O columns (falling) as vertical sequences of points
x_points = []
o_points = []

for col_idx, (start, end, direction) in enumerate(columns):
    low = min(start, end)
    high = max(start, end)
    if direction == "X":
        # Rising column - plot X's from bottom to top
        for price_level in np.arange(low, high + box_size, box_size):
            x_points.append((col_idx, price_level))
    else:
        # Falling column - plot O's from top to bottom
        for price_level in np.arange(low, high + box_size, box_size):
            o_points.append((col_idx, price_level))

# Add series
chart.add("X (Rising)", x_points, stroke=False)
chart.add("O (Falling)", o_points, stroke=False)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
