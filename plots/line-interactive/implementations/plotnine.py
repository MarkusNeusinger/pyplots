""" pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    annotate,
    element_line,
    element_rect,
    element_text,
    geom_hline,
    geom_line,
    geom_point,
    geom_rect,
    ggplot,
    labs,
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
daily_pattern = 30 * np.sin(2 * np.pi * np.arange(n_points) / 24)  # Daily cycle
weekly_pattern = 15 * np.sin(2 * np.pi * np.arange(n_points) / 168)  # Weekly cycle
noise = np.random.normal(0, 10, n_points)
trend = np.linspace(0, 20, n_points)  # Slight upward trend

# Add some spike anomalies
response_times = base_response + daily_pattern + weekly_pattern + noise + trend
spike_indices = [45, 120, 175]
for idx in spike_indices:
    response_times[idx] += np.random.uniform(50, 100)

# Create main DataFrame
df = pd.DataFrame({"datetime": dates, "response_time": response_times, "point_type": "data"})

# Calculate average for reference line
avg_response = np.mean(response_times)

# Create DataFrame for scatter points (every 5th point for cleaner visualization)
scatter_df = df.iloc[::5].copy()
scatter_df["point_type"] = "scatter"

# Create anomaly DataFrame
anomaly_df = df.iloc[spike_indices].copy()
anomaly_df["point_type"] = "anomaly"
anomaly_df["label"] = [f"Anomaly: {v:.0f} ms" for v in anomaly_df["response_time"]]

# Zoom region data (demonstrating range selection)
zoom_start_dt = dates[70]
zoom_end_dt = dates[100]
y_min = df["response_time"].min() - 5
y_max = df["response_time"].max() + 40

zoom_df = pd.DataFrame({"xmin": [zoom_start_dt], "xmax": [zoom_end_dt], "ymin": [y_min], "ymax": [y_max]})

# Demo hover tooltip position
demo_idx = 75  # Point within the zoom region for demonstration
demo_x = dates[demo_idx]
demo_y = response_times[demo_idx]
demo_date_str = demo_x.strftime("%Y-%m-%d %H:%M")

# Create tooltip annotation data
tooltip_df = pd.DataFrame(
    {"x": [demo_x], "y": [demo_y], "label": [f"Time: {demo_date_str}\nResponse: {demo_y:.1f} ms"]}
)

# Build the plot
plot = (
    ggplot()
    # Zoom region highlight
    + geom_rect(aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"), data=zoom_df, fill="#2A9D8F", alpha=0.15)
    # Main line
    + geom_line(aes(x="datetime", y="response_time"), data=df, color="#306998", size=1.5)
    # Scatter points for hover targets
    + geom_point(
        aes(x="datetime", y="response_time"), data=scatter_df, color="#306998", fill="#306998", size=3, alpha=0.8
    )
    # Average reference line
    + geom_hline(yintercept=avg_response, linetype="dashed", color="#808080", size=1, alpha=0.7)
    # Anomaly markers
    + geom_point(
        aes(x="datetime", y="response_time"), data=anomaly_df, color="#E63946", fill="#E63946", size=5, shape="^"
    )
    # Demo hover tooltip (showing what interactivity would display)
    + annotate(
        "rect",
        xmin=demo_x - pd.Timedelta(hours=8),
        xmax=demo_x + pd.Timedelta(hours=8),
        ymin=demo_y + 15,
        ymax=demo_y + 50,
        fill="#FFD43B",
        alpha=0.95,
    )
    + annotate(
        "text",
        x=demo_x,
        y=demo_y + 32,
        label=f"Time: {demo_date_str}\nResponse: {demo_y:.1f} ms",
        size=10,
        fontweight="bold",
        color="#306998",
    )
    # Arrow from tooltip to point
    + annotate("segment", x=demo_x, xend=demo_x, y=demo_y + 15, yend=demo_y + 3, color="#306998", size=1)
    # Zoom region label
    + annotate(
        "text",
        x=dates[85],
        y=y_min + 15,
        label="Zoom Region\n(use scroll/drag)",
        size=9,
        color="#2A9D8F",
        fontweight="bold",
    )
    # Average line label
    + annotate(
        "text",
        x=dates[5],
        y=avg_response + 8,
        label=f"Average: {avg_response:.0f} ms",
        size=9,
        color="#808080",
        ha="left",
    )
    # Labels and title
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
        plot_margin=0.02,
    )
)

# Add footer text explaining interactivity
plot = plot + annotate(
    "label",
    x=dates[100],
    y=y_min + 3,
    label="Interactive Controls: Hover points for values • Scroll to zoom • Click-drag to pan • Home to reset",
    size=8,
    fill="#f0f0f0",
    color="#555555",
    fontstyle="italic",
    alpha=0.9,
)

# Save the plot
plot.save("plot.png", dpi=300, verbose=False)
