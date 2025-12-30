"""pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 87/100 | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_line,
    element_rect,
    element_text,
    geom_line,
    geom_point,
    geom_rect,
    ggplot,
    guide_legend,
    guides,
    labs,
    scale_color_manual,
    scale_x_datetime,
    theme,
    theme_minimal,
)


# Data - Server response time metrics (realistic monitoring scenario)
np.random.seed(42)
n_points = 200

# Generate datetime index for one week of hourly data
dates = pd.date_range("2024-01-01", periods=n_points, freq="h")

# Generate realistic server response times with patterns
base_response = 120  # Base response time in ms
daily_pattern = 30 * np.sin(2 * np.pi * np.arange(n_points) / 24)
weekly_pattern = 15 * np.sin(2 * np.pi * np.arange(n_points) / 168)
noise = np.random.normal(0, 10, n_points)
trend = np.linspace(0, 20, n_points)

# Add spike anomalies
response_times = base_response + daily_pattern + weekly_pattern + noise + trend
spike_indices = [45, 120, 175]
for idx in spike_indices:
    response_times[idx] += np.random.uniform(50, 100)

# Calculate bounds
avg_response = np.mean(response_times)
y_min = np.min(response_times) - 10
y_max = np.max(response_times) + 50

# Create unified DataFrame with series type for legend
df = pd.DataFrame({"datetime": dates, "response_time": response_times, "series": "Response Time"})

# Add anomaly points
anomaly_df = pd.DataFrame(
    {"datetime": dates[spike_indices], "response_time": response_times[spike_indices], "series": "Anomaly Spike"}
)

# Add average line
avg_df = pd.DataFrame(
    {"datetime": [dates[0], dates[-1]], "response_time": [avg_response, avg_response], "series": "Average"}
)

# Combine for legend
combined_df = pd.concat([df, anomaly_df, avg_df], ignore_index=True)

# Demo hover tooltip
demo_idx = 75
demo_x = dates[demo_idx]
demo_y = response_times[demo_idx]
demo_date_str = demo_x.strftime("%Y-%m-%d %H:%M")

# Zoom region bounds
zoom_start = dates[70]
zoom_end = dates[100]

# Build plot
plot = (
    ggplot(combined_df, aes(x="datetime", y="response_time", color="series"))
    # Zoom region highlight
    + geom_rect(
        aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"),
        data=pd.DataFrame({"xmin": [zoom_start], "xmax": [zoom_end], "ymin": [y_min], "ymax": [y_max]}),
        inherit_aes=False,
        fill="#2A9D8F",
        alpha=0.15,
    )
    # Main time series line
    + geom_line(data=df, size=1.8)
    # Scatter points for hover targets (larger for visibility)
    + geom_point(data=df.iloc[::5], size=5, alpha=0.9)
    # Average reference line
    + geom_line(data=avg_df, linetype="dashed", size=1.5)
    # Anomaly markers (large triangles)
    + geom_point(data=anomaly_df, size=8, shape="^")
    # Color scale with explicit legend
    + scale_color_manual(
        name="Data Series",
        values={"Response Time": "#306998", "Anomaly Spike": "#E63946", "Average": "#808080"},
        breaks=["Response Time", "Average", "Anomaly Spike"],
    )
    + guides(color=guide_legend(override_aes={"size": 6}))
    # Demo tooltip box
    + annotate(
        "rect",
        xmin=demo_x - pd.Timedelta(hours=8),
        xmax=demo_x + pd.Timedelta(hours=8),
        ymin=demo_y + 18,
        ymax=demo_y + 55,
        fill="#FFD43B",
        alpha=0.95,
    )
    + annotate(
        "text",
        x=demo_x,
        y=demo_y + 36,
        label=f"Time: {demo_date_str}\nResponse: {demo_y:.1f} ms",
        size=11,
        fontweight="bold",
        color="#306998",
    )
    + annotate("segment", x=demo_x, xend=demo_x, y=demo_y + 18, yend=demo_y + 4, color="#306998", size=1.2)
    # Zoom region label
    + annotate(
        "text",
        x=dates[85],
        y=y_min + 12,
        label="Zoom Region\n(range selection)",
        size=10,
        color="#2A9D8F",
        fontweight="bold",
    )
    # Subtitle
    + annotate(
        "text",
        x=dates[100],
        y=y_max - 3,
        label="Static demonstration of interactive concepts: tooltips, zoom regions, anomaly markers",
        size=11,
        color="#666666",
        fontstyle="italic",
    )
    # Labels
    + labs(x="Time", y="Response Time (ms)", title="line-interactive · plotnine · pyplots.ai")
    + scale_x_datetime(date_labels="%b %d\n%H:%M")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=14),
        axis_text_x=element_text(rotation=30),
        panel_grid_major=element_line(color="#CCCCCC", size=0.5, alpha=0.3),
        panel_grid_minor=element_line(color="#EEEEEE", size=0.3, alpha=0.2),
        plot_background=element_rect(fill="white"),
        panel_background=element_rect(fill="white"),
        legend_title=element_text(size=16, weight="bold"),
        legend_text=element_text(size=14),
        legend_position="right",
        legend_key_size=20,
        legend_background=element_rect(fill="white", color="#CCCCCC"),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
