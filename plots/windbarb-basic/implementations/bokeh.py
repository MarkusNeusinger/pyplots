"""pyplots.ai
windbarb-basic: Wind Barb Plot for Meteorological Data
Library: bokeh | Python 3.13
Quality: pending | Created: 2026-01-11
"""

from math import pi

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Grid of wind observations
np.random.seed(42)

# Create a grid of observation points
x_grid = np.linspace(0, 10, 6)
y_grid = np.linspace(0, 8, 5)
xx, yy = np.meshgrid(x_grid, y_grid)
x_positions = xx.flatten()
y_positions = yy.flatten()

# Generate realistic wind components (u=east-west, v=north-south)
# Simulate a weather pattern with winds varying across the domain
n_barbs = len(x_positions)
base_u = 15 + 10 * np.sin(x_positions * 0.5)  # Zonal component
base_v = 10 * np.cos(y_positions * 0.4)  # Meridional component
u = base_u + np.random.randn(n_barbs) * 3  # Add some noise
v = base_v + np.random.randn(n_barbs) * 3

# Calculate wind speed (knots) and direction
wind_speed = np.sqrt(u**2 + v**2)
wind_direction = np.arctan2(v, u)  # Direction wind is going TO

# Barb parameters
barb_length = 0.6  # Length of the staff
barb_spacing = 0.08  # Spacing between barbs on the staff
half_barb_len = 0.15  # Length of half barb (5 knots)
full_barb_len = 0.25  # Length of full barb (10 knots)
pennant_len = 0.25  # Length of pennant base
barb_angle = 70 * pi / 180  # Angle of barbs relative to staff (degrees)

# Lists to collect line segments for all barbs
all_x0, all_y0, all_x1, all_y1 = [], [], [], []

# Draw each wind barb
for i in range(n_barbs):
    x, y = x_positions[i], y_positions[i]
    speed = wind_speed[i]

    # Wind barbs point FROM where wind is coming, so reverse direction
    direction = wind_direction[i] + pi  # Reverse direction

    # Draw staff
    dx = barb_length * np.cos(direction)
    dy = barb_length * np.sin(direction)
    staff_end_x = x + dx
    staff_end_y = y + dy
    all_x0.append(x)
    all_y0.append(y)
    all_x1.append(staff_end_x)
    all_y1.append(staff_end_y)

    # Calculate number of each barb type
    remaining_speed = speed
    num_pennants = int(remaining_speed // 50)
    remaining_speed -= num_pennants * 50
    num_full_barbs = int(remaining_speed // 10)
    remaining_speed -= num_full_barbs * 10
    num_half_barbs = 1 if remaining_speed >= 2.5 else 0

    # Position along the staff (start from the end)
    pos = 0  # Distance from staff end

    # Draw pennants (50 knots each) - triangular flags
    for _ in range(num_pennants):
        # Pennant is a filled triangle
        px = staff_end_x - pos * np.cos(direction)
        py = staff_end_y - pos * np.sin(direction)

        # Triangle vertices
        tip_x = px + pennant_len * np.cos(direction + barb_angle)
        tip_y = py + pennant_len * np.sin(direction + barb_angle)

        base_x = px - barb_spacing * 1.5 * np.cos(direction)
        base_y = py - barb_spacing * 1.5 * np.sin(direction)

        # Draw pennant as three line segments forming a triangle
        all_x0.extend([px, tip_x, base_x])
        all_y0.extend([py, tip_y, base_y])
        all_x1.extend([tip_x, base_x, px])
        all_y1.extend([tip_y, base_y, py])

        pos += barb_spacing * 2

    # Draw full barbs (10 knots each)
    for _ in range(num_full_barbs):
        bx = staff_end_x - pos * np.cos(direction)
        by = staff_end_y - pos * np.sin(direction)

        end_x = bx + full_barb_len * np.cos(direction + barb_angle)
        end_y = by + full_barb_len * np.sin(direction + barb_angle)

        all_x0.append(bx)
        all_y0.append(by)
        all_x1.append(end_x)
        all_y1.append(end_y)
        pos += barb_spacing

    # Draw half barbs (5 knots each)
    for _ in range(num_half_barbs):
        # If this is the only barb, offset it slightly from the end
        if num_pennants == 0 and num_full_barbs == 0:
            pos = barb_spacing

        bx = staff_end_x - pos * np.cos(direction)
        by = staff_end_y - pos * np.sin(direction)

        end_x = bx + half_barb_len * np.cos(direction + barb_angle)
        end_y = by + half_barb_len * np.sin(direction + barb_angle)

        all_x0.append(bx)
        all_y0.append(by)
        all_x1.append(end_x)
        all_y1.append(end_y)
        pos += barb_spacing

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="windbarb-basic · bokeh · pyplots.ai",
    x_axis_label="X Position (grid units)",
    y_axis_label="Y Position (grid units)",
    x_range=(-1, 11),
    y_range=(-1, 9),
)

# Create data source for all segments
segment_source = ColumnDataSource(data={"x0": all_x0, "y0": all_y0, "x1": all_x1, "y1": all_y1})

# Draw all barb segments
p.segment(
    x0="x0", y0="y0", x1="x1", y1="y1", source=segment_source, line_color="#306998", line_width=3, line_cap="round"
)

# Add station markers at observation points
station_source = ColumnDataSource(data={"x": x_positions, "y": y_positions, "speed": wind_speed})

p.scatter(
    x="x",
    y="y",
    source=station_source,
    size=12,
    marker="circle",
    fill_color="white",
    line_color="#306998",
    line_width=2,
)

# Styling
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

p.grid.grid_line_alpha = 0.3
p.grid.grid_line_dash = [6, 4]

p.background_fill_color = "#f8f9fa"
p.border_fill_color = "white"

# Save
export_png(p, filename="plot.png")
