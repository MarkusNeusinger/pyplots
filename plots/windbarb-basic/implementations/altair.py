"""pyplots.ai
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
wind_direction = np.degrees(np.arctan2(-u, -v))  # Degrees from north, clockwise

# Create DataFrame
df = pd.DataFrame({"x": x, "y": y, "u": u, "v": v, "speed": wind_speed, "direction": wind_direction})

# Scale factor for arrow length
scale = 0.03

# Calculate staff endpoints (barb points INTO the wind)
df["dx"] = -df["u"] * scale
df["dy"] = -df["v"] * scale
df["x2"] = df["x"] + df["dx"]
df["y2"] = df["y"] + df["dy"]

# Create barb data inline (no functions - KISS principle)
barb_records = []
pennant_records = []

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

    # Add pennants (50 knots each) - triangular filled shapes
    while remaining_speed >= 50 and barb_count < 3:
        pos_factor = barb_position - barb_count * 0.18
        bx = row["x"] + ux * staff_length * pos_factor
        by = row["y"] + uy * staff_length * pos_factor
        # Pennant triangle vertices (base on staff, tip perpendicular)
        # Create filled triangle by using area mark with 3 points
        tip_x = bx + px * 0.45
        tip_y = by + py * 0.45
        base2_x = bx + ux * staff_length * 0.12
        base2_y = by + uy * staff_length * 0.12
        pennant_records.append({"x": bx, "y": by, "x2": tip_x, "y2": tip_y, "x3": base2_x, "y3": base2_y, "order": 0})
        pennant_records.append({"x": tip_x, "y": tip_y, "x2": base2_x, "y2": base2_y, "x3": bx, "y3": by, "order": 1})
        pennant_records.append({"x": base2_x, "y": base2_y, "x2": bx, "y2": by, "x3": tip_x, "y3": tip_y, "order": 2})
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
            {"x": bx, "y": by, "type": "half", "speed": speed, "x2": bx + px * 0.18, "y2": by + py * 0.18}
        )

barb_df = pd.DataFrame(barb_records)
pennant_df = pd.DataFrame(pennant_records) if pennant_records else pd.DataFrame(columns=["x", "y", "x2", "y2"])

# Create legend data - positioned in top-right corner
legend_x = 9.5
legend_y_start = 7.5
legend_entries = [
    {"label": "Wind Barb Notation:", "y_offset": 0, "type": "header"},
    {"label": "Half barb = 5 knots", "y_offset": -0.6, "type": "half"},
    {"label": "Full barb = 10 knots", "y_offset": -1.2, "type": "full"},
    {"label": "Pennant = 50 knots", "y_offset": -1.8, "type": "pennant"},
    {"label": "Barb points into wind", "y_offset": -2.4, "type": "note"},
]

legend_text_data = []
legend_symbol_data = []

for entry in legend_entries:
    y_pos = legend_y_start + entry["y_offset"]
    legend_text_data.append({"x": legend_x - 0.3, "y": y_pos, "text": entry["label"], "type": entry["type"]})

    if entry["type"] == "half":
        # Half barb symbol
        legend_symbol_data.append(
            {"x": legend_x - 1.0, "y": y_pos, "x2": legend_x - 0.5, "y2": y_pos, "barb_type": "staff"}
        )
        legend_symbol_data.append(
            {"x": legend_x - 0.55, "y": y_pos, "x2": legend_x - 0.55, "y2": y_pos + 0.15, "barb_type": "half"}
        )
    elif entry["type"] == "full":
        # Full barb symbol
        legend_symbol_data.append(
            {"x": legend_x - 1.0, "y": y_pos, "x2": legend_x - 0.5, "y2": y_pos, "barb_type": "staff"}
        )
        legend_symbol_data.append(
            {"x": legend_x - 0.55, "y": y_pos, "x2": legend_x - 0.55, "y2": y_pos + 0.3, "barb_type": "full"}
        )
    elif entry["type"] == "pennant":
        # Pennant symbol (filled triangle)
        legend_symbol_data.append(
            {"x": legend_x - 1.0, "y": y_pos, "x2": legend_x - 0.5, "y2": y_pos, "barb_type": "staff"}
        )
        legend_symbol_data.append(
            {"x": legend_x - 0.55, "y": y_pos, "x2": legend_x - 0.55, "y2": y_pos + 0.35, "barb_type": "pennant_line"}
        )
        legend_symbol_data.append(
            {"x": legend_x - 0.55, "y": y_pos + 0.35, "x2": legend_x - 0.7, "y2": y_pos, "barb_type": "pennant_line"}
        )
        legend_symbol_data.append(
            {"x": legend_x - 0.7, "y": y_pos, "x2": legend_x - 0.55, "y2": y_pos, "barb_type": "pennant_line"}
        )

legend_text_df = pd.DataFrame(legend_text_data)
legend_symbol_df = pd.DataFrame(legend_symbol_data)

# Layer 1: Staff (main line of wind barb)
staff = (
    alt.Chart(df)
    .mark_rule(strokeWidth=2.5, color="#306998")
    .encode(
        x=alt.X("x:Q", title="X Coordinate", scale=alt.Scale(domain=[-1, 12])),
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
    .mark_circle(size=80, color="#306998")
    .encode(x="x:Q", y="y:Q", tooltip=[alt.Tooltip("speed:Q", title="Speed (knots)", format=".1f")])
)

# Layer 3: Barb flags (speed indicators)
barbs = alt.Chart(barb_df).mark_rule(strokeWidth=2.5, color="#306998").encode(x="x:Q", y="y:Q", x2="x2:Q", y2="y2:Q")

# Layer 4: Pennant triangles (using path/lines for triangular shape)
pennants = (
    (alt.Chart(pennant_df).mark_rule(strokeWidth=2.5, color="#306998").encode(x="x:Q", y="y:Q", x2="x2:Q", y2="y2:Q"))
    if len(pennant_df) > 0
    else alt.Chart(pd.DataFrame({"x": []})).mark_point()
)

# Layer 5: Legend text
legend_text = (
    alt.Chart(legend_text_df)
    .mark_text(align="left", fontSize=14, font="sans-serif", color="#333333")
    .encode(x="x:Q", y="y:Q", text="text:N")
)

# Layer 6: Legend symbols
legend_symbols = (
    alt.Chart(legend_symbol_df)
    .mark_rule(strokeWidth=2.5, color="#306998")
    .encode(x="x:Q", y="y:Q", x2="x2:Q", y2="y2:Q")
)

# Combine layers
chart = (
    alt.layer(staff, points, barbs, pennants, legend_text, legend_symbols)
    .properties(width=1600, height=900, title=alt.Title("windbarb-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
