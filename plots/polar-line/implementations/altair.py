"""pyplots.ai
polar-line: Polar Line Plot
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data: Simulate monthly temperature pattern (cyclical data)
np.random.seed(42)
months = np.arange(0, 360, 30)  # 12 months as angles (0, 30, 60, ..., 330)
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Two cities with different seasonal patterns
city_a_temps = 15 + 12 * np.sin(np.radians(months - 90)) + np.random.randn(12) * 1.5
city_b_temps = 10 + 8 * np.sin(np.radians(months - 90)) + np.random.randn(12) * 1.5

# Close the loop by repeating first point
months_closed = np.append(months, 360)
month_names_closed = month_names + ["Jan"]
city_a_closed = np.append(city_a_temps, city_a_temps[0])
city_b_closed = np.append(city_b_temps, city_b_temps[0])

# Create DataFrame
df = pd.DataFrame(
    {
        "angle": np.tile(months_closed, 2),
        "angle_rad": np.tile(np.radians(months_closed), 2),
        "temperature": np.concatenate([city_a_closed, city_b_closed]),
        "city": ["City A"] * len(months_closed) + ["City B"] * len(months_closed),
        "month": month_names_closed * 2,
    }
)

# Convert polar to Cartesian coordinates for line plotting
# Normalize temperature to radius (shift to ensure positive radius)
df["radius"] = df["temperature"] - df["temperature"].min() + 5  # offset for visibility
df["x"] = df["radius"] * np.cos(df["angle_rad"])
df["y"] = df["radius"] * np.sin(df["angle_rad"])

# Create the polar line chart using Cartesian projection of polar coordinates
lines = (
    alt.Chart(df)
    .mark_line(strokeWidth=4)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[-45, 45]), title=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[-45, 45]), title=None),
        color=alt.Color(
            "city:N",
            scale=alt.Scale(domain=["City A", "City B"], range=["#306998", "#FFD43B"]),
            legend=alt.Legend(
                title="Location",
                titleFontSize=20,
                labelFontSize=18,
                orient="right",
                symbolStrokeWidth=4,
                symbolSize=300,
            ),
        ),
        order="angle:Q",
    )
)

# Add points at each data location
points = (
    alt.Chart(df)
    .mark_circle(size=180)
    .encode(
        x=alt.X("x:Q"),
        y=alt.Y("y:Q"),
        color=alt.Color(
            "city:N", scale=alt.Scale(domain=["City A", "City B"], range=["#306998", "#FFD43B"]), legend=None
        ),
    )
)

# Create radial grid lines (concentric circles)
grid_radii = [10, 20, 30]
grid_data = []
for r in grid_radii:
    theta_fine = np.linspace(0, 2 * np.pi, 100)
    for i, t in enumerate(theta_fine):
        grid_data.append({"x": r * np.cos(t), "y": r * np.sin(t), "radius": r, "order": i})

grid_df = pd.DataFrame(grid_data)

circles = (
    alt.Chart(grid_df)
    .mark_line(strokeWidth=1, color="#cccccc", opacity=0.5)
    .encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), detail="radius:N", order="order:Q")
)

# Create angular grid lines (spokes for each month)
spoke_data = []
for angle, name in zip(months, month_names, strict=True):
    rad = np.radians(angle)
    spoke_data.append({"x1": 0, "y1": 0, "x2": 35 * np.cos(rad), "y2": 35 * np.sin(rad), "angle": angle, "month": name})

spoke_df = pd.DataFrame(spoke_data)

spokes = (
    alt.Chart(spoke_df)
    .mark_rule(strokeWidth=1, color="#cccccc", opacity=0.5)
    .encode(x=alt.X("x1:Q"), y=alt.Y("y1:Q"), x2="x2:Q", y2="y2:Q")
)

# Add month labels around the perimeter
label_radius = 40
label_data = []
for angle, name in zip(months, month_names, strict=True):
    rad = np.radians(angle)
    label_data.append({"x": label_radius * np.cos(rad), "y": label_radius * np.sin(rad), "month": name})

label_df = pd.DataFrame(label_data)

labels = (
    alt.Chart(label_df).mark_text(fontSize=18, fontWeight="bold").encode(x=alt.X("x:Q"), y=alt.Y("y:Q"), text="month:N")
)

# Combine all layers
chart = (
    alt.layer(circles, spokes, lines, points, labels)
    .properties(
        width=1000,
        height=1000,
        title=alt.Title(
            "Monthly Temperature Pattern · polar-line · altair · pyplots.ai", fontSize=28, anchor="middle", offset=20
        ),
    )
    .configure_view(strokeWidth=0)
    .configure_axis(labels=False, ticks=False, domain=False, grid=False)
)

# Save as PNG
chart.save("plot.png", scale_factor=3.6)

# Save as HTML for interactivity
chart.save("plot.html")
