"""pyplots.ai
parliament-basic: Parliament Seat Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-30
"""

import math

import pygal
from pygal.style import Style


# Data - Parliament composition by party (fictional neutral parties)
parties = ["Progressive Alliance", "Centrist Union", "Reform Party", "Green Coalition", "Independent"]
seats = [145, 98, 72, 35, 15]
total_seats = sum(seats)
majority_threshold = total_seats // 2 + 1  # 183 seats needed for majority

# Custom colors (colorblind-safe, politically neutral)
party_colors = ["#306998", "#FFD43B", "#4ECDC4", "#45B7D1", "#96CEB4"]

# Calculate seat positions in concentric arcs
num_rows = 5
row_ratios = [(i + 1) for i in range(num_rows)]
total_ratio = sum(row_ratios)
seats_per_row = [max(1, round(total_seats * r / total_ratio)) for r in row_ratios]
seats_per_row[-1] += total_seats - sum(seats_per_row)  # Adjust to match total exactly

# Build cumulative seat counts for party assignment
cumulative_seats = [0]
for count in seats:
    cumulative_seats.append(cumulative_seats[-1] + count)

# Generate seat positions
seat_positions = []
seat_index = 0
for row_idx, row_count in enumerate(seats_per_row):
    radius = 0.4 + row_idx * 0.12  # Rows from 0.4 to 0.88
    for i in range(row_count):
        # Angle from left (π) to right (0) - semicircle
        angle = math.pi - (i + 0.5) * math.pi / row_count
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        # Determine which party this seat belongs to
        party_index = 0
        for p_idx in range(len(seats)):
            if seat_index < cumulative_seats[p_idx + 1]:
                party_index = p_idx
                break

        seat_positions.append((x, y, party_index))
        seat_index += 1

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#1a1a1a",
    foreground_subtle="#666666",
    colors=tuple(party_colors),
    title_font_size=64,
    label_font_size=40,
    major_label_font_size=40,
    legend_font_size=38,
    value_font_size=36,
    tooltip_font_size=32,
)

# Create XY chart for individual seat dots
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Parliament Composition · parliament-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=32,
    x_title=f"Total: {total_seats} seats | Majority threshold: {majority_threshold} seats (50%+1)",
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    stroke=False,
    dots_size=18,
    range=(-1.1, 1.1),
    xrange=(-1.1, 1.1),
    margin=50,
    margin_bottom=180,
)

# Add each party's seats as a separate series
for party_idx, party_name in enumerate(parties):
    seat_coords = [(x, y) for x, y, pidx in seat_positions if pidx == party_idx]
    chart.add(f"{party_name} ({seats[party_idx]})", seat_coords)

# Add majority threshold line (visual marker at 50%+1 position)
threshold_ratio = majority_threshold / total_seats
threshold_points = []
for radius in [0.35, 0.95]:  # Inner and outer arc boundaries
    angle = math.pi * (1 - threshold_ratio)  # Position on semicircle
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    threshold_points.append((x, y))

chart.add("Majority (183)", threshold_points, stroke=True, dots_size=0, stroke_style={"width": 4, "dasharray": "10,5"})

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
