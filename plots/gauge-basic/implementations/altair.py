""" pyplots.ai
gauge-basic: Basic Gauge Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-14
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
value = 72
min_value = 0
max_value = 100
thresholds = [30, 70]


# Calculate angles for semi-circular gauge (180 degrees)
# Altair arc uses radians starting from 12 o'clock, going clockwise
# We want: left side = min_value, right side = max_value (like a speedometer)
# So we map min_value to -pi/2 (9 o'clock) and max_value to pi/2 (3 o'clock)
def value_to_angle(v):
    """Convert value to angle in radians."""
    ratio = (v - min_value) / (max_value - min_value)
    # Map from -pi/2 (left, 9 o'clock) to pi/2 (right, 3 o'clock)
    return -np.pi / 2 + ratio * np.pi


# Create arc segments for color zones
zones = []
zone_colors = ["#E53935", "#FFD43B", "#4CAF50"]  # Red, Yellow, Green
boundaries = [min_value] + thresholds + [max_value]

for i in range(len(boundaries) - 1):
    start_angle = value_to_angle(boundaries[i])
    end_angle = value_to_angle(boundaries[i + 1])
    zones.append(
        {
            "zone": i,
            "start": boundaries[i],
            "end": boundaries[i + 1],
            "startAngle": start_angle,
            "endAngle": end_angle,
            "color": zone_colors[i],
        }
    )

zones_df = pd.DataFrame(zones)

# Create the gauge background arcs
gauge_arcs = (
    alt.Chart(zones_df)
    .mark_arc(innerRadius=200, outerRadius=320, cornerRadius=4)
    .encode(
        theta=alt.Theta("startAngle:Q", scale=None),
        theta2="endAngle:Q",
        color=alt.Color("color:N", scale=None, legend=None),
    )
)

# Create needle indicator
needle_angle = value_to_angle(value)
needle_length = 280
# Adjust coordinates: angle 0 is 12 o'clock, positive is clockwise
# x = length * sin(angle), y = length * cos(angle) for 12 o'clock start
needle_x = needle_length * np.sin(needle_angle)
needle_y = needle_length * np.cos(needle_angle)

needle_df = pd.DataFrame([{"x": 0, "y": 0, "x2": needle_x, "y2": needle_y}])

needle = (
    alt.Chart(needle_df)
    .mark_rule(color="#306998", strokeWidth=8, strokeCap="round")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[-400, 400]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[-150, 400]), axis=None),
        x2="x2:Q",
        y2="y2:Q",
    )
)

# Center hub circle
hub_df = pd.DataFrame([{"x": 0, "y": 0}])
hub = alt.Chart(hub_df).mark_circle(size=1500, color="#306998").encode(x="x:Q", y="y:Q")

# Value label
value_label_df = pd.DataFrame([{"x": 0, "y": -100, "text": str(value)}])
value_label = (
    alt.Chart(value_label_df)
    .mark_text(fontSize=72, fontWeight="bold", color="#306998")
    .encode(x="x:Q", y="y:Q", text="text:N")
)

# Min and max labels
min_label_x = 340 * np.sin(value_to_angle(min_value))
min_label_y = 340 * np.cos(value_to_angle(min_value))
max_label_x = 340 * np.sin(value_to_angle(max_value))
max_label_y = 340 * np.cos(value_to_angle(max_value))

labels_df = pd.DataFrame(
    [
        {"x": min_label_x - 40, "y": min_label_y, "text": str(min_value)},
        {"x": max_label_x + 40, "y": max_label_y, "text": str(max_value)},
    ]
)
range_labels = alt.Chart(labels_df).mark_text(fontSize=32, color="#666666").encode(x="x:Q", y="y:Q", text="text:N")

# Threshold labels on the arc
threshold_labels_data = []
for t in thresholds:
    angle = value_to_angle(t)
    label_radius = 370
    threshold_labels_data.append({"x": label_radius * np.sin(angle), "y": label_radius * np.cos(angle), "text": str(t)})

threshold_labels_df = pd.DataFrame(threshold_labels_data)
threshold_labels = (
    alt.Chart(threshold_labels_df).mark_text(fontSize=28, color="#666666").encode(x="x:Q", y="y:Q", text="text:N")
)

# Combine all layers
chart = (
    alt.layer(gauge_arcs, needle, hub, value_label, range_labels, threshold_labels)
    .properties(
        width=1600, height=900, title=alt.Title("gauge-basic · altair · pyplots.ai", fontSize=48, anchor="middle")
    )
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
