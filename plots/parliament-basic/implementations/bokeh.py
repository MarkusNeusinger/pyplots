"""pyplots.ai
parliament-basic: Parliament Seat Chart
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-01-09
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Generic parliament with 5 parties (neutral names)
parties = ["Progressive Alliance", "Green Coalition", "Center Party", "Conservative Union", "Liberal Democrats"]
seats = [85, 45, 120, 95, 55]  # Total 400 seats
colors = ["#306998", "#2E8B57", "#FFD43B", "#DC143C", "#FF8C00"]

total_seats = sum(seats)
majority_threshold = total_seats // 2 + 1

# Calculate seat positions in semicircular arcs
# Seats are arranged filling rows from inner to outer, parties fill left-to-right
n_rows = 8  # Number of arc rows
base_seats = total_seats // n_rows

# Calculate seats per row (inner rows have fewer)
seats_per_row = []
for i in range(n_rows):
    # Inner rows have fewer seats, outer rows have more
    factor = 0.6 + 0.1 * i
    row_seats = int(base_seats * factor)
    seats_per_row.append(row_seats)

# Adjust to match total
diff = total_seats - sum(seats_per_row)
for i in range(abs(diff)):
    if diff > 0:
        seats_per_row[-(i % n_rows) - 1] += 1
    else:
        seats_per_row[-(i % n_rows) - 1] -= 1

# Generate all seat positions first (row by row, left to right within each row)
all_positions = []
inner_radius = 2.5
row_spacing = 0.9

for row_idx, n_seats_in_row in enumerate(seats_per_row):
    radius = inner_radius + row_idx * row_spacing
    # Angles from pi (left) to 0 (right) for semicircle
    angles = np.linspace(np.pi * 0.95, np.pi * 0.05, n_seats_in_row)
    for angle in angles:
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        all_positions.append((x, y, row_idx, angle))

# Sort positions to fill left-to-right across the entire parliament
# Use angle as primary sort (larger angle = more left)
all_positions.sort(key=lambda p: -p[3])

# Assign colors based on sorted order
x_positions = []
y_positions = []
seat_colors = []
seat_parties = []

seat_count = 0
party_idx = 0
cumulative_seats = [sum(seats[: i + 1]) for i in range(len(seats))]

for pos in all_positions:
    x, y, row_idx, angle = pos
    x_positions.append(x)
    y_positions.append(y)

    # Find which party this seat belongs to
    while party_idx < len(parties) - 1 and seat_count >= cumulative_seats[party_idx]:
        party_idx += 1

    seat_colors.append(colors[party_idx])
    seat_parties.append(parties[party_idx])
    seat_count += 1

# Create figure - square format suits circular layouts
p = figure(
    width=3600,
    height=3600,
    title="parliament-basic · bokeh · pyplots.ai",
    x_range=(-12, 12),
    y_range=(-3, 12),
    tools="",
    toolbar_location=None,
)

# Remove axes and grid for cleaner look
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Plot seats grouped by party for proper legend
for i, (party, color) in enumerate(zip(parties, colors, strict=True)):
    # Filter data for this party
    indices = [j for j, p in enumerate(seat_parties) if p == party]
    party_source = ColumnDataSource(
        data={"x": [x_positions[j] for j in indices], "y": [y_positions[j] for j in indices]}
    )
    p.scatter(
        x="x",
        y="y",
        source=party_source,
        size=22,
        fill_color=color,
        line_color="white",
        line_width=1.5,
        alpha=0.95,
        legend_label=f"{party} ({seats[i]})",
    )

# Configure legend
p.legend.location = "bottom_center"
p.legend.orientation = "horizontal"
p.legend.label_text_font_size = "18pt"
p.legend.glyph_height = 22
p.legend.glyph_width = 22
p.legend.spacing = 15
p.legend.padding = 15
p.legend.background_fill_alpha = 0.9
p.add_layout(p.legend[0], "below")

# Add majority threshold annotation
p.text(
    x=[0],
    y=[-0.8],
    text=[f"Majority threshold: {majority_threshold} seats"],
    text_font_size="22pt",
    text_align="center",
    text_color="#444444",
)

# Add total seats annotation
p.text(
    x=[0],
    y=[-1.8],
    text=[f"Total: {total_seats} seats"],
    text_font_size="20pt",
    text_align="center",
    text_color="#666666",
)

# Title styling
p.title.text_font_size = "32pt"
p.title.align = "center"

# Save output
export_png(p, filename="plot.png")
