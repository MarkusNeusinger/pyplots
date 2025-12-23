""" pyplots.ai
rose-basic: Basic Rose Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-23
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Monthly rainfall in mm (cyclical 12-month pattern)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
rainfall = [78, 52, 68, 45, 35, 28, 22, 30, 55, 85, 92, 88]

n = len(months)

# Calculate angles starting at 12 o'clock (top) and going clockwise
# -90 degrees offset to start at top, then proceeding clockwise
angle_step = 360 / n
start_angles = [-90 + i * angle_step for i in range(n)]
end_angles = [-90 + (i + 1) * angle_step for i in range(n)]

# Create DataFrame with explicit angles
df = pd.DataFrame(
    {
        "month": months,
        "value": rainfall,
        "order": range(n),
        "startAngle": np.radians(start_angles),
        "endAngle": np.radians(end_angles),
    }
)

# Max value for radius scaling - use 100 for nicer gridline values
max_val = 100

# Color palette - colorblind-friendly distinct colors
colors = [
    "#306998",  # Python Blue (Jan)
    "#FFD43B",  # Python Yellow (Feb)
    "#4ECDC4",  # Teal (Mar)
    "#FF6B6B",  # Coral (Apr)
    "#95E1D3",  # Mint (May)
    "#F38181",  # Salmon (Jun)
    "#A8D5BA",  # Sage (Jul)
    "#FFC93C",  # Gold (Aug)
    "#5D9CEC",  # Sky Blue (Sep)
    "#AC92EB",  # Lavender (Oct)
    "#EC87C0",  # Pink (Nov)
    "#48CFAD",  # Seafoam (Dec)
]

# Create radial gridlines data (concentric circles at 25, 50, 75, 100 mm)
grid_values = [25, 50, 75, 100]
grid_data = pd.DataFrame({"value": grid_values, "label": [f"{v}" for v in grid_values]})

# Radial gridlines - concentric circles using mark_arc
gridlines = (
    alt.Chart(grid_data)
    .mark_arc(filled=False, stroke="#cccccc", strokeWidth=1.5, strokeDash=[6, 4])
    .encode(
        theta=alt.value(2 * np.pi),  # Full circle
        radius=alt.Radius("value:Q", scale=alt.Scale(type="linear", domain=[0, max_val], range=[0, 400])),
    )
)

# Grid labels positioned at 3 o'clock position (right side) to avoid overlap with data
grid_label_data = pd.DataFrame(
    {
        "value": grid_values,
        "label": [f"{v} mm" for v in grid_values],
        # Position labels at 3 o'clock (right) - angle = 0 degrees
        "theta": [0.0] * len(grid_values),
    }
)

grid_labels = (
    alt.Chart(grid_label_data)
    .mark_text(fontSize=18, fontWeight="bold", dx=10, color="#666666", align="left", baseline="middle")
    .encode(
        theta=alt.Theta("theta:Q"),
        radius=alt.Radius("value:Q", scale=alt.Scale(type="linear", domain=[0, max_val], range=[0, 400])),
        text="label:N",
    )
)

# Rose chart using mark_arc with explicit angles to start at 12 o'clock
rose = (
    alt.Chart(df)
    .mark_arc(stroke="#ffffff", strokeWidth=2, innerRadius=0)
    .encode(
        theta=alt.Theta("startAngle:Q", stack=None),
        theta2=alt.Theta2("endAngle:Q"),
        radius=alt.Radius("value:Q", scale=alt.Scale(type="linear", domain=[0, max_val], range=[0, 400])),
        color=alt.Color(
            "month:N",
            scale=alt.Scale(domain=months, range=colors),
            legend=alt.Legend(
                title="Month",
                titleFontSize=24,
                labelFontSize=20,
                symbolSize=500,
                orient="right",
                titlePadding=15,
                offset=30,
            ),
        ),
        tooltip=[alt.Tooltip("month:N", title="Month"), alt.Tooltip("value:Q", title="Rainfall (mm)")],
    )
)

# Calculate label positions - midpoint angle for each segment
mid_angles = [(-90 + (i + 0.5) * angle_step) for i in range(n)]

# Create label data with theta and radius for polar positioning
label_data = pd.DataFrame(
    {
        "month": months,
        "value": rainfall,
        "theta": np.radians(mid_angles),
        # Position labels just outside the segment edge
        "labelRadius": [v * 1.18 for v in rainfall],
    }
)

# Text labels showing values on each segment using polar coordinates
text = (
    alt.Chart(label_data)
    .mark_text(fontSize=22, fontWeight="bold")
    .encode(
        theta=alt.Theta("theta:Q"),
        radius=alt.Radius("labelRadius:Q", scale=alt.Scale(type="linear", domain=[0, max_val], range=[0, 400])),
        text=alt.Text("value:Q"),
        color=alt.value("#333333"),
    )
)

# Combine layers - landscape format to better utilize canvas space
# Altair radial charts position content in upper portion, so use reduced height
chart = (
    alt.layer(gridlines, grid_labels, rose, text)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(text="rose-basic · altair · pyplots.ai", fontSize=32, anchor="middle", dy=-10),
    )
    .configure_view(strokeWidth=0)
    .configure_axis(grid=False, domain=False, ticks=False, labels=False, title=None)
)

# Save at scale_factor=3 for 4800x2700 resolution
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
