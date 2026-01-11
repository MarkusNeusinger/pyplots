""" pyplots.ai
windbarb-basic: Wind Barb Plot for Meteorological Data
Library: altair 6.0.0 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-11
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - synthetic wind observations from weather stations on a grid
np.random.seed(42)

# Create a grid of observation points (6x5 grid = 30 stations)
x_coords = np.linspace(0, 10, 6)
y_coords = np.linspace(0, 8, 5)
xx, yy = np.meshgrid(x_coords, y_coords)
x = xx.flatten()
y = yy.flatten()

# Generate wind components (u: east-west, v: north-south) in knots
# Simulate a weather pattern with varying wind speeds and directions
u = np.random.uniform(-30, 30, len(x))  # Zonal component
v = np.random.uniform(-25, 25, len(x))  # Meridional component

# Calculate wind speed and direction
wind_speed = np.sqrt(u**2 + v**2)
# Direction FROM which wind blows (meteorological convention)
# Wind barbs point into the wind direction (opposite of velocity vector)
wind_direction = np.degrees(np.arctan2(-u, -v))  # Degrees from north, clockwise

# Create DataFrame
df = pd.DataFrame({"x": x, "y": y, "u": u, "v": v, "speed": wind_speed, "direction": wind_direction})

# Create wind barb visualization using layered marks
# Since Altair doesn't have native wind barb marks, we use rotated shapes
# to approximate the wind barb notation

# Normalize components for arrow display (scaled by speed)
scale = 0.03  # Scale factor for arrow length
df["dx"] = -df["u"] * scale  # Negative because barb points INTO the wind
df["dy"] = -df["v"] * scale
df["x2"] = df["x"] + df["dx"]
df["y2"] = df["y"] + df["dy"]

# Calculate positions for speed indicator marks (barbs)
# Place barbs along the staff at intervals


def create_barb_data(df):
    """Create additional data for wind speed indicator barbs."""
    barb_records = []

    for _, row in df.iterrows():
        speed = row["speed"]
        direction_rad = np.radians(row["direction"])

        # Unit vector in wind direction (pointing INTO the wind)
        ux = -np.sin(direction_rad)
        uy = -np.cos(direction_rad)

        # Perpendicular vector for barb flags (left side in NH)
        px = -uy
        py = ux

        # Staff length for barb positioning
        staff_length = speed * scale

        # Add barbs based on speed
        remaining_speed = speed
        barb_position = 0.85  # Start near the end of staff
        barb_count = 0

        # Add pennants (50 knots each)
        while remaining_speed >= 50 and barb_count < 3:
            pos_factor = barb_position - barb_count * 0.15
            bx = row["x"] + ux * staff_length * pos_factor
            by = row["y"] + uy * staff_length * pos_factor
            # Pennant triangle points
            barb_records.append(
                {"x": bx, "y": by, "type": "pennant", "speed": speed, "x2": bx + px * 0.4, "y2": by + py * 0.4}
            )
            remaining_speed -= 50
            barb_count += 1

        # Add full barbs (10 knots each)
        while remaining_speed >= 10 and barb_count < 6:
            pos_factor = barb_position - barb_count * 0.12
            bx = row["x"] + ux * staff_length * pos_factor
            by = row["y"] + uy * staff_length * pos_factor
            barb_records.append(
                {"x": bx, "y": by, "type": "full", "speed": speed, "x2": bx + px * 0.35, "y2": by + py * 0.35}
            )
            remaining_speed -= 10
            barb_count += 1

        # Add half barb (5 knots) if remaining
        if remaining_speed >= 5:
            pos_factor = barb_position - barb_count * 0.12
            bx = row["x"] + ux * staff_length * pos_factor
            by = row["y"] + uy * staff_length * pos_factor
            barb_records.append(
                {"x": bx, "y": by, "type": "half", "speed": speed, "x2": bx + px * 0.2, "y2": by + py * 0.2}
            )

    return pd.DataFrame(barb_records)


barb_df = create_barb_data(df)

# Create the layered chart
# Layer 1: Staff (main line of wind barb)
staff = (
    alt.Chart(df)
    .mark_rule(strokeWidth=2, color="#306998")
    .encode(
        x=alt.X("x:Q", title="X Coordinate", scale=alt.Scale(domain=[-1, 11])),
        y=alt.Y("y:Q", title="Y Coordinate", scale=alt.Scale(domain=[-1, 9])),
        x2="x2:Q",
        y2="y2:Q",
        tooltip=[
            alt.Tooltip("x:Q", title="X", format=".1f"),
            alt.Tooltip("y:Q", title="Y", format=".1f"),
            alt.Tooltip("speed:Q", title="Wind Speed (knots)", format=".1f"),
            alt.Tooltip("direction:Q", title="Direction (deg)", format=".0f"),
        ],
    )
)

# Layer 2: Station points (base of barb)
points = (
    alt.Chart(df)
    .mark_circle(size=60, color="#306998")
    .encode(x="x:Q", y="y:Q", tooltip=[alt.Tooltip("speed:Q", title="Speed (knots)", format=".1f")])
)

# Layer 3: Barb flags (speed indicators)
barbs = alt.Chart(barb_df).mark_rule(strokeWidth=2, color="#306998").encode(x="x:Q", y="y:Q", x2="x2:Q", y2="y2:Q")

# Combine layers
chart = (
    alt.layer(staff, points, barbs)
    .properties(width=1600, height=900, title=alt.Title("windbarb-basic \u00b7 altair \u00b7 pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
