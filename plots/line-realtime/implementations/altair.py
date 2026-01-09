""" pyplots.ai
line-realtime: Real-Time Updating Line Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-09
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - simulated CPU usage with real-time streaming effect
np.random.seed(42)
n_points = 100

# Generate timestamps (last 10 seconds of data at 100ms intervals)
timestamps = pd.date_range(end=pd.Timestamp.now(), periods=n_points, freq="100ms")

# Generate realistic CPU usage pattern with some spikes
base_usage = 45 + np.cumsum(np.random.randn(n_points) * 0.5)
spikes = np.random.rand(n_points) > 0.95
spike_values = spikes * np.random.uniform(15, 25, n_points)
values = np.clip(base_usage + spike_values + np.sin(np.linspace(0, 4 * np.pi, n_points)) * 5, 0, 100)

df = pd.DataFrame({"timestamp": timestamps, "value": values})

# Create gradient effect for trailing fade (older points more transparent)
df["opacity"] = np.linspace(0.3, 1.0, n_points)
df["size"] = np.linspace(1, 3, n_points)

# Main line chart
line = (
    alt.Chart(df)
    .mark_line(color="#306998", strokeWidth=3)
    .encode(
        x=alt.X("timestamp:T", title="Time", axis=alt.Axis(format="%H:%M:%S", labelFontSize=18, titleFontSize=22)),
        y=alt.Y(
            "value:Q",
            title="CPU Usage (%)",
            scale=alt.Scale(domain=[0, 100]),
            axis=alt.Axis(labelFontSize=18, titleFontSize=22),
        ),
    )
)

# Points with size gradient for trailing effect
points = (
    alt.Chart(df)
    .mark_circle(color="#306998")
    .encode(
        x="timestamp:T",
        y="value:Q",
        size=alt.Size("size:Q", scale=alt.Scale(range=[30, 150]), legend=None),
        opacity=alt.Opacity("opacity:Q", scale=alt.Scale(range=[0.3, 1.0]), legend=None),
    )
)

# Latest point highlighted
latest_point = (
    alt.Chart(df.tail(1))
    .mark_circle(color="#FFD43B", size=300, stroke="#306998", strokeWidth=3)
    .encode(x="timestamp:T", y="value:Q")
)

# Current value annotation
current_value = df["value"].iloc[-1]
latest_annotation = (
    alt.Chart(df.tail(1))
    .mark_text(align="left", dx=15, dy=-5, fontSize=20, fontWeight="bold", color="#306998")
    .encode(x="timestamp:T", y="value:Q", text=alt.value(f"{current_value:.1f}%"))
)

# Direction arrow indicating scrolling (right arrow at the end)
arrow_df = pd.DataFrame({"x": [timestamps[-1]], "y": [current_value + 8]})

arrow = (
    alt.Chart(arrow_df)
    .mark_text(fontSize=28, color="#306998", fontWeight="bold")
    .encode(x="x:T", y="y:Q", text=alt.value("▶"))
)

# Fade effect text on left side
fade_text_df = pd.DataFrame({"x": [timestamps[5]], "y": [90]})

fade_text = (
    alt.Chart(fade_text_df)
    .mark_text(fontSize=16, color="#888888", fontStyle="italic", align="left")
    .encode(x="x:T", y="y:Q", text=alt.value("← older data fades out"))
)

# Combine all layers
chart = (
    alt.layer(line, points, latest_point, latest_annotation, arrow, fade_text)
    .properties(
        width=1600,
        height=900,
        title=alt.Title("Server CPU Monitor · line-realtime · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_axis(labelFontSize=18, titleFontSize=22, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
