"""pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: altair | Python 3.13
Quality: pending | Created: 2025-01-09
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Simulated CPU usage over time with realistic patterns
np.random.seed(42)

# Generate 100 points (showing recent window of data)
n_points = 100
timestamps = pd.date_range(end=pd.Timestamp("2025-01-09 14:30:00"), periods=n_points, freq="1s")

# Create realistic CPU usage pattern with occasional spikes
base_usage = 35 + 10 * np.sin(np.linspace(0, 4 * np.pi, n_points))  # Slow oscillation
noise = np.random.randn(n_points) * 3
spikes = np.zeros(n_points)
spike_indices = [20, 45, 72, 88]
for idx in spike_indices:
    spikes[idx : idx + 5] = np.array([15, 25, 20, 10, 5])[: min(5, n_points - idx)]

values = np.clip(base_usage + noise + spikes, 5, 95)

df = pd.DataFrame({"timestamp": timestamps, "value": values})

# Add gradient effect column for visual trailing indication
df["opacity"] = np.linspace(0.3, 1.0, n_points)

# Calculate current value for annotation
current_value = values[-1]
current_time = timestamps[-1]

# Create main line chart
line = (
    alt.Chart(df)
    .mark_line(strokeWidth=4, color="#306998")
    .encode(
        x=alt.X(
            "timestamp:T",
            axis=alt.Axis(title="Time", format="%H:%M:%S", labelAngle=-45, titleFontSize=22, labelFontSize=16),
        ),
        y=alt.Y(
            "value:Q",
            axis=alt.Axis(title="CPU Usage (%)", titleFontSize=22, labelFontSize=16),
            scale=alt.Scale(domain=[0, 100]),
        ),
    )
)

# Add area fill with gradient effect
area = (
    alt.Chart(df)
    .mark_area(opacity=0.3, color="#306998")
    .encode(
        x=alt.X("timestamp:T"),
        y=alt.Y("value:Q", scale=alt.Scale(domain=[0, 100])),
        y2=alt.value(900),  # Fill down to baseline
    )
)

# Add points with fade effect (newer points more visible)
points = (
    alt.Chart(df)
    .mark_circle(color="#306998")
    .encode(
        x=alt.X("timestamp:T"),
        y=alt.Y("value:Q"),
        size=alt.Size("opacity:Q", scale=alt.Scale(range=[30, 150]), legend=None),
        opacity=alt.Opacity("opacity:Q", scale=alt.Scale(range=[0.3, 1.0]), legend=None),
    )
)

# Highlight current value point
current_df = pd.DataFrame({"timestamp": [current_time], "value": [current_value]})

current_point = (
    alt.Chart(current_df)
    .mark_circle(size=300, color="#FFD43B", stroke="#306998", strokeWidth=3)
    .encode(x=alt.X("timestamp:T"), y=alt.Y("value:Q"))
)

# Add current value annotation
current_annotation = (
    alt.Chart(current_df)
    .mark_text(align="left", baseline="middle", dx=15, fontSize=20, fontWeight="bold", color="#306998")
    .encode(x=alt.X("timestamp:T"), y=alt.Y("value:Q"), text=alt.value(f"Current: {current_value:.1f}%"))
)

# Add scrolling direction indicator (arrow shape on left side)
arrow_df = pd.DataFrame({"x": [timestamps[0], timestamps[5], timestamps[0]], "y": [45, 50, 55], "order": [1, 2, 3]})

scroll_indicator = (
    alt.Chart(arrow_df)
    .mark_line(strokeWidth=3, color="#FFD43B", opacity=0.7)
    .encode(x=alt.X("x:T"), y=alt.Y("y:Q"), order="order:O")
)

# Add "LIVE" indicator text
live_df = pd.DataFrame({"x": [timestamps[-10]], "y": [92]})

live_indicator = (
    alt.Chart(live_df)
    .mark_text(fontSize=24, fontWeight="bold", color="#FF4444")
    .encode(x=alt.X("x:T"), y=alt.Y("y:Q"), text=alt.value("● LIVE"))
)

# Combine all layers
chart = (
    alt.layer(area, line, points, current_point, current_annotation, scroll_indicator, live_indicator)
    .properties(width=1600, height=900, title=alt.Title("line-realtime · altair · pyplots.ai", fontSize=28))
    .configure_axis(labelFontSize=16, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
