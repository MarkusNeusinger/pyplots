""" pyplots.ai
point-and-figure-basic: Point and Figure Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-15
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

# Colorblind-safe colors: Blue for X (rising), Orange for O (falling)
x_color = "#0066CC"  # Blue
o_color = "#E56B00"  # Orange
support_color = "#228B22"  # Forest green for support line
resistance_color = "#8B0000"  # Dark red for resistance line

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(x_color, o_color, support_color, resistance_color),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=48,
    value_font_size=48,
    tooltip_font_size=36,
    stroke_width=8,
)

# Collect all price levels to set y_labels at box size intervals
all_prices = []
for start, end, _ in columns:
    all_prices.extend([start, end])

y_min = min(all_prices) - box_size
y_max = max(all_prices) + box_size
y_labels = list(np.arange(y_min, y_max + box_size, box_size))

# Create XY chart for Point and Figure visualization
# Using large dots with distinct visual patterns for X and O
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="point-and-figure-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    show_y_guides=True,
    show_x_guides=True,
    x_title="Column (Reversal)",
    y_title="Price ($)",
    margin=50,
    margin_bottom=200,
    margin_left=200,
    margin_top=150,
    y_labels=y_labels,
    range=(y_min, y_max),
    dots_size=25,  # Large visible markers
    stroke=False,
)

# Plot X columns (rising) and O columns (falling) as vertical sequences of points
x_points = []
o_points = []

for col_idx, (start, end, direction) in enumerate(columns):
    low = min(start, end)
    high = max(start, end)
    if direction == "X":
        # Rising column - X markers
        for price_level in np.arange(low, high + box_size, box_size):
            x_points.append({"value": (col_idx, price_level), "label": "X"})
    else:
        # Falling column - O markers
        for price_level in np.arange(low, high + box_size, box_size):
            o_points.append({"value": (col_idx, price_level), "label": "O"})

# Add series - X as filled circles (blue), O as filled circles (orange)
# Legend will show "X (Rising)" and "O (Falling)" with distinctive colors
chart.add("X (Rising)", x_points, stroke=False)
chart.add("O (Falling)", o_points, stroke=False)

# Calculate support and resistance trend lines
# Find lows of O columns for support line (45-degree uptrend)
# Find highs of X columns for resistance line (45-degree downtrend)
support_lows = []
resistance_highs = []

for col_idx, (start, end, direction) in enumerate(columns):
    low = min(start, end)
    high = max(start, end)
    if direction == "O":
        support_lows.append((col_idx, low))
    else:
        resistance_highs.append((col_idx, high))

# Draw support line from ascending low (45-degree uptrend)
if len(support_lows) >= 2:
    # Start from the first O column low
    support_start = support_lows[0]
    # Extend 45-degree line (1 box up per column)
    support_end_col = min(support_start[0] + 6, len(columns) - 1)
    support_line_points = [
        {"value": (support_start[0], support_start[1])},
        {"value": (support_end_col, support_start[1] + (support_end_col - support_start[0]) * box_size)},
    ]
    chart.add("Support (45° up)", support_line_points, stroke=True, show_dots=False, dots_size=0)

# Draw resistance line from descending high (45-degree downtrend)
if len(resistance_highs) >= 2:
    # Start from the first X column high
    resistance_start = resistance_highs[0]
    # Extend 45-degree line down (1 box down per column)
    resistance_end_col = min(resistance_start[0] + 6, len(columns) - 1)
    resistance_line_points = [
        {"value": (resistance_start[0], resistance_start[1])},
        {"value": (resistance_end_col, resistance_start[1] - (resistance_end_col - resistance_start[0]) * box_size)},
    ]
    chart.add("Resistance (45° down)", resistance_line_points, stroke=True, show_dots=False, dots_size=0)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
