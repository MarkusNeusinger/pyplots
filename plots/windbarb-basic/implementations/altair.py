"""pyplots.ai
windbarb-basic: Wind Barb Plot for Meteorological Data
Library: altair 6.0.0 | Python 3.13.11
Quality: 82/100 | Created: 2026-01-11
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
# Include some calm conditions (< 2.5 knots) and high winds (>= 50 knots)
np.random.seed(42)
u = np.random.uniform(-30, 30, len(x))
v = np.random.uniform(-25, 25, len(x))

# Force a few calm conditions and one high wind (pennant) for feature coverage
u[0] = 0.5
v[0] = 0.3  # Calm (~0.6 knots)
u[5] = 1.0
v[5] = -0.8  # Calm (~1.3 knots)
u[15] = 45
v[15] = 25  # High wind (~51 knots - 1 pennant)
u[20] = 50
v[20] = 15  # High wind (~52 knots - 1 pennant)

# Calculate wind speed and direction
wind_speed = np.sqrt(u**2 + v**2)
# Direction FROM which wind blows (meteorological convention)
wind_direction = np.degrees(np.arctan2(-u, -v))

# Create DataFrame
df = pd.DataFrame({"x": x, "y": y, "u": u, "v": v, "speed": wind_speed, "direction": wind_direction})

# Separate calm winds (< 2.5 knots) - shown as open circles
calm_df = df[df["speed"] < 2.5].copy()
barbed_df = df[df["speed"] >= 2.5].copy()

# Scale factor for arrow length
scale = 0.03

# Calculate staff endpoints for barbed winds
barbed_df = barbed_df.copy()
barbed_df["dx"] = -barbed_df["u"] * scale
barbed_df["dy"] = -barbed_df["v"] * scale
barbed_df["x2"] = barbed_df["x"] + barbed_df["dx"]
barbed_df["y2"] = barbed_df["y"] + barbed_df["dy"]

# Create barb and pennant data (KISS - inline processing)
barb_records = []
pennant_records = []

for _, row in barbed_df.iterrows():
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
    barb_position = 0.85
    barb_count = 0

    # Add pennants (50 knots each) - represented by triangle markers
    while remaining_speed >= 50 and barb_count < 3:
        pos_factor = barb_position - barb_count * 0.18
        bx = row["x"] + ux * staff_length * pos_factor
        by = row["y"] + uy * staff_length * pos_factor
        # Store pennant position and angle for triangle marker
        pennant_records.append(
            {
                "x": bx + px * 0.15,  # Offset slightly for visual centering
                "y": by + py * 0.15,
                "angle": row["direction"] + 90,  # Rotate to point perpendicular to staff
                "speed": speed,
            }
        )
        remaining_speed -= 50
        barb_count += 1

    # Add full barbs (10 knots each)
    while remaining_speed >= 10 and barb_count < 6:
        pos_factor = barb_position - barb_count * 0.12
        bx = row["x"] + ux * staff_length * pos_factor
        by = row["y"] + uy * staff_length * pos_factor
        barb_records.append({"x": bx, "y": by, "type": "full", "x2": bx + px * 0.35, "y2": by + py * 0.35})
        remaining_speed -= 10
        barb_count += 1

    # Add half barb (5 knots) if remaining
    if remaining_speed >= 5:
        pos_factor = barb_position - barb_count * 0.12
        bx = row["x"] + ux * staff_length * pos_factor
        by = row["y"] + uy * staff_length * pos_factor
        barb_records.append({"x": bx, "y": by, "type": "half", "x2": bx + px * 0.18, "y2": by + py * 0.18})

barb_df = pd.DataFrame(barb_records) if barb_records else pd.DataFrame(columns=["x", "y", "x2", "y2"])
pennant_df = pd.DataFrame(pennant_records) if pennant_records else pd.DataFrame(columns=["x", "y", "angle"])

# Layer 1: Staff (main line of wind barb) for barbed winds only
staff = (
    alt.Chart(barbed_df)
    .mark_rule(strokeWidth=2.5, color="#306998")
    .encode(
        x=alt.X("x:Q", title="Station X Position (grid units)", scale=alt.Scale(domain=[-1, 12])),
        y=alt.Y("y:Q", title="Station Y Position (grid units)", scale=alt.Scale(domain=[-1, 9.5])),
        x2="x2:Q",
        y2="y2:Q",
        tooltip=[
            alt.Tooltip("x:Q", title="X Position", format=".1f"),
            alt.Tooltip("y:Q", title="Y Position", format=".1f"),
            alt.Tooltip("speed:Q", title="Wind Speed (knots)", format=".1f"),
            alt.Tooltip("direction:Q", title="Direction (deg from N)", format=".0f"),
        ],
    )
)

# Layer 2: Station points for barbed winds (base of barb)
points = (
    alt.Chart(barbed_df)
    .mark_circle(size=80, color="#306998")
    .encode(x="x:Q", y="y:Q", tooltip=[alt.Tooltip("speed:Q", title="Speed (knots)", format=".1f")])
)

# Layer 3: Calm wind indicators (open circles for < 2.5 knots)
calm_circles = (
    alt.Chart(calm_df)
    .mark_circle(size=150, stroke="#306998", strokeWidth=2.5, fill="white")
    .encode(
        x="x:Q",
        y="y:Q",
        tooltip=[
            alt.Tooltip("x:Q", title="X Position", format=".1f"),
            alt.Tooltip("y:Q", title="Y Position", format=".1f"),
            alt.Tooltip("speed:Q", title="Wind Speed (knots)", format=".1f"),
        ],
    )
)

# Layer 4: Barb flags (speed indicators)
barbs = (
    (alt.Chart(barb_df).mark_rule(strokeWidth=2.5, color="#306998").encode(x="x:Q", y="y:Q", x2="x2:Q", y2="y2:Q"))
    if len(barb_df) > 0
    else alt.Chart(pd.DataFrame({"x": []})).mark_point()
)

# Layer 5: Pennant triangles (filled markers for 50 knots)
# Using mark_point with triangle-up shape (Altair standard shape)
pennants = (
    (
        alt.Chart(pennant_df)
        .mark_point(shape="triangle-up", size=350, color="#306998", filled=True)
        .encode(
            x="x:Q",
            y="y:Q",
            angle=alt.Angle("angle:Q"),
            tooltip=[alt.Tooltip("speed:Q", title="Speed (knots)", format=".1f")],
        )
    )
    if len(pennant_df) > 0
    else alt.Chart(pd.DataFrame({"x": []})).mark_point()
)

# Create legend as text annotations within the main chart coordinate space
# Position in top-right corner with proper spacing
legend_base_x = 10.5
legend_base_y = 7.5

legend_text_data = pd.DataFrame(
    {
        "x": [legend_base_x, legend_base_x, legend_base_x, legend_base_x, legend_base_x],
        "y": [legend_base_y, legend_base_y - 0.7, legend_base_y - 1.4, legend_base_y - 2.1, legend_base_y - 2.8],
        "text": [
            "Wind Barb Legend:",
            "○  Calm (< 2.5 knots)",
            "—  Half barb = 5 knots",
            "——  Full barb = 10 knots",
            "▲  Pennant = 50 knots",
        ],
    }
)

legend_text = (
    alt.Chart(legend_text_data)
    .mark_text(align="left", fontSize=16, font="sans-serif", color="#333333")
    .encode(x="x:Q", y="y:Q", text="text:N")
)

# Main wind barb chart with all layers including legend
chart = (
    alt.layer(staff, points, calm_circles, barbs, pennants, legend_text)
    .properties(width=1600, height=900, title=alt.Title("windbarb-basic · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save as PNG only
chart.save("plot.png", scale_factor=3.0)
