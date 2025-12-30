"""pyplots.ai
parliament-basic: Parliament Seat Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 68/100 | Created: 2025-12-30
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
threshold_color = "#E74C3C"

# Calculate seat positions in concentric arcs
num_rows = 7
base_radius = 1.0
row_spacing = 0.22
seats_per_row = []
remaining = total_seats
for row in range(num_rows):
    radius = base_radius + row * row_spacing
    arc_length = math.pi * radius
    max_seats_in_row = int(arc_length / 0.18)
    seats_in_row = min(max_seats_in_row, remaining)
    if seats_in_row > 0:
        seats_per_row.append((radius, seats_in_row))
        remaining -= seats_in_row
    if remaining <= 0:
        break

# Build cumulative seat counts for party assignment
cumulative_seats = [0]
for count in seats:
    cumulative_seats.append(cumulative_seats[-1] + count)

# Generate seat positions (scaled for pygal coordinates)
seat_positions = []
seat_index = 0
for radius, row_count in seats_per_row:
    for i in range(row_count):
        angle = math.pi - (i + 0.5) * math.pi / row_count
        x = radius * math.cos(angle) * 100  # Scale to pygal coordinate space
        y = radius * math.sin(angle) * 100

        party_index = 0
        for p_idx in range(len(seats)):
            if seat_index < cumulative_seats[p_idx + 1]:
                party_index = p_idx
                break

        seat_positions.append((x, y, party_index))
        seat_index += 1

# Calculate threshold line position
threshold_ratio = majority_threshold / total_seats
threshold_angle = math.pi * (1 - threshold_ratio)
inner_radius = (base_radius - 0.15) * 100
outer_radius = (base_radius + num_rows * row_spacing + 0.1) * 100
threshold_x1 = inner_radius * math.cos(threshold_angle)
threshold_y1 = inner_radius * math.sin(threshold_angle)
threshold_x2 = outer_radius * math.cos(threshold_angle)
threshold_y2 = outer_radius * math.sin(threshold_angle)

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#1a1a1a",
    foreground_subtle="#666666",
    colors=tuple(party_colors) + (threshold_color,),
    title_font_size=72,
    label_font_size=44,
    major_label_font_size=44,
    legend_font_size=42,
    value_font_size=38,
    tooltip_font_size=36,
)

# Create XY chart for individual seat dots
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title=f"Parliament Composition · parliament-basic · pygal · pyplots.ai\nTotal: {total_seats} seats | Majority: {majority_threshold} seats (50%+1)",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=36,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    stroke=False,
    dots_size=35,
    xrange=(-300, 300),
    range=(-30, 300),
    margin=60,
    margin_bottom=200,
    explicit_size=True,
    print_values=False,
    print_labels=False,
)

# Add each party's seats as a separate series
for party_idx, party_name in enumerate(parties):
    seat_coords = [(x, y) for x, y, pidx in seat_positions if pidx == party_idx]
    chart.add(f"{party_name} ({seats[party_idx]})", seat_coords)

# Add majority threshold line with multiple points to make it visible
num_line_points = 20
threshold_line_points = []
for i in range(num_line_points + 1):
    t = i / num_line_points
    x = threshold_x1 + t * (threshold_x2 - threshold_x1)
    y = threshold_y1 + t * (threshold_y2 - threshold_y1)
    threshold_line_points.append((x, y))

chart.add(
    f"Majority Line ({majority_threshold})",
    threshold_line_points,
    stroke=True,
    dots_size=6,
    stroke_style={"width": 8, "dasharray": "15,10"},
)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
