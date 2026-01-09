"""pyplots.ai
parliament-basic: Parliament Seat Chart
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-01-09
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource, Legend, LegendItem
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - Fictional parliament composition
parties = [
    "Progressive Alliance",
    "Green Coalition",
    "Center Party",
    "Liberal Democrats",
    "Conservative Union",
    "National Front",
]
seats = [85, 42, 58, 67, 92, 56]
colors = ["#306998", "#2E8B57", "#FFD43B", "#FFA500", "#8B0000", "#4B0082"]
total_seats = sum(seats)

# Calculate seat positions in semicircular arcs
# More rows for better distribution
rows = 8
base_radius = 0.35
radius_step = 0.12

# Calculate seats per row based on arc length (outer rows have more seats)
seats_per_row = []
for i in range(rows):
    radius = base_radius + i * radius_step
    # Arc length is proportional to radius
    row_capacity = int(radius * 30)  # Scale factor
    seats_per_row.append(row_capacity)

# Normalize to match total seats
total_capacity = sum(seats_per_row)
seats_per_row = [int(s * total_seats / total_capacity) for s in seats_per_row]

# Adjust to match total exactly
diff = total_seats - sum(seats_per_row)
for i in range(abs(diff)):
    idx = (rows - 1 - i) % rows if diff > 0 else i % rows
    seats_per_row[idx] += 1 if diff > 0 else -1

# Build party assignment - each seat gets a party in order
party_assignments = []
for i, (party, seat_count) in enumerate(zip(parties, seats, strict=True)):
    party_assignments.extend([(party, colors[i])] * seat_count)

# Generate seat positions - fill row by row
x_positions = []
y_positions = []
seat_colors = []
seat_parties = []

seat_idx = 0
for row in range(rows):
    row_seat_count = seats_per_row[row]
    if row_seat_count <= 0 or seat_idx >= total_seats:
        continue

    radius = base_radius + row * radius_step
    # Angles from pi to 0 (left to right semicircle) with small margin
    angles = np.linspace(np.pi - 0.05, 0.05, row_seat_count)

    for angle in angles:
        if seat_idx >= total_seats:
            break
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        x_positions.append(x)
        y_positions.append(y)
        party, color = party_assignments[seat_idx]
        seat_colors.append(color)
        seat_parties.append(party)
        seat_idx += 1

# Create data source
source = ColumnDataSource(data={"x": x_positions, "y": y_positions, "color": seat_colors, "party": seat_parties})

# Create figure - square format for semicircle
p = figure(
    width=3600,
    height=3600,
    title="parliament-basic · bokeh · pyplots.ai",
    tools="",
    toolbar_location=None,
    x_range=(-1.35, 1.35),
    y_range=(-0.35, 1.45),
)

# Plot seats
p.scatter(x="x", y="y", source=source, color="color", size=30, alpha=0.9, line_color="white", line_width=2)

# Create legend items manually
legend_items = []
for party, seat_count, color in zip(parties, seats, colors, strict=True):
    dummy_source = ColumnDataSource(data={"x": [-10], "y": [-10]})
    dummy_scatter = p.scatter(x="x", y="y", source=dummy_source, color=color, size=22, alpha=1)
    legend_items.append(LegendItem(label=f"{party} ({seat_count})", renderers=[dummy_scatter]))

legend = Legend(items=legend_items, location="bottom_center", orientation="horizontal")
legend.label_text_font_size = "22pt"
legend.spacing = 35
legend.padding = 30
legend.glyph_height = 28
legend.glyph_width = 28
p.add_layout(legend, "below")

# Add majority threshold annotation
majority = total_seats // 2 + 1
p.text(
    x=[0],
    y=[-0.18],
    text=[f"Majority threshold: {majority} seats (Total: {total_seats})"],
    text_align="center",
    text_font_size="24pt",
    text_color="#444444",
)

# Style the plot
p.title.text_font_size = "36pt"
p.title.align = "center"
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
p.outline_line_color = None
p.background_fill_color = "#FFFFFF"

# Save
export_png(p, filename="plot.png")
save(p, filename="plot.html", resources=CDN, title="parliament-basic · bokeh · pyplots.ai")
